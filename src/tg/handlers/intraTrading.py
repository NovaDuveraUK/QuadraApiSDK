import time
from typing import List

import pandas as pd
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from src.rest.examples.account.getTradesHistory import get_trades_history
from src.rest.examples.public.getPrices import get_price_by_symbol
from src.tg.config.columns.intraPnl import intra_pnl_columns
from src.tg.config.venues.intraPnl import intra_pnl_venues
from src.tg.handlers.shared import get_my_venues, send_telegram_table, get_unix_timestamp_for_hour


async def fetch_trades(start_time: int, exchange_ids: List[str]):
    limit = 10000
    # Get venues firstly:
    venues_df = await get_my_venues()
    # Filter ones that are not in exchange_ids, col: 'exchange_id'
    active_ids = venues_df[venues_df['exchange_id'].isin(exchange_ids)]['company_exchange_id'].tolist()

    # Asyncio gather on all venues to get all ttr
    tasks = [get_trades_history(x, start_time, limit) for x in active_ids]
    trades_list = await asyncio.gather(*tasks)

    # Create an empty list to hold all DataFrames
    trades_summary = []
    for i, trades in enumerate(trades_list):
        # Convert each list of trades to a DataFrame
        df = pd.DataFrame(trades)
        # print("Processing trades for company_exchange_id: ", active_ids[i])
        # print("Trades DF", df.head(5))

        # If the DataFrame is empty, skip it
        if df.empty:
            continue

        # Group by 'company_exchange_id' and 'symbol'
        grouped_df = df.groupby(['company_exchange_id', 'symbol'])

        # Loop over each group
        for (company_exchange_id, symbol), group in grouped_df:

            # Create a dictionary to hold the summary of the trades
            trade_summary = dict()
            trade_summary['company_exchange_id'] = company_exchange_id
            trade_summary['exchange_id'] = venues_df[venues_df['company_exchange_id'] == company_exchange_id]['exchange_id'].iloc[0]
            trade_summary['symbol'] = symbol
            trade_summary['alias'] = venues_df[venues_df['company_exchange_id'] == trade_summary['company_exchange_id']]['alias'].iloc[0]
            trade_summary['no_trades'] = len(group)
            trade_summary['vol_base'] = group['base_notional'].sum()
            trade_summary['vol_quote'] = group['quote_notional'].sum()
            # Ensure 'entry_price' and 'base_notional' are available in your DataFrame

            group_buys_df = group[group['trade_direction'] == 'buy']
            group_sells_df = group[group['trade_direction'] == 'sell']

            trade_summary['vol_base_buys'] = group_buys_df['base_notional'].sum()
            trade_summary['vol_base_sells'] = group_sells_df['base_notional'].sum()

            # Calculate avg_buy safely
            if group_buys_df['base_notional'].sum() == 0:
                trade_summary['avg_buy'] = None
            else:
                trade_summary['avg_buy'] = (group_buys_df['entry_price'] * group_buys_df['base_notional']).sum() / \
                                           group_buys_df['base_notional'].sum()

            # Calculate avg_sell safely
            if group_sells_df['base_notional'].sum() == 0:
                trade_summary['avg_sell'] = None
            else:
                trade_summary['avg_sell'] = (group_sells_df['entry_price'] * group_sells_df['base_notional']).sum() / \
                                            group_sells_df['base_notional'].sum()

            # trade_summary['avg_price'] = (group['entry_price'] * group['adjusted_notional']).sum() / group['base_notional'].sum()

            trade_summary['fees_usd'] = group['commission_usd'].sum()
            # Calculate the maker volume
            maker_volume = group.loc[group['order_type'] == 'maker', 'base_notional'].sum()
            trade_summary['maker_pct'] = (100 * maker_volume / trade_summary['vol_base']) if trade_summary['vol_base'] > 0 else 0
            # Get mark price for each symbol
            mark_price_data = await get_price_by_symbol(trade_summary['exchange_id'], trade_summary['symbol'])

            trade_summary['mark_price'] = mark_price_data['mid']
            trade_summary['vol_24h'] = mark_price_data['volume']
            # Check if 24h_vol is not zero to avoid division by zero
            if trade_summary['vol_24h'] != 0:
                trade_summary['pct_vol_24h'] = 100 * trade_summary['vol_base'] / trade_summary['vol_24h']
            else:
                trade_summary['pct_vol_24h'] = 0  # Or handle it however you prefer (e.g., None, 'N/A')

            trade_summary['pnl_quote_buys'] = trade_summary['vol_base_buys'] * (trade_summary['mark_price'] - trade_summary['avg_buy'])\
                if trade_summary['avg_buy'] is not None else 0

            trade_summary['pnl_quote_sells'] = trade_summary['vol_base_sells'] * (trade_summary['avg_sell'] - trade_summary['mark_price']) \
                if trade_summary['avg_sell'] is not None else 0
            trade_summary['pnl_quote'] = trade_summary['pnl_quote_buys'] + trade_summary['pnl_quote_sells']
            # Convert to USD using last quote_index_price from group
            trade_summary['pnl_usd'] = trade_summary['pnl_quote'] * group['quote_index_price'].iloc[0]
            trade_summary['pnl_incl_fees'] = trade_summary['pnl_usd'] - trade_summary['fees_usd']
            trade_summary['pnl_per_vol_bps'] = trade_summary['pnl_usd'] / trade_summary['vol_quote'] * 1e4
            trade_summary['pnl_per_vol_bps_fees'] = trade_summary['pnl_incl_fees'] / trade_summary['vol_quote'] * 1e4

            trade_summary['trade_1'] = group['trade_dt'].min()
            trade_summary['trade_n'] = group['trade_dt'].max()

            # print("Grouped DF", group.head(5))

            trades_summary.append(trade_summary)

    # Check if trades summary empty
    if not trades_summary:
        return pd.DataFrame()

    combined_df = pd.DataFrame(trades_summary)
    # print("Combined DF", combined_df.head(5))

    combined_df = combined_df[intra_pnl_columns()]
    return combined_df


async def run_intra_pnl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching intra pnl data...")
    try:
        hour_input = "0"
        exchange_ids = intra_pnl_venues()
        # # Get the arguments passed after the command (intraPnl <variable> <variable2>)
        if context.args:  # Check if there are any arguments passed
            hour_input = context.args[0]  # First argument after the command
            # print("Hour input: ", hour_input)
            if len(context.args) > 1:
                exchange_ids = [context.args[1]]  # First argument after the command
            # Apply filter to the table based on exchange_id
        timestamp_ms, target_datetime = get_unix_timestamp_for_hour(hour_input)
        # print("Timestamps: ", timestamp_ms, target_datetime)
        pnl_table = await fetch_trades(timestamp_ms, exchange_ids)

        # Check if the table is empty
        if pnl_table.empty:
            await update.message.reply_text("No trades found.")
            return

        pnl_file = await send_telegram_table(pnl_table)
        # Send the image
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=pnl_file)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


