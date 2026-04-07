import { getGraphStats, runPageRank, type PageRankResponse, type RankedAirport } from "../lib/api";
import { drawMap } from "./map";
import { drawConvergence } from "./convergence";

export function initPageRank(container: HTMLElement) {
  container.innerHTML = `
    <div class="pr-layout">
      <aside class="pr-controls">
        <div class="section-title">Graph Info</div>
        <div class="stats-grid" id="pr-stats">
          <div class="stat-card"><div class="stat-value" id="pr-n">—</div><div class="stat-label">Airports</div></div>
          <div class="stat-card"><div class="stat-value" id="pr-e">—</div><div class="stat-label">Routes</div></div>
          <div class="stat-card"><div class="stat-value" id="pr-disc">—</div><div class="stat-label">Disconnected</div></div>
          <div class="stat-card"><div class="stat-value" id="pr-iter">—</div><div class="stat-label">Iterations</div></div>
        </div>

        <div class="section-title">Parameters</div>
        <div class="form-group">
          <label class="form-label">Damping Factor (L): <span id="pr-damp-val">0.80</span></label>
          <input type="range" id="pr-damping" min="0.50" max="0.99" step="0.01" value="0.80" />
        </div>
        <div class="form-group">
          <label class="form-label">Initialization</label>
          <select class="form-select" id="pr-init">
            <option value="nth" selected>Uniform (1/n)</option>
            <option value="one">Single node</option>
            <option value="square">Sqrt(n) nodes</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Tolerance</label>
          <select class="form-select" id="pr-tol">
            <option value="1e-8">10⁻⁸</option>
            <option value="1e-10" selected>10⁻¹⁰</option>
            <option value="1e-12">10⁻¹²</option>
          </select>
        </div>
        <button class="btn btn-primary" id="pr-run">Run PageRank</button>

        <div class="section-title" style="margin-top:1rem">Convergence</div>
        <div class="convergence-chart" id="pr-conv"></div>
      </aside>

      <div class="pr-map" id="pr-map"></div>

      <aside class="pr-results">
        <div class="section-title">Top Airports</div>
        <div id="pr-time" style="font-size:0.72rem;color:var(--text-muted);margin-bottom:0.4rem"></div>
        <div id="pr-table-wrap" style="overflow-y:auto;max-height:calc(100vh - 160px)"></div>
      </aside>
    </div>
  `;

  const dampSlider = container.querySelector<HTMLInputElement>("#pr-damping")!;
  const dampVal = container.querySelector<HTMLSpanElement>("#pr-damp-val")!;
  dampSlider.addEventListener("input", () => { dampVal.textContent = parseFloat(dampSlider.value).toFixed(2); });

  const runBtn = container.querySelector<HTMLButtonElement>("#pr-run")!;
  const mapEl = container.querySelector<HTMLElement>("#pr-map")!;

  getGraphStats().then((s) => {
    container.querySelector("#pr-n")!.textContent = s.n_airports.toLocaleString();
    container.querySelector("#pr-e")!.textContent = s.n_routes.toLocaleString();
    container.querySelector("#pr-disc")!.textContent = s.n_disconnected.toLocaleString();
  });

  let currentResult: PageRankResponse | null = null;

  async function run() {
    runBtn.disabled = true;
    runBtn.textContent = "Running...";
    try {
      const result = await runPageRank({
        damping: parseFloat(dampSlider.value),
        init_strategy: (container.querySelector<HTMLSelectElement>("#pr-init")!).value,
        max_iterations: 300,
        tolerance: parseFloat((container.querySelector<HTMLSelectElement>("#pr-tol")!).value),
      });
      currentResult = result;
      container.querySelector("#pr-iter")!.textContent = String(result.iterations);
      container.querySelector("#pr-time")!.textContent = `${result.time_ms.toFixed(1)}ms · ${result.iterations} iter · L=${result.damping}`;
      renderTable(result.rankings);
      drawMap(mapEl, result.rankings);
      drawConvergence(container.querySelector<HTMLElement>("#pr-conv")!, result.convergence);
    } catch (e) {
      console.error(e);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = "Run PageRank";
    }
  }

  runBtn.addEventListener("click", run);

  function renderTable(rankings: RankedAirport[]) {
    const wrap = container.querySelector<HTMLElement>("#pr-table-wrap")!;
    const top = rankings.slice(0, 25);
    wrap.innerHTML = `
      <table class="rank-table">
        <thead><tr><th>#</th><th>Code</th><th>Airport</th><th>Score</th></tr></thead>
        <tbody>
          ${top.map((r) => `
            <tr>
              <td>${r.rank}</td>
              <td class="rank-code">${r.code}</td>
              <td>${r.name}</td>
              <td style="font-family:var(--font-mono)">${(r.score * 10000).toFixed(2)}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  }

  run();
}
