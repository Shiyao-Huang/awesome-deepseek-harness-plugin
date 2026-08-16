"""Public rich-media projection checks for the generated store."""

from __future__ import annotations

import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site


class RichMediaSiteProjectionTests(unittest.TestCase):
    def test_home_is_a_small_decision_surface_not_the_full_directory(self) -> None:
        page_path = ROOT / "docs" / "index.html"
        page = page_path.read_text(encoding="utf-8")

        self.assertLess(page_path.stat().st_size, 500_000)
        self.assertLessEqual(page.count('class="skill-card'), 24)
        self.assertIn('href="market.html"', page)
        self.assertIn('href="directories.html"', page)

    def test_market_page_projects_the_agent_registry(self) -> None:
        registry = json.loads((ROOT / "docs" / "data" / "market-registry.json").read_text(encoding="utf-8"))
        page = (ROOT / "docs" / "market.html").read_text(encoding="utf-8")
        first = registry["plugins"][0]

        self.assertEqual(page.count('class="skill-card market-plugin-card"'), registry["count"])
        self.assertIn(first["id"], page)
        self.assertIn(first["install"]["spec"], page)
        self.assertIn(f'dsh plugin --profile web add {first["install"]["spec"]}', page)
        self.assertIn(f'href="plugins/{first["id"]}.html"', page)
        sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("https://deeplugin.store/market.html", sitemap)
        self.assertIn(f"https://deeplugin.store/plugins/{first['id']}.html", sitemap)

    def test_market_registry_has_one_stable_detail_page_per_plugin(self) -> None:
        registry = build_site.load_market_registry()
        plugins = registry["plugins"]
        assert isinstance(plugins, list)
        generated = sorted((ROOT / "docs" / "plugins").glob("*.html"))

        self.assertEqual(len(generated), len(plugins))
        self.assertEqual(
            {path.stem for path in generated},
            {plugin["id"] for plugin in plugins if isinstance(plugin, dict)},
        )

    def test_market_registry_has_one_stable_detail_page_per_active_pack(self) -> None:
        registry = build_site.load_market_registry()
        packs = registry["packs"]
        assert isinstance(packs, list)
        generated = sorted((ROOT / "docs" / "packs").glob("*.html"))

        self.assertEqual(
            {path.stem for path in generated},
            {pack["id"] for pack in packs if isinstance(pack, dict)},
        )
        sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
        for pack in packs:
            self.assertIn(f"https://deeplugin.store/packs/{pack['id']}.html", sitemap)

    def test_market_detail_exposes_install_share_and_source_evidence(self) -> None:
        registry = build_site.load_market_registry()
        plugins = registry["plugins"]
        assert isinstance(plugins, list)
        plugin = plugins[0]
        assert isinstance(plugin, dict)
        page = (ROOT / "docs" / "plugins" / f"{plugin['id']}.html").read_text(encoding="utf-8")
        canonical = f"https://deeplugin.store/plugins/{plugin['id']}.html"
        command = f"dsh plugin --profile web add {plugin['install']['spec']}"

        self.assertIn(f'<link rel="canonical" href="{canonical}">', page)
        self.assertIn(plugin["id"], page)
        self.assertIn(command, page)
        self.assertIn("方式一 · 自己安装", page)
        self.assertIn("方式二 · 交给 DEEPSEEK", page)
        self.assertIn("等我明确批准后再安装", page)
        self.assertIn("Copy link", page)
        self.assertIn("Copy badge", page)
        self.assertIn("assets/deeplugin-listed.svg", page)
        self.assertIn("Verification is a claim made by the named Registry Source", page)
        self.assertIn("not a security, compatibility, quality, or official endorsement", page)
        self.assertIn('<script src="../assets/store.js" defer></script>', page)
        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', page)
        self.assertIsNotNone(match)
        assert match is not None
        structured_data = json.loads(match.group(1))
        self.assertEqual(structured_data.get("@type"), "SoftwareApplication")
        self.assertEqual(structured_data.get("identifier"), plugin["id"])
        self.assertEqual(structured_data.get("url"), canonical)

    def test_detail_page_version_changes_only_with_record_evidence(self) -> None:
        with build_site.connection() as db:
            record = next(
                record
                for record in build_site.load_records(db)
                if build_site.install_command(record)
            )
        config = build_site.read_config()

        older_global = build_site.render_detail(record, "v-global-old", "2026-08-16T01:00:00Z", config)
        newer_global = build_site.render_detail(record, "v-global-new", "2026-08-16T03:00:00Z", config)

        self.assertEqual(older_global, newer_global)
        self.assertIn(f"<dt>Evidence dataset</dt><dd>{record['evidence_dataset_version']}</dd>", newer_global)
        self.assertIn(f"Evidence updated {record['evidence_updated_at']}", newer_global)
        self.assertIn('<script src="../assets/store.js" defer></script>', newer_global)

        updated_record = dict(record)
        updated_record["evidence_dataset_version"] = "v-record-new"
        updated_record["evidence_updated_at"] = "2026-08-16T03:00:00Z"
        updated = build_site.render_detail(updated_record, "v-global-new", "2026-08-16T03:00:00Z", config)

        self.assertNotEqual(newer_global, updated)
        self.assertIn("<dt>Evidence dataset</dt><dd>v-record-new</dd>", updated)

    def test_local_media_assets_are_published_with_the_site(self) -> None:
        source = ROOT / "media" / "screenshots" / "official.png"
        published = ROOT / "docs" / "media" / "screenshots" / "official.png"

        self.assertTrue(published.is_file())
        self.assertEqual(published.read_bytes(), source.read_bytes())

    def test_video_detail_exposes_google_video_structured_data(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-502.html").read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            page,
        )
        self.assertIsNotNone(match)
        assert match is not None
        structured_data = json.loads(match.group(1))

        self.assertEqual(
            {
                "type": structured_data.get("@type"),
                "thumbnail": structured_data.get("thumbnailUrl"),
                "embed": structured_data.get("embedUrl"),
                "published": structured_data.get("uploadDate"),
            },
            {
                "type": "VideoObject",
                "thumbnail": [
                    "http://i2.hdslb.com/bfs/archive/edee3acd06e6b20bafe126e3214020c4758eb834.jpg"
                ],
                "embed": "https://player.bilibili.com/player.html?bvid=BV11CgF6uE4k",
                "published": "2026-08-14T02:41:52Z",
            },
        )

    def test_video_reference_renders_as_a_player_with_its_rights_note(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-38.html").read_text(encoding="utf-8")

        self.assertIn(
            '<iframe class="media-video-player" src="https://www.youtube-nocookie.com/embed/qg9EyGOZd9U"',
            page,
        )
        self.assertNotIn(
            '<img src="https://www.youtube.com/watch?v=qg9EyGOZd9U"',
            page,
        )
        self.assertIn("External URL; do not mirror without permission.", page)

    def test_sitemap_exposes_captured_video_evidence(self) -> None:
        root = ET.parse(ROOT / "docs" / "sitemap.xml").getroot()
        sitemap_ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        video_ns = "http://www.google.com/schemas/sitemap-video/1.1"
        entries = {
            entry.findtext(f"{{{sitemap_ns}}}loc"): entry
            for entry in root.findall(f"{{{sitemap_ns}}}url")
        }
        video = entries["https://deeplugin.store/skills/id-502.html"].find(
            f"{{{video_ns}}}video"
        )
        self.assertIsNotNone(video)
        assert video is not None

        self.assertEqual(
            {
                child.tag.removeprefix(f"{{{video_ns}}}"): child.text
                for child in video
            },
            {
                "thumbnail_loc": "http://i2.hdslb.com/bfs/archive/edee3acd06e6b20bafe126e3214020c4758eb834.jpg",
                "title": "【热门AI鉴定】DeepSeek Harness是什么？强在哪里？Harness实测效果如何？一口气搞懂！",
                "description": "DeepSeek Harness是什么？ 强在哪里？ Harness实测效果如何？ 本期视频教会你",
                "player_loc": "https://player.bilibili.com/player.html?bvid=BV11CgF6uE4k",
                "publication_date": "2026-08-14T02:41:52Z",
            },
        )

    def test_local_captured_media_is_visible_on_its_detail_page(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-504.html").read_text(encoding="utf-8")

        self.assertIn("Local and external references · rights noted", page)
        self.assertIn('src="../media/images/og-bilibili-video.jpg"', page)
        self.assertIn("Local capture from the dated raw snapshot.", page)

    def test_external_images_do_not_send_the_store_referrer(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-504.html").read_text(encoding="utf-8")

        self.assertIn(
            'src="https://i1.hdslb.com/bfs/face/c6eaa43c435acaa8a7eec57e6447c2858e088c13.jpg" '
            'alt="Public media reference" loading="lazy" referrerpolicy="no-referrer"',
            page,
        )

    def test_video_without_a_thumbnail_uses_the_site_social_image(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-38.html").read_text(encoding="utf-8")

        self.assertIn(
            '<meta property="og:image" content="https://deeplugin.store/media/screenshots/official.png">',
            page,
        )
        self.assertNotIn(
            '<meta property="og:image" content="https://www.youtube.com/watch?v=qg9EyGOZd9U">',
            page,
        )

    def test_image_detail_exposes_its_captured_image_in_structured_data(self) -> None:
        page = (ROOT / "docs" / "skills" / "id-1.html").read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            page,
        )
        self.assertIsNotNone(match)
        assert match is not None
        structured_data = json.loads(match.group(1))
        with build_site.connection() as db:
            record = next(record for record in build_site.load_records(db) if record["id"] == "id-1")
        image = build_site.record_image(record)
        self.assertIsNotNone(image)
        assert image is not None

        self.assertEqual(
            structured_data.get("image"),
            [build_site.absolute_media_url(image, build_site.read_config()["site_url"])],
        )


if __name__ == "__main__":
    unittest.main()
