# Agent instructions for this repository

The rules for this deck live in **[`CLAUDE.md`](CLAUDE.md)** in this same directory. Read it in full
before touching `deck.html`. It is not Claude-specific — the filename is only what Claude Code loads
automatically. Codex loads this file, Gemini loads `GEMINI.md`, and both are pointers to the same
source so the three CLIs cannot drift apart.

Short version, all of it learned by getting it wrong on 2026-08-31:

1. "Rebuilt" means composed in HTML from the individual images in `img/src2025/` (the unzipped pptx
   `/media` folder), with every word set in the deck's own type. Dimming the flat PowerPoint export
   and cutting clip-path windows in it is NOT a rebuild and is refused by the splicer.
2. A slide may never come back less visual than it was. More is always welcome.
3. Type floor is 1.10% of slide width. "Optimize SRE" usually means the defect is inside the figure.
4. Run `bash tools/preflight.sh` before you commit. Read the rendered PNGs; the tools have documented
   blind spots and DOM inspection is not verification here.
