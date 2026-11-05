# project-papers

An agent skill that finds research papers matching what your code actually does, and refuses to invent any.

Tools like this usually fail in two ways. They return papers that match the README's marketing words rather than the techniques in the code, and the agent "remembers" papers, authors or quotes that do not exist. project-papers is built around stopping both.

- **Grounded in the code.** Every topic ("facet") it searches for must point to evidence in your project, such as `app/detector.py:52`, a model file, or a dependency. The script checks that the quoted line really exists.
- **You confirm before anything leaves your machine.** The facets and search queries are shown to you first.
- **The agent never writes paper metadata.** Titles, authors, years, DOIs and links come only from OpenAlex and Crossref responses. The agent can refer to a paper only by an ID the script gave it.
- **Every claim is checked.** Each "why this paper is relevant" must quote the abstract word for word, and the script rejects paraphrases. Listed papers are then verified against Crossref or arXiv.
- **"Nothing relevant" is a valid answer.** Facets with no strong match say so instead of being padded.

Output: `docs/papers.md` (grouped by facet, with the project evidence and the abstract quote for each paper) and `docs/papers.bib`.

## Install

The skill is a folder with `SKILL.md` and one Python script (3.8+, standard library only, no `pip install`).

**Claude Code, as a plugin:**

```
/plugin marketplace add Nawxtz/project-papers
/plugin install project-papers@project-papers
```

**Claude Code or any agent that reads `SKILL.md` files, manually:** copy `skills/project-papers/` into your skills folder, for example `~/.claude/skills/project-papers/`.

The plugin also installs a `PreToolUse` hook (`hooks/lookup_hook.py`). When the agent is about to edit a file that `docs/papers.md` links to papers, the hook adds those papers (title, link, abstract quote, reason) to its context, once per file per session. It reads only `.papers/codemap.json`, makes no network calls, and never blocks an edit. With a manual install, add it yourself in `.claude/settings.json`:

```json
{"hooks": {"PreToolUse": [{"matcher": "Edit|MultiEdit|Write",
  "hooks": [{"type": "command", "command": "python3 /path/to/project-papers/hooks/lookup_hook.py", "timeout": 10}]}]}}
```

## API keys (recommended)

The skill works without keys, but OpenAlex limits anonymous use to a small shared daily budget per IP address and sometimes pauses anonymous search entirely. A free key gives about 1000 searches a day. One project run uses roughly 10-25.

1. Create a key at <https://openalex.org/settings/api>.
2. Put it in `~/.config/project-papers/keys.env` (create the file, `chmod 600`):

```
OPENALEX_API_KEY=your-key
PAPERS_MAILTO=you@example.com
```

Environment variables with the same names work too. Use your own key. Do not share keys or create several to get around the limits. The key is sent only to OpenAlex, in an `Authorization` header.

## Use

Ask your agent something like "find papers related to this project". The skill runs this pipeline:

1. `scan` collects evidence: dependencies (requirements, pyproject, package.json, go.mod, Cargo.toml, environment.yml, Gemfile), imports (Python, notebooks, JS/TS, CDN script tags, R, Julia), model files and references, paper IDs already in the repo, README/CLAUDE.md lines. A project with no research technique gets no facets, and the skill says so and stops.
   It also ranks the techniques the code is about (docstrings, comments, citations such as "Bailey & López de Prado (2014)" or links to paper PDFs, imported names, class and function names), weighting core code over scratch, tests and examples.
2. The agent writes 1-6 facets (task, method, setting, evidence, queries, optional seed papers). Papers the code itself cites can be seeds (`seed_cites`); the script finds them by author, year and title words.
3. `check` validates the evidence, and requires every top-ranked technique to be covered by a facet or skipped with a reason, so different agents look at the same parts of the code. It prints a review table. **You confirm or edit it.**
4. `search` runs OpenAlex title+abstract search, finds papers citing each seed and the seed's related works, adds Crossref results, then dedupes and scores (about 10 seconds).
5. `show` gives the agent a compact candidate list. The agent judges each candidate with a task/method/setting rubric and a verbatim abstract quote, and `judge` validates those judgments.
6. `finalize` verifies the accepted papers against Crossref/arXiv and writes the markdown, BibTeX and `docs/papers.json`, with a code map of which papers explain which files. Original papers of a library or method the code uses are listed apart as "Foundations".

`papers.md` also has a "Lineage" section: which listed papers cite which (from OpenAlex references), so you can read a foundation before the work built on it.

Later, before an agent changes a file, `papers.py lookup <file>` prints the papers linked to it, with the abstract quote and the reason. The plugin's hook does this automatically.

To hide a paper permanently, run `papers.py reject C12`. Running the skill again marks new papers with `[new]`. State and cache live in `<project>/.papers/`; add that folder to `.gitignore`.

## How the sources were chosen

`bench/` compares 9 retrieval methods on 5 facets from 2 real projects (face detection, Thai address parsing). The 262 pooled candidates were labelled blind to the method that found them.

| Method | P@10 | Recall | Tokens per relevant paper |
|---|---|---|---|
| OpenAlex title+abstract search | **0.34** | **0.36** | 353 |
| OpenAlex `search=` parameter | 0.28 | 0.31 | 586 |
| Crossref bibliographic search | 0.22 | 0.24 | 321 |
| Seed's related works | 0.26 | 0.11 | **227** |
| Papers citing seed, relevance-ranked | 0.24 | 0.10 | 379 |
| arXiv keyword search | 0.14 | 0.05 | 956 |
| Seed's references | 0.00 | 0.00 | - |

No single source covers everything. Text search wins on classic topics, while the seed citation graph wins on new, niche models (8/10 relevant versus 2/10 from text search for a 2023 face detector). The default combination (text search + citing seed + related works + Crossref) found 45 relevant papers versus 17 for the best single method, at a similar token cost per relevant paper.

Label checks: a second explicit per-axis pass agreed on accept/reject for 19 of 20 sampled items (kappa 0.90). An independent keyword-rule judge agreed on 84% of all items (kappa 0.63) and picked the same top method. The labels come from a model, not a human panel, and the test set is small. Treat these numbers as a direction, not a guarantee.

## Tested on real projects

The full workflow was run on 6 projects of different kinds: a Python quant-trading engine, a single-file HTML/JS hand-tracking app, Jupyter notebooks, a Go ML library, and two projects with no research technique (a resume builder and a Next.js site), which correctly got no facets. Scanning was also checked on a Rust workspace, a JS ML library and a Java course project.

- **Precision of the final list.** 48 accepted papers from two projects were labelled blind by a second model (Gemini) from another vendor: it agreed on 30. The 18 disagreements were settled against the code with a written rule (`bench/agreement.md`): 9 kept, 9 dropped, so 39 of 48 (0.81) were relevant. The settling was done by Claude, not by a human, so treat 0.81 as an estimate. Most wrong accepts were same-task papers about a technique the code does not use; the rubric now scores those as method 0.
- **Different agents, same facets.** Claude and Gemini wrote facets for the same projects independently. Before the technique inventory and coverage check they shared 4 of 10 techniques on the trading engine; after, 9 of 12, and 10 of 10 on the Go library.
- **Another agent can run it.** Gemini (through the Antigravity CLI) followed `SKILL.md` end to end on three projects with no help and fixed its own queries when `search` warned.
- **API use per run** (6 facets, empty cache): `search` makes about 35 requests and costs about $0.02 of the OpenAlex daily budget, so a free key covers about 50 full runs a day; `finalize` makes about 28 (mostly Crossref). Re-runs within 24 hours are served from the cache.

## Tested on real code tasks

Finding relevant papers is one question. Whether they help an agent change code is another. `bench/codetask/` tests the second one on the hand-tracking app. There are two tasks: replace the fingertip smoothing, and replace the pinch detector. Each result is scored by a hidden simulator.

- **Setup.** 16 runs (Claude Sonnet and Haiku, web access off), each with no papers, with the skill's earlier output, or with its current output.
- **Every run beat the original code by a wide margin.** Lag on fast strokes fell from 33 px to 7-16 px, and false pinches fell from 133 to 0-1.
- **With versus without papers: no measurable difference.** Every smoothing run picked a One Euro filter from its own knowledge. Parameter choices varied more than the arms did.
- **What the papers added was a correct origin.** With the current output, every smoothing run cited the 1€ filter paper the method comes from. With the earlier output, the agents said the papers did not help.
- **One run stated a tuning procedure "from the paper" that the abstract does not contain.** `lookup` and the hook now say that only the quoted sentence is checked.

So expect the skill to tell you and your agent where the code's methods come from, with checked citations. Do not expect it to make an agent's code better on techniques the model already knows. This test is small (2-4 runs per cell), and its traces are synthetic.

The same test found three holes, now fixed:

- `scan` could not see hand-written techniques such as `p.x = p.x * 0.5 + rx * 0.5`, so it now reports them as `idiom` evidence.
- Queries worded around the app ("air writing") returned only app papers that never mention the algorithm. SKILL.md now asks for one method-and-signal query, and scores a same-app paper that lacks the method as method 0.
- `show` printed over 40 KB at once. It now runs per facet with 8 candidates.

## Limits

- Narrow topics without a well-known seed paper (for example, Thai address parsing) have few relevant papers in any source. The skill says so instead of padding.
- Papers without an abstract in OpenAlex or Crossref cannot be accepted, because there is nothing to quote.
- The script checks that each quote is real, not that the agent's scores are fair. In one test an agent accepted a paper with a single distance threshold for a facet about two-threshold (hysteresis) pinch detection. Read the "Why" and "Abstract says" lines before relying on a match.
- Ranking cannot tell a peer-reviewed study from a student project write-up. `show` prints the venue so the agent and you can tell them apart.
- Papers with no DOI or arXiv ID (some theses and repository copies) cannot be cross-checked and are marked NOT verified.
- Google Scholar and Semantic Scholar are not used. Google Scholar has no API and blocks automated access. Semantic Scholar needs a key for reliable access.
- The skill sends your facet queries (technical terms, not code) to OpenAlex, Crossref and optionally arXiv.

## Security notes

- Network access goes only to `api.openalex.org`, `api.crossref.org`, `api.datacite.org` and, with `--arxiv` or for verification, `export.arxiv.org`.
- The only secret is `OPENALEX_API_KEY`. It is read from the environment or `~/.config/project-papers/keys.env` and sent only to OpenAlex, in an `Authorization` header, never in a URL, cache file or log. Static scanners such as SkillSpector flag this as "environment value flows to network". That flow is the intended one.
- Code is never uploaded. Only the facet queries and seed titles you approved leave your machine.
- The script writes only inside `<project>/.papers/` and the output paths (`docs/papers.md`, `docs/papers.bib` by default).

## Tests

```
python3 -m unittest discover -s tests
```

## Credits

The workflow borrows ideas, not code, from paper-lookup (K-Dense), Researchbot, grounded-citations (Hermes Agent) and claude-scholar's citation-verification. Data comes from [OpenAlex](https://openalex.org), [Crossref](https://www.crossref.org) and [arXiv](https://arxiv.org). Thank you to arXiv for use of its open access interoperability.

## License

MIT. See [LICENSE](LICENSE).
