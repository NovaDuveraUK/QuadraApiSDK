import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, JobQueue
from decouple import config

from src.tg.handlers.intraTrading import run_intra_pnl
from src.tg.handlers.openOrders import run_open_orders
from src.tg.handlers.positions import run_positions

TOKEN = config('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, from py')


def main():
    print("Starting the application...")
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("positions", run_positions))
    application.add_handler(CommandHandler("openOrders", run_open_orders))
    application.add_handler(CommandHandler("intraPnl", run_intra_pnl))

    # Create a JobQueue instance and start it
    # job_queue = JobQueue()
    # job_queue.set_application(application)  # Attach job queue to the application

    # Schedule the check_pnl function to run every 10 minutes
    # job_queue.run_repeating(check_pnl_scheduled, interval=600, first=600)  # Runs every 10 minutes, first run after 10s

    # Start the JobQueue (await the async job queue start)
    # await job_queue.start()

    # Run the bot until the user presses Ctrl-C
    # application.run_polling(stop_signals=None)
    return application


if __name__ == '__main__':
    application = main()
    application.run_polling(stop_signals=None)