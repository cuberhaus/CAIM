import { scaleLinear, scaleLog } from "d3-scale";
import { line } from "d3-shape";
import { select } from "d3-selection";
import type { ZipfResponse } from "../lib/api";

export function drawZipfChart(container: HTMLElement, data: ZipfResponse, isLog: boolean) {
  container.innerHTML = "";
  const W = 600, H = 280;
  const margin = { top: 15, right: 15, bottom: 35, left: 55 };
  const iw = W - margin.left - margin.right;
  const ih = H - margin.top - margin.bottom;

  const svg = select(container).append("svg").attr("viewBox", `0 0 ${W} ${H}`);
  const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

  const ranks = data.ranks;
  const freqs = data.frequencies;
  const fitted = data.fitted;

  const xDomain: [number, number] = [1, ranks.length];
  const yDomain: [number, number] = [Math.max(freqs[freqs.length - 1], 1), freqs[0]];

  const xScale = isLog
    ? scaleLog().domain(xDomain).range([0, iw])
    : scaleLinear().domain(xDomain).range([0, iw]);
  const yScale = isLog
    ? scaleLog().domain(yDomain).range([ih, 0])
    : scaleLinear().domain([0, freqs[0]]).range([ih, 0]);

  // Grid
  const xTicks = isLog ? xScale.ticks(5) : xScale.ticks(6);
  const yTicks = isLog ? yScale.ticks(5) : yScale.ticks(6);
  for (const t of yTicks) {
    g.append("line").attr("x1", 0).attr("x2", iw).attr("y1", yScale(t)).attr("y2", yScale(t))
      .attr("stroke", "#1a1a2e").attr("stroke-width", 0.5);
    g.append("text").attr("x", -6).attr("y", yScale(t) + 3)
      .attr("fill", "#64748b").attr("font-size", "8px").attr("text-anchor", "end")
      .text(isLog ? formatSI(t) : formatSI(t));
  }
  for (const t of xTicks) {
    g.append("line").attr("x1", xScale(t)).attr("x2", xScale(t)).attr("y1", 0).attr("y2", ih)
      .attr("stroke", "#1a1a2e").attr("stroke-width", 0.5);
    g.append("text").attr("x", xScale(t)).attr("y", ih + 12)
      .attr("fill", "#64748b").attr("font-size", "8px").attr("text-anchor", "middle")
      .text(isLog ? formatSI(t) : formatSI(t));
  }

  // Actual data
  const step = Math.max(1, Math.floor(ranks.length / 400));
  const sampled = ranks.filter((_, i) => i % step === 0);
  for (const i of sampled) {
    const idx = i - 1;
    if (idx >= freqs.length) continue;
    const cx = xScale(i);
    const cy = yScale(Math.max(freqs[idx], isLog ? 1 : 0));
    if (isFinite(cx) && isFinite(cy)) {
      g.append("circle").attr("cx", cx).attr("cy", cy).attr("r", 1.5)
        .attr("fill", "#3b82f6").attr("fill-opacity", 0.6);
    }
  }

  // Fitted curve
  const fittedLine = line<number>()
    .x((_, i) => xScale(i + 1))
    .y((d) => yScale(Math.max(d, isLog ? 1 : 0)))
    .defined((d, i) => {
      const x = xScale(i + 1);
      const y = yScale(Math.max(d, isLog ? 1 : 0));
      return isFinite(x) && isFinite(y);
    });

  g.append("path")
    .datum(fitted)
    .attr("d", fittedLine as any)
    .attr("fill", "none")
    .attr("stroke", "#ef4444")
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", "4,2");

  // Axes labels
  g.append("text").attr("x", iw / 2).attr("y", ih + 28)
    .attr("fill", "#64748b").attr("font-size", "9px").attr("text-anchor", "middle")
    .text("Rank");
  g.append("text").attr("x", -ih / 2).attr("y", -40)
    .attr("fill", "#64748b").attr("font-size", "9px").attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Frequency");

  // Legend
  g.append("circle").attr("cx", iw - 100).attr("cy", 8).attr("r", 3).attr("fill", "#3b82f6");
  g.append("text").attr("x", iw - 94).attr("y", 11).attr("fill", "#cbd5e1").attr("font-size", "8px").text("Actual");
  g.append("line").attr("x1", iw - 46).attr("x2", iw - 32).attr("y1", 8).attr("y2", 8)
    .attr("stroke", "#ef4444").attr("stroke-width", 1.5).attr("stroke-dasharray", "3,1");
  g.append("text").attr("x", iw - 28).attr("y", 11).attr("fill", "#cbd5e1").attr("font-size", "8px").text("Fitted");
}

function formatSI(n: number): string {
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `${(n / 1e3).toFixed(n >= 1e4 ? 0 : 1)}K`;
  return n >= 100 ? String(Math.round(n)) : n.toPrecision(2);
}
