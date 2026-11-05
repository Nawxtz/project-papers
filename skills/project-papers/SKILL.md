---
name: project-papers
description: Find research papers that match what a code project actually does, grounded in evidence from the code (imports, model files, configs, paper IDs), with every listed paper fetched from OpenAlex/arXiv and checked against Crossref/arXiv. Use when the user asks for related papers, references, prior work, a literature list or citations for a repository or project.
license: MIT
metadata:
  version: "0.1.0"
---

# project-papers

Writes `docs/papers.md` and `docs/papers.bib` for the current project.

The script `scripts/papers.py` (Python 3.8+, stdlib only) does every step that has a right answer: scanning, searching, dedupe, verbatim-quote checks, verification and rendering. You do the judgment steps. The split exists to stop two failure modes: papers that do not match the project, and invented papers or claims.

## Hard rules

1. Never write a paper title, author, year, venue, DOI or link yourself. Papers come only from `show` output, and you refer to them only by their `C` id.
2. Never cite from memory. If a paper you know is missing, put its exact title in `seed_titles`. The script looks it up and drops it if no record matches.
3. Every facet needs evidence from this project: an `E` id from `scan`, or `{file, line, quote}` that the script checks. If the code does not show it, it is not a facet.
4. Judge only from the abstract text that `show` printed. The `quote` must be copied character for character from that printed text.
5. Saying "no relevant paper" is a correct result. Never lower the bar to fill a facet.

## Workflow

Set `P=<this skill dir>/scripts/papers.py` and run every command with `--project <repo root>`. File paths you pass to a command (such as the profile) may be relative to your current directory or to the repo root.

### 1. Scan

```bash
python3 $P --project . scan
```

This prints evidence ids (`E1`, `E2`, ...) for paper IDs found in the repo, citations in code comments (`Bailey & López de Prado (2014)`, links to paper PDFs), technique lines from docstrings and comments, hand-written numeric steps (`idiom`: an exponential smoothing update, a release threshold next to an entry threshold), model references and files, dependencies, imports, imported names (`api`), and class or function names (`symbol`), plus README/CLAUDE.md lines.

Two ranked lists close the output. `top techniques` (up to 15) is what the code is mostly about, weighted toward core code over scratch, tests and examples, with at most 3 items per file. `check` requires each of them to be covered or skipped. One facet usually covers several items: an item is covered when the facet's evidence cites that id, or a line in the same file (within 40 lines when the file has several items). `more techniques` is optional reading. Open the files behind both lists (for example `sed -n 1,40p core/labeling.py`) to see which algorithm is actually used before you write facets.

### 2. Write the profile

Write `.papers/profile.input.json`:

```json
{"facets": [
  {"id": "F1", "name": "CNN face detection with YuNet",
   "task": "face detection", "method": "lightweight anchor-free CNN (YuNet) via ONNX",
   "setting": "real-time, CPU, webcam frames",
   "evidence": ["E18", {"file": "app/core/detector.py", "line": 4, "quote": "FaceDetectorYN"}],
   "queries": ["lightweight face detection convolutional neural network real-time", "YuNet face detector"],
   "seed_titles": ["YuNet: A Tiny Millisecond-level Face Detector"],
   "seed_ids": [],
   "seed_cites": []}
 ],
 "skip": [{"evidence": "E40", "reason": "web dashboard code, not a research technique"}]}
```

Rules for a good profile:

- 0-6 facets. A facet is a technique the project depends on (a model, an algorithm, a data method, an evaluation method). Leave out generic infrastructure such as the web framework, database, Docker or the UI, unless that infrastructure is the subject of the project.
- `task` is the problem. `method` is the specific technique the code uses, not the product name. `setting` covers constraints such as language, domain, hardware or latency.
- 1-4 `queries` per facet, each 3-8 words of technical terms a paper title or abstract would use. Use no product names unless they are model names (YuNet, BERT). Add an acronym expansion as a second query when it helps.
- Every query names the task or domain, not only the method. "gradient boosting" alone returns house prices and medical papers; "gradient boosting intraday price direction" does not.
- When the evidence is a general algorithm the code writes by hand (smoothing a signal, a threshold switch, a scoring formula), the useful papers are about that algorithm, not about the app. Write `task` as the algorithmic problem (for a hand-written BM25 score in a recipe app: "rank documents by relevance to a short query", not "recipe search"), and let at least one query name the method and the data without the app ("BM25 term weighting short query document ranking"). The data or signal counts as the domain. In testing, app-worded queries returned only app papers that never mention the algorithm.
- `seed_titles` (optional, at most 3): exact titles of the original papers behind the method or library the code uses (for example the XGBoost or LightGBM paper when the evidence is that import). Seeds give the best recall, so add them whenever you know the paper. The script keeps a seed only when a registry title matches yours closely, so a title you are unsure of is dropped, never guessed: adding your best recollection is safe.
- `evidence`: E ids are enough. Add `{file, line, quote}` for a line the scan did not list (find the line number with `grep -n`). An `idiom` item lists every site in the file; when the sites do different jobs (smoothing a cursor and smoothing brightness), cite the line you mean as `{file, line, quote}`, so the code map points at it.
- `seed_ids` (optional, inside the facet it belongs to): only `paper_id` values from the scan output, such as `"arXiv:1506.02640"`.
- `seed_cites` (optional): papers the code itself cites in a comment. Use one entry per `citation` or `doc` item, for example `{"evidence": "E86", "author": "Bailey", "year": 2014, "words": "Deflated Sharpe Ratio"}`. The author, the year and every word in `words` must appear on that source line (`scan` prints the line after the citation). `words` is then used as the title search. The script finds the paper by author, year and words, and skips it if no record matches. For a link to a PDF, open the comment, and if it names the paper put the exact title in `seed_titles`.
- `skip`: every `top techniques` item that no facet covers needs a skip with a reason (generic infrastructure, plotting, a metric). A facet covers an item when its evidence cites that id or any line in the same file. Do not skip a real technique just to get past `check`: the user sees the skips in the review table.

If the project uses no research technique (a CRUD app, a static site, a document builder), write `{"facets": [], "skip": [...]}` with a skip for each top technique. `check` then exits with code 4: tell the user there is nothing to search for and stop. Never invent a facet from the README alone.

### 3. Check, then show the user (required)

```bash
python3 $P --project . check .papers/profile.input.json
```

Fix every `ERROR` and run it again. Then show the user the printed review table and ask them to confirm or edit it. The queries leave the machine, and the user knows the project better than the scan does. Do not search before the user confirms.

### 4. Search

```bash
python3 $P --project . search
```

This takes about 10 seconds. Per facet it runs one OpenAlex title+abstract search and one Crossref search. It resolves seed titles (OpenAlex, then Crossref by exact title), then adds papers that cite each seed ranked by relevance to the facet, plus the seed's related works. Finally it dedupes and scores everything. `--arxiv` adds arXiv keyword hits. They are slow and were the least precise source in the benchmark, so use it only when very recent preprints matter.

`search` also counts how many papers each query matches. `WARN ... too broad` (over 20,000) means results will drift off topic: add task or domain words to that query, run `check`, show the user the change, and search again. `WARN ... matches no paper` means a word is wrong or too rare.

When OpenAlex text search is unavailable, the script continues with seeds, related works and Crossref, and prints a `WARN`. Pass that warning to the user, because recall is lower in that case. Exit code 3 means no candidate with an abstract was found: stop and tell the user.

Keys are read from the environment or from `~/.config/project-papers/keys.env` (`OPENALEX_API_KEY`, `PAPERS_MAILTO`). A free OpenAlex key, created by the user at openalex.org/settings/api, gives about 1000 searches a day. Each person uses their own key.

### 5. Judge

```bash
python3 $P --project . show --facet F1   # --top 8 per facet, --chars 700 per abstract
```

Run `show` once per facet. All facets at once can exceed 40 KB, more than many agent tools display. The default is 8 candidates. Ask for `--top 16` only when the first 8 held at least one match: on a facet where the first 8 are off topic, the next 8 rarely help.

Each line shows id, year, citation count, source tag, venue class, title and venue. Venue class is `established` (core list or venue h-index 80+), `preprint`, `thesis`, `book`, `unvetted` (any other journal or conference; in testing mostly short student write-ups) or `unknown`. An `unvetted` paper needs one more point than usual to be listed (total 5 by default; `judge` enforces it). The list takes turns between sources (seed, text search, citing papers, related works, Crossref), so no single source fills it. Candidates without a usable abstract are hidden, because there is nothing to quote. For each candidate that really fits a facet, add an entry to `.papers/judgments.json`. Do not list the ones that do not fit. A paper that fits two facets can have one entry per facet.

```json
{"judgments": [
  {"cid": "C1", "facet": "F1", "task": 2, "method": 2, "setting": 2,
   "quote": "we present a millisecond-level anchor-free face detector, YuNet, which is specifically designed for edge devices",
   "reason": "Original paper of the YuNet model loaded in app/core/detector.py."}
]}
```

Optional `"code": ["execution/gauntlet.py"]` narrows which of the facet's evidence files the paper explains; the code map and `lookup` use it. Without it the paper is linked to every evidence file of the facet.

A SEED paper that is the original publication of a method or library the code uses (the XGBoost paper for `XGBClassifier`, Kelly 1956 for a Kelly sizing function) can be judged with `"role": "foundation"`. It needs method 2 only, no task match, and is listed under "Foundations" for that facet. Use it only for SEED papers; `judge` rejects it for anything else. Everything else is `"role": "match"` (the default).

Score each axis against the facet, using only the abstract:

| score | task | method | setting |
|---|---|---|---|
| 2 | same problem | same technique or its direct origin | same constraints |
| 1 | closely related problem | same family of techniques | partly overlapping |
| 0 | different | different | unrelated |

Score method against the facet's `method`, not against the app: a paper on the same app task whose abstract never mentions that method scores method 0. Method 1 means the paper's technique could replace, extend or tune the one in the code. A competing technique the code does not use (another hand tracker when the code uses MediaPipe) is method 0, unless the facet itself is about choosing between techniques. In testing, most wrongly accepted papers were same-task papers with an unused technique.

The script lists a paper only if task >= 1, method >= 1 and the total is >= 4 (change this with `--min-score`). The `quote` (5 or more words) must show the match. The `reason` is one sentence that links the paper to this project's evidence. It must not claim anything the quote does not support.

```bash
python3 $P --project . judge .papers/judgments.json
```

A `WARN ... shares no term with the facet` means the quote does not show why the paper fits. Pick a sentence that does, or drop the entry. If an entry comes back `REJECTED`, fix that entry by copying the exact text again or dropping it. Never change the quote to something the abstract does not say. If any entry is rejected, `judge` writes nothing, so `finalize` never sees a half-checked list. `judge` keeps a copy of each accepted paper. C ids stay the same across searches, so `judgments.json` and `reject` still work after running `search` again.

### 6. Finalize

```bash
python3 $P --project . finalize        # --out docs/papers.md
```

This verifies each accepted paper against Crossref (DOI), DataCite or arXiv (ID). A paper with neither is looked up by exact title (and year within 2) in Crossref, then arXiv. Papers whose title does not match the registry are removed. Then it writes the markdown and BibTeX files.

It also writes `docs/papers.json` and a "Code map" section: which papers explain which files, taken from each facet's evidence.

Report to the user: the output path, the number of papers per facet, any facet with no match, and any paper marked NOT verified.

## Using the papers while changing code

With the plugin installed, a hook adds the linked papers to your context automatically before you edit such a file. Otherwise, before you change a file in a project that has `.papers/codemap.json`, run `python3 $P --project . lookup <file or directory>`. It prints the papers linked to that code, with the verbatim abstract quote and why each one was linked. Use them to understand the method; do not claim more than the quote supports.

## Refresh and feedback

- Run the workflow again later. Papers listed before are marked as known, and new ones get `[new]`.
- When the user rejects a paper (by `C` id from the last search), run `python3 $P --project . reject C12 C40`. That paper is never shown again.
- `.papers/` holds the cache and state. Suggest adding it to `.gitignore`.

## Sources used

- OpenAlex: title+abstract search, papers citing a seed, related works. A free key is recommended.
- Crossref: keyword search (only records with an abstract), seed title lookup, DOI verification.
- arXiv API: optional recent preprints (`--arxiv`), arXiv ID verification.

The method choice comes from the benchmark in `bench/` (5 facets, 9 methods, blind relevance labels). OpenAlex text search + citing-seed + related works + Crossref found the most relevant papers. Each source on its own missed a different part.

Google Scholar is not used: it has no API and blocks automated access.
