"""Package a manim-slides one-file HTML export for GitHub Pages.

Remove speaker notes and externalize embedded videos without re-encoding them.
Only the Python standard library is required.
"""

import argparse
import base64
import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path


class NotesParser(HTMLParser):
    """Find complete notes elements while leaving inline JavaScript untouched."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.spans = []
        self.start = None
        self.depth = 0

    def source_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "aside":
            if self.start is not None:
                self.depth += 1
            elif "notes" in attrs.get("class", "").split():
                self.start = self.source_offset()
                self.depth = 1

    def handle_endtag(self, tag):
        if tag == "aside" and self.start is not None:
            self.depth -= 1
            if self.depth == 0:
                end = self.source.index(">", self.source_offset()) + 1
                self.spans.append((self.start, end))
                self.start = None


def package(source, destination):
    parser = NotesParser(source)
    parser.feed(source)
    parser.close()
    if parser.start is not None:
        raise ValueError("Unclosed speaker notes element")
    for start, end in reversed(parser.spans):
        source = source[:start] + source[end:]

    # The notes and Markdown plugins are unused once narration is removed.
    source = re.sub(
        r"<script\b[^>]*>(.*?)</script>",
        lambda match: "" if any(marker in match[1][:400]
                               for marker in ("e.RevealNotes=t()", "e.RevealMarkdown=t()"))
        else match[0],
        source, flags=re.S,
    )

    media = {}

    def extract(match):
        payload = base64.b64decode(match[2], validate=True)
        filename = hashlib.sha256(payload).hexdigest() + ".mp4"
        media[filename] = payload
        return f'data-background-video={match[1]}assets/{filename}{match[1]}'

    source, count = re.subn(
        r'''data-background-video=(["'])data:video/mp4;base64,([A-Za-z0-9+/=]+)\1''',
        extract,
        source,
    )
    if count == 0 or "data:video/mp4;base64," in source:
        raise ValueError("Expected a one-file manim-slides export with embedded MP4 slides")

    source = re.sub(r"<title>.*?</title>",
                    "<title>Tiny Snakes on a Board | Cyra Locsin</title>",
                    source, count=1, flags=re.S)
    source = source.replace("<html>", '<html lang="en">', 1)
    source = source.replace(
        "</head>",
        '<meta name="description" content="A Python WA talk by Cyra Locsin: '
        'MicroPython, ESP32, Wi-Fi sensing, Doppler radar and concert lightsticks.">\n'
        '<link rel="icon" href="data:,">\n</head>',
        1,
    )
    # Restrict changes to the converter's configuration block, not vendor code.
    source = source.replace("plugins: [ RevealMarkdown, RevealNotes ],", "plugins: [],")
    for name, value in (("controls", "true"), ("progress", "true"),
                        ("hash", "true"), ("respondToHashChanges", "true"),
                        ("slideNumber", '"c/t"'),
                        ("viewDistance", "2"), ("mobileViewDistance", "1")):
        source = re.sub(rf"^(\s*{name}:) [^\n,]+,", rf"\g<1> {value},",
                        source, count=1, flags=re.M)

    destination = Path(destination)
    assets = destination / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for filename, payload in media.items():
        (assets / filename).write_bytes(payload)
    (destination / "index.html").write_text(source, encoding="utf-8")
    (destination / ".nojekyll").touch()
    # Only prune files owned by this builder, after the replacement page exists.
    for path in assets.iterdir():
        if re.fullmatch(r"[0-9a-f]{64}\.mp4", path.name) and path.name not in media:
            path.unlink()
    return count, len(parser.spans)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    videos, notes = package(args.source.read_text(encoding="utf-8"), args.destination)
    print(f"Packaged {videos} video slides; removed {notes} notes elements")


if __name__ == "__main__":
    main()
