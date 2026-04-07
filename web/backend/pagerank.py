from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


@dataclass(slots=True)
class Airport:
    code: str
    name: str
    country: str
    lat: float
    lon: float
    index: int = 0
    outweight: float = 0.0
    in_edges: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class GraphInfo:
    n_airports: int
    n_routes: int
    n_disconnected: int


@dataclass(slots=True)
class PageRankResult:
    rankings: list[dict]
    iterations: int
    time_ms: float
    convergence: list[float]
    damping: float
    init_strategy: str


_airports: dict[str, Airport] = {}
_airport_list: list[Airport] = []
_loaded = False


def _load():
    global _airports, _airport_list, _loaded
    if _loaded:
        return
    _airports = {}
    _airport_list = []

    with open(DATA_DIR / "airports.txt", encoding="utf-8") as f:
        idx = 0
        for line in f:
            parts = line.strip().split(",")
            try:
                if len(parts[4]) != 5:
                    continue
                code = parts[4][1:-1]
                name = parts[1][1:-1] + ", " + parts[3][1:-1]
                country = parts[3][1:-1]
                lat = float(parts[6])
                lon = float(parts[7])
                a = Airport(code=code, name=name, country=country, lat=lat, lon=lon, index=idx)
                _airports[code] = a
                _airport_list.append(a)
                idx += 1
            except (IndexError, ValueError):
                continue

    with open(DATA_DIR / "routes.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            try:
                if len(parts[2]) != 3 or len(parts[4]) != 3:
                    continue
                origin = parts[2]
                dest = parts[4]
                if origin not in _airports or dest not in _airports:
                    continue
                dest_ap = _airports[dest]
                if origin in dest_ap.in_edges:
                    dest_ap.in_edges[origin] += 1.0
                else:
                    dest_ap.in_edges[origin] = 1.0
                _airports[origin].outweight += 1.0
            except (IndexError, ValueError):
                continue

    _loaded = True


def get_airports() -> list[dict]:
    _load()
    return [
        {"code": a.code, "name": a.name, "country": a.country, "lat": a.lat, "lon": a.lon}
        for a in _airport_list
    ]


def get_graph_stats() -> GraphInfo:
    _load()
    n_routes = sum(len(a.in_edges) for a in _airport_list)
    n_disc = sum(1 for a in _airport_list if a.outweight == 0)
    return GraphInfo(n_airports=len(_airport_list), n_routes=n_routes, n_disconnected=n_disc)


def compute_pagerank(
    damping: float = 0.8,
    init_strategy: str = "nth",
    max_iterations: int = 200,
    tolerance: float = 1e-10,
) -> PageRankResult:
    _load()
    t0 = time.perf_counter()
    n = len(_airport_list)

    if init_strategy == "one":
        P = [0.0] * n
        P[0] = 1.0
    elif init_strategy == "square":
        sqr = int(math.sqrt(n))
        P = [0.0] * n
        for i in range(sqr):
            P[i] = 1.0 / sqr
    else:
        P = [1.0 / n] * n

    L = damping
    base = (1.0 - L) / n
    disconnected = [a for a in _airport_list if a.outweight == 0]
    n_disc = len(disconnected)

    convergence: list[float] = []

    for it in range(max_iterations):
        disc_mass = sum(P[a.index] for a in disconnected)
        disc_contrib = L * disc_mass / n

        Q = [0.0] * n
        for i, airport in enumerate(_airport_list):
            s = 0.0
            for origin_code, weight in airport.in_edges.items():
                origin = _airports[origin_code]
                s += P[origin.index] * weight / origin.outweight
            Q[i] = L * s + base + disc_contrib

        max_diff = max(abs(P[i] - Q[i]) for i in range(n))
        convergence.append(max_diff)

        P = Q
        if max_diff < tolerance:
            break

    elapsed = (time.perf_counter() - t0) * 1000

    ranked = sorted(
        [(a, P[a.index]) for a in _airport_list],
        key=lambda x: x[1],
        reverse=True,
    )

    rankings = [
        {
            "rank": i + 1,
            "code": a.code,
            "name": a.name,
            "country": a.country,
            "lat": a.lat,
            "lon": a.lon,
            "score": score,
        }
        for i, (a, score) in enumerate(ranked)
    ]

    return PageRankResult(
        rankings=rankings,
        iterations=len(convergence),
        time_ms=elapsed,
        convergence=convergence,
        damping=L,
        init_strategy=init_strategy,
    )
