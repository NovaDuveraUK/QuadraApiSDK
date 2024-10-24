# Description: Columns for the intra pnl table.
def intra_pnl_columns():
    return [
        'alias',
        # 'company_exchange_id',
        'exchange_id',
        'symbol',
        'no_trades',
        'vol_base',
        'vol_quote',
        'vol_24h',
        'pct_vol_24h',
        'maker',
        'avg_price',
        'mark_price',
        'fees_usd',
        'pnl_quote',
        'pnl_incl_fees',
        'pnl_per_vol_bps',
        'pnl_per_vol_bps_fees',
    ]

