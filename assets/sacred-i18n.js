/* KRIOS Sacred page: on-page language picker (English, Greek, Spanish), radio buttons, translates in place.
   Only languages present in #s-i18n are offered: the public build includes a language only after named human review.
   Section label "Sacred Days" stays in English with a hover, focus or tap explanation (director decision, Oct 23).
   Shares the visitor's choice with the Page Guide (localStorage "krios-guide-lang" and ?lang=). No tracking. */
(function () {
  var el = document.getElementById("s-i18n"); if (!el) return;
  var D; try { D = JSON.parse(el.textContent); } catch (e) { return; }
  var langs = Object.keys(D.ui); if (langs.length < 2) return;
  var LANG = "en";
  var origGuide = {};
  var LOC = { en: "en-US", es: "es-419", el: "el-GR" };

  function T(k) { var u = D.ui[LANG] || {}; return u[k] != null ? u[k] : D.ui.en[k]; }
  function tipSpan(text) {
    var t = document.createElement("span"); t.className = "g-tip"; t.lang = LANG;
    var sr = document.createElement("span"); sr.className = "g-sr"; sr.textContent = ", ";
    t.appendChild(sr); t.appendChild(document.createTextNode(text)); return t;
  }
  function termify(node, text) {
    var map = LANG !== "en" ? (D.terms[LANG] || {}) : null;
    node.textContent = "";
    if (!map || !map["Sacred Days"]) { node.textContent = text; return; }
    var parts = text.split("Sacred Days");
    parts.forEach(function (p, i) {
      node.appendChild(document.createTextNode(p));
      if (i < parts.length - 1) {
        var s = document.createElement("span"); s.className = "g-term"; s.lang = "en"; s.tabIndex = 0;
        s.appendChild(document.createTextNode("Sacred Days")); s.appendChild(tipSpan(map["Sacred Days"])); node.appendChild(s);
      }
    });
  }
  function tipLink(a, label) {
    var old = a.querySelector(".g-tip"); if (old) old.remove();
    a.classList.remove("g-has-tip"); a.textContent = label;
    var map = LANG !== "en" ? (D.terms[LANG] || {}) : null;
    if (map && map[label]) { a.classList.add("g-has-tip"); a.appendChild(tipSpan(map[label])); }
  }
  function fmt(iso, opts) { try { return new Intl.DateTimeFormat(LOC[LANG], Object.assign({ timeZone: "UTC" }, opts)).format(new Date(iso + "T12:00:00Z")); } catch (e) { return null; } }

  function setLang(l, save) {
    if (langs.indexOf(l) < 0) l = "en";
    LANG = l;
    document.documentElement.lang = l;
    document.querySelectorAll("[data-t]").forEach(function (n) {
      var k = n.getAttribute("data-t"), v = T(k); if (v == null) return;
      if (k === "c2_t" || k === "open_c2" || k === "page_note") termify(n, v); else n.textContent = v;
    });
    document.querySelectorAll("[data-talt]").forEach(function (n) { var v = T(n.getAttribute("data-talt")); if (v) n.alt = v; });
    document.querySelectorAll("[data-taria]").forEach(function (n) { var v = T(n.getAttribute("data-taria")); if (v) n.setAttribute("aria-label", v); });
    /* calendar rows: local month, day name and feast name; Greek name shown beside the Spanish or English name */
    document.querySelectorAll(".s-calnext li[data-date]").forEach(function (li) {
      var iso = li.getAttribute("data-date"), en = li.getAttribute("data-en");
      var m = fmt(iso, { month: "short" }), full = fmt(iso, { weekday: "long", year: "numeric", month: "long", day: "numeric" });
      var i = li.querySelector(".s-cd i"); if (i && m) i.textContent = m.replace(".", "");
      var sm = li.querySelector("small"); if (sm && full) sm.textContent = full;  /* Spanish keeps weekdays lowercase (RAE); Greek day names are capitalised by Intl */
      var fn = li.querySelector(".s-fn"), fel = li.querySelector(".s-fel");
      if (LANG === "el") { fn.textContent = fel.textContent; fn.lang = "el"; fel.hidden = true; }
      else { fn.textContent = LANG === "es" ? (D.feasts_es[en] || en) : en; fn.removeAttribute("lang"); fel.hidden = false; }
    });
    /* in-page Guide questions and answers (same reviewed drafts as the full Page Guide) */
    document.querySelectorAll("[data-gq]").forEach(function (n) {
      var id = n.getAttribute("data-gq"); if (!(id in origGuide)) origGuide[id] = { q: n.textContent, a: Array.prototype.map.call(document.querySelectorAll('[data-ga="' + id + '"] p'), function (p) { return p.textContent; }) };
      var tr = LANG !== "en" ? (D.items[id] || {})[LANG] : null;
      n.textContent = tr ? tr[0] : origGuide[id].q;
      var box = document.querySelector('[data-ga="' + id + '"]'); if (!box) return;
      box.textContent = "";
      (tr ? tr.slice(1) : origGuide[id].a).forEach(function (t) { var p = document.createElement("p"); termify(p, t); box.appendChild(p); });
    });
    document.querySelectorAll("[data-gs]").forEach(function (n) {
      if (!n.dataset.en) n.dataset.en = n.textContent;
      var m = LANG !== "en" ? D.status[LANG] : null; n.textContent = (m && m[n.getAttribute("data-gs")]) || n.dataset.en;
    });
    document.querySelectorAll("a[data-term]").forEach(function (a) { tipLink(a, a.getAttribute("data-term")); });
    var dr = document.getElementById("s-draft");
    if (dr) { var draft = l !== "en" && D.review[l] !== "reviewed"; dr.hidden = !draft; if (draft) { dr.textContent = D.draft[l]; dr.lang = l; } }
    document.querySelectorAll('input[name="s-lang"]').forEach(function (r) { r.checked = r.value === l; });
    if (save) { try { localStorage.setItem("krios-guide-lang", l); } catch (e) {} try { var u = new URL(location.href); if (l === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", l); history.replaceState(null, "", u); } catch (e) {} }
  }

  document.querySelectorAll('input[name="s-lang"]').forEach(function (r) { r.addEventListener("change", function () { if (r.checked) setLang(r.value, true); }); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") document.querySelectorAll(".g-term:hover,.g-has-tip:hover,.g-term:focus,.g-has-tip:focus").forEach(function (n) { n.classList.add("g-hide"); }); });
  ["mouseout", "focusout"].forEach(function (t) { document.addEventListener(t, function (ev) { var n = ev.target.closest && ev.target.closest(".g-hide"); if (n) n.classList.remove("g-hide"); }); });
  var want = new URLSearchParams(location.search).get("lang");
  if (!want) { try { want = localStorage.getItem("krios-guide-lang"); } catch (e) {} }
  if (want && want !== "en") setLang(want, false);
})();
