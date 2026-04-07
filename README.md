# CAIM
This repository contains code and materials for the lab sessions in the course "Cerca i Anàlisi de la Informació" (Search and Analysis of Information), which covers various topics in information retrieval and natural language processing.

## Contents
The following lab sessions are included in this repository:

- PageRank: implementation of the PageRank algorithm for ranking web pages based on the structure of hyperlinks between them.
- Zipf law: analysis of the frequency distribution of words in a text corpus, and visualization of the Zipf law.
- TF-IDF: implementation of the TF-IDF (term frequency-inverse document frequency) weighting scheme for text retrieval.
- Rocchio: implementation of the Rocchio algorithm for relevance feedback in text retrieval.
- MapReduce: implementation of the MapReduce programming model for processing large-scale data sets.
- iGraph: introduction to the iGraph library for network analysis and visualization.
Each lab session is contained in its own directory, which includes a file with instructions and explanations, as well as any necessary code and data files.

## Web App

An interactive information retrieval explorer: PageRank on the global airport network with world map visualization, and Zipf's Law analysis with curve fitting on text corpora.

**Stack:** Vanilla TypeScript (Vite) + D3.js (geo projection, charts) + FastAPI backend (SciPy)

### Quick Start

```bash
# Docker (recommended)
docker compose up -d        # http://localhost:8086

# Dev mode
make web-dev                # Backend :8086, Vite dev server
```

### Features

- **PageRank tab:** D3.js world map with airport nodes sized by PageRank score, convergence chart, top-N ranking table
- **Zipf's Law tab:** Word frequency distribution with Zipf curve fitting (SciPy `curve_fit`), configurable corpus selection
- Tab-based navigation with dark theme

### Web Structure

```
web/
├── frontend/          # Vanilla TypeScript + Vite + D3.js
│   └── src/
│       ├── pagerank/          # Map visualization + PageRank controls
│       ├── zipf/              # Frequency charts + curve fitting
│       └── styles/            # Dark theme CSS
├── backend/           # FastAPI + SciPy + NetworkX
│   └── app.py
└── requirements.txt
```

## Requirements

### Lab sessions (original)

- Python 3.6 or higher
- Jupyter Notebook (for some lab sessions)
- The following Python libraries: numpy, pandas, matplotlib, scipy, scikit-learn, networkx, igraph, mrjob

### Web app

- Docker (recommended), or Python 3.12+ and Node.js 18+
