# Implementation Plan & Tasks

## Epics
- E0: Abstractions/compatibility
- E1: CEX provider(s)
- E2: DEX provider (Uniswap v3)
- E3: Execution simulators (CEX/DEX)
- E4: PortfolioV2 + Backtester updates
- E5: Risk manager updates
- E6: Backend API/schema changes
- E7: Frontend UX changes
- E8: Docs/examples
- E9: Tests/CI

## Tasks (condensed)
- Add enums/models in src/data/models.py
- Add interfaces in src/markets/base.py
- Implement src/markets/cex/binance.py, coinbase.py
- Implement src/markets/dex/uniswap.py
- Add simulators in src/markets/simulators/{cex,dex}.py
- Upgrade backtester calendar/exec path (crypto/equity modes)
- Update risk manager for spot constraints
- Extend backend request/response schemas; route by market_type
- Frontend: market/pair/exchange/chain/interval/fees UI + payload
- Unit/integration tests and fixtures
