#!/usr/bin/env python3
"""Compare retrieval methods for project-papers.

  bench.py run      run every method on every facet in facets.json, save ranked lists
  bench.py pool     merge the top-K of all methods into one shuffled, method-blind list to label
  bench.py score    read labels.json and print P@K, recall, abstract coverage, tokens per relevant paper

Labels are written by a judge who sees only pool.txt (no method names).
"""
import json
import math
import os
import random
import re
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, "..", "skills", "project-papers", "scripts"))
import papers as pp  # noqa: E402

OUT = os.path.join(HERE, "out")
K = 10
SHOW_CHARS = 700  # same truncation as `papers.py show`
SELECT = pp.OA_SELECT + ",referenced_works"


def terms_of(queries):
    stop = {"the", "and", "for", "with", "using", "based", "via", "from", "real", "time"}
    return {t for q in queries for t in re.findall(r"[a-z0-9]+", q.lower()) if len(t) > 2 and t not in stop}


def local_match(p, terms, need=2):
    text = (p["title"] + " " + p["abstract"]).lower()
    return sum(1 for t in terms if t in text) >= need


def run(http, facets):
    seeds = {}
    for f in facets:
        got = []
        for title in f["seed_titles"]:
            data = http.openalex("works", {"filter": "title.search:" + title.replace(",", " "),
                                           "per_page": 5, "select": SELECT, "sort": "cited_by_count:desc"})
            best = max(data["results"], key=lambda w: pp.title_sim(w.get("title"), title), default=None)
            if best and pp.title_sim(best.get("title"), title) >= 0.9:
                got.append(best)
            else:
                print("seed not found: " + title)
        seeds[f["id"]] = got

    def m1_oa_filter(f):
        q = " OR ".join("(%s)" % x for x in f["queries"])
        d = http.openalex("works", {"filter": "title_and_abstract.search:" + q.replace(",", " "),
                                    "per_page": 25, "select": pp.OA_SELECT})
        return [pp.oa_to_paper(w) for w in d["results"]]

    def m1b_oa_search_param(f):
        q = " OR ".join("(%s)" % x for x in f["queries"])
        d = http.openalex("works", {"search": q, "per_page": 25, "select": pp.OA_SELECT})
        return [pp.oa_to_paper(w) for w in d["results"]]

    def m2_cites_search(f):
        out = []
        q = " OR ".join("(%s)" % x for x in f["queries"])
        for s in seeds[f["id"]]:
            sid = s["id"].rsplit("/", 1)[-1]
            d = http.openalex("works", {"filter": "cites:%s,title_and_abstract.search:%s" % (sid, q.replace(",", " ")),
                                        "per_page": 25, "select": pp.OA_SELECT, "sort": "cited_by_count:desc"})
            out += [pp.oa_to_paper(w) for w in d["results"]]
        return out

    def m2b_cites_search_relevance(f):
        out = []
        q = " OR ".join("(%s)" % x for x in f["queries"])
        for s in seeds[f["id"]]:
            sid = s["id"].rsplit("/", 1)[-1]
            d = http.openalex("works", {"filter": "cites:" + sid, "search": q,
                                        "per_page": 25, "select": pp.OA_SELECT})
            out += [pp.oa_to_paper(w) for w in d["results"]]
        return out

    def m3_cites_local(f):
        out, terms = [], terms_of(f["queries"])
        for s in seeds[f["id"]]:
            sid = s["id"].rsplit("/", 1)[-1]
            d = http.openalex("works", {"filter": "cites:" + sid, "per_page": 100,
                                        "select": pp.OA_SELECT, "sort": "cited_by_count:desc"})
            out += [p for p in map(pp.oa_to_paper, d["results"]) if local_match(p, terms)]
        return out

    def by_ids(ids):
        if not ids:
            return []
        d = http.openalex("works", {"filter": "openalex_id:" + "|".join(ids[:50]),
                                    "per_page": min(len(ids), 50), "select": pp.OA_SELECT})
        ps = [pp.oa_to_paper(w) for w in d["results"]]
        return sorted(ps, key=lambda p: -(p["cited_by"] or 0))

    def m4_related(f):
        ids = [r.rsplit("/", 1)[-1] for s in seeds[f["id"]] for r in s.get("related_works") or []]
        return by_ids(ids)

    def m5_references(f):
        ids = [r.rsplit("/", 1)[-1] for s in seeds[f["id"]] for r in s.get("referenced_works") or []]
        terms = terms_of(f["queries"])
        return [p for p in by_ids(ids) if local_match(p, terms, need=1)]

    def m6_arxiv(f):
        out = []
        for q in f["queries"][:2]:
            ts = [t for t in re.findall(r"[A-Za-z0-9\-]+", q) if len(t) > 2]
            sq = " AND ".join("all:%s" % t for t in ts[:6])
            url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
                {"search_query": sq, "max_results": 15, "sortBy": "relevance"})
            out += pp.parse_arxiv(http.get(url, arxiv=True, kind="arxiv"))
        return out

    def m7_crossref(f):
        q = " ".join(f["queries"])
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
            {"query.bibliographic": q, "rows": 25, "select": "DOI,title,abstract,author,issued,is-referenced-by-count"})
        out = []
        for it in http.get_json(url)["message"]["items"]:
            ab = re.sub(r"<[^>]+>", " ", it.get("abstract") or "")
            out.append({"title": (it.get("title") or [""])[0], "doi": it["DOI"].lower(), "arxiv": None,
                        "abstract": re.sub(r"\s+", " ", ab).strip(), "cited_by": it.get("is-referenced-by-count", 0),
                        "year": ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                        "authors": [], "venue": "", "url": "https://doi.org/" + it["DOI"]})
        return out

    methods = {"M1_oa_title_abstract": m1_oa_filter, "M1b_oa_search_param": m1b_oa_search_param,
               "M2_cites_plus_search": m2_cites_search, "M2b_cites_search_relevance": m2b_cites_search_relevance,
               "M3_cites_local_filter": m3_cites_local, "M4_related_works": m4_related,
               "M5_references": m5_references, "M6_arxiv": m6_arxiv, "M7_crossref": m7_crossref}
    runs = {}
    for name, fn in methods.items():
        for f in facets:
            before = dict(http.requests)
            t0 = time.time()
            try:
                ps = fn(f)
                err = None
            except Exception as e:  # record and continue
                ps, err = [], str(e)[:200]
            seen, ranked = set(), []
            for p in ps:
                key = (pp.paper_keys(p) or [None])[0]
                if key and key not in seen and p.get("title"):
                    seen.add(key)
                    ranked.append({"key": key, "title": p["title"], "abstract": p.get("abstract") or "",
                                   "year": p.get("year"), "cited_by": p.get("cited_by")})
            reqs = sum(http.requests.values()) - sum(before.values())
            runs.setdefault(name, {})[f["id"]] = {"ranked": ranked[:K], "n_total": len(ranked), "requests": reqs,
                                                  "seconds": round(time.time() - t0, 1), "error": err}
            print("%-28s %s n=%-3d req=%d %s" % (name, f["id"], len(ranked), reqs, err or ""))
    runs["_seeds"] = {fid: [s.get("title") for s in v] for fid, v in seeds.items()}
    return runs



def cmd_pool():
    runs = json.load(open(os.path.join(OUT, "runs.json")))
    facets = {f["id"]: f for f in json.load(open(os.path.join(HERE, "facets.json")))}
    pool = {}
    for name, per in runs.items():
        if name.startswith("_"):
            continue
        for fid, r in per.items():
            for p in r["ranked"]:
                t = pp.norm_title(p["title"])
                item = pool.setdefault((fid, t), {"facet": fid, "title": p["title"], "abstract": ""})
                if len(p["abstract"]) > len(item["abstract"]):
                    item["abstract"] = p["abstract"]
    items = list(pool.values())
    random.Random(7).shuffle(items)
    items.sort(key=lambda x: x["facet"])
    lines = []
    for i, it in enumerate(items, 1):
        it["pid"] = "P%d" % i
    for fid in sorted(facets):
        f = facets[fid]
        lines.append("\n## %s %s | task: %s | method: %s | setting: %s" % (fid, f["name"], f["task"], f["method"], f["setting"]))
        for it in [x for x in items if x["facet"] == fid]:
            ab = it["abstract"][:500] or "(no abstract)"
            lines.append("%s | %s\n   %s" % (it["pid"], it["title"], ab))
    json.dump(items, open(os.path.join(OUT, "pool.json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, "pool.txt"), "w").write("\n".join(lines))
    print("pool: %d items -> out/pool.txt" % len(items))


def cmd_score():
    runs = json.load(open(os.path.join(OUT, "runs.json")))
    items = json.load(open(os.path.join(OUT, "pool.json")))
    labels = json.load(open(os.path.join(OUT, "labels.json")))  # {"P1": 2, ...}  2 relevant, 1 partly, 0 no
    rel = {(it["facet"], pp.norm_title(it["title"])): labels.get(it["pid"], 0) for it in items}
    facets = sorted({it["facet"] for it in items})
    total_rel = {f: sum(1 for (ff, _), v in rel.items() if ff == f and v == 2) for f in facets}
    rows = []
    for name, per in runs.items():
        if name.startswith("_"):
            continue
        p_sum, r_sum, cov, toks, found, reqs, secs, nf = 0, 0, 0, 0, 0, 0, 0, 0
        for f in facets:
            r = per.get(f, {"ranked": [], "requests": 0, "seconds": 0})
            ranked = r["ranked"]
            hits = sum(1 for p in ranked if rel.get((f, pp.norm_title(p["title"]))) == 2)
            p_sum += hits / K
            r_sum += hits / total_rel[f] if total_rel[f] else 0
            cov += sum(1 for p in ranked if p["abstract"])
            toks += sum((len(p["title"]) + min(len(p["abstract"]), SHOW_CHARS)) / 4 for p in ranked)
            found += hits
            reqs += r["requests"]
            secs += r["seconds"]
            nf += 1
        n_listed = sum(len(per.get(f, {}).get("ranked", [])) for f in facets)
        rows.append({"method": name, "P@10": round(p_sum / nf, 3), "recall": round(r_sum / nf, 3),
                     "relevant": found, "listed": n_listed,
                     "abs_cov": round(cov / n_listed, 2) if n_listed else 0,
                     "tok_per_rel": round(toks / found) if found else None, "tokens": round(toks),
                     "requests": reqs, "seconds": round(secs, 1)})
    rows.sort(key=lambda x: (-(x["P@10"] + x["recall"]), x["tok_per_rel"] or math.inf))
    hdr = ["method", "P@10", "recall", "relevant", "listed", "abs_cov", "tok_per_rel", "tokens", "requests", "seconds"]
    print(" | ".join(hdr))
    for r in rows:
        print(" | ".join(str(r[h]) for h in hdr))
    print("relevant papers per facet in pool: %s" % total_rel)
    json.dump(rows, open(os.path.join(OUT, "scores.json"), "w"), indent=1)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(OUT, exist_ok=True)
    if cmd == "run":
        pp.load_keys_file()
        http = pp.Http(OUT)
        facets = json.load(open(os.path.join(HERE, "facets.json")))
        runs = run(http, facets)
        json.dump(runs, open(os.path.join(OUT, "runs.json"), "w"), ensure_ascii=False, indent=1)
        print("requests: %s" % http.requests)
    elif cmd == "pool":
        cmd_pool()
    elif cmd == "score":
        cmd_score()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
