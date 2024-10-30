def balance_columns():
    return [
        "alias",
        # "company_exchange_id"
        "exchange_id",
        "asset",
        "live_bal",
        "upl",
        "im",
        "mm",
        "im_usd",
        "mm_usd",
        "upl_usd",
        "im_usd_pct",
        "mm_usd_pct",
        "live_bal_usd",
        "index_price",
        "avail_bal",
        # "update_ms",
        "margin_mode",
        # "is_margin_asset",
        # "avail_bal_usd"
    ]


# Description: Columns to SUM in the intra pnl table.
def balance_columns_to_sum():
    return [
        # 'live_bal',
        'im_usd',
        'mm_usd',
        'upl_usd',
        'live_bal_usd',
        # "avail_bal_usd"
    ]
