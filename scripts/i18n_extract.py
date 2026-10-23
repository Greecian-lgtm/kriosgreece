"""Extract translatable text from built KRIOS pages for the site-wide language layer.
Usage: python3 scripts/i18n_extract.py PAGE.html [...]   -> prints JSON {page_key: {"strings": [...], "attrs": [...]}}
A 'string' is the normalized text of a leaf block (an element whose children are only inline tags). Mixed content
(inline links or emphasis) is kept as HTML so links survive translation. Film titles and section names are handled
separately (kept in English by director decision)."""
import sys, re, json, html
from html.parser import HTMLParser

BLOCK = {"p","li","h1","h2","h3","h4","h5","h6","figcaption","label","summary","dt","dd","td","th","blockquote","button","a","span","small","div","i","b","strong","em","legend","option"}
INLINE = {"a","b","i","em","strong","span","small","br","abbr","code","time","sup","sub"}
SKIP = {"script","style","noscript","svg","template","code"}

def norm(s): return re.sub(r"\s+", " ", html.unescape(s)).strip()

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=False); s.stack=[]; s.out=[]; s.attrs=[]; s.skip=0; s.inbody=False
    def handle_starttag(s, t, a):
        a=dict(a)
        if t in SKIP: s.skip+=1
        for k in ("alt","aria-label","placeholder","title"):
            v=a.get(k)
            if v and re.search("[A-Za-z]{2}", v) and not s.skip: s.attrs.append(norm(v))
        if t in ("br","img","input","meta","link","source","hr","wbr"):
            if s.stack: s.stack[-1]["html"]+=s.get_starttag_text() if t=="br" else ""
            return
        s.stack.append({"t":t,"html":"","text":"","blockkids":False})
    def handle_endtag(s, t):
        if t in SKIP: s.skip=max(0,s.skip-1)
        if not s.stack: return
        # pop until matching tag
        while s.stack:
            n=s.stack.pop()
            if n["t"]==t: break
        txt=norm(n["text"])
        leaf = not n["blockkids"]
        if s.stack:
            par=s.stack[-1]
            if n["t"] in INLINE and leaf:
                par["html"]+=f"<{n['t']}>"+n["html"]+f"</{n['t']}>" if n["t"]!="a" else n["_open"]+n["html"]+"</a>" if "_open" in n else n["html"]
                par["text"]+=n["text"]
            else:
                par["blockkids"]=True; par["text"]+=n["text"]
        if leaf and txt and re.search("[A-Za-z]{2}", txt) and not s.skip and n["t"] in BLOCK:
            mixed = "<" in n["html"]
            s.out.append({"en":txt, "html": norm(n["html"]) if mixed else None})
    def handle_data(s, d):
        if s.skip or not s.stack: return
        s.stack[-1]["html"]+=html.escape(html.unescape(d), quote=False); s.stack[-1]["text"]+=d
    def handle_entityref(s, name): s.handle_data(f"&{name};")
    def handle_charref(s, name): s.handle_data(f"&#{name};")
    def handle_startendtag(s, t, a): s.handle_starttag(t, a); 

def extract(path):
    src=open(path,encoding="utf-8").read()
    body=src[src.find("<body"):]
    p=P()
    # remember link openings so hrefs survive
    _st=p.handle_starttag
    def st(t,a,_st=_st):
        _st(t,a)
        if t=="a" and p.stack and p.stack[-1]["t"]=="a": p.stack[-1]["_open"]=p.get_starttag_text()
    p.handle_starttag=st
    p.feed(body)
    seen=set(); strings=[]
    for o in p.out:
        if o["en"] in seen: continue
        seen.add(o["en"]); strings.append(o)
    return {"strings":strings,"attrs":sorted(set(p.attrs))}

def key(path):
    k=path.replace("index.html","").strip("/").replace("/","__")
    return k or "home"

if __name__=="__main__":
    print(json.dumps({key(f):extract(f) for f in sys.argv[1:]},ensure_ascii=False,indent=1))
