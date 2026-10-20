"""Tell Bing and other IndexNow search engines which pages changed.

Usage: python3 scripts/indexnow.py OLD_SITEMAP NEW_SITEMAP
Sends every URL that is new, or whose lastmod changed. Google does not use IndexNow;
it reads sitemap.xml (submitted in Search Console). Never fails the build.
"""
import json, re, sys, urllib.request

SITE = "kriosgreece.com"
KEY = "0c3ff38bcca4bcb0d0ff58ac478f0251e62cebf4fb5ee5a71a3c50cd2618251d"


def entries(path):
    try:
        t = open(path, encoding="utf-8").read()
    except OSError:
        return {}
    return dict(re.findall(r"<loc>([^<]+)</loc>(?:<lastmod>([^<]*)</lastmod>)?", t))


def main(old, new):
    a, b = entries(old), entries(new)
    urls = [u for u, d in b.items() if a.get(u) != d][:10000]
    if not urls:
        print("IndexNow: nothing changed")
        return
    body = json.dumps({"host": SITE, "key": KEY, "keyLocation": f"https://{SITE}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: sent {len(urls)} URLs, HTTP {r.status}")
    except Exception as ex:  # report, never block publishing
        print(f"IndexNow: not sent ({ex})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
