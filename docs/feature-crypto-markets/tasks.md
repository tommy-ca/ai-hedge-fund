# Tasks — Crypto Markets (CEX + DEX)

## Legend
- [REQ-###]: maps to Requirements
- (UT): unit test, (IT): integration test, (E2E): end-to-end

## Sequenced Tasks

1. Foundations (E0)
   - T1.1 Add enums and models (MarketType, Instrument, BarInterval) [REQ-001..003]
   - T1.2 Create interfaces in `src/markets/base.py` [REQ-004..008]
   - Tests: (UT) model validation; provider interface contracts

2. CCXT Provider (E1)
   - T2.1 Implement `src/markets/cex/ccxt_provider.py` with routing for Binance/OKX/Bybit/Bitget [REQ-004]
   - T2.2 Symbol normalization and market_id mapping [REQ-004]
   - T2.3 Rate-limit/backoff integration; cache OHLCV [REQ-010]
   - Tests: (IT) OHLCV fetch for BTC/USDC hourly; (UT) normalization edge cases

3. Cryptofeed Streams (E1 optional)
   - T3.1 Implement `src/markets/cex/cryptofeed_stream.py` to capture trades/orderbook snapshots [REQ-004]
   - T3.2 Snapshot persistence for simulator use [REQ-004]
   - Tests: (IT) subscribe and collect bounded samples; (UT) reconnection logic

4. Uniswap v3 Provider (E2)
   - T4.1 Implement `src/markets/dex/uniswap.py` pool resolution and poolDayData/hourData [REQ-005]
   - T4.2 Derive OHLCV from snapshots [REQ-005]
   - Tests: (IT) WETH/USDC hourly series; (UT) OHLCV derivation

5. Simulators (E3)
   - T5.1 Implement `src/markets/simulators/cex.py` (fee/slippage; orderbook when available) [REQ-007]
   - T5.2 Implement `src/markets/simulators/dex.py` (AMM price impact, fee tier, gas) [REQ-005, REQ-007]
   - Tests: (UT) AMM invariants and fee math; (UT) slippage application; (IT) run small trade set

6. PortfolioV2 and Backtester (E4)
   - T6.1 Add PortfolioV2 with decimal balances and valuation [REQ-008]
   - T6.2 Update backtester: 24/7 calendar for crypto; interval param [REQ-006]
   - T6.3 Update execution path to use simulators, decimal qty [REQ-007]
   - T6.4 Disable short by default in crypto modes [REQ-007]
   - Tests: (UT) valuation; (E2E) BTC/USDC backtest 30 days

7. Risk Manager Updates (E5)
   - T7.1 Add spot constraints and per-asset caps [REQ-007]
   - T7.2 Optionally add vol-based sizing for crypto
   - Tests: (UT) constraints applied; (IT) no invalid shorts

8. Backend API/Schema (E6)
   - T8.1 Extend request models with new fields [REQ-001..009]
   - T8.2 Route by market_type; validate exchange/chain/pool [REQ-002..003]
   - T8.3 Maintain backward compatibility [REQ-009]
   - Tests: (UT) schema; (IT) API runs for equity and crypto

9. Frontend UX (E7)
   - T9.1 Add market selector and crypto configuration inputs [REQ-001..003]
   - T9.2 Include interval/fees/gas in payload [REQ-006..007]
   - T9.3 Keep equities UX unchanged by default [REQ-001]
   - Tests: (E2E) configure and run crypto flow

10. Docs & Examples (E8)
   - T10.1 Update README/app docs; .env notes for keys
   - T10.2 Provide example configs for Binance/OKX/Bybit/Bitget

11. CI & Tests (E9)
   - T11.1 Add CI jobs for unit/integration tests with recorded fixtures
   - T11.2 Flaky WS tests marked optional/skipped by default