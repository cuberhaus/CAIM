from __future__ import annotations

# ── Phase 14 (Option A) — Sentry SDK + JSON-line stdout (no-op if missing) ─
try:
    from ._sentry_obs import init_observability  # type: ignore[import-not-found]

    init_observability(service="caim")
except ImportError:
    pass

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import pagerank, zipf

app = FastAPI(title="CAIM Explorer")
_pool = ThreadPoolExecutor(max_workers=2)

DIST_DIR = Path(__file__).parent.parent / "frontend" / "dist"


class PageRankRequest(BaseModel):
    damping: float = 0.8
    init_strategy: str = "nth"
    max_iterations: int = 200
    tolerance: float = 1e-10


class ZipfAnalyzeRequest(BaseModel):
    dataset: str = "novels"
    top_n: int = 1000


class ZipfCustomRequest(BaseModel):
    text: str
    top_n: int = 1000


@app.get("/api/status")
async def status():
    return {"status": "ok"}


@app.get("/api/airports")
async def airports():
    return pagerank.get_airports()


@app.get("/api/graph-stats")
async def graph_stats():
    info = pagerank.get_graph_stats()
    return {"n_airports": info.n_airports, "n_routes": info.n_routes, "n_disconnected": info.n_disconnected}


@app.post("/api/pagerank")
async def run_pagerank(req: PageRankRequest):
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        _pool,
        lambda: pagerank.compute_pagerank(
            damping=req.damping,
            init_strategy=req.init_strategy,
            max_iterations=req.max_iterations,
            tolerance=req.tolerance,
        ),
    )
    return {
        "rankings": result.rankings[:100],
        "iterations": result.iterations,
        "time_ms": round(result.time_ms, 2),
        "convergence": result.convergence,
        "damping": result.damping,
        "init_strategy": result.init_strategy,
        "total_airports": len(result.rankings),
    }


@app.get("/api/zipf/datasets")
async def zipf_datasets():
    return zipf.list_datasets()


@app.post("/api/zipf/analyze")
async def zipf_analyze(req: ZipfAnalyzeRequest):
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            _pool, lambda: zipf.analyze_dataset(req.dataset, req.top_n)
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    return result


@app.post("/api/zipf/custom")
async def zipf_custom(req: ZipfCustomRequest):
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        _pool, lambda: zipf.analyze_custom(req.text, req.top_n)
    )
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static")
