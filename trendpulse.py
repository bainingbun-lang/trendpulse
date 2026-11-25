import argparse
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

GOOGLE_RSS = "https://trends.google.com/trending/rss?geo={geo}"
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
NS = {"ht": "https://trends.google.com/trending/rss"}


def fetch(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read()


def parse_traffic(text):
    # "200K+" -> 200000, "1M+" -> 1000000
    m = re.match(r"([\d.,]+)\s*([KM]?)", text.strip().upper())
    if not m:
        return 0
    value = float(m.group(1).replace(",", ""))
    return int(value * {"K": 1_000, "M": 1_000_000}.get(m.group(2), 1))


def google(geo, limit):
    root = ET.fromstring(fetch(GOOGLE_RSS.format(geo=geo)))
    items = []
    for item in root.iter("item"):
        traffic = item.findtext("ht:approx_traffic", default="", namespaces=NS)
        items.append({
            "topic": item.findtext("title", default=""),
            "platform": "Google",
            "metric": parse_traffic(traffic),
            "label": f"{traffic} búsquedas",
        })
    items.sort(key=lambda x: x["metric"], reverse=True)
    return items[:limit]


def hackernews(limit):
    ids = json.loads(fetch(HN_TOP))[:limit]
    items = []
    for story_id in ids:
        story = json.loads(fetch(HN_ITEM.format(id=story_id)))
        items.append({
            "topic": story.get("title", ""),
            "platform": "HackerNews",
            "metric": story.get("score", 0),
            "label": f"{story.get('score', 0)} puntos",
        })
    items.sort(key=lambda x: x["metric"], reverse=True)
    return items


def main():
    p = argparse.ArgumentParser(description="Tendencias de Google Trends y Hacker News")
    p.add_argument("--source", choices=["google", "hn", "all"], default="all")
    p.add_argument("--limit", "-N", type=int, default=10)
    p.add_argument("--geo", default="MX", help="código de país para Google Trends")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    results = []
    if args.source in ("google", "all"):
        results += google(args.geo, args.limit)
    if args.source in ("hn", "all"):
        results += hackernews(args.limit)

    # cada fuente usa unidades distintas, así que se normaliza a su máximo
    for platform in {r["platform"] for r in results}:
        group = [r for r in results if r["platform"] == platform]
        top = max(r["metric"] for r in group) or 1
        for r in group:
            r["score"] = round(r["metric"] / top, 3)

    results.sort(key=lambda r: r["score"], reverse=True)
    results = results[:args.limit]
    for rank, r in enumerate(results, 1):
        r["rank"] = rank

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for r in results:
        print(f"{r['rank']:>3}. [{r['platform']}] {r['topic']}  ({r['label']})")


if __name__ == "__main__":
    main()
