import ast
import base64
import importlib.util
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts/build_pages.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.videos = []
        self.notes = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "aside" and "notes" in attrs.get("class", "").split():
            self.notes += 1
        for key in ("src", "href", "data-background-video", "data-background-image"):
            if key in attrs:
                self.references.append(attrs[key])
        if "data-background-video" in attrs:
            self.videos.append(attrs["data-background-video"])


class PackagingTests(unittest.TestCase):
    def test_notes_removed_and_video_bytes_preserved(self):
        clip = b"test-video-bytes"
        uri = "data:video/mp4;base64," + base64.b64encode(clip).decode()
        html = ('<html><head><title>Old</title></head><body>'
                f'<section data-background-video="{uri}">'
                '<aside data-markdown class="extra notes">private <b>narration</b>'
                '<aside>nested note</aside></aside></section>'
                f'<section data-background-video="{uri}"></section>'
                '<script>const text = "<aside class=notes>not HTML</aside>";</script>'
                '</body></html>')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            self.assertEqual(builder.package(html, output), (2, 1))
            published = (output / "index.html").read_text()
            self.assertNotIn("private", published)
            self.assertIn("not HTML", published)
            files = list((output / "assets").glob("*.mp4"))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].read_bytes(), clip)
            self.assertTrue((output / ".nojekyll").exists())

    def test_malformed_input_does_not_replace_site(self):
        for invalid in ('<aside class="notes">private', '<html>No embedded slides</html>'):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                (output / "index.html").write_text("previous site")
                with self.assertRaises(ValueError):
                    builder.package(invalid, output)
                self.assertEqual((output / "index.html").read_text(), "previous site")

    def test_rebuild_prunes_only_owned_stale_media(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            def export(payload):
                uri = base64.b64encode(payload).decode()
                return f'<section data-background-video="data:video/mp4;base64,{uri}"></section>'
            builder.package(export(b"old"), output)
            (output / "assets/keep.mp4").write_bytes(b"hand-maintained")
            builder.package(export(b"new"), output)
            self.assertEqual(sorted(p.read_bytes() for p in (output / "assets").iterdir()),
                             [b"hand-maintained", b"new"])


class PublicRepositoryTests(unittest.TestCase):
    def test_source_has_no_narration_and_assets_exist(self):
        for name in ("script.md", "speakernotes.txt", "NOTES.txt", "HANDOFF.md", "TONE.md"):
            self.assertFalse((ROOT / name).exists(), name)
        tree = ast.parse((ROOT / "deck.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                self.assertFalse(any(k.arg == "notes" for k in node.keywords),
                                 f"Embedded notes at line {node.lineno}")
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value.startswith("assets/"):
                    self.assertTrue((ROOT / node.value).is_file(), node.value)

    def test_published_site_is_complete_and_has_no_notes(self):
        html = (ROOT / "docs/index.html").read_text()
        inventory = Inventory()
        inventory.feed(html)
        self.assertEqual(inventory.notes, 0)
        self.assertGreater(len(inventory.videos), 0)
        for reference in inventory.references:
            parsed = urlsplit(reference)
            if parsed.scheme == "data":
                continue
            self.assertFalse(parsed.scheme or parsed.netloc, reference)
            self.assertFalse(parsed.path.startswith("/"), reference)
            self.assertNotIn("..", Path(parsed.path).parts)
            self.assertTrue((ROOT / "docs" / parsed.path).is_file(), reference)
        for name in ("controls", "progress", "hash", "respondToHashChanges"):
            self.assertRegex(html, rf"(?m)^\s*{name}: true,")
        self.assertNotIn("plugins: [ RevealMarkdown, RevealNotes ]", html)
        self.assertTrue((ROOT / "docs/.nojekyll").exists())


if __name__ == "__main__":
    unittest.main()
