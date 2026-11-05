#!/usr/bin/env python3
"""PreToolUse hook: before an agent edits a file that has linked papers, add them to its context.

Reads the hook event on stdin. Looks for <project>/.papers/codemap.json above the edited file
(written by `papers.py finalize`). Adds each file's papers once per session, so repeated edits
cost no extra tokens. Never blocks the edit: on any problem it exits 0 and says nothing.
Stdlib only, no network.
"""
import json
import os
import sys

MAX_CHARS = 1800


def find_root(path):
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.isfile(os.path.join(d, ".papers", "codemap.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def main():
    event = json.load(sys.stdin)
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return
    root = find_root(path)
    if not root:
        return
    rel = os.path.relpath(os.path.abspath(path), root)
    state_dir = os.path.join(root, ".papers")
    with open(os.path.join(state_dir, "codemap.json"), encoding="utf-8") as f:
        papers = [p for p in json.load(f).get("papers", []) if rel in p.get("files", [])]
    if not papers:
        return
    seen_path = os.path.join(state_dir, "hook_seen.json")
    try:
        with open(seen_path, encoding="utf-8") as f:
            seen = json.load(f)
    except (OSError, ValueError):
        seen = {}
    session = str(event.get("session_id", ""))
    if seen.get("session") != session:
        seen = {"session": session, "files": []}
    if rel in seen["files"]:
        return
    seen["files"].append(rel)
    with open(seen_path, "w", encoding="utf-8") as f:
        json.dump(seen, f)
    out = ["Papers linked to %s (from docs/papers.md; each quote is checked word for word against the abstract):" % rel]
    for p in papers:
        out.append("- %s (%s) [%s, %s]%s: %s" % (p["title"], p.get("year") or "n.d.", p["facet_name"], p["role"],
                                               "" if p.get("verified") else " NOT verified", p["url"]))
        out.append('  abstract: "%s" | why: %s' % (p["quote"], p["reason"]))
    out.append("Use them to understand the method. Only the quoted sentence is checked. Anything else you recall "
               "about these papers (parameters, procedures, results) is unchecked: say so when you rely on it.")
    text = "\n".join(out)
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n(more: run papers.py lookup %s)" % rel
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # a broken hook must never stop an edit
    sys.exit(0)
