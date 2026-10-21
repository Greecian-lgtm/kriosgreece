# Motion pieces for kriosgreece.com (draft). Route map in the "Transit Map" manner, built from approved source text only.
# Loaded by build_films.py. Data lives in data/motion/<film-slug>.route.json; no file, no route section.
import json, os
from site_lib import ROOT, e


def route_data(slug):
    p = os.path.join(ROOT, "data", "motion", f"{slug}.route.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _wave_svg(origin, dests, color_cls, label):
    # Narrow viewBox so labels stay near 18px on a phone. One trunk, evenly spaced branches.
    n = len(dests)
    step = 58
    h = 74 + step * (n - 1)
    mid = h / 2
    x0, xb, xs, xe = 60, 150, 190, 250
    paths, stops = [], []
    for i, name in enumerate(dests):
        y = 37 + step * i
        d = f"M{x0} {mid:g} H{xe}" if abs(y - mid) < 0.5 else f"M{x0} {mid:g} H{xb} L{xs} {y:g} H{xe}"
        paths.append(f'<path class="mo-line {color_cls}" pathLength="1" style="--i:{i}" d="{d}"/>')
        stops.append(f'<g class="mo-stop" style="--i:{i}"><circle cx="{xe}" cy="{y:g}" r="8"/><text x="{xe + 18}" y="{y + 8:g}">{e(name)}</text></g>')
    origin_g = (f'<g class="mo-origin"><circle cx="{x0}" cy="{mid:g}" r="11"/><text x="{x0}" y="{mid - 22:g}" text-anchor="middle">{e(origin)}</text></g>')
    return (f'<svg class="mo-svg" viewBox="0 0 470 {h:g}" role="img" aria-label="{e(label)}" focusable="false">'
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
