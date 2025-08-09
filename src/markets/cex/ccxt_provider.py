from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

import ccxt

from src.markets.base import BarInterval, Instrument, MarketDataProvider, OhlcvBar


_INTERVAL_MAP = {
    BarInterval.M1: "1m",
    BarInterval.M5: "5m",
    BarInterval.H1: "1h",
    BarInterval.D1: "1d",
}


class CcxtProvider(MarketDataProvider):
    def __init__(self, exchange_id: str = "binance", enable_rate_limit: bool = True, api_key: Optional[str] = None, secret: Optional[str] = None):
        if not hasattr(ccxt, exchange_id):
            raise ValueError(f"Unsupported exchange: {exchange_id}")
        exchange_cls = getattr(ccxt, exchange_id)
        self.exchange = exchange_cls({
            "enableRateLimit": enable_rate_limit,
            "apiKey": api_key or None,
            "secret": secret or None,
        })
        self.exchange.load_markets()

    def _symbol(self, instrument: Instrument) -> str:
        sym1 = f"{instrument.base}/{instrument.quote}"
        # ccxt may have multiple market ids; we rely on unified symbol mapping after load_markets
        if sym1 in self.exchange.markets:
            return sym1
        # try uppercase normalization
        sym2 = f"{instrument.base.upper()}/{instrument.quote.upper()}"
        if sym2 in self.exchange.markets:
            return sym2
        # attempt USDT vs USDC substitution when necessary
        alt_quote = "USDT" if instrument.quote.upper() == "USDC" else instrument.quote.upper()
        sym3 = f"{instrument.base.upper()}/{alt_quote}"
        if sym3 in self.exchange.markets:
            return sym3
        raise ValueError(f"Symbol not found on {self.exchange.id}: {instrument.base}/{instrument.quote}")

    def get_ohlcv(self, instrument: Instrument, interval: BarInterval, start_ms: int, end_ms: int) -> list[OhlcvBar]:
        timeframe = _INTERVAL_MAP[interval]
        symbol = self._symbol(instrument)
        limit = 1000
        results: list[OhlcvBar] = []
        since = start_ms
        while True:
            batch = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
            if not batch:
                break
            for ts, o, h, l, c, v in batch:
                if ts > end_ms:
                    return results
                results.append(OhlcvBar(time=ts, open=o, high=h, low=l, close=c, volume=v))
            # advance since to last + timeframe
            last_ts = batch[-1][0]
            # safety: break if no progress
            if last_ts == since:
                break
            since = last_ts + 1
            # be gentle
            time.sleep(self.exchange.rateLimit / 1000.0)
        return results

    def get_quote(self, instrument: Instrument) -> float:
        symbol = self._symbol(instrument)
        ticker = self.exchange.fetch_ticker(symbol)
        if ticker and ticker.get("last"):
            return float(ticker["last"])
        if ticker and ticker.get("close"):
            return float(ticker["close"])
        raise RuntimeError(f"No quote available for {symbol}")