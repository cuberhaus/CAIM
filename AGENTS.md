# CAIM

Frozen FIB-UPC coursework for *Cerca i Anàlisi de la Informació* (Search & Analysis of Information): per-session IR/NLP labs (Zipf, TF-IDF, Rocchio, PageRank, MapReduce K-Means, iGraph) plus a modern `web/` app that revisits PageRank and Zipf with interactive visualizations.

## Architecture

- `sesioN/` — one folder per lab session, each standalone:
  - `sesio1/` Zipf & Heaps law on text corpora (20 Newsgroups, arXiv abstracts).
  - `sesio2/` TF-IDF over ElasticSearch (`IndexFilesPreprocess.py`, `TFIDFViewer.py`).
  - `sesio3/` Rocchio relevance feedback on the ES index.
  - `sesio5/` PageRank on the airport network (`PageRank.py`, `airports.txt`, `routes.txt`).
  - `sesio6/` MapReduce K-Means with `mrjob` (`MRKmeans*.py`); see `Docker.md`.
  - `sesio7/` iGraph network analysis (R + Jupyter).
- `TFIDFViewer.py` — top-level ElasticSearch TF-IDF viewer (duplicated in `sesio2/`).
- `web/` — separate modern app: FastAPI + SciPy backend (`backend/app.py` on `:8086`) and Vanilla TypeScript + Vite + D3.js frontend (`frontend/`); only PageRank and Zipf tabs.

## Build and Test

- Web app (recommended): `docker compose up -d` → http://localhost:8086 (single `web` service, no ES).
- Web dev: `make install` then `make dev` (uvicorn `:8086` + Vite dev server). Tests: `pytest web/backend/test_app.py`.
- Lab sessions: per-folder, ad-hoc. Python 3.6+ with numpy/scipy/sklearn/networkx/igraph/mrjob (see `README.md`). Some sessions use Jupyter (`.ipynb`).

## Conventions

- Each `sesioN/` is self-contained and frozen as submitted (`Envio/`, `prac_*.zip`, lab PDFs); treat as historical artifacts.
- `web/` is a separate codebase from the labs — do not import lab code into it or vice versa.

## Pitfalls

- Frozen coursework: do **not** refactor `sesioN/` or merge code across sessions.
- `sesio2/`, `sesio3/`, and root `TFIDFViewer.py` require a running ElasticSearch instance — **not** provided by `docker-compose.yml` (which only ships the `web/` FastAPI app); run ES separately.
- `web/` deliberately reimplements PageRank/Zipf in SciPy/NetworkX; it is **not** a wrapper around the lab scripts.

See [README.md](README.md).
