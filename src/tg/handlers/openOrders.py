import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from src.rest.examples.account.getOpenOrders import get_open_orders
from src.tg.handlers.shared import get_my_venues, send_telegram_table
from src.tg.config.columns.openOrders import open_order_columns


async def fetch_open_orders():
    # Get venues firstly:
    venues_df = await get_my_venues()
    # Return column as list for column called 'company_exchange_id'
    active_ids = venues_df['company_exchange_id'].tolist()
    open_orders = await get_open_orders(active_ids)
    # Collect all open orders into a single list
    all_open_orders = [order for item in open_orders for order in item['open_orders']]
    open_orders_df = pd.DataFrame(all_open_orders)

    if open_orders_df.empty:
        return open_orders_df

    open_orders_df = pd.merge(open_orders_df, venues_df[['company_exchange_id', 'alias']], on='company_exchange_id', how='left')
    # Only want specific columns from my list here
    open_orders_df = open_orders_df[open_order_columns()]
    return open_orders_df


async def run_open_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching open orders data...")
    try:
        open_order_table = await fetch_open_orders()

        # Get the arguments passed after the command (positions <variable>)
        if context.args:  # Check if there are any arguments passed
            exchange_id = context.args[0]  # First argument after the command
            # Apply filter to the table based on exchange_id
            open_order_table = open_order_table[open_order_table['exchange_id'] == exchange_id]

        # Check if the table is empty
        if open_order_table.empty:
            await update.message.reply_text("No open orders found.")
            return

        open_order_file = await send_telegram_table(open_order_table)
        # Send the image
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open_order_file)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


