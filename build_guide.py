# Builds the Page Guide at /guide/ from data/guide.json (Phase 1 curated answers) plus Phase 2a:
# an in-browser question box over data/guide_index.json, an English/Greek/Spanish switch and an opt-in topic suggestion.
# No external AI API, no tracking. Translations marked "unreviewed" in data/guide_i18n.json are left out of the
# public build (shown in English) unless GUIDE_PREVIEW=1 is set for a staging preview.
# Run: python3 build_guide_index.py && python3 build_guide.py
import json, os, re, html, copy
from site_lib import ROOT, e
from site_parts import head, header, footer, SCRIPTS, breadcrumbs

G = json.load(open(os.path.join(ROOT, "data/guide.json"), encoding="utf-8"))
OUT = "guide/index.html"
I18N = json.load(open(os.path.join(ROOT, "data/guide_i18n.json"), encoding="utf-8"))
CONF = json.load(open(os.path.join(ROOT, "data/guide_config.json"), encoding="utf-8"))
PREVIEW = os.environ.get("GUIDE_PREVIEW") == "1"


def chips(labels):
    if not labels:
        return ""
    t = "".join(f'<li><abbr data-l="{l}" title="{e(G["labels"][l])}">{l}</abbr></li>' for l in labels)
    return f'<ul class="g-labels" aria-label="Kind of statement">{t}</ul>'


def item(it):
    st = it["status"]
    paras = "".join(f"<p>{e(p)}</p>" for p in it["a"])
    read = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t, u in it["read"])
    src = "".join(f'<li><a href="{e(u)}" rel="noopener" target="_blank">{e(t)}<span class="g-ext"> (opens the source in a new tab)</span></a></li>' for t, u in it["sources"])
    srcblock = f'<h3 data-t="source">Source</h3><ul class="g-links">{src}</ul>' if src else ""
    return f'''<li class="g-item g-{st}" id="{e(it["id"])}">
  <details>
    <summary><span class="g-q">{e(it["q"])}</span></summary>
    <div class="g-a">
      <p class="g-status"><span>{e(G["status_text"][st])}</span></p>
      {chips(it["labels"])}
      <div class="g-a-text">{paras}</div>
      <h3 data-t="read">Read on KRIOS</h3><ul class="g-links">{read}</ul>
      {srcblock}
    </div>
  </details>
</li>'''


def build():
    groups = "".join(
        f'<section class="g-group" aria-labelledby="g-{e(g["id"])}"><h2 id="g-{e(g["id"])}" data-g="{e(g["id"])}" data-en="{e(g["title"])}">{e(g["title"])}</h2><ul class="g-list">{"".join(item(i) for i in g["items"])}</ul></section>'
        for g in G["groups"])
    legend = "".join(f'<li data-l="{k}"><b>{k}</b> <span>{e(v)}</span></li>' for k, v in G["labels"].items())
    client = copy.deepcopy(I18N)
    if not PREVIEW:
        for l, st in I18N["review"].items():
            if st == "unreviewed":
                client["ui"].pop(l, None); client["labels"].pop(l, None); client["status"].pop(l, None); client["groups"].pop(l, None); client.get("terms", {}).pop(l, None)
                for v in client["items"].values(): v.pop(l, None)
    client["ui"]["en"]["intro"] = G["intro"]
    json.dump(client, open(os.path.join(ROOT, "data/guide_client.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    cfg = json.dumps({"preview": PREVIEW, "suggest_url": CONF.get("suggest_url", "")})
    langs = "".join(f'<button type="button" value="{c}" lang="{c}" aria-pressed="{"true" if c == "en" else "false"}">{n}</button>' for c, n in (("en", "English"), ("el", "Ελληνικά"), ("es", "Español")))
    status_attrs = " ".join(f'data-status-{k}="{e(v)}"' for k, v in G["status_text"].items())
    desc = "Short, source-linked answers to common questions about KRIOS films, Sacred Days and how KRIOS works. Every answer links to a published page."
    extra = ('\n<link rel="stylesheet" href="/assets/universe-fonts.css">\n<link rel="stylesheet" href="/assets/guide.css">')
    body = f'''{head("Page Guide · KRIOS", desc, "/guide/", extra=extra, ld=[breadcrumbs(("Page Guide", "/guide/"))])}
<body class="g-page" {status_attrs}>
{header()}
<main id="main">
  <div class="g-wrap">
    <div class="g-top">
      <p class="g-kick" data-t="kick">Page Guide</p>
      <div class="g-langs" role="group" aria-label="Language" hidden>{langs}</div>
    </div>
    <p class="g-draft" id="g-draft" hidden data-t="draft">Draft translation for review. Not yet approved.</p>
    <h1 data-t="h1">Questions we can answer from published pages</h1>
    <p class="g-lede" data-t="intro">{e(G["intro"])}</p>
    <form class="g-ask" id="g-ask" role="search" hidden>
      <label for="g-ask-input" data-t="ask_label">Ask about Greece, the films or KRIOS</label>
      <div class="g-ask-row"><input id="g-ask-input" name="q" type="search" autocomplete="off" maxlength="200" placeholder="For example: Why do Greeks celebrate name days?"><button class="g-btn" type="submit" data-t="ask_btn">Ask</button></div>
      <p class="g-ask-note" data-t="ask_note">Answers come only from KRIOS's published films and articles. Your question stays on this device. Please do not enter personal information.</p>
    </form>
    <div id="g-results" class="g-results" aria-live="polite"></div>
    <details class="g-how"><summary data-t="how">How to read the labels</summary>
      <ul class="g-legend">{legend}</ul>
      <p data-t="privacy">Nothing you open or type here is saved or sent anywhere, unless you choose to suggest a topic. The Guide uses no tracking.</p>
    </details>
    <h2 class="g-curated-h" data-t="curated_h">Questions with prepared answers</h2>
    {groups}
    <p class="g-foot"><a href="/how-we-work/" data-t="foot_how">How KRIOS checks its sources</a> · <a href="/films/" data-t="foot_films">All films</a></p>
  </div>
</main>
{footer()}
{SCRIPTS}
<script type="application/json" id="g-config">{cfg}</script>
<script src="/assets/guide.js" defer></script>
<script>
(function(){{
  var list=document.querySelectorAll(".g-page details");
  function openFromHash(){{var id=location.hash.slice(1);if(!id)return;var li=document.getElementById(id);if(li){{var d=li.querySelector("details");if(d){{d.open=true;}}}}}}
  openFromHash();window.addEventListener("hashchange",openFromHash);
  document.addEventListener("keydown",function(ev){{
    if(ev.key!=="Escape")return;
    var a=document.activeElement,d=a&&a.closest?a.closest(".g-item details"):null;
    if(!d){{var o=document.querySelector(".g-item details[open]");if(!o)return;d=o;}}
    d.open=false;var s=d.querySelector("summary");if(s)s.focus();ev.preventDefault();
  }});
}})();
</script>
</body>
</html>
'''
    full = os.path.join(ROOT, OUT)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(body)
    print("wrote", OUT, len(body), "bytes")


if __name__ == "__main__":
    build()
