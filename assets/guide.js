/* KRIOS Page Guide, Phase 2a: ask your own question (in-browser search over approved KRIOS material),
   language switch (English, Greek, Spanish) and an opt-in topic suggestion. No tracking. Questions are not
   stored or sent, except the suggestion the visitor chooses to send. */
(function () {
  "use strict";
  var root = document.querySelector(".g-page");
  if (!root) return;
  var CFG = JSON.parse(document.getElementById("g-config").textContent);
  var I18N = null, IDX = null, LANG = "en", docs = [], df = {}, avgLen = 0;

  var STOP = {};
  ("a an and are as at be by can did do does for from has have how i in is it its me my of on or our so that the their " +
   "there this to was we were what when where which who why will with you your about into than then them they " +
   "ο η το οι τα του της των τον την στο στη στην στον στα στις στους σε και να με για απο από ειναι είναι τι πως πώς " +
   "γιατι γιατί ποιος ποια ποιο ποτε πότε που πού θα δεν μια ενα ένα ενας ένας " +
   "el la los las un una unos unas y de del al en que por para con como cómo qué que es son se su sus lo le les mi " +
   "por qué cuando cuándo donde dónde cuál cual quien quién hay").split(" ").forEach(function (w) { STOP[fold(w)] = 1; });

  function fold(s) {
    return (s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/ς/g, "σ");
  }
  function stem(t) {
    if (/^[a-z]+$/.test(t) && t.length > 4) return t.replace(/ies$/, "y").replace(/(ing|ed|es|s)$/, "");
    return t;
  }
  function tokens(s) {
    return (fold(s).match(/[\p{L}\p{N}]+/gu) || []).filter(function (t) { return t.length > 1 && !STOP[t]; });
  }
  function bridgeTerms(tok) {
    var out = [];
    ["el", "es", "en"].forEach(function (l) {
      var b = I18N.bridge[l] || {};
      Object.keys(b).forEach(function (k) {
        var kk = fold(k), p = kk.slice(0, Math.max(4, kk.length - 2));
        if (tok === kk || (tok.length >= 4 && tok.indexOf(p) === 0)) out = out.concat(tokens(b[k]));
      });
    });
    return out;
  }
  function queryTerms(q) {
    var base = tokens(q), all = [];
    base.forEach(function (t) { all.push(t); all = all.concat(bridgeTerms(t)); });
    var seen = {};
    return { n: base.length, terms: all.map(stem).filter(function (t) { if (seen[t]) return false; seen[t] = 1; return true; }) };
  }

  function indexDocs() {
    IDX.curated.forEach(function (c) {
      var tr = I18N.items[c.id] || {};
      var extra = ["el", "es"].map(function (l) { return tr[l] ? tr[l].join(" ") : ""; }).join(" ");
      var text = c.q + " " + c.q + " " + c.q + " " + c.x + " " + extra + " " + ((I18N.alias || {})[c.id] || "");
      docs.push({ kind: "c", ref: c, toks: tokens(text).map(stem) });
    });
    IDX.passages.forEach(function (p) {
      docs.push({ kind: "p", ref: p, toks: tokens(p.t + " " + p.h + " " + p.h + " " + p.x).map(stem) });
    });
    var tot = 0;
    docs.forEach(function (d) {
      tot += d.toks.length; d.tf = {};
      d.toks.forEach(function (t) { d.tf[t] = (d.tf[t] || 0) + 1; });
      Object.keys(d.tf).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
    });
    avgLen = tot / docs.length;
  }

  function search(q) {
    var qt = queryTerms(q), N = docs.length, res = [];
    docs.forEach(function (d) {
      var s = 0, hit = 0;
      qt.terms.forEach(function (t) {
        var f = d.tf[t]; if (!f) return; if (df[t] < 0.35 * N) hit++;
        var idf = Math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5));
        s += idf * (f * 2.2) / (f + 1.2 * (0.25 + 0.75 * d.toks.length / avgLen));
      });
      if (d.kind === "c") s *= 1.35;
      if (s > 0) res.push({ d: d, s: s, hit: hit });
    });
    res.sort(function (a, b) { return b.s - a.s; });
    /* A question the Guide deliberately declines wins a close match: declining beats answering around a HOLD. */
    for (var i = 1; i < Math.min(4, res.length); i++) {
      var x = res[i];
      if (x.d.kind === "c" && x.d.ref.s === "routed" && x.d.ref.id !== "not-found" && x.s >= 0.85 * res[0].s && x.hit >= 2) { res.splice(i, 1); res.unshift(x); break; }
    }
    var top = res[0], need = Math.min(2, Math.max(1, qt.n));
    var ok = top && top.s >= 3.2 && top.hit >= need;
    return { ok: !!ok, res: res, qn: qt.n };
  }

  /* ---------- language ---------- */
  /* "published_draft": live by director decision (Oct 23, 2026) while the named human review is pending; a draft notice stays visible */
  function allowed(l) { return l === "en" || CFG.preview || I18N.review[l] === "reviewed" || I18N.review[l] === "published_draft"; }
  function T(k) { var u = I18N.ui[LANG] || {}; return (u[k] != null ? u[k] : I18N.ui.en[k]) || ""; }
  function itemText(c) {
    var tr = (I18N.items[c.id] || {})[LANG];
    if (LANG !== "en" && tr && allowed(LANG)) return { q: tr[0], a: tr.slice(1), translated: true };
    return { q: c.q, a: [c.x], translated: LANG === "en" };
  }
  function labelText(l) { var m = (I18N.labels[LANG] || I18N.labels.en)[l] || I18N.labels.en[l]; return m; }
  function statusText(s) { var m = I18N.status[LANG]; return (m && m[s]) || root.getAttribute("data-status-" + s) || s; }

  function setLang(l, save) {
    if (!allowed(l)) l = "en";
    LANG = l;
    document.documentElement.lang = l;
    root.querySelectorAll("[data-t]").forEach(function (el) { var v = T(el.getAttribute("data-t")); if (v) el.textContent = v; });
    var inp = document.getElementById("g-ask-input"); if (inp) inp.placeholder = T("ask_ph");
    root.querySelectorAll(".g-langs button").forEach(function (b) { b.setAttribute("aria-pressed", b.value === l ? "true" : "false"); });
    var dr = document.getElementById("g-draft"); if (dr) dr.hidden = !(l !== "en" && I18N.review[l] !== "reviewed");
    root.querySelectorAll(".g-item").forEach(function (li) {
      var c = byId[li.id]; if (!c) return;
      var it = itemText(c);
      li.querySelector(".g-q").textContent = it.q;
      var a = li.querySelector(".g-a-text");
      if (a) { a.textContent = ""; it.a.forEach(function (p) { var e = document.createElement("p"); termify(e, p); a.appendChild(e); }); }
      li.querySelectorAll(".g-links a").forEach(tipLink);
      var st = li.querySelector(".g-status span"); if (st) st.textContent = statusText(c.s);
      li.querySelectorAll(".g-labels abbr").forEach(function (ab) { var m = labelText(ab.getAttribute("data-l")); ab.textContent = m[0]; ab.title = m[1]; });
    });
    root.querySelectorAll(".g-group h2[data-g]").forEach(function (h) { var g = (I18N.groups[l] || {})[h.getAttribute("data-g")]; h.textContent = g && allowed(l) ? g : h.getAttribute("data-en"); });
    root.querySelectorAll(".g-legend li").forEach(function (li) { var m = labelText(li.getAttribute("data-l")); li.querySelector("b").textContent = m[0]; li.querySelector("span").textContent = m[1]; });
    if (save) { try { localStorage.setItem("krios-guide-lang", l); } catch (e) {} }
    if (lastQ) render(lastQ);
  }

  /* ---------- section names: kept in English, explained on hover, focus or tap (director decision Oct 23) ---------- */
  function terms() { return LANG !== "en" && allowed(LANG) && I18N.terms ? I18N.terms[LANG] : null; }
  function tipSpan(text) {
    var t = document.createElement("span"); t.className = "g-tip"; t.lang = LANG;
    var sr = document.createElement("span"); sr.className = "g-sr"; sr.textContent = ", ";
    t.appendChild(sr); t.appendChild(document.createTextNode(text)); return t;
  }
  function termify(parent, text) {
    var map = terms();
    if (!map) { parent.textContent = text; return; }
    var keys = Object.keys(map).filter(function (k) { return k.length < 16; }).sort(function (a, b) { return b.length - a.length; });
    var re = new RegExp("(^|[^A-Za-z])(" + keys.map(function (k) { return k.replace(/[.*+?^${}()|[\]\\&]/g, "\\$&"); }).join("|") + ")(?![A-Za-z])", "g");
    var last = 0, m;
    while ((m = re.exec(text))) {
      var start = m.index + m[1].length;
      parent.appendChild(document.createTextNode(text.slice(last, start)));
      var s = document.createElement("span"); s.className = "g-term"; s.lang = "en"; s.tabIndex = 0;
      s.appendChild(document.createTextNode(m[2])); s.appendChild(tipSpan(map[m[2]])); parent.appendChild(s);
      last = start + m[2].length;
    }
    parent.appendChild(document.createTextNode(text.slice(last)));
  }
  function tipLink(a) {
    var old = a.querySelector(".g-tip"); if (old) old.remove();
    a.classList.remove("g-has-tip"); a.removeAttribute("lang");
    var map = terms(), label = (a.firstChild && a.firstChild.nodeType === 3) ? a.firstChild.nodeValue : a.textContent;
    if (map && map[label]) { a.classList.add("g-has-tip"); a.firstChild.nodeValue = label; a.appendChild(tipSpan(map[label])); }
  }
  document.addEventListener("keydown", function (ev) {   /* WCAG 1.4.13: Escape dismisses the explanation */
    if (ev.key !== "Escape") return;
    document.querySelectorAll(".g-term:hover,.g-has-tip:hover,.g-term:focus,.g-has-tip:focus").forEach(function (n) { n.classList.add("g-hide"); });
  });
  /* placement: above by default; below when the term sits on the first line of its block (so the line above, e.g. the
     attribution, stays readable) or when there is no room above; shifted sideways to stay inside the viewport */
  function placeTip(n) {
    var tip = n.querySelector(".g-tip"); if (!tip) return;
    n.classList.remove("g-tip-below"); n.style.removeProperty("--tip-dx");
    var r = n.getBoundingClientRect(), blk = n.closest("p,li") || n.parentNode, br = blk.getBoundingClientRect();
    var lh = parseFloat(getComputedStyle(blk).lineHeight) || r.height;
    var t = tip.getBoundingClientRect();
    if (r.top - br.top < lh * 0.8 || t.top < 8) n.classList.add("g-tip-below");
    t = tip.getBoundingClientRect();
    var dx = 0, vw = document.documentElement.clientWidth;
    if (t.right > vw - 8) dx = vw - 8 - t.right;
    if (t.left + dx < 8) dx = 8 - t.left;
    if (dx) n.style.setProperty("--tip-dx", Math.round(dx) + "px");
  }
  ["mouseover", "focusin"].forEach(function (t) { document.addEventListener(t, function (ev) { var n = ev.target.closest && ev.target.closest(".g-term,.g-has-tip"); if (n) requestAnimationFrame(function () { placeTip(n); }); }); });
  ["mouseout", "focusout"].forEach(function (t) { document.addEventListener(t, function (ev) { var n = ev.target.closest && ev.target.closest(".g-hide"); if (n) n.classList.remove("g-hide"); }); });

  /* ---------- rendering ---------- */
  var out, lastQ = "", byId = {};
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function linkList(items, ext) {
    var ul = el("ul", "g-links");
    items.forEach(function (pair) {
      var li = el("li"), a = el("a", null, pair[0]); a.href = pair[1]; tipLink(a);
      if (ext) { a.rel = "noopener"; a.target = "_blank"; }
      li.appendChild(a); ul.appendChild(li);
    });
    return ul;
  }
  function chipList(ls) {
    if (!ls || !ls.length) return null;
    var ul = el("ul", "g-labels");
    ls.forEach(function (l) { var m = labelText(l), li = el("li"), ab = el("abbr", null, m[0]); ab.title = m[1]; li.appendChild(ab); ul.appendChild(li); });
    return ul;
  }
  function excerpt(text, terms) {
    var f = fold(text), pos = -1;
    terms.some(function (t) { pos = f.indexOf(t); return pos >= 0; });
    var start = Math.max(0, (pos < 0 ? 0 : pos) - 90);
    var s = text.slice(start, start + 320);
    return (start > 0 ? "… " : "") + s.replace(/\s+\S*$/, "") + (start + 320 < text.length ? " …" : "");
  }
  function render(q) {
    lastQ = q; out.textContent = "";
    var r = search(q), terms = queryTerms(q).terms;
    if (!r.ok) { notCovered(q); return; }
    var best = r.res[0].d, card = el("section", "g-result");
    card.appendChild(el("p", "g-kicker", T("best")));
    if (best.kind === "c") {
      var c = best.ref, it = itemText(c);
      card.appendChild(el("h2", "g-r-q", it.q));
      var st = el("p", "g-status g-" + c.s); st.appendChild(el("span", null, statusText(c.s))); card.appendChild(st);
      var ch = chipList(c.l); if (ch) card.appendChild(ch);
      if (LANG !== "en" && !it.translated) card.appendChild(el("p", "g-only-en", T("only_en")));
      it.a.forEach(function (p) { var e = el("p"); termify(e, p); card.appendChild(e); });
      card.appendChild(el("h3", null, T("read"))); card.appendChild(linkList(c.read));
      if (c.src && c.src.length) { card.appendChild(el("h3", null, T("source"))); card.appendChild(linkList(c.src, true)); }
    } else {
      var p = best.ref;
      card.appendChild(el("h2", "g-r-q", p.h || p.t));
      var ch2 = chipList(p.l); if (ch2) card.appendChild(ch2);
      if (LANG !== "en") card.appendChild(el("p", "g-only-en", T("only_en")));
      card.appendChild(el("blockquote", "g-quote", excerpt(p.x, terms)));
      var a = el("a", "g-from", T("quote_from") + " " + p.t); a.href = p.u; card.appendChild(a);
    }
    out.appendChild(card);
    var seen = {}; seen[best.kind === "c" ? best.ref.id : best.ref.u] = 1;
    var more = r.res.slice(1).filter(function (x) {
      if (x.d.kind !== "p" || x.s < 1.5) return false;
      var key = x.d.ref.u.split("#")[0]; if (seen[key] || seen[x.d.ref.u]) return false; seen[key] = 1; return true;
    }).slice(0, 3);
    if (more.length) {
      var m = el("section", "g-more"); m.appendChild(el("h3", null, T("more")));
      m.appendChild(linkList(more.map(function (x) { return [x.d.ref.t + (x.d.ref.h && x.d.ref.h !== x.d.ref.t ? ": " + x.d.ref.h : ""), x.d.ref.u]; })));
      out.appendChild(m);
    }
    var gid = best.kind === "c" ? best.ref.g : null;
    var fol = IDX.curated.filter(function (c) { return c.s !== "routed" && (!gid || c.g === gid) && !(best.kind === "c" && c.id === best.ref.id); }).slice(0, 2);
    if (fol.length) {
      var f = el("section", "g-follow"); f.appendChild(el("h3", null, T("follow")));
      fol.forEach(function (c) { var b = el("button", "g-chip", itemText(c).q); b.type = "button"; b.addEventListener("click", function () { ask(itemText(c).q); }); f.appendChild(b); });
      out.appendChild(f);
    }
  }
  function notCovered(q) {
    var s = el("section", "g-result g-nc");
    s.appendChild(el("h2", "g-r-q", T("nc_h")));
    s.appendChild(el("p", null, T("nc_p")));
    var films = el("p"); var a = el("a", null, T("foot_films")); a.href = "/films/"; films.appendChild(a); s.appendChild(films);
    var box = el("div", "g-suggest");
    if (CFG.suggest_url) {
      box.appendChild(el("p", "g-suggest-what", T("sg_what")));
      var qp = el("p", "g-suggest-q", q); box.appendChild(qp);
      var b = el("button", "g-btn g-btn-quiet", T("sg_btn")); b.type = "button";
      b.addEventListener("click", function () { suggest(q, b, box); });
      box.appendChild(b);
    } else {
      box.appendChild(el("p", "g-suggest-off", T("sg_off")));
    }
    s.appendChild(box);
    out.appendChild(s);
  }
  function scrub(t) {
    return t.replace(/[\w.+-]+@[\w-]+\.[\w.]+/g, "[email removed]").replace(/\+?\d[\d\s().-]{7,}\d/g, "[number removed]").slice(0, 300);
  }
  function suggest(q, btn, box) {
    btn.disabled = true;
    var body = JSON.stringify({ question: scrub(q), lang: LANG, day: new Date().toISOString().slice(0, 10) });
    fetch(CFG.suggest_url, { method: "POST", headers: { "Content-Type": "application/json" }, body: body, credentials: "omit", referrerPolicy: "no-referrer" })
      .then(function (r) { if (!r.ok) throw 0; box.textContent = ""; box.appendChild(el("p", "g-suggest-ok", T("sg_sent"))); })
      .catch(function () { btn.disabled = false; box.appendChild(el("p", "g-suggest-err", T("sg_fail"))); });
  }
  function ask(q) {
    var inp = document.getElementById("g-ask-input"); inp.value = q; render(q);
    var h = out.querySelector(".g-r-q"); if (h) { h.tabIndex = -1; h.focus(); }
  }

  /* ---------- boot ---------- */
  Promise.all([fetch("/data/guide_index.json").then(function (r) { return r.json(); }),
               fetch("/data/guide_client.json").then(function (r) { return r.json(); })])
    .then(function (v) {
      IDX = v[0]; I18N = v[1];
      IDX.curated.forEach(function (c) { byId[c.id] = c; });
      indexDocs();
      out = document.getElementById("g-results");
      var form = document.getElementById("g-ask");
      form.hidden = false;
      form.addEventListener("submit", function (ev) {
        ev.preventDefault(); var q = document.getElementById("g-ask-input").value.trim(); if (q) ask(q);
      });
      var langs = root.querySelector(".g-langs");
      langs.querySelectorAll("button").forEach(function (b) {
        if (!allowed(b.value)) { b.hidden = true; return; }
        b.addEventListener("click", function () {
          setLang(b.value, true);
          try { var u = new URL(location.href); if (b.value === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", b.value); history.replaceState(null, "", u); } catch (e) {}
        });
      });
      langs.hidden = langs.querySelectorAll("button:not([hidden])").length < 2;
      var want = new URLSearchParams(location.search).get("lang");
      if (!want) { try { want = localStorage.getItem("krios-guide-lang"); } catch (e) {} }
      setLang(want || "en", false);
      window.__kriosGuideSearch = search; /* for automated tests only */
    })
    .catch(function () { /* the curated list keeps working without the search box */ });
})();
