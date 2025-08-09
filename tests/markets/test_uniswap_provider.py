from datetime import datetime, timedelta, timezone

import pytest

from src.markets.base import BarInterval, Instrument
from src.markets.dex.uniswap import get_ohlcv


@pytest.mark.integration
def test_uniswap_hourly_weth_usdc_smoke():
    inst = Instrument(base="WETH", quote="USDC")
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(days=2)
    bars = get_ohlcv(inst, BarInterval.H1, int(start.timestamp() * 1000), int(end.timestamp() * 1000))
    assert isinstance(bars, list)
    assert len(bars) > 0
    assert bars[0].open >= 0 and bars[0].close >= 0