# Media shelf

This folder keeps local visual captures that may help a human browse the ecosystem. They are not treated as evidence in SQLite until a dated raw observation records the source URL, collection time, platform, and capture method.

The aggregator stores external image/video/document URLs by default and avoids mirroring platform media. Local screenshots remain separate from `data/raw/` so a visual capture cannot silently become a structured fact.

The site build mirrors this directory into generated `docs/media/` so rights-cleared local captures resolve under the GitHub Pages deployment. That byte-for-byte deployment copy does not change provenance: a local file is indexed as evidence only when SQLite links it to a dated raw observation and records its rights note.
