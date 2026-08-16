# Store deployment and SEO

The generated store is the static homepage at `docs/index.html`. `scripts/build_views.py` rebuilds the homepage, the installable plugin Store at `docs/market.html` from the same `docs/data/market-registry.json` consumed by Market Plugin, one stable install page, Atom feed, and bilingual launch packet per Market plugin under `docs/plugins/`, global new/updated Atom feeds under `docs/feeds/`, one crawlable page per ecosystem record under `docs/skills/`, `docs/data/catalog.json`, the deployable local-media mirror under `docs/media/`, `robots.txt`, `sitemap.xml`, and `CNAME`.

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

Each detail page publishes the dataset version and timestamp of that record's latest material evidence. A collection run that does not observe the record updates the global homepage and catalog metadata without changing the detail page, keeping crawlable URLs stable while preserving record-level provenance.

Market plugin pages use the immutable normalized install identity at `plugins/<deeplugin-id>.html`. They publish exact install specs, review-first Agent requests, source-local verification claims, `SoftwareApplication` JSON-LD, related internal links, and a copyable backlink badge. The generator validates every stable id before writing and replaces the generated directory so removed plugins do not leave crawlable stale pages. All current Market plugin URLs are included in `sitemap.xml`.

`feeds/new.atom.xml` publishes first active observations and `feeds/updated.atom.xml` publishes later material Listing changes. Each `plugins/<deeplugin-id>.atom.xml` preserves that plugin's material event history, while `plugins/<deeplugin-id>.launch.json` gives authors the exact canonical link, install spec, badge, review-first Agent request, and bilingual draft text. Repeat observations and stars, likes, views, or other interaction-only changes do not create update entries. Feed time comes from the source observation, so rebuilding without a material change leaves feed bytes unchanged. External social posts remain drafts requiring human approval; the two-hour job never posts them automatically.

The site only publishes public metadata and attributed media references. It does not claim ownership of third-party screenshots, thumbnails, videos, or post content.
