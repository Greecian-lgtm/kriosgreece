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
  try { if (localStorage.getItem("krios-theme") === "dark") document.documentElement.setAttribute("data-theme", "dark"); } catch (e) {}
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
      nodes.forEach(function (n, i) { var v = n.nodeValue; setText(n, (v.match(/^\s+/) || [""])[0] + norm(tn[i].nodeValue) + (v.match(/\s+$/) || [""])[0]); });
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
      if (done.has(el) || /^(SCRIPT|STYLE|NOSCRIPT|SVG|TEMPLATE|CODE)$/.test(el.tagName) || el.closest("[data-k-tip],.k-langbar,.k-dock,.k-backbar,.g-tip")) continue;
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
      translate(); drafts(); askText(); uiText();
      document.querySelectorAll('input[name="k-lang"]').forEach(function (r) { r.checked = r.value === l; });
      if (save) { try { localStorage.setItem(KEY, l); } catch (e) {} try { var u = new URL(location.href); if (l === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", l); history.replaceState(null, "", u); } catch (e) {} }
      applying = false;
    });
  }
  var ASK = { en: ["Ask KRIOS", "Ask about Greece, the films or KRIOS", "Ask", "Answers come only from published KRIOS pages. Your question stays on this device.", "Close"],
    el: ["Ρωτήστε το KRIOS", "Ρωτήστε για την Ελλάδα, τις ταινίες ή το KRIOS", "Ερώτηση", "Οι απαντήσεις προέρχονται μόνο από δημοσιευμένες σελίδες του KRIOS. Η ερώτησή σας μένει σε αυτή τη συσκευή.", "Κλείσιμο"],
    es: ["Pregunte a KRIOS", "Pregunte sobre Grecia, las películas o KRIOS", "Preguntar", "Las respuestas provienen solo de páginas publicadas de KRIOS. Su pregunta se queda en este dispositivo.", "Cerrar"] };
  var UI = { en: { dark: "Dark mode", light: "Light mode", back: "Back" },
    el: { dark: "Σκούρο θέμα", light: "Ανοιχτό θέμα", back: "Πίσω" },
    es: { dark: "Modo oscuro", light: "Modo claro", back: "Volver" } };
  function isDark() { return document.documentElement.getAttribute("data-theme") === "dark"; }
  function uiText() {
    var u = UI[LANG] || UI.en, tb = document.getElementById("k-theme"), bk = document.getElementById("k-back");
    if (tb) { tb.setAttribute("aria-label", u.dark); tb.setAttribute("aria-pressed", String(isDark())); tb.title = isDark() ? u.light : u.dark; tb.lang = LANG; }
    if (bk) { bk.querySelector("span").textContent = u.back; bk.lang = LANG; }
  }
  function setTheme(dark) {
    if (dark) document.documentElement.setAttribute("data-theme", "dark"); else document.documentElement.removeAttribute("data-theme");
    try { localStorage.setItem("krios-theme", dark ? "dark" : "light"); } catch (e) {}
    var mc = document.querySelector('meta[name="color-scheme"]'); if (mc) mc.content = dark ? "dark" : "light";
    uiText();
  }
  function backHref() {
    var parts = location.pathname.replace(/index\.html$/, "").split("/").filter(Boolean);
    parts.pop(); return "/" + (parts.length ? parts.join("/") + "/" : "");
  }
  function backLink(after) {
    if (location.pathname === "/" || location.pathname === "/index.html") return;
    var wrap = document.createElement("div"); wrap.className = "k-backbar";
    var a = document.createElement("a"); a.id = "k-back"; a.className = "k-back"; a.href = backHref();
    a.innerHTML = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg><span>Back</span>';
    a.addEventListener("click", function (ev) {
      var same = false; try { same = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
      if (same && history.length > 1) { ev.preventDefault(); history.back(); }
    });
    wrap.appendChild(a); after.insertAdjacentElement("afterend", wrap);
    var bg = getComputedStyle(document.body).backgroundColor.match(/\d+(\.\d+)?/g);
    if (bg && bg.length >= 3 && (0.2126 * bg[0] + 0.7152 * bg[1] + 0.0722 * bg[2]) / 255 < 0.4 && (bg.length < 4 || +bg[3] > 0)) a.classList.add("on-dark");
  }
  function askText() {
    var t = ASK[LANG] || ASK.en, d = document.getElementById("k-dock"); if (!d) return;
    var set = function (sel, v, attr) { var e = d.querySelector(sel); if (e) { if (attr) e.setAttribute(attr, v); else e.textContent = v; } };
    set(".k-ask-btn span", t[0]); set(".k-ask-btn", t[0], "aria-label"); set("label[for=k-ask-q]", t[1]); set(".k-ask-go", t[2]); set(".k-ask-note", t[3]); set(".k-ask-x", t[4], "aria-label");
    d.querySelectorAll("[data-k-l]").forEach(function (e) { e.lang = LANG; });
  }
  function picker() {
    var hdr = document.querySelector("header"); if (!hdr) return;
    var onGuide = !!document.querySelector(".g-page");
    var langs = LANGS.filter(allowed);
    var after = hdr;
    if (!ownPicker) {                                           /* draft notice stays under the header */
      var bar = document.createElement("div"); bar.className = "k-langbar";
      var dr = document.createElement("p"); dr.className = "k-draft"; dr.id = "k-draft"; dr.hidden = true;
      bar.appendChild(dr); hdr.insertAdjacentElement("afterend", bar); after = bar;
    }
    backLink(after);
    var dock = document.createElement("div"); dock.className = "k-dock"; dock.id = "k-dock";
    var tb = document.createElement("button"); tb.type = "button"; tb.id = "k-theme"; tb.className = "k-theme";
    tb.innerHTML = '<svg class="k-moon" aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7Z"/></svg><svg class="k-sun" aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="4.2" fill="currentColor"/><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg>';
    tb.addEventListener("click", function () { setTheme(!isDark()); });
    if (onGuide) { dock.appendChild(tb); document.body.appendChild(dock); uiText(); return; }   /* the Guide page is the bot itself */
    if (!ownPicker && langs.length > 1) {
      var fs = document.createElement("fieldset"); fs.className = "k-lang";
      var lg = document.createElement("legend"); lg.className = "k-sr"; lg.textContent = "Language · Γλώσσα · Idioma"; fs.appendChild(lg);
      var SHORT = { en: "EN", el: "ΕΛ", es: "ES" };
      langs.forEach(function (l) {
        var lab = document.createElement("label"); lab.lang = l; lab.title = NAMES[l];
        var r = document.createElement("input"); r.type = "radio"; r.name = "k-lang"; r.value = l; r.checked = l === "en"; r.setAttribute("aria-label", NAMES[l]);
        r.addEventListener("change", function () { if (r.checked) setLang(l, true); });
        var s = document.createElement("span"); s.setAttribute("aria-hidden", "true"); s.textContent = SHORT[l];
        lab.appendChild(r); lab.appendChild(s); fs.appendChild(lab);
      });
      dock.appendChild(fs);
    }
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "k-ask-btn"; btn.setAttribute("aria-expanded", "false"); btn.setAttribute("aria-controls", "k-ask"); btn.setAttribute("data-k-l", "");
    btn.innerHTML = '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Zm3 6.5a1.5 1.5 0 1 0 0-.01Zm5 0a1.5 1.5 0 1 0 0-.01Zm5 0a1.5 1.5 0 1 0 0-.01Z"/></svg><span></span>';
    var panel = document.createElement("form"); panel.className = "k-ask"; panel.id = "k-ask"; panel.hidden = true; panel.setAttribute("data-k-l", "");
    panel.innerHTML = '<button type="button" class="k-ask-x">×</button><label for="k-ask-q"></label><div class="k-ask-row"><input id="k-ask-q" type="text" autocomplete="off" maxlength="200"><button type="submit" class="k-ask-go"></button></div><p class="k-ask-note"></p>';
    function toggle(open) { panel.hidden = !open; btn.setAttribute("aria-expanded", String(open)); if (open) panel.querySelector("input").focus(); else btn.focus(); }
    btn.addEventListener("click", function () { toggle(panel.hidden); });
    panel.querySelector(".k-ask-x").addEventListener("click", function () { toggle(false); });
    panel.addEventListener("keydown", function (ev) { if (ev.key === "Escape") toggle(false); });
    panel.addEventListener("submit", function (ev) {
      ev.preventDefault(); var q = panel.querySelector("input").value.trim(); if (!q) return;
      /* the question goes to the Guide through this browser's session storage, never in the address or to a server */
      try { sessionStorage.setItem("krios-guide-q", q); } catch (e) {}
      location.href = "/guide/" + (LANG !== "en" ? "?lang=" + LANG : "");
    });
    dock.appendChild(panel); dock.appendChild(tb); dock.appendChild(btn);
    document.body.appendChild(dock); askText(); uiText();
  }
  function css() {
    var s = document.createElement("style");
    s.textContent = ".k-langbar{max-width:1200px;margin:0 auto;padding:8px 20px 0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}.k-langbar:has(.k-draft[hidden]){display:none}"
      + ".k-dock{position:fixed;right:16px;bottom:16px;z-index:60;display:flex;align-items:center;gap:8px;font-family:Inter,system-ui,sans-serif}"
      + ".k-lang{display:inline-flex;background:#0b1424;border:1px solid #c0a05c;border-radius:999px;padding:3px;margin:0;gap:2px;box-shadow:0 4px 14px rgba(0,0,0,.28)}"
      + ".k-lang label{position:relative;cursor:pointer}.k-lang input{position:absolute;opacity:0;width:1px;height:1px}"
      + ".k-lang span{display:inline-block;min-width:44px;min-height:44px;line-height:44px;text-align:center;border-radius:999px;font-size:.9rem;font-weight:600;color:#f1e8d2}"
      + ".k-lang input:checked+span{background:#c0a05c;color:#14110a}"
      + ".k-lang input:focus-visible+span,.k-ask-btn:focus-visible,.k-ask button:focus-visible,.k-ask input:focus-visible{outline:3px solid #8fb3d9;outline-offset:2px}"
      + ".k-ask-btn{display:inline-flex;align-items:center;gap:8px;min-height:50px;padding:0 18px;border-radius:999px;border:1px solid #c0a05c;background:#c0a05c;color:#14110a;font:600 .95rem Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.28)}"
      + ".k-ask{position:absolute;right:0;bottom:62px;width:min(340px,calc(100vw - 32px));box-sizing:border-box;background:#0b1424;color:#f1e8d2;border:1px solid #c0a05c;border-radius:12px;padding:16px 16px 12px;box-shadow:0 8px 28px rgba(0,0,0,.35)}"
      + ".k-ask label{display:block;font-size:.95rem;margin:0 28px 8px 0;line-height:1.35}.k-ask-row{display:flex;gap:6px}"
      + ".k-ask input{flex:1;min-width:0;min-height:44px;padding:0 10px;border-radius:6px;border:1px solid #8a7a55;background:#fff;color:#14110a;font-size:1rem}"
      + ".k-ask-go{min-height:44px;padding:0 14px;border-radius:6px;border:0;background:#c0a05c;color:#14110a;font-weight:600;cursor:pointer}"
      + ".k-ask-note{margin:8px 0 0;font-size:.8rem;opacity:.85;line-height:1.35}.k-ask-x{position:absolute;top:6px;right:6px;width:36px;height:36px;border:0;background:none;color:#f1e8d2;font-size:1.5rem;cursor:pointer}"
      + "@media (max-width:600px){.k-dock{right:12px;bottom:12px}.k-ask-btn span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}.k-ask-btn{padding:0 14px}.k-lang span{min-width:40px}}"
      + ".k-theme{display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:50%;border:1px solid #c0a05c;background:#0b1424;color:#f1e8d2;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.28);padding:0}"
      + ".k-theme .k-sun{display:none}html[data-theme=dark] .k-theme .k-sun{display:block}html[data-theme=dark] .k-theme .k-moon{display:none}html[data-theme=dark] .k-theme{background:#f1e8d2;color:#0b1424}"
      + ".k-theme:focus-visible,.k-back:focus-visible{outline:3px solid #8fb3d9;outline-offset:2px}"
      + ".k-backbar{max-width:1200px;margin:0 auto;padding:6px 20px 0;box-sizing:border-box}"
      + ".k-back{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 10px 0 4px;font:500 1rem Inter,system-ui,sans-serif;color:#14213a;text-decoration:none;border-radius:4px}"
      + ".k-back:hover span{text-decoration:underline;text-underline-offset:3px}.k-back.on-dark,html[data-theme=dark] .k-back{color:#f1e8d2}"
      + "@media (max-width:600px){.k-theme{width:46px;height:46px}.k-backbar{padding:4px 12px 0}}"
      + ".k-draft{margin:0;font-size:.9rem;background:#fff3cd;color:#5c4400;border-left:3px solid #8a6a1f;padding:6px 10px}"
      + ".k-sr,.g-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}"
      + "a.g-has-tip{position:relative}[data-k-tip]{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}"
      + ".g-has-tip:hover>[data-k-tip],.g-has-tip:focus>[data-k-tip]{width:max-content;max-width:min(80vw,320px);height:auto;overflow:visible;clip-path:none;white-space:normal;left:0;top:100%;margin-top:6px;z-index:50;background:#1b1b1b;color:#fff;font-size:.875rem;line-height:1.35;font-weight:400;font-style:normal;letter-spacing:normal;text-transform:none;padding:5px 9px;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.3)}"
      + ".g-hide>[data-k-tip]{width:1px!important;height:1px!important;overflow:hidden!important;clip-path:inset(50%)!important;padding:0!important}@media print{.k-langbar,.k-dock,.k-backbar,[data-k-tip]{display:none}}";
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
    new MutationObserver(function (ms) { if (LANG === "en" || applying) return; ms.forEach(function (m) { m.addedNodes.forEach(function (n) { if (n.nodeType === 1 && !n.closest(".k-langbar,.k-dock,.k-backbar")) translate(n.parentNode || n); }); }); })
      .observe(document.body, { childList: true, subtree: true });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") document.querySelectorAll(".g-has-tip:hover,.g-has-tip:focus").forEach(function (n) { n.classList.add("g-hide"); }); });
  });
})();
