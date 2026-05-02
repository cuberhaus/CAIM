from __future__ import annotations

# ── Phase 14 (Option A) — Sentry SDK + JSON-line stdout (no-op if missing) ─
try:
    from ._sentry_obs import (  # type: ignore[import-not-found]
        init_observability,
        breadcrumb as _crumb,
        span as _span,
        tag as _tag,
        SessionIdMiddleware as _SessionIdMiddleware,
    )

    init_observability(service="caim")
except ImportError:
    from contextlib import contextmanager

    def _tag(*_a, **_kw):
        return None

    def _crumb(*_a, **_kw):
        return None

    @contextmanager
    def _span(*_a, **_kw):
        yield None

    class _SessionIdMiddleware:  # type: ignore[no-redef]
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            await self.app(scope, receive, send)

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import pagerank, zipf

app = FastAPI(title="CAIM Explorer")
app.add_middleware(_SessionIdMiddleware)
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
    _tag("damping", req.damping)
    _tag("init_strategy", req.init_strategy)
    _tag("max_iterations", req.max_iterations)
    _crumb(
        "pagerank", "param change",
        damping=req.damping,
        init_strategy=req.init_strategy,
        max_iterations=req.max_iterations,
        tolerance=req.tolerance,
    )
    loop = asyncio.get_event_loop()
    with _span(
        "pagerank.compute",
        description=f"damping={req.damping} init={req.init_strategy}",
        damping=req.damping,
        init_strategy=req.init_strategy,
        max_iterations=req.max_iterations,
    ):
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
    _tag("dataset", req.dataset)
    _tag("top_n", req.top_n)
    _crumb("zipf", "dataset switch", dataset=req.dataset, top_n=req.top_n)
    loop = asyncio.get_event_loop()
    with _span(
        "zipf.analyze",
        description=f"{req.dataset} top_n={req.top_n}",
        dataset=req.dataset,
        top_n=req.top_n,
    ):
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
    text_len = len(req.text or "")
    _tag("dataset", "custom")
    _tag("top_n", req.top_n)
    _crumb(
        "zipf", "custom-text submit",
        text_chars=text_len,
        top_n=req.top_n,
    )
    loop = asyncio.get_event_loop()
    with _span(
        "zipf.custom",
        description=f"custom-text top_n={req.top_n}",
        text_chars=text_len,
        top_n=req.top_n,
    ):
        result = await loop.run_in_executor(
            _pool, lambda: zipf.analyze_custom(req.text, req.top_n)
        )
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static")
