# Builds the Page Guide search index (Phase 2a) at data/guide_index.json.
# Only published pages in the current KRIOS direction plus the curated guide entries.
# No drafts, no staging pages, no pre-release pages, no topics the Guide routes (HOLD).
# The same forbidden-text rules as scripts/check_guide.py are applied to every passage.
# Run: python3 build_guide_index.py   (then python3 build_guide.py)
import json, os, re, glob
from bs4 import BeautifulSoup
from site_lib import ROOT

OUT = "data/guide_index.json"
G = json.load(open(os.path.join(ROOT, "data/guide.json"), encoding="utf-8"))

# Pages included. Answers pages: only the current-direction pages (not the archived mythology pages).
INCLUDE = [
    "how-we-work/index.html",
    "films/index.html",
    "films/the-greeks-who-left/index.html",
    "films/the-greek-dance/index.html",
    "sacred-days/index.html",
    "sacred-days/saint-demetrios-name-day/index.html",
    "ohi-day/index.html",
    "answers/what-does-xenitia-mean/index.html",
    "answers/what-is-a-greek-spoon-sweet/index.html",
    "answers/what-is-zeibekiko/index.html",
    "answers/who-was-athanasios-diakos/index.html",
    "answers/who-was-laskarina-bouboulina/index.html",
    "answers/who-were-the-vallahades/index.html",
    "answers/why-are-there-so-many-greeks-in-tarpon-springs/index.html",
    "answers/why-did-so-many-greeks-emigrate/index.html",
]
# Never indexed: routed or HOLD topics (Guide declines them), staging and pre-release pages.
EXCLUDE_NOTE = {
    "answers/is-sirtaki-a-traditional-greek-dance/": "HOLD H-14, routed in the Guide",
    "answers/why-was-rebetiko-censored/": "routed in the Guide (music censorship claim terms)",
    "films/saint-demetrios/": "pre-release; locked Oct 26 release",
    "sacred/": "staging page",
}
FORBID = [r"—", r"\bTESTIMONY\b", r"\blorem\b", r"\bDRAFT\b", r"\bTODO\b", r"narration v0", r"script v0", r"\bPeter\b",
          r"\bProvias\b", r"\bQuinn\b", r"\bMetaxas\b", r"\bTheodorakis\b", r"\bZeybek\b", r"\b1207\b", r"[Ss]irtaki"]
LABEL_HINTS = {"BELIEF": r"\b(Church teaches|believ|miracle|myrrh|saint'?s? intercession)", "HISTORY": r"\b(1[5-9]\d\d|census|records?|archive)",
               "PRACTICE": r"\b(families|celebrate|feast|name day|today)", "TRADITION": r"\b(custom|tradition|handed down)"}


def url_of(path):
    return "/" + path[: -len("index.html")]


def page_title(s):
    t = s.find("title")
    return re.sub(r"\s*[·|]\s*KRIOS\s*$", "", t.get_text(strip=True)) if t else ""


def passages(path):
    s = BeautifulSoup(open(os.path.join(ROOT, path), encoding="utf-8"), "html.parser")
    m = s.find("main") or s.body
    for bad in m.select("script,style,nav,form,.m-soon,[aria-hidden=true]"):
        bad.decompose()
    title, base = page_title(s), url_of(path)
    anchor, heading, out, buf = "", title, [], []

    def flush():
        txt = re.sub(r"\s+", " ", " ".join(buf)).strip()
        buf.clear()
        if len(txt.split()) < 8:
            return
        if any(re.search(p, txt) for p in FORBID):
            return
        labels = [k for k, p in LABEL_HINTS.items() if re.search(p, txt)]
        out.append({"t": title, "h": heading, "u": base + (f"#{anchor}" if anchor else ""), "x": txt[:900], "l": labels[:2]})

    for el in m.find_all(["h1", "h2", "h3", "p", "li", "dd", "blockquote", "figcaption"]):
        if el.find_parent(["li", "dd", "blockquote"]) is not None and el.name in ("p", "li"):
            continue
        if el.name in ("h1", "h2", "h3"):
            flush()
            heading = el.get_text(" ", strip=True)
            sid = el.get("id") or (el.find_parent(["section", "div"], id=True) or {}).get("id") if el.name != "h1" else ""
            anchor = sid or anchor
            continue
        buf.append(el.get_text(" ", strip=True))
        if len(" ".join(buf).split()) > 70:
            flush()
    flush()
    return out


def build():
    pages = []
    for p in INCLUDE:
        if not os.path.isfile(os.path.join(ROOT, p)):
            raise SystemExit(f"missing included page {p}")
        pages.extend(passages(p))
    curated = []
    for g in G["groups"]:
        for it in g["items"]:
            curated.append({"id": it["id"], "g": g["id"], "q": it["q"], "s": it["status"], "l": it["labels"],
                            "x": " ".join(it["a"]), "read": it["read"], "src": it["sources"]})
    idx = {"version": 1, "note": "Approved KRIOS material only. Built by build_guide_index.py.",
           "curated": curated, "passages": pages, "excluded": EXCLUDE_NOTE}
    path = os.path.join(ROOT, OUT)
    json.dump(idx, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {OUT}: {len(curated)} curated, {len(pages)} passages from {len(INCLUDE)} pages, {os.path.getsize(path)//1024} KB")


if __name__ == "__main__":
    build()
