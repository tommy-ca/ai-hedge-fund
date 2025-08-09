# Steering & Decision Log

## Principles
- Backward compatibility first
- Be explicit in market type and instrument modeling
- Prefer simple, testable simulators over perfect realism

## Key Decisions
- Use CCXT for CEX REST/data (Binance, OKX, Bybit, Bitget)
- Use Cryptofeed for WebSocket (trades/orderbook) where needed
- Use The Graph for Uniswap v3 pool data; AMM math for fills
- Decimal portfolio balances; keep equities positions intact via mapping

## Risks
- Exchange-specific quirks and symbol mappings; mitigate with unified adapter and tests
- Rate limits and disconnects; mitigate with backoff, retries, and caching

## Open Questions
- Which chains/pools to support beyond mainnet v3?
- How to model liquidity over intervals (snapshots vs continuous)?
