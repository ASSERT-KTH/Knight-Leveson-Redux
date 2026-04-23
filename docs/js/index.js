const DATA_URL = "./data/index.json";
const FACETS_URL = "./data/facets.json";

const state = {
  all: [],
  facets: null,
  filters: {
    search: "",
    languages: new Set(),
    agents: new Set(),
    statuses: new Set(),
    accept: "any",
    model: "",
  },
  sort: "default",
};

const els = {
  stats: document.getElementById("stats-bar"),
  search: document.getElementById("search"),
  fLang: document.getElementById("filter-languages"),
  fAgent: document.getElementById("filter-agents"),
  fStatus: document.getElementById("filter-statuses"),
  fAccept: document.getElementById("filter-accept"),
  fModel: document.getElementById("filter-model"),
  results: document.getElementById("results"),
  count: document.getElementById("result-count"),
  empty: document.getElementById("empty-state"),
  sort: document.getElementById("sort"),
  reset: document.getElementById("reset-filters"),
};

async function main() {
  const [data, facets] = await Promise.all([
    fetch(DATA_URL).then((r) => r.json()),
    fetch(FACETS_URL).then((r) => r.json()),
  ]);
  state.all = data;
  state.facets = facets;

  renderStats();
  renderFacetChips();
  renderModelSelect();
  bindInputs();
  render();
}

function renderStats() {
  const { totals } = state.facets;
  const cards = [
    { label: "Versions", value: totals.versions },
    { label: "Built OK", value: totals.built_ok },
    { label: "Acceptance passed", value: totals.accepted },
    { label: "Agents", value: state.facets.agents.length },
    { label: "Models", value: state.facets.models.length },
    { label: "Languages", value: state.facets.languages.length },
  ];
  els.stats.innerHTML = cards
    .map(
      (c) => `
      <div class="stat-card">
        <div class="value">${c.value}</div>
        <div class="label">${c.label}</div>
      </div>`
    )
    .join("");
}

function chip(label, count, pressed) {
  return `<button class="chip" aria-pressed="${
    pressed ? "true" : "false"
  }" data-value="${escapeAttr(label)}">${escapeHtml(
    label
  )} <span class="count">${count}</span></button>`;
}

function renderFacetChips() {
  els.fLang.innerHTML = state.facets.languages
    .map(([name, count]) => chip(name, count, false))
    .join("");
  els.fAgent.innerHTML = state.facets.agents
    .map(([name, count]) => chip(name, count, false))
    .join("");
  els.fStatus.innerHTML = state.facets.build_statuses
    .map(([name, count]) => chip(name, count, false))
    .join("");

  wireChipGroup(els.fLang, state.filters.languages);
  wireChipGroup(els.fAgent, state.filters.agents);
  wireChipGroup(els.fStatus, state.filters.statuses);

  els.fAccept.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button[data-accept]");
    if (!btn) return;
    els.fAccept
      .querySelectorAll("button[data-accept]")
      .forEach((b) => b.setAttribute("aria-pressed", "false"));
    btn.setAttribute("aria-pressed", "true");
    state.filters.accept = btn.dataset.accept;
    render();
  });
}

function wireChipGroup(root, set) {
  root.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".chip");
    if (!btn) return;
    const v = btn.dataset.value;
    if (set.has(v)) {
      set.delete(v);
      btn.setAttribute("aria-pressed", "false");
    } else {
      set.add(v);
      btn.setAttribute("aria-pressed", "true");
    }
    render();
  });
}

function renderModelSelect() {
  const opts = state.facets.models.map(
    ([name, count]) =>
      `<option value="${escapeAttr(name)}">${escapeHtml(name)} (${count})</option>`
  );
  els.fModel.insertAdjacentHTML("beforeend", opts.join(""));
}

function bindInputs() {
  els.search.addEventListener("input", () => {
    state.filters.search = els.search.value.trim().toLowerCase();
    render();
  });
  els.fModel.addEventListener("change", () => {
    state.filters.model = els.fModel.value;
    render();
  });
  els.sort.addEventListener("change", () => {
    state.sort = els.sort.value;
    render();
  });
  els.reset.addEventListener("click", resetFilters);
}

function resetFilters() {
  state.filters.search = "";
  els.search.value = "";
  state.filters.languages.clear();
  state.filters.agents.clear();
  state.filters.statuses.clear();
  state.filters.accept = "any";
  state.filters.model = "";
  els.fModel.value = "";
  state.sort = "default";
  els.sort.value = "default";
  document
    .querySelectorAll(".chip-group .chip")
    .forEach((c) => c.setAttribute("aria-pressed", "false"));
  els.fAccept
    .querySelector('[data-accept="any"]')
    .setAttribute("aria-pressed", "true");
  render();
}

function matches(item) {
  const f = state.filters;
  if (f.languages.size && !f.languages.has(item.language)) return false;
  if (f.agents.size && !f.agents.has(item.agent)) return false;
  if (f.statuses.size && !f.statuses.has(item.build_status)) return false;
  if (f.model && item.model !== f.model) return false;
  if (f.accept === "passed" && !item.acceptance_passed) return false;
  if (f.accept === "failed" && item.acceptance_passed) return false;
  if (f.search) {
    const hay = `${item.agent} ${item.model} ${item.language} ${item.version_id}`.toLowerCase();
    if (!hay.includes(f.search)) return false;
  }
  return true;
}

function sortItems(items) {
  const by = state.sort;
  const cmp = {
    default: (a, b) =>
      a.language.localeCompare(b.language) ||
      a.agent.localeCompare(b.agent) ||
      a.model.localeCompare(b.model) ||
      a.run_id - b.run_id,
    agent: (a, b) =>
      a.agent.localeCompare(b.agent) || a.model.localeCompare(b.model),
    model: (a, b) => a.model.localeCompare(b.model),
    language: (a, b) =>
      a.language.localeCompare(b.language) || a.agent.localeCompare(b.agent),
    lines: (a, b) => b.source_lines - a.source_lines,
    acceptance: (a, b) =>
      Number(b.acceptance_passed) - Number(a.acceptance_passed) ||
      a.agent.localeCompare(b.agent),
  }[by];
  return [...items].sort(cmp);
}

function render() {
  const filtered = state.all.filter(matches);
  const sorted = sortItems(filtered);
  els.count.textContent = `${sorted.length} of ${state.all.length} implementations`;
  els.empty.hidden = sorted.length !== 0;
  els.results.innerHTML = sorted.map(renderCard).join("");
}

function renderCard(item) {
  const url = `view.html?v=${encodeURIComponent(item.version_id)}`;
  return `<a class="card" href="${url}">
    <div class="top">
      <div>
        <div class="agent">${escapeHtml(item.agent)}</div>
        <div class="model">${escapeHtml(item.model)}</div>
      </div>
      <div class="badges">
        <span class="lang-badge lang-${escapeAttr(item.language)}">${escapeHtml(
    item.language
  )}</span>
      </div>
    </div>
    <div class="bottom">
      <span>
        <span class="status-badge ${escapeAttr(item.build_status)}">${escapeHtml(
    item.build_status
  )}</span>
        <span class="accept-badge ${item.acceptance_passed ? "yes" : "no"}">${
    item.acceptance_passed ? "accepted" : "not accepted"
  }</span>
      </span>
      <span class="lines">${item.source_lines} LOC</span>
    </div>
  </a>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>\"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[c]));
}
function escapeAttr(s) {
  return escapeHtml(s);
}

main().catch((err) => {
  console.error(err);
  els.results.innerHTML = `<p class="empty-state">Failed to load data: ${escapeHtml(
    err.message || err
  )}</p>`;
});
