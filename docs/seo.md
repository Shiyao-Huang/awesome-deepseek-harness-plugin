# Store deployment and SEO

The generated store is the static homepage at `docs/index.html`. `scripts/build_views.py` rebuilds the homepage, one crawlable page per registry record under `docs/skills/`, `docs/data/catalog.json`, `robots.txt`, `sitemap.xml`, and `CNAME` from the SQLite database.

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

Add a Domain property for `deeplugin.store`, place Google's TXT verification record in Hostinger DNS, then submit `https://deeplugin.store/sitemap.xml`. Search inclusion and ranking are controlled by Google; this repository supplies stable canonical URLs, descriptions, Open Graph metadata, JSON-LD, robots rules, and dated content pages.

The site only publishes public metadata and external media references. It does not claim ownership of third-party screenshots, thumbnails, videos, or post content.
