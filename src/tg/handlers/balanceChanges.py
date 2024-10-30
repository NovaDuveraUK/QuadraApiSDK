import time
from typing import List

import pandas as pd
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from src.rest.examples.account.getBalancesHistory import get_balances_history
from src.tg.config.columns.balanceChanges import balance_changes_columns_to_sum
from src.tg.config.columns.intraPnl import intra_pnl_columns_to_sum
from src.tg.config.venues.balanceChanges import balance_changes_venues
from src.tg.handlers.shared import get_my_venues, send_telegram_table, get_unix_timestamp_for_hour, add_totals_row


async def fetch_balances_history(start_time: int, exchange_ids: List[str], time_bucket: str = '1h'):
    # Get venues firstly:
    venues_df = await get_my_venues()
    # Filter ones that are not in exchange_ids, col: 'exchange_id'
    active_ids = venues_df[venues_df['exchange_id'].isin(exchange_ids)]['company_exchange_id'].tolist()

    # Asyncio gather on all venues to get all ttr
    tasks = [get_balances_history(x, start_time) for x in active_ids]
    balances_list = await asyncio.gather(*tasks)

    # Create an empty list to hold all DataFrames
    balances_summary = []

    # Process each set of balances and append to the summary list
    for i, balances in enumerate(balances_list):
        # Convert each list of trades to a DataFrame
        df = pd.DataFrame(balances)
        balances_summary.append(df)

    # Concatenate all the balance DataFrames into a single DataFrame
    combined_df = pd.concat(balances_summary, ignore_index=True)

    # Convert the 'dt' column to datetime format
    combined_df['dt'] = pd.to_datetime(combined_df['dt']).dt.tz_localize(None)

    # Bucket 'dt' to the nearest hour or minute
    # For nearest hour: combined_df['dt_bucket'] = combined_df['dt'].dt.floor('H')
    # For nearest minute: combined_df['dt_bucket'] = combined_df['dt'].dt.floor('T')
    combined_df['dt_bucket'] = combined_df['dt'].dt.floor(time_bucket)  # Adjust 'h' to 't' if minute-level bucketing is desired

    # Sort by 'dt' so that the earliest records in each hour are first
    combined_df = combined_df.sort_values(by=['company_exchange_id', 'dt'])

    combined_df = pd.merge(combined_df, venues_df[['company_exchange_id', 'alias']], on='company_exchange_id',
                         how='left')

    # Sort by 'dt' so that the earliest records in each hour are first
    combined_df = combined_df.sort_values(by=['company_exchange_id', 'dt'])

    # Group by 'company_exchange_id' and 'dt_bucket', and then sum 'current_balance_usd' while keeping the earliest timestamp in each hour
    grouped_df = (
        combined_df.groupby(['alias', 'dt_bucket', 'asset'], as_index=False)
        .first()
        .groupby(['alias', 'dt_bucket'], as_index=False)
        .agg({
            'current_balance_usd': 'sum'  # Sum across assets within each hour
        })
    )

    # Pivot the DataFrame to create the desired format with 'company_exchange_id' as rows and distinct 'dt' values as columns
    result_df = grouped_df.pivot_table(
        index='dt_bucket',
        columns='alias',
        values='current_balance_usd',
        aggfunc='first'
    ).reset_index()

    # Add a row-wise total column
    result_df['total'] = result_df.sum(axis=1, numeric_only=True)
    # Calculate percentage change and absolute change for the row_total column
    result_df['total_abs_chg'] = result_df['total'].diff()
    result_df['total_pct_chg'] = result_df['total'].pct_change() * 100  # Convert to percentage

    result_df = add_totals_row(result_df, 'dt_bucket', balance_changes_columns_to_sum())
    return result_df


async def run_balances_changes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching balance change data...")
    try:
        hour_input = "0"
        time_bucket = "1h"
        exchange_ids = balance_changes_venues()
        # # Get the arguments passed after the command (intraPnl <variable> <variable2>)
        if context.args:  # Check if there are any arguments passed
            hour_input = context.args[0]  # First argument after the command
            # print("Hour input: ", hour_input)
            if len(context.args) > 1:
                exchange_ids = [context.args[1]]  # Second argument after the command
                if len(context.args) > 2:
                    time_bucket = context.args[2]  # First argument after the command

            # Apply filter to the table based on exchange_id
        timestamp_ms, target_datetime = get_unix_timestamp_for_hour(hour_input)
        # print("Timestamps: ", timestamp_ms, target_datetime)
        bal_table = await fetch_balances_history(timestamp_ms, exchange_ids, time_bucket)

        # Check if the table is empty
        if bal_table.empty:
            await update.message.reply_text("No balances history found.")
            return

        bal_file = await send_telegram_table(bal_table, 2)
        # Send the image
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bal_file)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


