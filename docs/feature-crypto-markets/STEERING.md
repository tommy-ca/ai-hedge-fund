# Steering & Decision Log

## Principles
- Backward compatibility first
- Be explicit in market type and instrument modeling
- Prefer simple, testable simulators over perfect realism

## Key Decisions
- Use public CEX endpoints initially (Binance/Coinbase)
- Use The Graph for Uniswap v3 pool data; AMM math for fills
- Decimal portfolio balances; keep equities positions intact via mapping

## Open Questions
- Which chains/pools to support beyond mainnet v3?
- How to model liquidity over intervals (snapshots vs continuous)?
