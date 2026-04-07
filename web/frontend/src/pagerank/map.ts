import { geoNaturalEarth1, geoPath, geoGraticule } from "d3-geo";
import { scaleSequential, scaleSqrt } from "d3-scale";
import { select } from "d3-selection";
import type { RankedAirport } from "../lib/api";

const WORLD_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json";
let worldCache: any = null;

async function loadWorld() {
  if (worldCache) return worldCache;
  const resp = await fetch(WORLD_URL);
  const topo = await resp.json();
  const { feature } = await import("topojson-client");
  worldCache = feature(topo, topo.objects.land);
  return worldCache;
}

export async function drawMap(container: HTMLElement, rankings: RankedAirport[]) {
  const rect = container.getBoundingClientRect();
  const W = rect.width || 700;
  const H = rect.height || 500;

  container.innerHTML = "";
  const svg = select(container).append("svg").attr("width", W).attr("height", H);

  const projection = geoNaturalEarth1().fitSize([W, H], { type: "Sphere" } as any);
  const path = geoPath(projection);

  svg.append("rect").attr("width", W).attr("height", H).attr("fill", "#0a0a15");

  svg.append("path")
    .datum(geoGraticule()())
    .attr("d", path as any)
    .attr("fill", "none")
    .attr("stroke", "#1a1a2e")
    .attr("stroke-width", 0.3);

  try {
    const land = await loadWorld();
    svg.append("path")
      .datum(land)
      .attr("d", path as any)
      .attr("fill", "#1a1a2e")
      .attr("stroke", "#2a2a40")
      .attr("stroke-width", 0.5);
  } catch {}

  const maxScore = rankings[0]?.score ?? 1;
  const color = scaleSequential((t: number) => {
    const r = Math.round(99 + t * 156);
    const g = Math.round(102 + t * (200 - 102));
    const b = Math.round(241);
    return `rgb(${r},${g},${b})`;
  }).domain([0, maxScore]);

  const radius = scaleSqrt().domain([0, maxScore]).range([1.5, 12]);

  const top = rankings.slice(0, 500);
  const g = svg.append("g");

  for (const ap of [...top].reverse()) {
    const pt = projection([ap.lon, ap.lat]);
    if (!pt) continue;
    g.append("circle")
      .attr("cx", pt[0])
      .attr("cy", pt[1])
      .attr("r", radius(ap.score))
      .attr("fill", color(ap.score))
      .attr("fill-opacity", 0.8)
      .attr("stroke", "#0f0f1a")
      .attr("stroke-width", 0.5);
  }

  for (const ap of top.slice(0, 10)) {
    const pt = projection([ap.lon, ap.lat]);
    if (!pt) continue;
    g.append("text")
      .attr("x", pt[0] + radius(ap.score) + 3)
      .attr("y", pt[1] + 3)
      .attr("fill", "#e2e8f0")
      .attr("font-size", "9px")
      .attr("font-family", "var(--font-mono)")
      .text(ap.code);
  }
}
