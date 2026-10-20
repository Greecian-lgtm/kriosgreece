// KRIOS site tests (Gate C plan, section 5). Needs: npm i playwright @axe-core/playwright
// Usage: node tests/site.test.mjs http://localhost:8000 [screenshot-dir]
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
const BASE = process.argv[2] || 'http://localhost:8000';
const SHOTS = process.argv[3] || '';
const PAGES = ['/', '/films/', '/sacred-days/', '/how-we-work/', '/blog/', '/answers/', '/tools/',
  '/blog/ep014-rebetiko.html', '/films/the-greek-dance/', '/films/the-greeks-who-left/', '/films/saint-demetrios/', '/tools/quiz-the-greeks-who-left.html', '/answers/is-sirtaki-a-traditional-greek-dance/', '/tools/quiz-bouboulina.html', '/answers/who-was-athanasios-diakos/', '/answers/who-was-theseus/', '/tools/quiz-ep001-achilles.html', '/sacred-days/saint-demetrios-name-day/', '/ohi-day/'];
const WIDTHS = [320, 390, 768, 1440];
const opts = { headless: true };
if (process.env.CHROMIUM_PATH) Object.assign(opts, { executablePath: process.env.CHROMIUM_PATH, args: ['--headless=new'], ignoreDefaultArgs: ['--headless=old'] });
const b = await chromium.launch(opts);
let fails = 0; const fail = (m) => { fails++; console.log('FAIL', m); };
for (const path of PAGES) {
  for (const w of WIDTHS) {
    const ctxp = await b.newContext({ viewport: { width: w, height: 900 } });
    const p = await ctxp.newPage();
    const errs = []; p.on('pageerror', (x) => errs.push(x.message));
    await p.goto(BASE + path, { waitUntil: 'domcontentloaded' });
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach((e) => e.classList.add('in')));
    await p.waitForTimeout(700);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    if (sw > w) fail(`${path} @${w}: horizontal scroll (${sw}px)`);
    if (errs.length) fail(`${path} @${w}: script error ${errs[0]}`);
    if (w === 390 || w === 1440) {
      const r = await new AxeBuilder({ page: p }).withTags(['wcag2a', 'wcag2aa']).analyze();
      for (const v of r.violations.filter((v) => ['serious', 'critical'].includes(v.impact)))
        fail(`${path} @${w}: axe ${v.id} (${v.impact}) x${v.nodes.length}: ${v.nodes[0].target}`);
    }
    if (SHOTS) await p.screenshot({ path: `${SHOTS}/${path.replace(/\W+/g, '_') || 'home'}_${w}.png`, fullPage: true });
    // mobile menu behaviour
    if (w === 390) {
      const btn = p.locator('[data-menu-btn]');
      if (await btn.count() !== 1) { fail(`${path}: menu button missing`); await ctxp.close(); continue; }
      await btn.focus(); await p.keyboard.press('Enter');
      if (await btn.getAttribute('aria-expanded') !== 'true') fail(`${path}: menu did not open with Enter`);
      const focusedInMenu = await p.evaluate(() => !!document.activeElement.closest('#site-menu'));
      if (!focusedInMenu) fail(`${path}: focus did not move into the menu`);
      await p.keyboard.press('Escape');
      if (await btn.getAttribute('aria-expanded') !== 'false') fail(`${path}: Escape did not close the menu`);
      const back = await p.evaluate(() => document.activeElement.hasAttribute('data-menu-btn'));
      if (!back) fail(`${path}: focus did not return to the menu button`);
      await btn.press('Space');
      if (await btn.getAttribute('aria-expanded') !== 'true') fail(`${path}: menu did not open with Space`);
    }
    await ctxp.close();
  }
}
// filters: keyboard, hash deep link, no-JS fallback
{
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(BASE + '/films/#music', { waitUntil: 'domcontentloaded' });
  const pressed = await p.getAttribute('[data-f="music"]', 'aria-pressed');
  if (pressed !== 'true') fail('films: #music deep link did not filter');
  const shown = await p.evaluate(() => [...document.querySelectorAll('.m-films [data-tags]')].filter((x) => !x.hidden).length);
  if (shown < 1) fail('films: music filter shows nothing');
  await p.close();
  const ctx = await b.newContext({ javaScriptEnabled: false });
  const q = await ctx.newPage(); await q.goto(BASE + '/films/');
  const all = await q.evaluate(() => [...document.querySelectorAll('.m-films [data-tags]')].filter((x) => !x.hidden).length);
  if (all < 15) fail(`films without JS lists only ${all}`);
  await ctx.close();
}
// quiz: keyboard answer, feedback, score
{
  const p = await b.newPage({ viewport: { width: 390, height: 900 } });
  await p.goto(BASE + '/tools/quiz-the-greek-dance.html');
  for (let n = 0; n < 5; n++) {
    await p.locator('.m-opts button').first().focus(); await p.keyboard.press('Enter');
    const ex = await p.locator('.m-explain').textContent();
    if (!ex || ex.length < 10) fail('quiz: no explanation after answering');
    await p.keyboard.press('Enter');
  }
  if (!(await p.locator('#quiz-result').isVisible())) fail('quiz: score not shown after 5 answers');
  await p.close();
}
// lite video: loads YouTube only on click
{
  const p = await b.newPage(); await p.goto(BASE + '/films/the-greek-dance/');
  if (await p.locator('iframe').count() !== 0) fail('film page: iframe loaded before play');
  await p.close();
}
// reduced motion: reveal content visible without animation
{
  const ctx = await b.newContext({ reducedMotion: 'reduce' });
  const p = await ctx.newPage(); await p.goto(BASE + '/'); await p.waitForTimeout(300);
  const op = await p.evaluate(() => getComputedStyle(document.querySelector('.m-why blockquote')).opacity);
  if (op !== '1') fail('reduced motion: content hidden');
  await ctx.close();
}
await b.close();
console.log(fails ? `${fails} failures` : 'all site tests passed');
process.exit(fails ? 1 : 0);
