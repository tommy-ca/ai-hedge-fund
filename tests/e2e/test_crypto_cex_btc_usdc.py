from datetime import datetime, timedelta, timezone

from src.markets.base import BarInterval, Instrument
from src.markets.cex.ccxt_provider import CcxtProvider


def test_e2e_binance_btc_usdc_hourly_fetch_and_quote():
    provider = CcxtProvider(exchange_id="binance")
    inst = Instrument(base="BTC", quote="USDC", exchange="binance")
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(hours=6)
    bars = provider.get_ohlcv(inst, BarInterval.H1, int(start.timestamp() * 1000), int(end.timestamp() * 1000))
    assert len(bars) >= 1
    price = provider.get_quote(inst)
    # last bar close and quote should be in the same ballpark (sanity check, loose)
    last_close = bars[-1].close
    assert price > 0 and last_close > 0
    assert 0.5 < price / last_close < 2.0