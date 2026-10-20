"""Sync kriosgreece.com with the KRIOS YouTube channel.

Runs on GitHub Actions (see .github/workflows/sync-youtube.yml). It reads the channel's public
RSS feed, adds any new long-form video (Shorts are skipped) to data/episodes.json, handles a
matching entry in data/upcoming.json (removes the "Coming" card and copies its held files from the release branch,
for example the credits page), then rebuilds index.html and the Links page.

Exit status 0 always; prints what changed. The workflow commits and pushes only if files changed.
Run locally with --dry-run --feed FILE to test against a saved feed.
"""
import argparse, json, re, subprocess, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import date

CHANNEL_ID = "UC845GaAiIR51FFPD5wEsXAg"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}
SEASON3_FROM = "2026-10-11"          # director decision Oct 19, 2026: Season 3 starts at EP020
UA = {"User-Agent": "Mozilla/5.0 (kriosgreece.com site sync)", "Accept-Language": "en-US,en;q=0.9"}


def get(url, method="GET"):
    req = urllib.request.Request(url, headers=UA, method=method)
    return urllib.request.urlopen(req, timeout=30)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def is_short(vid):
    """YouTube serves /shorts/ID directly for Shorts and redirects for normal videos."""
    opener = urllib.request.build_opener(NoRedirect)
    try:
        r = opener.open(urllib.request.Request(f"https://www.youtube.com/shorts/{vid}", headers=UA), timeout=30)
        return r.status == 200
    except urllib.error.HTTPError as e:
        return False if e.code in (301, 302, 303, 307, 308) else None


def minutes(vid):
    try:
        html = get(f"https://www.youtube.com/watch?v={vid}").read().decode("utf-8", "replace")
        m = re.search(r'"lengthSeconds":"(\d+)"', html)
        return max(1, round(int(m.group(1)) / 60)) if m else None
    except Exception:
        return None


def clean_title(t):
    t = re.sub(r"\s*\|.*$", "", t)                      # drop " | Greek Diaspora Story" style suffixes
    t = re.sub(r"[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF]", "", t)  # flags and emoji
    t = t.replace("—", ",").replace("  ", " ").strip().rstrip(".")
    return t


def tease_from(desc):
    for line in desc.splitlines():
        line = re.sub(r"[#*_>]", "", line).strip()
        if not line or "AI-generated" in line or "AI use" in line or line.startswith("http") or len(line) < 25:
            continue
        line = line.replace("—", ",")
        return line if len(line) <= 170 else line[:167].rsplit(" ", 1)[0] + "…"
    return ""


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        out.append(dict(id=vid, title=e.findtext("a:title", namespaces=NS) or "",
                        published=(e.findtext("a:published", namespaces=NS) or "")[:10],
                        desc=e.findtext("media:group/media:description", default="", namespaces=NS) or ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--feed", help="read the feed from a local file instead of YouTube")
    a = ap.parse_args()

    xml_text = open(a.feed, encoding="utf-8").read() if a.feed else get(FEED).read().decode("utf-8")
    data = json.load(open("data/episodes.json", encoding="utf-8"))
    up = json.load(open("data/upcoming.json", encoding="utf-8"))
    known = {x["id"] for x in data["episodes"]} | {x["id"] for x in data["season1"]}
    known |= set(data.get("skipped", []))

    added, released = [], []
    for v in sorted(parse_feed(xml_text), key=lambda v: v["published"]):
        if v["id"] in known:
            continue
        short = None if a.feed else is_short(v["id"])
        if short:
            data.setdefault("skipped", []).append(v["id"]); continue
        if short is None and not a.feed:
            print("could not classify", v["id"], "- will retry next run"); continue
        match = next((u for u in up["upcoming"] if u["match"].lower() in v["title"].lower()), None)
        ep = dict(id=v["id"], date=v["published"], mins=(None if a.feed else minutes(v["id"])) or 10,
                  label=(match or {}).get("label") or "New",
                  title=(match or {}).get("title") or clean_title(v["title"]),
                  tease=(match or {}).get("tease") or tease_from(v["desc"]),
                  season=3 if v["published"] >= SEASON3_FROM else 2)
        if match:
            up["upcoming"].remove(match)
            released.append(match)
        data["episodes"].append(ep)
        added.append(ep)

    if not added:
        print("no new videos"); return
    for ep in added:
        print("added:", ep["date"], ep["id"], ep["title"])
    if a.dry_run:
        print(json.dumps(added, ensure_ascii=False, indent=1)); return

    json.dump(data, open("data/episodes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(up, open("data/upcoming.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for m in released:
        br, files = m.get("release_branch"), m.get("release_files", [])
        if br and files:
            subprocess.run(["git", "fetch", "--depth=1", "origin", br], check=True)
            r = subprocess.run(["git", "checkout", "FETCH_HEAD", "--"] + files)
            print("released files from", br, files, "ok" if r.returncode == 0 else "FAILED")
    subprocess.run([sys.executable, "build_home.py"], check=True)


if __name__ == "__main__":
    main()
