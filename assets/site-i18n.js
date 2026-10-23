/* KRIOS site-wide language layer (English, Greek, Spanish). Loaded by site-nav.js on every page.
   - Same choice everywhere: localStorage "krios-guide-lang" and ?lang= (shared with the Sacred page and the Page Guide).
   - English text is the source. For Greek or Spanish it loads /data/i18n/site.json (menu, footer) and the page's own
     table /data/i18n/pages/<page>.json, then swaps matching text in place. Anything without a translation stays English.
   - Languages appear only when data/i18n/site.json "review" marks them "reviewed" or "published_draft"; a draft notice
     shows until a named reviewer signs the language off.
   - Section labels (Films, Sacred, Articles, Q&A, Quizzes, Sacred Days ...) stay in English with a hover, focus or tap
     explanation (director decision, Oct 23, 2026). Pages with their own picker (Sacred, Page Guide) keep it; this script
     then only follows their choice for the menu and footer. No tracking, no outside services. */
(function () {
  var KEY = "krios-guide-lang", LANGS = ["en", "el", "es"], NAMES = { en: "English", el: "Ελληνικά", es: "Español" };
  var ownPicker = !!(document.getElementById("s-i18n") || document.querySelector(".g-langs"));
  var path = location.pathname.replace(/index\.html$/, "");
  var page = path.replace(/^\/|\/$/g, "").replace(/\//g, "__") || "home";
  var SITE = null, PAGE = null, LANG = "en", applying = false;
  var origText = new Map(), origAttr = new Map(), done = new WeakSet();
  function norm(s) { return (s || "").replace(/\s+/g, " ").trim(); }
  function getJSON(u) { return fetch(u, { credentials: "same-origin" }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }
  function allowed(l) { var r = (SITE && SITE.review) || {}; return l === "en" || r[l] === "reviewed" || r[l] === "published_draft"; }

  function table() {
    var t = {}, a = {};
    [SITE, PAGE].forEach(function (d) {
      if (!d) return;
      (d.strings || []).forEach(function (s) { if (s[LANG]) t[norm(s.en)] = s; });
      (d.attrs || []).forEach(function (s) { if (s[LANG]) a[norm(s.en)] = s[LANG]; });
    });
    return { t: t, a: a };
  }
  function textNodes(el) {
    var out = [], w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    while (w.nextNode()) { if (norm(w.currentNode.nodeValue)) out.push(w.currentNode); }
    return out;
  }
  function setText(node, v) { if (!origText.has(node)) origText.set(node, node.nodeValue); node.nodeValue = v; }
  function apply(el, entry) {
    var nodes = textNodes(el); if (!nodes.length) return false;
    var htmlv = entry[LANG + "_html"];
    if (htmlv) {
      var tpl = document.createElement("template"); tpl.innerHTML = htmlv;
      var tn = textNodes(tpl.content);
      if (tn.length !== nodes.length) return false;            /* structure differs: keep English rather than break links */
      nodes.forEach(function (n, i) { setText(n, (/^\s/.test(n.nodeValue) ? " " : "") + norm(tn[i].nodeValue) + (/\s$/.test(n.nodeValue) ? " " : "")); });
    } else {
      setText(nodes[0], entry[LANG]); for (var i = 1; i < nodes.length; i++) setText(nodes[i], "");
    }
    return true;
  }
  function tip(a, text) {
    if (a.querySelector(".g-tip")) return;
    var t = document.createElement("span"); t.className = "g-tip"; t.lang = LANG; t.setAttribute("data-k-tip", "");
    var sr = document.createElement("span"); sr.className = "g-sr"; sr.textContent = ", ";
    t.appendChild(sr); t.appendChild(document.createTextNode(text)); a.classList.add("g-has-tip"); a.appendChild(t);
  }
  function translate(root) {
    if (LANG === "en") return;
    var T = table(), terms = (SITE && SITE.terms && SITE.terms[LANG]) || {};
    var skipMain = ownPicker;                                  /* Sacred and Guide translate their own content */
    var els = (root || document.body).querySelectorAll("*");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (done.has(el) || /^(SCRIPT|STYLE|NOSCRIPT|SVG|TEMPLATE|CODE)$/.test(el.tagName) || el.closest("[data-k-tip],.k-langbar,.g-tip")) continue;
      if (skipMain && el.closest("main")) continue;
      ["alt", "aria-label", "placeholder", "title"].forEach(function (k) {
        var v = el.getAttribute(k); if (!v) return; var tr = T.a[norm(v)];
        if (tr) { if (!origAttr.has(el)) origAttr.set(el, {}); var o = origAttr.get(el); if (!(k in o)) o[k] = v; el.setAttribute(k, tr); }
      });
      var key = norm(el.textContent);
      if (!key) continue;
      if (el.tagName === "A" && terms[key] && !el.children.length) { tip(el, terms[key]); done.add(el); continue; }
      var entry = T.t[key];
      if (entry && apply(el, entry)) { done.add(el); el.querySelectorAll("*").forEach(function (c) { done.add(c); }); }
    }
  }
  function restore() {
    origText.forEach(function (v, n) { n.nodeValue = v; }); origText.clear();
    origAttr.forEach(function (o, el) { for (var k in o) el.setAttribute(k, o[k]); }); origAttr.clear();
    document.querySelectorAll("[data-k-tip]").forEach(function (t) { var a = t.parentNode; t.remove(); if (a) a.classList.remove("g-has-tip"); });
    done = new WeakSet();
  }
  function drafts() {
    var dr = document.getElementById("k-draft"); if (!dr) return;
    var untranslated = LANG !== "en" && !ownPicker && !(PAGE && PAGE._status !== "source");
    var show = LANG !== "en" && SITE && SITE.review && (SITE.review[LANG] !== "reviewed" || untranslated);
    dr.hidden = !show; if (show) { dr.textContent = untranslated ? SITE.untranslated[LANG] : SITE.draft[LANG]; dr.lang = LANG; }
  }
  function setLang(l, save) {
    if (LANGS.indexOf(l) < 0 || !allowed(l)) l = "en";
    applying = true;
    restore(); LANG = l;
    if (!ownPicker) document.documentElement.lang = l;
    var load = l === "en" || ownPicker ? Promise.resolve(null) : (PAGE ? Promise.resolve(PAGE) : ((SITE.pages || []).indexOf(page) < 0 ? Promise.resolve(null) : getJSON("/data/i18n/pages/" + page + ".json")));
    return load.then(function (p) {
      if (p) PAGE = p;
      translate(); drafts();
      document.querySelectorAll('input[name="k-lang"]').forEach(function (r) { r.checked = r.value === l; });
      if (save) { try { localStorage.setItem(KEY, l); } catch (e) {} try { var u = new URL(location.href); if (l === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", l); history.replaceState(null, "", u); } catch (e) {} }
      applying = false;
    });
  }
  function picker() {
    var hdr = document.querySelector("header"); if (!hdr || ownPicker) return;
    var langs = LANGS.filter(allowed); if (langs.length < 2) return;
    var bar = document.createElement("div"); bar.className = "k-langbar";
    var fs = document.createElement("fieldset"); fs.className = "k-lang";
    var lg = document.createElement("legend"); lg.className = "k-sr"; lg.textContent = "Language"; fs.appendChild(lg);
    langs.forEach(function (l) {
      var lab = document.createElement("label"); lab.lang = l;
      var r = document.createElement("input"); r.type = "radio"; r.name = "k-lang"; r.value = l; r.checked = l === "en";
      r.addEventListener("change", function () { if (r.checked) setLang(l, true); });
      var s = document.createElement("span"); s.textContent = NAMES[l];
      lab.appendChild(r); lab.appendChild(s); fs.appendChild(lab);
    });
    var dr = document.createElement("p"); dr.className = "k-draft"; dr.id = "k-draft"; dr.hidden = true;
    bar.appendChild(fs); bar.appendChild(dr);
    hdr.insertAdjacentElement("afterend", bar);
  }
  function css() {
    var s = document.createElement("style");
    s.textContent = ".k-langbar{max-width:1200px;margin:0 auto;padding:8px 20px 0;box-sizing:border-box;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;justify-content:flex-end;font-family:Inter,system-ui,sans-serif}"
      + ".k-lang{display:inline-flex;border:1px solid rgba(192,160,92,.6);border-radius:999px;padding:3px;margin:0;gap:2px}"
      + ".k-lang label{position:relative;cursor:pointer}.k-lang input{position:absolute;opacity:0;width:1px;height:1px}"
      + ".k-lang span{display:inline-block;min-height:40px;line-height:40px;padding:0 15px;border-radius:999px;font-size:.95rem;color:inherit;opacity:.85}"
      + ".k-lang input:checked+span{background:#c0a05c;color:#14110a;font-weight:600;opacity:1}"
      + ".k-lang input:focus-visible+span{outline:3px solid #1a4a73;outline-offset:2px}"
      + ".k-draft{margin:0;font-size:.9rem;background:#fff3cd;color:#5c4400;border-left:3px solid #8a6a1f;padding:6px 10px}"
      + ".k-sr,.g-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}"
      + "a.g-has-tip{position:relative}[data-k-tip]{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}"
      + ".g-has-tip:hover>[data-k-tip],.g-has-tip:focus>[data-k-tip]{width:max-content;max-width:min(80vw,320px);height:auto;overflow:visible;clip-path:none;white-space:normal;left:0;top:100%;margin-top:6px;z-index:50;background:#1b1b1b;color:#fff;font-size:.875rem;line-height:1.35;font-weight:400;font-style:normal;letter-spacing:normal;text-transform:none;padding:5px 9px;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.3)}"
      + ".g-hide>[data-k-tip]{width:1px!important;height:1px!important;overflow:hidden!important;clip-path:inset(50%)!important;padding:0!important}@media print{.k-langbar,[data-k-tip]{display:none}}";
    document.head.appendChild(s);
  }
  getJSON("/data/i18n/site.json").then(function (s) {
    SITE = s; if (!SITE) return;
    css(); picker();
    var want = new URLSearchParams(location.search).get("lang");
    if (!want) { try { want = localStorage.getItem(KEY); } catch (e) {} }
    if (ownPicker) {
      /* follow the page's own picker: re-apply the menu and footer whenever <html lang> changes */
      new MutationObserver(function () { var l = document.documentElement.lang; if (l !== LANG && !applying) setLang(l, false); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
      setLang(document.documentElement.lang || "en", false);
    } else if (want && want !== "en") setLang(want, false);
    /* text added later (quizzes, interactive parts) is translated as it appears */
    new MutationObserver(function (ms) { if (LANG === "en" || applying) return; ms.forEach(function (m) { m.addedNodes.forEach(function (n) { if (n.nodeType === 1 && !n.closest(".k-langbar")) translate(n.parentNode || n); }); }); })
      .observe(document.body, { childList: true, subtree: true });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") document.querySelectorAll(".g-has-tip:hover,.g-has-tip:focus").forEach(function (n) { n.classList.add("g-hide"); }); });
  });
})();
