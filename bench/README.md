# Retrieval benchmark

Compares the ways project-papers can find candidate papers. The skill's defaults come from this run.

```
python3 bench.py run     # 9 methods x facets.json, saves out/runs.json (about 45 API requests)
python3 bench.py pool    # merges every method's top 10 into out/pool.txt, shuffled, no method names
# label out/pool.txt into out/labels.json: {"P1": 2, ...}  2 = accept by the SKILL.md rubric, 1 = partly, 0 = no
python3 bench.py score   # P@10, recall against the pooled relevant set, abstract coverage, tokens per relevant paper
```

Methods: M1 OpenAlex title+abstract filter, M1b OpenAlex `search=`, M2 citing seed + search sorted by citations, M2b citing seed ranked by relevance, M3 citing seed + local keyword filter, M4 seed related works, M5 seed references, M6 arXiv keyword, M7 Crossref bibliographic.

Caveats: 5 facets from 2 projects, labels by a model (checked by a second per-axis pass and a keyword-rule judge), recall is relative to the pooled set, not to all literature. Files in `out/` are the run used for the README numbers. `spotcheck.md` is a blank sheet for a human check of 20 sampled labels.
