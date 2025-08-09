# Architecture & Design - Crypto Markets

## Abstractions
- MarketType: EQUITY | CRYPTO_CEX | CRYPTO_DEX
- Instrument: { base, quote, exchange?, chain?, pool_address? }
- MarketDataProvider: get_ohlcv(), get_quote()
- ExecutionSimulator: simulate_buy(), simulate_sell()
  - CEX: taker fee bps, slippage bps
  - DEX: x*y=k AMM (fee tier), gas per trade
- PortfolioV2: balances by asset (decimals), plus legacy equities mapping

## Providers
- CEX: Binance (klines), Coinbase (candles)
- DEX: Uniswap v3 via The Graph (poolDayData/hourData)

## Backtester Changes
- 24/7 calendar; interval param; decimal qty; apply fees/slippage/gas
- Equities path preserved

## API Changes
Extend HedgeFundRequest with crypto params (market_type, instruments, bar_interval, quote_currency, fee_bps, slippage_bps, gas_usd_per_trade).
Defaults preserve equities behavior.
