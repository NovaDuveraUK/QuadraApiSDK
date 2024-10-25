import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from src.rest.examples.account.getPositions import get_positions
from src.tg.handlers.shared import get_my_venues, send_telegram_table
from src.tg.config.columns.positions import position_columns


async def fetch_positions():
    # Get venues firstly:
    venues_df = await get_my_venues()
    # Return column as list for column called 'company_exchange_id'
    active_ids = venues_df['company_exchange_id'].tolist()
    positions = await get_positions(['92a59c8a-db55-49ed-84f9-3c71a9a090c9'])   # active_ids
    # Collect all positions into a single list
    all_positions = [pos for item in positions for pos in item['positions']]
    positions_df = pd.DataFrame(all_positions)

    if positions_df.empty:
        return positions_df

    positions_df = pd.merge(positions_df, venues_df[['company_exchange_id', 'alias']], on='company_exchange_id', how='left')
    # Only want specific columns from my list here
    positions_df = positions_df[position_columns()]
    return positions_df


async def run_positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching positions data...")
    try:
        pos_table = await fetch_positions()

        # Get the arguments passed after the command (positions <variable>)
        if context.args:  # Check if there are any arguments passed
            exchange_id = context.args[0]  # First argument after the command
            # Apply filter to the table based on exchange_id
            pos_table = pos_table[pos_table['exchange_id'] == exchange_id]

        # Check if the table is empty
        if pos_table.empty:
            await update.message.reply_text("No positions found.")
            return

        pos_file = await send_telegram_table(pos_table)
        # Send the image
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=pos_file)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


