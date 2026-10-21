# Motion pieces for kriosgreece.com (draft). Route map in the "Transit Map" manner, built from approved source text only.
# Loaded by build_films.py. Data lives in data/motion/<film-slug>.route.json; no file, no route section.
import json, os
from site_lib import ROOT, e


def route_data(slug):
    p = os.path.join(ROOT, "data", "motion", f"{slug}.route.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _wave_svg(origin, dests, color_cls, label):
    n = len(dests)
    step = 54
    h = 70 + step * (n - 1)
    mid = h / 2
    x0, xs, xe = 70, 300, 540
    paths, stops = [], []
    for i, name in enumerate(dests):
        y = 35 + step * i
        dy = abs(y - mid)
        bend = xs - dy if y != mid else xs
        d = f"M{x0} {mid:g} H{bend:g} L{xs:g} {y:g} H{xe}" if y != mid else f"M{x0} {mid:g} H{xe}"
        paths.append(f'<path class="mo-line {color_cls}" pathLength="1" style="--i:{i}" d="{d}"/>')
        stops.append(f'<g class="mo-stop" style="--i:{i}"><circle cx="{xe}" cy="{y:g}" r="7"/><text x="{xe + 18}" y="{y + 5:g}">{e(name)}</text></g>')
    origin_g = (f'<g class="mo-origin"><circle cx="{x0}" cy="{mid:g}" r="10"/><text x="{x0}" y="{mid - 20:g}" text-anchor="middle">{e(origin)}</text></g>')
    return (f'<svg class="mo-svg" viewBox="0 0 760 {h:g}" role="img" aria-label="{e(label)}" focusable="false">'
            + "".join(paths) + origin_g + "".join(stops) + "</svg>")


def route_html(slug):
    r = route_data(slug)
    if not r:
        return None
    rows = []
    for k, w in enumerate(r["waves"]):
        cls = "mo-a" if k == 0 else "mo-b"
        label = f'{w["years"]}: from {r["origin"]} to ' + ", ".join(w["to"])
        rows.append(f'<div class="mo-wave"><h3>{e(w["years"])}</h3><p>{e(w["note"])}</p>{_wave_svg(r["origin"], w["to"], cls, label)}</div>')
    src = r["source"]
    return (f'<p>{e(r["intro"])}</p><div class="mo-route" data-mo>{"".join(rows)}</div>'
            f'<p class="m-note-sm">Source: <a href="{src["url"]}" rel="noopener">{e(src["text"])}</a></p>')
