# Design — Crypto Markets (CEX + DEX)

## Architecture Overview
- Market types: EQUITY | CRYPTO_CEX | CRYPTO_DEX
- Providers:
  - CCXT REST (OHLCV, markets metadata) for Binance, OKX, Bybit, Bitget
  - Cryptofeed WS (trades/orderbook) optional for slippage modeling
  - Uniswap v3 via The Graph for DEX pool data
- Execution:
  - CEXSimulator: taker fee bps, optional slippage via L2/trades snapshot
  - DEXSimulator: x*y=k AMM with fee tier and gas cost
- Portfolio:
  - PortfolioV2 for crypto: balances by asset (Decimal), valuation in quote and USD
  - Legacy equities positions preserved for equities mode

## Key Modules
- src/markets/base.py
  - MarketType (Enum)
  - Instrument
  - MarketDataProvider: get_ohlcv(pair, interval, start, end), get_quote(pair), get_orderbook(pair, levels), get_trades(pair, since)
  - ExecutionSimulator: simulate_buy(ctx), simulate_sell(ctx)
- src/markets/cex/ccxt_provider.py
  - CCXT adapter with exchange routing (binance, okx, bybit, bitget)
  - Symbol normalization and market_id mapping
  - Rate-limit/backoff and caching integration
- src/markets/cex/cryptofeed_stream.py
  - Optional consumer for trades/orderbook snapshots (for testing and advanced slippage)
- src/markets/dex/uniswap.py
  - Pool resolution, poolDayData/hourData retrieval, OHLCV derivation
- src/markets/simulators/cex.py
  - Fee and slippage application using orderbook/trades when available; fallback to bps
- src/markets/simulators/dex.py
  - Constant product AMM math (price impact), fee tier, gas

## Data Models (Pydantic)
- Instrument: { base: str, quote: str, exchange?: str, market_id?: str, chain?: str, pool_address?: str }
- BarInterval: enum { 1m, 5m, 1h, 1d }
- OhlcvBar: { time: str, open: float, high: float, low: float, close: float, volume: float }
- OrderbookSnapshot: { bids: list[[price, size]], asks: list[[price, size]], ts: int }
- Trade: { price: float, size: float, side: str, ts: int }
- ExecutionContext: { instrument, qty, side, price_ref, fee_bps, slippage_bps, gas_usd, orderbook?, trades? }
- PortfolioV2: { balances: dict[str, Decimal], quote_currency: str }

## API Contract Changes
- Extend HedgeFundRequest with:
  - market_type: string (EQUITY | CRYPTO_CEX | CRYPTO_DEX)
  - instruments?: array[Instrument]
  - exchange?: string (for CRYPTO_CEX)
  - bar_interval?: BarInterval
  - quote_currency?: string
  - fee_bps?: number
  - slippage_bps?: number
  - gas_usd_per_trade?: number
- Backwards compatibility: if missing, default to EQUITY and current fields.

## Backtester Behavior
- Calendar:
  - EQUITY: business days
  - CRYPTO_*: 24/7; interval-driven resampling
- Execution:
  - Use decimal quantities; apply fees/slippage; apply gas for DEX
  - Disable short by default for crypto spot

## Error Handling & Resilience
- CCXT: handle DDoSProtection/RateLimitExceeded; retry with backoff
- Cryptofeed: auto-reconnect; bounded buffers; snapshot throttling
- Caching: reuse OHLCV results keyed by (exchange, pair, interval, start, end)

## Security & Compliance
- No private keys stored; no trading endpoints used
- Respect exchange TOS and data policies

## Testing Strategy
- Unit tests for adapters, AMM math, simulators
- Integration tests: BTC/USDC and ETH/USDC across Binance/OKX/Bybit/Bitget
- Fixtures: recorded OHLCV, sample orderbooks/trades, pool snapshots