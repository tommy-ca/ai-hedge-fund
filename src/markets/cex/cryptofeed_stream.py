from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple

try:
    from cryptofeed import FeedHandler
    from cryptofeed.callback import BookCallback, TradeCallback
    from cryptofeed.defines import L2_BOOK, TRADES
    from cryptofeed.exchanges import Binance, OKX, Bybit, Bitget
except Exception:  # pragma: no cover - optional dependency
    FeedHandler = None


@dataclass
class OrderbookSnapshot:
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]
    ts: float


class StreamCollector:
    """Collects a bounded number of trades and L2 orderbooks per symbol."""

    def __init__(self, maxlen: int = 100):
        self.trades: Dict[str, Deque[dict]] = {}
        self.books: Dict[str, Deque[OrderbookSnapshot]] = {}
        self.maxlen = maxlen

    def _ensure(self, symbol: str):
        if symbol not in self.trades:
            self.trades[symbol] = deque(maxlen=self.maxlen)
        if symbol not in self.books:
            self.books[symbol] = deque(maxlen=self.maxlen)

    async def trade_cb(self, feed, pair: str, order_id: str, timestamp: float, side: str, amount: float, price: float, **kwargs):
        self._ensure(pair)
        self.trades[pair].append({"ts": timestamp, "side": side, "amount": amount, "price": price})

    async def book_cb(self, feed, pair: str, book, timestamp: float, **kwargs):
        self._ensure(pair)
        bids = [(float(p), float(q)) for p, q in list(book.book.bids.items())[:20]]
        asks = [(float(p), float(q)) for p, q in list(book.book.asks.items())[:20]]
        self.books[pair].append(OrderbookSnapshot(bids=bids, asks=asks, ts=timestamp))


def start_stream(exchanges: list[str], pairs: list[str], collector: StreamCollector, run_seconds: int = 10):
    """Start Cryptofeed FeedHandler for selected exchanges/pairs and collect briefly."""
    if FeedHandler is None:
        raise RuntimeError("cryptofeed not installed")
    fh = FeedHandler()
    exchange_map = {
        "binance": Binance,
        "okx": OKX,
        "bybit": Bybit,
        "bitget": Bitget,
    }
    for ex in exchanges:
        ex_cls = exchange_map.get(ex.lower())
        if not ex_cls:
            continue
        fh.add_feed(ex_cls(channels=[L2_BOOK, TRADES], symbols=pairs, callbacks={
            L2_BOOK: BookCallback(collector.book_cb),
            TRADES: TradeCallback(collector.trade_cb),
        }))
    fh.run(after=run_seconds)