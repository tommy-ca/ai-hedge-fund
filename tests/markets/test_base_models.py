from decimal import Decimal

from src.markets.base import BarInterval, ExecutionContext, Instrument, MarketType


def test_market_type_values():
    assert MarketType.EQUITY.value == "EQUITY"
    assert MarketType.CRYPTO_CEX.value == "CRYPTO_CEX"
    assert MarketType.CRYPTO_DEX.value == "CRYPTO_DEX"


def test_instrument_dataclass():
    inst = Instrument(base="BTC", quote="USDC", exchange="binance")
    assert inst.base == "BTC"
    assert inst.quote == "USDC"
    assert inst.exchange == "binance"


def test_execution_context_defaults():
    ctx = ExecutionContext(instrument=Instrument("BTC", "USDC"), qty=Decimal("0.5"), side="buy")
    assert ctx.fee_bps == 0.0
    assert ctx.slippage_bps == 0.0
    assert ctx.gas_usd == 0.0


def test_bar_interval_members():
    assert BarInterval.M1.value == "1m"
    assert BarInterval.M5.value == "5m"
    assert BarInterval.H1.value == "1h"
    assert BarInterval.D1.value == "1d"