const params = new URLSearchParams(location.search);
const versionId = params.get("v");

const els = {
  title: document.getElementById("view-title"),
  subtitle: document.getElementById("view-subtitle"),
  meta: document.getElementById("meta-list"),
  errorSection: document.getElementById("meta-error"),
  errorText: document.getElementById("error-text"),
  promptText: document.getElementById("prompt-text"),
  codeFilename: document.getElementById("code-filename"),
  codeStats: document.getElementById("code-stats"),
  codeBody: document.getElementById("code-body"),
  rawJson: document.getElementById("raw-json"),
  copyBtn: document.getElementById("copy-code"),
};

const LANG_MAP = {
  python: { hljs: "python", filename: "decide.py" },
  pascal: { hljs: "delphi", filename: "lipdecide.pas" },
  rust: { hljs: "rust", filename: "src/lib.rs" },
};

async function main() {
  if (!versionId) {
    showError("Missing ?v=… parameter.");
    return;
  }
  const dataUrl = `./data/versions/${encodeURIComponent(versionId)}.json`;
  let payload;
  try {
    const resp = await fetch(dataUrl);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    payload = await resp.json();
  } catch (err) {
    showError(`Could not load ${dataUrl}: ${err.message}`);
    return;
  }

  const agent = payload.agent_name || payload.agent || "unknown";
  const model = payload.model_name || payload.configured_model || payload.model || "unknown";
  const language = payload.language || "unknown";
  const run = payload.run_id ?? 0;
  const langInfo = LANG_MAP[language] || { hljs: "plaintext", filename: "source.txt" };

  document.title = `${agent} · ${model} · ${language} · NVP`;
  els.title.textContent = `${agent} — ${model}`;
  els.subtitle.innerHTML = `<span class="lang-badge lang-${escapeAttr(
    language
  )}">${escapeHtml(language)}</span> · run ${run} · <code>${escapeHtml(
    versionId
  )}</code>`;

  const metaRows = [
    ["Agent", agent],
    ["Model", model],
    ["Language", language],
    ["Run", run],
    ["Build status", payload.build_status || "unknown"],
    ["Acceptance", payload.acceptance_passed ? "passed" : "not passed"],
    ["Timestamp", payload.timestamp || "—"],
    ["Source bytes", (payload.source_code || "").length.toLocaleString()],
    ["Source lines", ((payload.source_code || "").match(/\n/g) || []).length + 1],
  ];
  if (payload.generation_config) {
    if (payload.generation_config.cli)
      metaRows.push(["CLI", payload.generation_config.cli]);
    if (payload.generation_config.base_url)
      metaRows.push(["Base URL", payload.generation_config.base_url]);
  }
  els.meta.innerHTML = metaRows
    .map(
      ([k, v]) =>
        `<dt>${escapeHtml(k)}</dt><dd>${escapeHtml(String(v))}</dd>`
    )
    .join("");

  if (payload.error_message) {
    els.errorSection.hidden = false;
    els.errorText.textContent = payload.error_message;
  }

  els.promptText.textContent = payload.prompt || "(no prompt recorded)";

  els.codeFilename.textContent = langInfo.filename;
  const source = payload.source_code || "(no source captured)";
  els.codeStats.textContent = `${source.length.toLocaleString()} bytes`;
  els.codeBody.textContent = source;
  els.codeBody.className = `hljs language-${langInfo.hljs}`;
  if (window.hljs) {
    window.hljs.highlightElement(els.codeBody);
  }

  els.rawJson.href = dataUrl;
  els.copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(source);
      flash(els.copyBtn, "Copied!");
    } catch {
      flash(els.copyBtn, "Copy failed");
    }
  });
}

function flash(btn, text) {
  const prev = btn.textContent;
  btn.textContent = text;
  setTimeout(() => {
    btn.textContent = prev;
  }, 1400);
}

function showError(msg) {
  els.title.textContent = "Unable to load implementation";
  els.subtitle.textContent = msg;
  els.codeBody.textContent = "";
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

main();
