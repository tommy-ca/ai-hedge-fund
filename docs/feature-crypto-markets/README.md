# Crypto Markets (CEX + DEX) Integration

## Purpose
Add crypto market simulation (CEX spot + DEX AMM) to the AI Hedge Fund while preserving equities behavior.

## Scope
- Equities remain default and unchanged by default inputs
- Crypto CEX via CCXT: Binance, OKX, Bybit, Bitget (public REST; optional keys)
- Crypto DEX (Uniswap v3) supported
- No live trading; simulation/backtesting only

## CEX Integrations
- Libraries: CCXT (REST/metadata), Cryptofeed (WebSocket trades/orderbook)
- Exchanges: Binance, OKX, Bybit, Bitget
- Data: OHLCV via CCXT; optional L2/trades via Cryptofeed for slippage modeling
## Non-Goals
- Derivatives, perps, options, real execution, wallets/signing
- Margin/short for spot by default
