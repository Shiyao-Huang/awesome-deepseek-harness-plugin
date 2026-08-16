# Store deployment and SEO

The generated store is the static homepage at `docs/index.html`. `scripts/build_views.py` rebuilds the homepage, one crawlable page per registry record under `docs/skills/`, `docs/data/catalog.json`, the deployable local-media mirror under `docs/media/`, `robots.txt`, `sitemap.xml`, and `CNAME` from the SQLite database.

## GitHub Pages

1. In the repository settings, enable Pages from the `main` branch and the `/docs` folder.
2. The repository ships `docs/CNAME` for `deeplugin.store`; GitHub Pages will issue HTTPS after DNS resolves.
3. The workflow refreshes the data and regenerated pages every two hours at minute 17 UTC.

## Hostinger DNS

At Hostinger, keep the domain registration there and point the apex `deeplugin.store` to the GitHub Pages A records:

```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Remove conflicting parking A records. If a `www` hostname is desired, create a CNAME from `www` to `Shiyao-Huang.github.io`; the canonical site remains the apex domain.

## Google Search Console

The `deeplugin.store` Domain property was verified through its Hostinger TXT record on 2026-08-16, and `https://deeplugin.store/sitemap.xml` was submitted successfully. Keep the TXT record in DNS to preserve ownership verification. Search inclusion and ranking are controlled by Google; this repository supplies stable canonical URLs, descriptions, Open Graph metadata, JSON-LD, robots rules, and dated content pages.

## Rich media indexing

The sitemap declares Google image and video namespaces. Captured public images become `image:image` entries. A record becomes a `video:video` entry and a `VideoObject` only when SQLite contains the public video URL, a captured thumbnail, and the platform publication date, and the site can derive a supported external player URL. Missing publication dates or thumbnails stay missing; the generator does not reuse collection time as publication time.

Detail pages render supported YouTube, Bilibili, and WeChat video references through external players. Unsupported video references remain reviewable source links and are never used as image URLs. Rights-cleared local captures are copied from `media/` into `docs/media/` for GitHub Pages; third-party media remains an external reference unless its rights note explicitly permits a local copy.

The site only publishes public metadata and attributed media references. It does not claim ownership of third-party screenshots, thumbnails, videos, or post content.
