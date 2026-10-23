#!/usr/bin/env python3
"""Page Guide claim gate. Fails the build if an answer is unsourced, links to a missing page, uses a non-canonical label,
or contains text that must never appear (HOLD claims, private terms, draft markers). Run: python3 scripts/check_guide.py"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = json.load(open(os.path.join(ROOT, "data/guide.json"), encoding="utf-8"))
CANON = {"HISTORY", "TRADITION", "BELIEF", "PRACTICE"}
FORBID = [r"—", r"\bTESTIMONY\b", r"\blorem\b", r"\bDRAFT\b", r"\bTODO\b", r"narration v0", r"script v0", r"\bPeter\b",
          r"\bProvias\b", r"\bQuinn\b", r"\bMetaxas\b", r"\bTheodorakis\b", r"\bZeybek\b", r"\b1207\b"]
# Wikipedia-sourced or news-sourced claims may only be routed, never stated (ledger H-14 and film source notes).
fails = []
def anchors_of(path):
    s = open(path, encoding="utf-8", errors="ignore").read()
    return set(re.findall(r'id="([^"]+)"', s))
def page_for(u):
    p = u.split("#")[0].lstrip("/")
    for c in ([p + "index.html"] if p == "" else [p.rstrip("/") + "/index.html", p]):
        if os.path.isfile(os.path.join(ROOT, c)):
            return os.path.join(ROOT, c)
    return None
n = 0; ids = set()
for g in G["groups"]:
    for it in g["items"]:
        n += 1
        if it["id"] in ids: fails.append(f"duplicate id {it['id']}")
        ids.add(it["id"])
        if it["status"] not in G["status_text"]: fails.append(f"{it['id']}: unknown status")
        if not it["read"]: fails.append(f"{it['id']}: no published link")
        if it["status"] == "answered" and not it["sources"]: fails.append(f"{it['id']}: answered without a named source")
        if it["status"] != "routed" and it["status"] == "answered":
            if not all(u.startswith("https://") for _, u in it["sources"]): fails.append(f"{it['id']}: source not https")
        for l in it["labels"]:
            if l not in CANON: fails.append(f"{it['id']}: non-canonical label {l}")
        for t, u in it["read"]:
            if not u.startswith("/"): fails.append(f"{it['id']}: read link not internal {u}")
            else:
                pg = page_for(u)
                if not pg: fails.append(f"{it['id']}: missing page {u}")
                elif "#" in u and u.split("#")[1] not in anchors_of(pg): fails.append(f"{it['id']}: missing anchor {u}")
        text = " ".join(it["a"]) + " " + it["q"]
        for pat in FORBID:
            if re.search(pat, text): fails.append(f"{it['id']}: forbidden text /{pat}/")
        if it["status"] == "routed" and not re.search(r"does not|not answer|no single|open question|cannot", text):
            fails.append(f"{it['id']}: routed answer must say it is not answered")
# Phase 2a: the search index may contain only approved published passages
ip = os.path.join(ROOT, "data/guide_index.json")
if os.path.isfile(ip):
    IX = json.load(open(ip, encoding="utf-8"))
    for i, ps in enumerate(IX["passages"]):
        for pat in FORBID + [r"[Ss]irtaki"]:
            if re.search(pat, ps["x"]): fails.append(f"index passage {i} ({ps['u']}): forbidden text /{pat}/")
        pg = page_for(ps["u"])
        if not pg: fails.append(f"index passage {i}: missing page {ps['u']}")
        elif "#" in ps["u"] and ps["u"].split("#")[1] not in anchors_of(pg): fails.append(f"index passage {i}: missing anchor {ps['u']}")
        for bad in ("/sacred/", "/films/saint-demetrios/", "/answers/is-sirtaki", "/answers/why-was-rebetiko"):
            if ps["u"].startswith(bad): fails.append(f"index passage {i}: excluded page {ps['u']}")
    print(f"index gate: {len(IX['passages'])} passages checked")
ic = os.path.join(ROOT, "data/guide_client.json")
if os.path.isfile(ic):
    CL = json.load(open(ic, encoding="utf-8")); I18 = json.load(open(os.path.join(ROOT, "data/guide_i18n.json"), encoding="utf-8"))
    for l, st in I18["review"].items():
        if st == "unreviewed" and l in CL["ui"] and os.environ.get("GUIDE_PREVIEW") != "1":
            fails.append(f"unreviewed language {l} present in the public client file")
    if re.search("—", json.dumps(CL, ensure_ascii=False)): fails.append("em dash in client strings")
print(f"page guide gate: {n} items, {len(fails)} failures")
for f in fails: print("FAIL", f)
sys.exit(1 if fails else 0)
