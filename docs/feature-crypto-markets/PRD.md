# Product Requirements (PRD) - Crypto Markets

## Goals
- Add crypto spot markets with CEX and DEX support.
- Keep existing equities workflows intact (backward compatible).

## Must-haves
- Market type selector: Equities | Crypto CEX | Crypto DEX
- Instruments: base/quote pairs (e.g., BTC/USDC).
- 24/7 calendar; configurable bars (1m/5m/1h/1d).
- Decimal quantities; fees/slippage modeling; gas for DEX.
- Portfolio valuation in quote currency; USD conversion.
- DEX AMM execution (Uniswap v3), fee tier, price impact.

## Nice-to-haves
- Multi-provider fallback (Binance->Coinbase).
- Volatility-adjusted position sizing.

## Constraints
- Educational; no execution; public endpoints preferred.
- Backward compatible API/UI/CLI.
