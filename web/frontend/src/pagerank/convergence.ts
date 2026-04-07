import { scaleLinear, scaleLog } from "d3-scale";
import { line } from "d3-shape";
import { select } from "d3-selection";

export function drawConvergence(container: HTMLElement, convergence: number[]) {
  container.innerHTML = "";
  if (convergence.length < 2) return;

  const W = 230, H = 100;
  const margin = { top: 8, right: 8, bottom: 20, left: 35 };
  const iw = W - margin.left - margin.right;
  const ih = H - margin.top - margin.bottom;

  const svg = select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`);

  const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = scaleLinear().domain([0, convergence.length - 1]).range([0, iw]);
  const minVal = Math.max(convergence[convergence.length - 1], 1e-15);
  const yScale = scaleLog().domain([convergence[0], minVal]).range([0, ih]);

  g.append("line").attr("x1", 0).attr("x2", iw).attr("y1", ih).attr("y2", ih)
    .attr("stroke", "#2a2a40").attr("stroke-width", 0.5);
  g.append("line").attr("x1", 0).attr("x2", 0).attr("y1", 0).attr("y2", ih)
    .attr("stroke", "#2a2a40").attr("stroke-width", 0.5);

  const lineFn = line<number>()
    .x((_, i) => xScale(i))
    .y((d) => yScale(Math.max(d, minVal)));

  g.append("path")
    .datum(convergence)
    .attr("d", lineFn as any)
    .attr("fill", "none")
    .attr("stroke", "var(--accent)")
    .attr("stroke-width", 1.5);

  g.append("text").attr("x", iw / 2).attr("y", ih + 14)
    .attr("fill", "var(--text-muted)").attr("font-size", "7px").attr("text-anchor", "middle")
    .text("Iteration");
  g.append("text").attr("x", -ih / 2).attr("y", -24)
    .attr("fill", "var(--text-muted)").attr("font-size", "7px").attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("L∞ Error (log)");

  const xTicks = xScale.ticks(4);
  for (const t of xTicks) {
    g.append("text").attr("x", xScale(t)).attr("y", ih + 10)
      .attr("fill", "var(--text-muted)").attr("font-size", "6px").attr("text-anchor", "middle")
      .text(String(Math.round(t)));
  }
}
