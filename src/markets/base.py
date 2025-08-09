from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Protocol, Iterable, Optional


class MarketType(str, Enum):
    EQUITY = "EQUITY"
    CRYPTO_CEX = "CRYPTO_CEX"
    CRYPTO_DEX = "CRYPTO_DEX"


@dataclass(frozen=True)
class Instrument:
    base: str
    quote: str
    exchange: Optional[str] = None
    market_id: Optional[str] = None
    chain: Optional[str] = None
    pool_address: Optional[str] = None


@dataclass(frozen=True)
class OhlcvBar:
    time: int  # epoch ms
    open: float
    high: float
    low: float
    close: float
    volume: float


class BarInterval(str, Enum):
    M1 = "1m"
    M5 = "5m"
    H1 = "1h"
    D1 = "1d"


class MarketDataProvider(Protocol):
    def get_ohlcv(self, instrument: Instrument, interval: BarInterval, start_ms: int, end_ms: int) -> list[OhlcvBar]:
        ...

    def get_quote(self, instrument: Instrument) -> float:
        ...


@dataclass
class ExecutionContext:
    instrument: Instrument
    qty: Decimal
    side: str  # "buy" or "sell"
    price_ref: Optional[float] = None
    fee_bps: float = 0.0
    slippage_bps: float = 0.0
    gas_usd: float = 0.0


class ExecutionSimulator(Protocol):
    def simulate_buy(self, ctx: ExecutionContext) -> tuple[Decimal, float]:
        """Returns (filled_qty, cost_in_quote)."""
        ...

    def simulate_sell(self, ctx: ExecutionContext) -> tuple[Decimal, float]:
        """Returns (filled_qty, proceeds_in_quote)."""
        ...