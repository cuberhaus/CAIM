const BASE = import.meta.env.VITE_API_URL ?? "";

export interface AirportInfo {
  code: string;
  name: string;
  country: string;
  lat: number;
  lon: number;
}

export interface GraphStats {
  n_airports: number;
  n_routes: number;
  n_disconnected: number;
}

export interface RankedAirport {
  rank: number;
  code: string;
  name: string;
  country: string;
  lat: number;
  lon: number;
  score: number;
}

export interface PageRankResponse {
  rankings: RankedAirport[];
  iterations: number;
  time_ms: number;
  convergence: number[];
  damping: number;
  init_strategy: string;
  total_airports: number;
}

export interface ZipfDataset {
  id: string;
  label: string;
}

export interface ZipfResponse {
  words: string[];
  ranks: number[];
  frequencies: number[];
  fitted: number[];
  params: { a: number; b: number; c: number };
  r_squared: number;
  n: number;
}

async function get<T>(url: string): Promise<T> {
  const r = await fetch(`${BASE}${url}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function post<T>(url: string, body: unknown): Promise<T> {
  const r = await fetch(`${BASE}${url}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export const getAirports = () => get<AirportInfo[]>("/api/airports");
export const getGraphStats = () => get<GraphStats>("/api/graph-stats");
export const runPageRank = (p: { damping: number; init_strategy: string; max_iterations: number; tolerance: number }) =>
  post<PageRankResponse>("/api/pagerank", p);
export const getZipfDatasets = () => get<ZipfDataset[]>("/api/zipf/datasets");
export const analyzeZipf = (dataset: string, top_n: number) =>
  post<ZipfResponse>("/api/zipf/analyze", { dataset, top_n });
export const analyzeZipfCustom = (text: string, top_n: number) =>
  post<ZipfResponse>("/api/zipf/custom", { text, top_n });
