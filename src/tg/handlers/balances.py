import asyncio
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from src.rest.examples.account.getBalances import get_balances
from src.tg.handlers.shared import get_my_venues, send_telegram_table, add_totals_row
from src.tg.config.columns.balances import balance_columns, balance_columns_to_sum

BALANCE_THRESHOLD_USD = 10


def add_balance_totals_row(df, label_column, total_columns):
    # Calculate the totals for the specified columns
    totals_data = {col: df[col].sum() for col in total_columns}
    totals_data['im_usd_pct'] = df['im_usd'].sum() / df['live_bal_usd'].sum() * 100
    totals_data['mm_usd_pct'] = df['mm_usd'].sum() / df['live_bal_usd'].sum() * 100

    # Set the label for the totals row
    totals_data[label_column] = "TOTAL"

    # Create a new DataFrame for the totals row with the same columns as the original DataFrame
    totals_row = pd.DataFrame([totals_data], columns=df.columns)

    # Append the totals row to the original DataFrame and return it
    df_with_totals = pd.concat([df, totals_row], ignore_index=True)
    return df_with_totals


def rename_cols(df):
    df.rename(columns={
        'initial_margin': 'im',
        'maintenance_margin': 'mm',
        'unrealised_pnl': 'upl',
        'current_balance_usd': 'live_bal_usd',
        'current_balance': 'live_bal',
        'available_balance': 'avail_bal',
    }, inplace=True)
    return df


async def fetch_balances(exchange_id: str):
    # Get venues firstly:
    venues_df = await get_my_venues()
    # Filter by exchange_id
    if exchange_id is None:
        active_ids = venues_df['company_exchange_id'].tolist()
    else:
        active_ids = venues_df[venues_df['exchange_id'] == exchange_id]['company_exchange_id'].tolist()

    balances = await get_balances(active_ids)   # active_ids
    # Collect all balances into a single list
    all_balances = [pos for item in balances for pos in item['balances']]
    balances_df = pd.DataFrame(all_balances)

    if balances_df.empty:
        return balances_df

    balances_df = pd.merge(balances_df, venues_df[['company_exchange_id', 'alias']], on='company_exchange_id', how='left')

    # Rename columns
    balances_df = rename_cols(balances_df)

    # Remove rows where col 'live_bal_usd' < BALANCE_THRESHOLD_USD
    balances_df = balances_df[balances_df['live_bal_usd'] > BALANCE_THRESHOLD_USD]

    balances_df['im_usd'] = balances_df['im'] * balances_df['index_price']
    balances_df['mm_usd'] = balances_df['mm'] * balances_df['index_price']
    balances_df['upl_usd'] = balances_df['upl'] * balances_df['index_price']
    balances_df['avail_bal_usd'] = balances_df['avail_bal'] * balances_df['index_price']
    balances_df['im_usd_pct'] = balances_df['im_usd'] / balances_df['live_bal_usd'] * 100
    balances_df['mm_usd_pct'] = balances_df['mm_usd'] / balances_df['live_bal_usd'] * 100

    balances_df.fillna(0, inplace=True)
    result_df = add_balance_totals_row(balances_df, 'alias', balance_columns_to_sum())
    # Only want specific columns from my list here
    result_df = result_df[balance_columns()]
    return result_df


async def run_balances(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching balances data...")
    try:

        exchange_id = None

        # Get the arguments passed after the command (balances <variable>)
        if context.args:  # Check if there are any arguments passed
            exchange_id = context.args[0]  # First argument after the command
            # Apply filter to the table based on exchange_id

        bal_table = await fetch_balances(exchange_id)

        if bal_table.empty:
            await update.message.reply_text("No balances found.")
            return

        bal_file = await send_telegram_table(bal_table, 2)
        # Send the image
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bal_file)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


# df = asyncio.run(fetch_balances())