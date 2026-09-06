PYTHON ?= python3
Q ?= l

render:
	uv run manim-slides render -q $(Q) deck.py Deck

render-nocache:
	uv run manim-slides render -q $(Q) --disable_caching deck.py Deck

present: render
	uv run manim-slides present Deck --full-screen

html: Q = h
html: render
	uv run python mux_audio.py
	uv run manim-slides convert Deck out.html --one-file --offline

pages: html
	$(PYTHON) scripts/build_pages.py out.html docs
	$(MAKE) check

pages-from-export:
	$(PYTHON) scripts/build_pages.py out.html docs
	$(MAKE) check

serve:
	$(PYTHON) -m http.server 8000 --bind 127.0.0.1 --directory docs

pptx: Q = h
pptx: render
	uv run python mux_audio.py
	uv run manim-slides convert Deck out.pptx

notebook:
	uv run marimo edit --watch deck.py

check:
	$(PYTHON) -m unittest discover -s tests -v

.PHONY: render render-nocache present html pages pages-from-export serve pptx notebook check
