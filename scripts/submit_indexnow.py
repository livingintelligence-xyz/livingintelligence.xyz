#!/usr/bin/env python3
"""Submit canonical sitemap URLs to IndexNow after a production release."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit


ORIGIN = "https://livingintelligence.xyz"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = Path("www/sitemap.xml")
KEY_FILE = Path("www/2e90d09004b00d32654621d377eb2b17.txt")
SITEMAP_NAMESPACE = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def canonical_urls(sitemap: Path) -> list[str]:
    tree = ET.parse(sitemap)
    urls = [node.text for node in tree.findall("./s:url/s:loc", SITEMAP_NAMESPACE)]
    if not urls or any(url is None for url in urls):
        raise ValueError("The sitemap contains no canonical page URLs.")
    if len(urls) > 10_000:
        raise ValueError("IndexNow accepts at most 10,000 URLs per request.")
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "livingintelligence.xyz":
            raise ValueError(f"Refusing non-canonical URL: {url}")
    return [url for url in urls if url is not None]


def indexnow_key(key_file: Path) -> str:
    key = key_file.read_text(encoding="utf-8").strip()
    if key_file.stem != key:
        raise ValueError("The IndexNow key must match the key filename.")
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        raise ValueError("The IndexNow key has an invalid format.")
    return key


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Validate and print URLs without submitting them.")
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--sitemap", type=Path, default=SITEMAP)
    parser.add_argument("--key-file", type=Path, default=KEY_FILE)
    args = parser.parse_args()

    urls = canonical_urls(args.sitemap)
    key = indexnow_key(args.key_file)
    key_location = f"{ORIGIN}/{args.key_file.name}"
    payload = {
        "host": "livingintelligence.xyz",
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }

    if args.dry_run:
        print(f"IndexNow endpoint: {args.endpoint}")
        print(f"Key location: {key_location}")
        print("URLs:")
        for url in urls:
            print(f"- {url}")
        return 0

    request = urllib.request.Request(
        args.endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "LivingIntelligence-IndexNow/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        detail = error.read(1000).decode("utf-8", errors="replace").strip()
        print(f"IndexNow rejected the submission (HTTP {error.code}): {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as error:
        print(f"IndexNow request failed: {error.reason}", file=sys.stderr)
        return 1

    if status not in (200, 202):
        print(f"Unexpected IndexNow response: HTTP {status}", file=sys.stderr)
        return 1
    print(f"IndexNow accepted {len(urls)} URLs (HTTP {status}).")
    if status == 202:
        print("The key validation is pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
