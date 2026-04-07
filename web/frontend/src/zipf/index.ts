import { getZipfDatasets, analyzeZipf, analyzeZipfCustom, type ZipfResponse } from "../lib/api";
import { drawZipfChart } from "./chart";

export function initZipf(container: HTMLElement) {
  container.innerHTML = `
    <div class="zf-layout">
      <aside class="zf-controls">
        <div class="section-title">Dataset</div>
        <div class="form-group">
          <label class="form-label">Source</label>
          <select class="form-select" id="zf-source">
            <option value="dataset">Bundled dataset</option>
            <option value="custom">Custom text</option>
          </select>
        </div>
        <div class="form-group" id="zf-dataset-group">
          <label class="form-label">Dataset</label>
          <select class="form-select" id="zf-dataset"></select>
        </div>
        <div class="form-group" id="zf-custom-group" style="display:none">
          <label class="form-label">Paste text</label>
          <textarea class="zf-textarea" id="zf-text" placeholder="Paste any text here..."></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Top N words: <span id="zf-n-val">1000</span></label>
          <input type="range" id="zf-topn" min="50" max="5000" step="50" value="1000" />
        </div>
        <button class="btn btn-primary" id="zf-run">Analyze</button>

        <div class="section-title" style="margin-top:1rem">Fitted Parameters</div>
        <div class="params-display" id="zf-params">
          <div class="param-row"><span class="param-label">a</span><span class="param-value" id="zf-a">—</span></div>
          <div class="param-row"><span class="param-label">b</span><span class="param-value" id="zf-b">—</span></div>
          <div class="param-row"><span class="param-label">c</span><span class="param-value" id="zf-c">—</span></div>
          <div class="param-row"><span class="param-label">R²</span><span class="param-value" id="zf-r2">—</span></div>
          <div class="param-row"><span class="param-label">n words</span><span class="param-value" id="zf-nw">—</span></div>
        </div>

        <div class="section-title" style="margin-top:0.75rem">Formula</div>
        <div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-secondary);background:var(--bg-card);padding:0.4rem;border-radius:var(--radius-sm);border:1px solid var(--border)">
          f(r) = c / (r + b)<sup>a</sup>
        </div>
      </aside>
      <div class="zf-charts">
        <div class="chart-container">
          <div class="chart-title">Frequency vs Rank (Linear)</div>
          <div id="zf-chart-linear"></div>
        </div>
        <div class="chart-container">
          <div class="chart-title">Frequency vs Rank (Log-Log)</div>
          <div id="zf-chart-log"></div>
        </div>
      </div>
    </div>
  `;

  const sourceSelect = container.querySelector<HTMLSelectElement>("#zf-source")!;
  const datasetGroup = container.querySelector<HTMLElement>("#zf-dataset-group")!;
  const customGroup = container.querySelector<HTMLElement>("#zf-custom-group")!;
  const datasetSelect = container.querySelector<HTMLSelectElement>("#zf-dataset")!;
  const topnSlider = container.querySelector<HTMLInputElement>("#zf-topn")!;
  const topnVal = container.querySelector<HTMLSpanElement>("#zf-n-val")!;
  const runBtn = container.querySelector<HTMLButtonElement>("#zf-run")!;

  sourceSelect.addEventListener("change", () => {
    const isCustom = sourceSelect.value === "custom";
    datasetGroup.style.display = isCustom ? "none" : "flex";
    customGroup.style.display = isCustom ? "flex" : "none";
  });

  topnSlider.addEventListener("input", () => { topnVal.textContent = topnSlider.value; });

  getZipfDatasets().then((ds) => {
    datasetSelect.innerHTML = ds.map((d) => `<option value="${d.id}">${d.label}</option>`).join("");
  });

  function showParams(r: ZipfResponse) {
    container.querySelector("#zf-a")!.textContent = String(r.params.a);
    container.querySelector("#zf-b")!.textContent = String(r.params.b);
    container.querySelector("#zf-c")!.textContent = String(r.params.c);
    const r2El = container.querySelector<HTMLElement>("#zf-r2")!;
    r2El.textContent = String(r.r_squared);
    r2El.className = `param-value ${r.r_squared > 0.95 ? "r2-good" : r.r_squared > 0.85 ? "r2-ok" : "r2-bad"}`;
    container.querySelector("#zf-nw")!.textContent = String(r.n);
  }

  async function run() {
    runBtn.disabled = true;
    runBtn.textContent = "Analyzing...";
    try {
      const topN = parseInt(topnSlider.value);
      let result: ZipfResponse;
      if (sourceSelect.value === "custom") {
        const text = (container.querySelector<HTMLTextAreaElement>("#zf-text")!).value;
        result = await analyzeZipfCustom(text, topN);
      } else {
        result = await analyzeZipf(datasetSelect.value, topN);
      }
      showParams(result);
      drawZipfChart(container.querySelector<HTMLElement>("#zf-chart-linear")!, result, false);
      drawZipfChart(container.querySelector<HTMLElement>("#zf-chart-log")!, result, true);
    } catch (e: any) {
      console.error(e);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = "Analyze";
    }
  }

  runBtn.addEventListener("click", run);
  run();
}
