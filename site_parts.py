# Shared pieces for every generated KRIOS page: head, header (with the accessible mobile menu) and footer.
import html

YT = "https://www.youtube.com/@KriosGreece"
SUB = YT + "?sub_confirmation=1"
NAV = [("/films/", "Films"), ("/sacred-days/", "Sacred Days"), ("/blog/", "Articles"), ("/answers/", "Q&amp;A"), ("/tools/", "Quizzes")]
DEDICATION_FOOTER = "For my father, Peter (Πέτρος)."
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">')


def menu_button(menu_id="site-menu"):
    return (f'<button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="{menu_id}">'
            '<span class="bars" aria-hidden="true"></span><span>Menu</span></button>')


def nav_links(active="", menu_id="site-menu", cls="nav-links"):
    cur = ' aria-current="page"'
    a = "".join(f'<a href="{h}"{cur if t == active else ""}>{t}</a>' for h, t in NAV)
    return f'<div class="{cls}" id="{menu_id}">{a}</div>'


def header(active=""):
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top">\n  <div class="wrap">\n'
            '    <a class="brand" href="/"><b>KRIOS</b><span>Greek cultural preservation</span></a>\n'
            f'    <nav class="nav" aria-label="Main">{menu_button()}{nav_links(active)}'
            f'<a class="btn btn-gold" href="{SUB}" rel="noopener">Subscribe<span class="m-hide-sm">&nbsp;on YouTube</span></a></nav>\n'
            '  </div>\n</header>')


def footer():
    return f'''<footer>
  <div class="wrap">
    <div>
      <b>KRIOS</b>
      <p>The living story of Greek civilization.<br>Preserve. Teach. Understand. Connect. Pass forward.</p>
    </div>
    <ul>
      <li><a href="/films/">Films</a></li>
      <li><a href="/sacred-days/">Sacred Days</a></li>
      <li><a href="/how-we-work/">How we work</a></li>
      <li><a href="/answers/">Q&amp;A</a></li>
    </ul>
    <ul>
      <li><a href="{YT}" rel="noopener">YouTube ↗</a></li>
      <li><a href="/blog/">Articles</a></li>
      <li><a href="/tools/">Quizzes</a></li>
      <li><a href="/legal/">Legal</a></li>
    </ul>
    <div class="dedic">
      <span>© 2026 KRIOS · kriosgreece.com</span>
      <i>{DEDICATION_FOOTER}</i>
    </div>
  </div>
</footer>'''


SCRIPTS = '''<script src="/assets/site-nav.js" defer></script>
<script>
(function(){
  var els=[].slice.call(document.querySelectorAll('.reveal'));
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){els.forEach(function(e){e.classList.add('in')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px',threshold:0.08});
  els.forEach(function(e){io.observe(e)});}
  var on=function(){document.body.classList.toggle('scrolled',window.scrollY>8)}; window.addEventListener('scroll',on,{passive:true}); on();
})();
</script>'''


def head(title, desc, canonical, extra=""):
    e = html.escape
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://kriosgreece.com{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="https://kriosgreece.com{canonical}">
<meta name="theme-color" content="#14213a">
<script>document.documentElement.classList.add("js")</script>
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{extra}
</head>'''
