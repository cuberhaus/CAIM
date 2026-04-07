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
