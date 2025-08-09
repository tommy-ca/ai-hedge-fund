from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import requests

from src.markets.base import BarInterval, Instrument, OhlcvBar


UNI_V3_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"


@dataclass
class PoolInfo:
    id: str
    feeTier: int
    token0: str
    token1: str


def _query_graph(query: str, variables: dict) -> dict:
    resp = requests.post(UNI_V3_SUBGRAPH, json={"query": query, "variables": variables}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def resolve_pool(base: str, quote: str, fee_preference: Optional[int] = 3000) -> PoolInfo:
    # Try popular fee tiers: 500, 3000, 10000 (0.05%, 0.3%, 1%)
    fee_tiers = [fee_preference or 3000, 500, 10000]
    for fee in fee_tiers:
        q = """
        query($t0: String!, $t1: String!, $fee: Int!) {
          pools(first: 1, where: {feeTier: $fee, token0_: {symbol: $t0}, token1_: {symbol: $t1}}) { id feeTier token0 { symbol } token1 { symbol } }
        }
        """
        res = _query_graph(q, {"t0": base.upper(), "t1": quote.upper(), "fee": fee})
        pools = res.get("pools", [])
        if pools:
            p = pools[0]
            return PoolInfo(id=p["id"], feeTier=int(p["feeTier"]), token0=p["token0"]["symbol"], token1=p["token1"]["symbol"])
    raise RuntimeError(f"Pool not found for {base}/{quote}")


def fetch_hourly_ohlcv(pool_id: str, start_ts: int, end_ts: int) -> List[OhlcvBar]:
    # Use poolHourData for ohlc
    q = """
    query($pool: String!, $start: Int!, $end: Int!) {
      poolHourDatas(first: 1000, where: { pool: $pool, periodStartUnix_gte: $start, periodStartUnix_lte: $end }, orderBy: periodStartUnix, orderDirection: asc) {
        periodStartUnix
        high
        low
        open
        close
        volumeUSD
      }
    }
    """
    res = _query_graph(q, {"pool": pool_id, "start": start_ts, "end": end_ts})
    items = res.get("poolHourDatas", [])
    bars: List[OhlcvBar] = []
    for it in items:
        ts = int(it["periodStartUnix"]) * 1000
        bars.append(OhlcvBar(time=ts, open=float(it["open"]), high=float(it["high"]), low=float(it["low"]), close=float(it["close"]), volume=float(it["volumeUSD"])) )
    return bars


def get_ohlcv(instrument: Instrument, interval: BarInterval, start_ms: int, end_ms: int) -> List[OhlcvBar]:
    if interval != BarInterval.H1:
        raise NotImplementedError("Uniswap provider currently supports hourly data only")
    pool = resolve_pool(instrument.base, instrument.quote)
    return fetch_hourly_ohlcv(pool.id, int(start_ms / 1000), int(end_ms / 1000))