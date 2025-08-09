import time
from datetime import datetime, timedelta, timezone

import pytest

from src.markets.base import BarInterval, Instrument
from src.markets.cex.ccxt_provider import CcxtProvider


@pytest.mark.integration
def test_binance_ohlcv_hourly_btc_usdc_smoke():
    provider = CcxtProvider(exchange_id="binance")
    inst = Instrument(base="BTC", quote="USDC", exchange="binance")
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(days=2)
    bars = provider.get_ohlcv(inst, BarInterval.H1, int(start.timestamp() * 1000), int(end.timestamp() * 1000))
    assert isinstance(bars, list)
    assert len(bars) > 0
    first = bars[0]
    assert first.open >= 0 and first.close >= 0


@pytest.mark.integration
def test_binance_quote_btc_usdc_smoke():
    provider = CcxtProvider(exchange_id="binance")
    inst = Instrument(base="BTC", quote="USDC", exchange="binance")
    price = provider.get_quote(inst)
    assert price > 0