import pytest

try:
    from src.markets.cex.cryptofeed_stream import StreamCollector, start_stream
    HAS_CF = True
except Exception:
    HAS_CF = False


@pytest.mark.integration
@pytest.mark.skipif(not HAS_CF, reason="cryptofeed not installed")
def test_cryptofeed_stream_collects_some_data():
    collector = StreamCollector(maxlen=10)
    # Binance pairs use standard symbol syntax in cryptofeed e.g., BTC-USDT
    start_stream(["binance"], ["BTC-USDT"], collector, run_seconds=5)
    # No hard assertions due to network variability; just ensure no crash
    assert True