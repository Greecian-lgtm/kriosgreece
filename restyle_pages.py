# Restyles blog/ and answers/ pages onto /assets/krios.css with the shared KRIOS header/footer.
# Text content and URLs are kept. Run from the repo root: python3 restyle_pages.py
import glob, re, sys

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="/assets/krios.css">')
TOP = ('<header class="k-top"><div class="k-in">'
       '<a class="k-brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>'
       '<nav class="k-nav" aria-label="Site"><a href="/#episodes">Episodes</a><a href="/blog/">Articles</a>'
       '<a href="/answers/">Q&amp;A</a><a href="/tools/">Quizzes</a>'
       '<a class="k-sub" href="https://www.youtube.com/@KriosGreece?sub_confirmation=1" rel="noopener">Subscribe</a></nav>'
       '</div></header>')
FOOT = ('<footer class="k-foot"><div class="k-in"><span>© 2026 KRIOS · '
        '<a href="/">kriosgreece.com</a> · <a href="https://www.youtube.com/@KriosGreece" rel="noopener">YouTube ↗</a></span>'
        '<i>For my father, Peter (Πέτρος).</i></div></footer>')
MARK = 'data-k="v1"'

def fix_text(s):
    s = s.replace("youtube.com/@KriosMythology", "youtube.com/@KriosGreece")
    s = s.replace("@KriosMythology", "@KriosGreece")
    s = re.sub(r"Krios Mythology", "KRIOS", s)
    return s

def restyle(s):
    if MARK in s:
        return s, False
    s = fix_text(s)
    # remove stray markdown fences that leaked into pages
    s = re.sub(r"```(?:html)?", "", s)
    # drop every <style> block (old dark themes)
    s = re.sub(r"<style[\s\S]*?</style>", "", s)
    head_end = s.find("</head>")
    if head_end == -1:
        return s, False
    body_m = re.search(r"<body[^>]*>", s)
    if not body_m:
        return s, False
    head = s[:head_end] + FONT + "\n"
    body = s[body_m.end():]
    # flatten a whole document accidentally nested inside <body>
    body = re.sub(r"<!DOCTYPE[^>]*>", "", body, flags=re.I)
    body = re.sub(r"</?html[^>]*>", "", body, flags=re.I)
    body = re.sub(r"<head>[\s\S]*?</head>", "", body, flags=re.I)
    body = re.sub(r"</?body[^>]*>", "", body, flags=re.I)
    out = (head + "</head>\n<body " + MARK + ">" + TOP + '\n<div class="k-main">' + body.strip() +
           "\n</div>\n" + FOOT + "\n</body>\n</html>\n")
    return out, True

files = sorted(set(glob.glob("blog/**/*.html", recursive=True) + glob.glob("answers/**/*.html", recursive=True)))
changed = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    if 'http-equiv="refresh"' in s:          # redirect stubs: only fix the target and wording
        t = fix_text(s)
        if t != s:
            open(f, "w", encoding="utf-8").write(t); changed += 1
        continue
    out, ok = restyle(s)
    if ok:
        open(f, "w", encoding="utf-8").write(out); changed += 1
    else:
        print("skipped", f, file=sys.stderr)
print("pages", len(files), "changed", changed)
