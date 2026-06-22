# NVP Agent Implementations — GitHub Pages site

Static site that showcases every configured AI-agent version of the Knight & Leveson
Launch Interceptor Program stored under
[`results/versions/`](../results/versions/).

## Local preview

The site loads JSON via `fetch`, so you need an HTTP server — you cannot just
`file://` the HTML.

```bash
python3 docs/build.py                # (re)generate docs/data/*
python3 -m http.server -d docs 8000  # open http://localhost:8000
```

Then browse to http://localhost:8000/.

## Deploy on GitHub Pages

1. Commit and push the contents of `docs/` to the default branch.
2. In the repository settings, enable **Pages → Deploy from branch** and
   select `main` (or your default branch) with the folder **`/docs`**.
3. GitHub Pages will serve the site at
   `https://<user>.github.io/<repo>/`.

`docs/.nojekyll` disables Jekyll so files beginning with `_` are served as-is.

## Layout

```
docs/
├── index.html           # filterable listing of all implementations
├── view.html            # single implementation viewer (?v=<version_id>)
├── build.py             # regenerates docs/data/ from results/versions/
├── css/style.css
├── js/
│   ├── index.js
│   └── view.js
└── data/
    ├── index.json       # summary list (drives the listing page)
    ├── facets.json      # filter choices + totals
    └── versions/*.json  # one file per implementation (copied from results/)
```

## Build status note

The browser displays `api_unavailable` as `timeout (api_unavailable)`: the
generation attempt did not produce an artifact because the agent/API call timed
out or was unavailable.

## Refreshing the data

Whenever `results/versions/` changes, rerun the build script:

```bash
python3 docs/build.py
```

The script is idempotent: it clears `docs/data/versions/`, re-copies the
upstream JSON files, and rebuilds the index and facet files. Commit the
resulting changes.

## Extending

- **Other experiments.** Pass `--source` to point at another directory under
  `results/` (for example `results/main-v2/versions/`) to generate an
  alternate site.
- **Extra facets.** Extend `SUMMARY_FIELDS` / the per-entry dict in
  `build.py` and add matching filter UI in `js/index.js`.
- **Syntax highlighting.** Pascal maps to highlight.js' `delphi` grammar
  since Pascal is not a built-in language; see `LANG_MAP` in `js/view.js`.
