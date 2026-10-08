# Enochian UI UX Elements

A control atlas of hardware-inspired interface elements for the web: dials, switches, meters, keys and instruments that are felt before they are understood. Every element is a working interaction study with keyboard access, spring motion and a copyable implementation behind the Code Veil.

Volume I lives at [uncommoncore.web.app/enochian_knobs_keys](https://uncommoncore.web.app/enochian_knobs_keys/). This repository holds Volumes II and III.

## Volumes

| Volume | Open | Contents |
|---|---|---|
| **II · signal, scale and sequence** | [`volume-2/index.html`](volume-2/index.html) | Lumen VU, Cantor Ladder, Meridian Fader, Regie Bank, Aperture Scale, Interlock Bank, Lantern Row, Strobe Platter, Lumen Pad, Transport Bank, Cadence Pads, Penumbra Deck, Tally Keypad, Sigil Remote, Orbit Wheel, Excursion Pair, Monitor Pair, Augur rangefinder, Lodestar compass, Climate thermostat |
| **III · after Drams** | [`volume-3/index.html`](volume-3/index.html) | Twenty small controls after the [Drams](https://drams.framer.website/) collection: OP-1 Keys, Bouncin' Ball, Rollin' Search, Fidget Poppin', Triple Switch, Standard Switch, Triple Push Buttons, Pinchin' Switch, Triple Light Switch, Pinchin' Track Switch, Coloured Switch, Trackin' Slider, LED Switch, Round On/Off Knob, Joypad Controller, Square Slider, Concaved Switch, Pushin' Click Button, Dimpled Slider, I/O Switch |

Each `index.html` is a single self-contained file. Open it in a browser and it works, with no build step and no install.

`enochian-elements-vol2.html` and `enochian-elements-vol3.html` at the root are the same pages without the `<!doctype>` and `<head>` wrapper. They are the sources the hosted previews are published from.

## Design rules

- **Palette:** black, white and one signal accent: Cinnabar `#CC0000`, or Ember `#E76A2E` (switchable on each page). Other colours appear only on sensors and gauges, for example amber meter lamps and the thermostat's cooling blue.
- **Type:** IBM Plex Sans, Mono and Serif.
- **Finishes:** every instrument has an Ivory and an Obsidian finish.
- **Motion:** springs, using the same constants throughout: `SNAP {700, 35, 0.8}` and `HEAVY {300, 30, 1.2}`. Motion is reduced when the visitor prefers reduced motion.
- **Access:** every control works from the keyboard and exposes its state through ARIA.
- **Portable:** no libraries and no hosted services. The springs, clicks, synth voices, drum kit and physics are written inline with the Web Audio and DOM APIs.

## Use and remix

To lift a single control into your own project, or to contribute a remix, see **[HOW_TO_USE_AND_REMIX.md](HOW_TO_USE_AND_REMIX.md)**. It covers where each control's code lives, the shared core it needs, and the checklist a remix should pass.

## License

[CC BY-NC 4.0](LICENSE.md). You are free to share and remix with credit, but not for commercial use.

## Credits

Hardware lineage is noted on each card, for example Braun, Technics, Nakamichi, Leica, Work Louder and Teenage Engineering. Volume III is a homage to [Drams](https://drams.framer.website/) by [@mrblackstudio](https://x.com/mrblackstudio). Brand names appear only as design references, and every element carries the UnCommon Core mark instead.
