# Enochian control sources

These three self-contained studies supply the 55 working controls in the [single Enochian showcase](../UIUX/index.html):

| Source | Controls | Purpose |
|---|---:|---|
| [`index.html`](index.html) | 11 | Foundation controls, including dials, keys, clocks, and the receiver |
| [`volume-3/index.html`](volume-3/index.html) | 20 | Compact actions, switches, sliders, and navigation |
| [`volume-2/index.html`](volume-2/index.html) | 24 | Instruments, meters, transport, and displays |

The showcase generator in [`../scripts/generate_uiux.py`](../scripts/generate_uiux.py) combines their markup, styles, and behavior. The source files remain available for editing individual instruments. The public deployment contains only the combined showcase and its assets.

Black, white, and Cinnabar `#CC0000` define the palette. Ivory and Obsidian are component material finishes. Use semantic controls, visible focus, synchronized ARIA state, and reduced-motion support when adapting a control.

See [`HOW_TO_USE_AND_REMIX.md`](HOW_TO_USE_AND_REMIX.md) for implementation details and [`LICENSE.md`](LICENSE.md) for source terms.

## Standalone typing keyboard

[`typing-keyboard/index.html`](typing-keyboard/index.html) adds the reference-inspired 79-key mechanical typing surface: Cinnabar Escape/arrows, two Enochian rotary knobs, a live clock, and Ivory/Obsidian finishes. Keys edit real text; the knobs adjust local key-sound volume and display backlight. It is an offline single-file component with scoped input/key/parameter events for reuse. The showcase can add it as a device study from its separate source checkout. See [`typing-keyboard/README.md`](typing-keyboard/README.md) for embedding, extraction, controls, and acceptance checks.

`python -m unittest tests.test_typing_keyboard -q`

## Composed instrument study

[`op-1/index.html`](op-1/index.html) combines the Canticle Keys, spring-driven encoders, and interlocked transport into a Teenage Engineering OP-1-inspired Enochian control surface. This is an additional study, not a replacement for the existing sources or part of the 55-control showcase count.

Open it directly in a browser, or serve this directory with `python -m http.server 8765 --bind 127.0.0.1` and visit <http://127.0.0.1:8765/op-1/>. It has no build step or runtime dependencies. The reference's blue, green, white, and orange encoder colors identify parameters; this study intentionally extends the atlas's Cinnabar-only palette.

Browser acceptance checks (test-only dependencies):

```bash
python -m pip install playwright
python -m playwright install chromium
python -m unittest discover -s tests -v
python tests/capture_op1.py
```

Captures and diagnostic reports go under `.qa/op-1/` (ignored by git).

## Audio-object studies

[`speakers/index.html`](speakers/index.html) adds two hardware-inspired audio surfaces: **Mesh / compact** (the woven-grille CM-15 form) and **Twin / portable** (the handled twin-driver speaker, with Ivory and Obsidian finishes). These are additional component studies, not changes to the original showcase's control count.

Open the HTML directly or visit <http://127.0.0.1:8765/speakers/> with the same local server. The page uses only inline HTML/CSS/JavaScript; audio is generated locally and starts off. See [`speakers/README.md`](speakers/README.md) for controls, reuse contracts, and limitations.

```bash
python -m unittest discover -s tests -p 'test_speakers*.py' -v
python tests/capture_speakers.py
```

Speaker visual captures and reports go under `.qa/speakers/` (ignored by git).

## Recorder and DJ studies

- [`tp-7/index.html`](tp-7/index.html): TP-7-inspired recorder control surface, with silver and Obsidian materials. The original orange signal details are **Cinnabar `#CC0000`**. Record captures a locally generated demo, not a microphone; audio and recording are opt-in.
- [`dj-decks/index.html`](dj-decks/index.html): twin jog decks and a two-channel mixer with independently remembered **White/Obsidian** finishes. Orange pad/cue accents become **Cinnabar `#CC0000`**; green remains a play-state signal. Source audio is generated locally, not remote music or a DJ software connection.

Both are additive, self-contained HTML/CSS/JS studies with no application dependencies, remote assets, or build step. Open directly or use the same local server at `/tp-7/` and `/dj-decks/`. Controls reuse the atlas's knob, Spring, transport, and audio vocabulary. These do not change the original showcase's 55-control count.

```bash
python -m unittest discover -s tests -v
python tests/capture_transports.py
```

Details and limits live in each study's README. Verification captures go under `.qa/transports/` (ignored by git).

## Keyboard and MIDI-pad studies

- [`keyboard/index.html`](keyboard/index.html): **Canticle / 25**, a compact White/Obsidian keyboard with 25 playable notes, two touch strips, eight encoders, and a 2×8 chord/function pad bank. Its finish preference persists independently; musical black/white keys remain distinct in either finish.
- [`midi-pad/index.html`](midi-pad/index.html): **Grid16**, a White/Obsidian 4×4 pad instrument with generated drums, pitched notes, a local step sequencer, three scenes, and four encoders. The finish preference persists independently. Orange details become Cinnabar; multicolor pad identities and semantic green Play remain.

Both work offline as individual HTML files. Local preview is initially muted. Web MIDI output is optional: open the playing guide, explicitly connect, then select an output and channel. No output is selected automatically, no microphone is requested, and no hardware connection is needed for local play. Physical MIDI devices have not been exercised in the automated checks; MIDI routing tests use a labelled browser-boundary test double.

```bash
python -m unittest discover -s tests -v
python tests/capture_controllers.py
```

Local server paths: `/keyboard/` and `/midi-pad/`. Details are in each study's README. Real browser captures and independent probes are saved under `.qa/controllers/`. These additions leave the original 55-control showcase unchanged.

White/Obsidian palette and responsive checks for DJ-Decks and Keyboard: `python tests/capture_finishes.py`. Captures and geometry results are saved under `.qa/finishes/` (ignored by git).

## Blank device-frame studies

[`apple-devices/index.html`](apple-devices/index.html) adds the five Apple-hardware-inspired compositions from the supplied references: **display + Mac mini**, **iMac + keyboard/mouse**, **MacBook**, **iPad + Pencil**, and **iPhone**. All nine bodies have matching White/Ivory and Obsidian materials. The five screens are completely empty—no built-in images, wallpapers, lock-screen UI, or app content. Named `[data-screen]` containers are ready for your own content; see [`apple-devices/README.md`](apple-devices/README.md) for insertion selectors and ratios.

Open directly or use `/apple-devices/` on the existing local server. Finish selection is accessible and remembers its own isolated preference. These additive CSS/HTML frames are not Apple products or OS emulators, and leave the original 55-control showcase count unchanged.

```bash
python -m unittest tests.test_apple_devices -v
python tests/capture_apple_devices.py
```

Device captures and geometry evidence go under `.qa/apple-devices/` (ignored by git).
