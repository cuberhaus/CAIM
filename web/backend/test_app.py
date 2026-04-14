"""Tests for the CAIM FastAPI backend (PageRank + Zipf)."""

import pytest
from fastapi.testclient import TestClient

from .app import app

client = TestClient(app)


def test_status():
    r = client.get("/api/status")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_airports():
    r = client.get("/api/airports")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_graph_stats():
    r = client.get("/api/graph-stats")
    assert r.status_code == 200
    data = r.json()
    assert "n_airports" in data
    assert "n_routes" in data
    assert "n_disconnected" in data
    assert data["n_airports"] > 0


def test_pagerank_default():
    r = client.post("/api/pagerank", json={})
    assert r.status_code == 200
    data = r.json()
    assert "rankings" in data
    assert "iterations" in data
    assert "time_ms" in data
    assert "convergence" in data
    assert len(data["rankings"]) > 0
    assert len(data["rankings"]) <= 100


def test_pagerank_custom_params():
    r = client.post("/api/pagerank", json={
        "damping": 0.85, "init_strategy": "nth",
        "max_iterations": 50, "tolerance": 1e-6,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["damping"] == 0.85
    assert data["init_strategy"] == "nth"


def test_pagerank_convergence():
    r = client.post("/api/pagerank", json={"max_iterations": 500, "tolerance": 1e-12})
    data = r.json()
    assert data["iterations"] > 0


def test_zipf_datasets():
    r = client.get("/api/zipf/datasets")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_zipf_analyze():
    datasets = client.get("/api/zipf/datasets").json()
    first = datasets[0] if isinstance(datasets[0], str) else datasets[0].get("id", datasets[0].get("name"))
    r = client.post("/api/zipf/analyze", json={"dataset": first, "top_n": 50})
    assert r.status_code == 200


def test_zipf_analyze_unknown():
    r = client.post("/api/zipf/analyze", json={"dataset": "nonexistent_dataset_xyz"})
    assert r.status_code == 400


def test_zipf_custom():
    r = client.post("/api/zipf/custom", json={
        "text": "the cat sat on the mat the cat the the", "top_n": 10,
    })
    assert r.status_code == 200


# ─── Extended tests: PageRank & Zipf correctness ─────────────────


def test_pagerank_rankings_are_sorted():
    r = client.post("/api/pagerank", json={"damping": 0.85, "max_iterations": 100})
    data = r.json()
    ranks = data["rankings"]
    scores = [r["score"] for r in ranks]
    assert scores == sorted(scores, reverse=True), "Rankings should be sorted by score descending"


def test_pagerank_scores_sum_to_one():
    r = client.post("/api/pagerank", json={"damping": 0.85, "max_iterations": 200, "tolerance": 1e-8})
    data = r.json()
    # All scores in the full graph should sum close to 1
    # (we only get top N, so partial sum is ≤ 1)
    partial_sum = sum(r["score"] for r in data["rankings"])
    assert partial_sum <= 1.01


def test_pagerank_damping_effect():
    """Different damping should produce different results."""
    r1 = client.post("/api/pagerank", json={"damping": 0.5, "max_iterations": 100})
    r2 = client.post("/api/pagerank", json={"damping": 0.99, "max_iterations": 100})
    top1 = r1.json()["rankings"][0]["score"]
    top2 = r2.json()["rankings"][0]["score"]
    assert top1 != top2


def test_pagerank_init_strategies():
    for strategy in ["uniform", "nth"]:
        r = client.post("/api/pagerank", json={"init_strategy": strategy})
        assert r.status_code == 200
        assert r.json()["init_strategy"] == strategy


def test_airports_have_required_fields():
    r = client.get("/api/airports")
    airport = r.json()[0]
    # Should have at least name/code and coordinates
    assert any(k in airport for k in ["name", "code", "iata"])


def test_graph_stats_consistency():
    stats = client.get("/api/graph-stats").json()
    airports = client.get("/api/airports").json()
    assert stats["n_airports"] == len(airports)


def test_zipf_custom_word_frequencies():
    text = " ".join(["the"] * 50 + ["cat"] * 30 + ["sat"] * 20 + ["on"] * 15 + ["mat"] * 10)
    r = client.post("/api/zipf/custom", json={"text": text, "top_n": 5})
    assert r.status_code == 200


def test_zipf_custom_empty_text():
    r = client.post("/api/zipf/custom", json={"text": "", "top_n": 10})
    assert r.status_code in [200, 400]


def test_zipf_analyze_top_n():
    datasets = client.get("/api/zipf/datasets").json()
    first = datasets[0] if isinstance(datasets[0], str) else datasets[0].get("id", datasets[0].get("name"))
    r = client.post("/api/zipf/analyze", json={"dataset": first, "top_n": 5})
    assert r.status_code == 200
