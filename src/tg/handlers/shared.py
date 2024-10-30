import pandas as pd
from datetime import datetime, timedelta, timezone
from src.rest.examples.account.getVenues import get_venues
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from io import BytesIO


async def get_my_venues():
    # Get venues firstly:
    print("Getting my venues...")
    venues = await get_venues()
    venues_df = pd.DataFrame(venues)
    # Filter dataframe to only include active venues
    venues_df = venues_df[venues_df['deleted'] == False]

    return venues_df


async def send_telegram_table(table, round_value: int = 3):
    # Round numeric columns and fill NaNs with empty strings for clean display
    formatted_table = table.round(round_value).fillna("")

    # Format only numeric columns
    for col in formatted_table.select_dtypes(include=[float, int]).columns:
        formatted_table[col] = formatted_table[col].apply(lambda x: f"{x:,.{round_value}f}" if x != "" else x)

    # Reset the index and rename the index column if needed
    plot_table = formatted_table.reset_index().rename(columns={'index': 'Index'})

    fig, ax = plt.subplots(1, 1)  # Adjust figure size based on table length
    ax.axis('off')
    the_table = ax.table(cellText=plot_table.values,
                         colLabels=plot_table.columns,
                         cellLoc='right',
                         loc='center')

    # Dynamically adjust column width based on content
    the_table.auto_set_column_width(col=list(range(len(plot_table.columns))))
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(9)
    plt.tight_layout()
    plot_file = BytesIO()
    plt.savefig(plot_file, format='png', bbox_inches='tight')  # Increased DPI for better quality
    plot_file.seek(0)
    plt.close(fig)  # Close the figure to free up memory
    return plot_file


def get_unix_timestamp_for_hour(hour_str):
    # Convert the input hour to an integer
    target_hour = int(hour_str)

    # Get the current UTC time (ensuring it's naive to avoid local timezone issues)
    now_utc = datetime.now(timezone.utc)

    # If the target hour is greater than the current hour, we go to yesterday
    if target_hour > now_utc.hour:
        # Use yesterday's date
        target_datetime = (now_utc - timedelta(days=1)).replace(hour=target_hour, minute=0, second=0, microsecond=0)
    else:
        # Use today's date
        target_datetime = now_utc.replace(hour=target_hour, minute=0, second=0, microsecond=0)

    # Convert to Unix timestamp (milliseconds)
    unix_timestamp_ms = int(target_datetime.timestamp() * 1000)

    return unix_timestamp_ms, target_datetime


def add_totals_row(df, label_column, total_columns):
    # Calculate the totals for the specified columns
    totals_data = {col: df[col].sum() for col in total_columns}

    # Set the label for the totals row
    totals_data[label_column] = "TOTAL"

    # Create a new DataFrame for the totals row with the same columns as the original DataFrame
    totals_row = pd.DataFrame([totals_data], columns=df.columns)

    # Append the totals row to the original DataFrame and return it
    df_with_totals = pd.concat([df, totals_row], ignore_index=True)
    return df_with_totals


