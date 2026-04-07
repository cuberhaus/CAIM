from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

DATA_DIR = Path(__file__).parent / "data"

DATASETS = {
    "novels": {"file": "data_novels.csv", "label": "Novels corpus"},
    "news": {"file": "data_words_news.csv", "label": "News corpus"},
    "abstracts": {"file": "data_words_abs.csv", "label": "Arxiv abstracts"},
}


def _zipf_func(rank: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    return c / ((rank + b) ** a)


def list_datasets() -> list[dict]:
    return [{"id": k, "label": v["label"]} for k, v in DATASETS.items()]


def _load_dataset(name: str, top_n: int) -> tuple[list[str], list[int]]:
    info = DATASETS.get(name)
    if not info:
        raise ValueError(f"Unknown dataset: {name}")
    path = DATA_DIR / info["file"]
    words: list[str] = []
    freqs: list[int] = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= top_n:
                break
            parts = line.strip().split("\t")
            if len(parts) == 2:
                freqs.append(int(parts[0]))
                words.append(parts[1])
            elif len(parts) == 1:
                freqs.append(int(parts[0]))
                words.append(f"word_{i + 1}")
    return words, freqs


def _tokenize(text: str) -> list[tuple[str, int]]:
    tokens = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
    counts = Counter(tokens)
    return counts.most_common()


def analyze_dataset(dataset: str, top_n: int = 1000) -> dict:
    words, freqs = _load_dataset(dataset, top_n)
    return _fit(words, freqs)


def analyze_custom(text: str, top_n: int = 1000) -> dict:
    pairs = _tokenize(text)[:top_n]
    if len(pairs) < 5:
        return {"error": "Not enough words (need at least 5 distinct words)"}
    words = [w for w, _ in pairs]
    freqs = [f for _, f in pairs]
    return _fit(words, freqs)


def _fit(words: list[str], freqs: list[int]) -> dict:
    n = len(freqs)
    ranks = np.arange(1, n + 1, dtype=float)
    freq_arr = np.array(freqs, dtype=float)

    try:
        popt, _ = curve_fit(
            _zipf_func, ranks, freq_arr,
            p0=[1.0, 1.0, float(freqs[0])],
            bounds=([0.5, -500000.0, -500000.0], [3.0, 500000.0, 50000000.0]),
            maxfev=5000,
        )
        a, b, c = float(popt[0]), float(popt[1]), float(popt[2])
        fitted = _zipf_func(ranks, a, b, c)
        ss_res = float(np.sum((freq_arr - fitted) ** 2))
        ss_tot = float(np.sum((freq_arr - np.mean(freq_arr)) ** 2))
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    except Exception:
        a, b, c = 1.0, 0.0, float(freqs[0])
        fitted = _zipf_func(ranks, a, b, c)
        r_squared = 0.0

    return {
        "words": words[:200],
        "ranks": list(range(1, n + 1)),
        "frequencies": freqs,
        "fitted": [float(v) for v in fitted],
        "params": {"a": round(a, 4), "b": round(b, 4), "c": round(c, 4)},
        "r_squared": round(r_squared, 6),
        "n": n,
    }
