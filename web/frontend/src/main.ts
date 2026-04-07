import { initPageRank } from "./pagerank/index";
import { initZipf } from "./zipf/index";

function setupTabs() {
  const btns = document.querySelectorAll<HTMLButtonElement>(".tab");
  const sections = document.querySelectorAll<HTMLElement>(".tab-content");

  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab!;
      btns.forEach((b) => b.classList.toggle("active", b === btn));
      sections.forEach((s) => s.classList.toggle("active", s.id === `${target}-tab`));
    });
  });
}

setupTabs();
initPageRank(document.getElementById("pagerank-tab")!);
initZipf(document.getElementById("zipf-tab")!);
