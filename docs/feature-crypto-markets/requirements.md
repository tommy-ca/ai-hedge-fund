# Requirements — Crypto Markets (CEX + DEX)

## Summary
Add crypto spot market simulation to the AI Hedge Fund using CCXT (REST/metadata) and optional Cryptofeed (WebSocket) for Binance, OKX, Bybit, and Bitget, plus DEX via Uniswap v3. Preserve equities behavior by default.

## Stakeholders and Goals
- Learners and researchers: run crypto strategies alongside equities via the same UI/CLI.
- Developers: extendable market abstraction with well-defined interfaces.
- Product: keep backwards compatibility and clear configuration.

## Assumptions
- No real trading or account actions; simulation/backtesting only.
- Public endpoints first; API keys optional where supported.
- Spot only. No derivatives or margin by default.

## Out of Scope
- Perpetuals/options, wallets/signing, on-chain execution, SOR across venues, live trading.

## User Stories
1) As a user, I can select market type (Equity | Crypto CEX | Crypto DEX) so that workflows run in the appropriate mode.
2) As a user, I can configure crypto instruments as base/quote pairs (e.g., BTC/USDC) and choose an exchange (Binance, OKX, Bybit, Bitget) for CEX, or chain/pool for DEX.
3) As a user, I can choose bar interval (1m/5m/1h/1d) and date range and run a backtest.
4) As a user, I see portfolio values and PnL in the quote currency (and USD conversion when applicable).
5) As a user, I see trades executed with fees/slippage modeled; for DEX, gas is included.
6) As a user, I can keep running equities flows without changing my existing configs.

## Acceptance Criteria (EARS)
- [REQ-001] When the user selects market type = "Equity", then the system shall run the existing equities flow unchanged.
- [REQ-002] When the user selects market type = "Crypto CEX", then the system shall require selecting an exchange in {Binance, OKX, Bybit, Bitget} and a base/quote pair.
- [REQ-003] When the user selects market type = "Crypto DEX", then the system shall require selecting chain and pool (Uniswap v3) or a resolvable base/quote to pool mapping.
- [REQ-004] When market type is "Crypto CEX", the system shall fetch OHLCV via CCXT and may fetch recent trades/orderbook via Cryptofeed when available to estimate slippage.
- [REQ-005] When market type is "Crypto DEX", the system shall fetch pool data via The Graph (poolDayData/hourData) and simulate execution via constant product AMM with fee tier and gas costs.
- [REQ-006] When market type is crypto (CEX or DEX), the backtester shall use a 24/7 calendar and support intervals {1m,5m,1h,1d}.
- [REQ-007] When executing trades in crypto modes, the system shall support decimal quantities and apply configured taker fees (bps), slippage (bps) and, for DEX, gas (USD) per trade.
- [REQ-008] The system shall maintain portfolio balances by asset (decimals) for crypto while preserving equities positions format for equities runs.
- [REQ-009] The system shall remain backwards compatible when new fields are omitted (defaults to equities behavior).
- [REQ-010] The system shall gracefully handle rate limits and disconnections with retries/backoff and local caching.

## Non-Functional Requirements
- Reliability: retries/backoff for CCXT/Cryptofeed; cache OHLCV results.
- Performance: batch requests where possible; reuse markets metadata.
- Observability: log provider requests, retries, and simulator summaries per trade.
- Testability: unit tests for adapters, AMM math, and simulators; integration tests per exchange.

## Data Providers & Exchanges
- CCXT for REST OHLCV/metadata: Binance, OKX, Bybit, Bitget.
- Cryptofeed for optional WebSocket trades/orderbook: same exchanges (where supported).
- Uniswap v3 via The Graph for DEX pool data.

## Compliance & Legal
- Educational use only; no execution of real orders; respect exchange TOS and rate limits.