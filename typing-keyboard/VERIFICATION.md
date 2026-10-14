# Verification — 2026-10-14

The requested deliverable is a reusable UI element and standalone page. The gallery source is on the user's other laptop; this change is ready to copy into that gallery's study pipeline. The deployed gallery is unchanged.

## Red / green evidence

The initial six acceptance checks failed because `typing-keyboard/index.html` was missing. After implementation they passed. Further failing probes caught physical Shift not affecting virtual typing, Unicode Backspace splitting an emoji sequence, the focused mobile scroll region intercepting its own native arrow navigation, key event payloads using visual labels instead of semantic key values, and the knob rail's intrinsic size inflating the chassis height. Scoped regression checks now cover all five. Existing lint/type/rule/harness files were not changed.

Final command: `python -m unittest tests.test_typing_keyboard -q` — **13 tests passed in under 10 seconds**. Existing atlas smoke: `python -m unittest tests.test_atlas_smoke -q` — **2 tests passed**. The added test module observes real Chromium; its audio audit wraps real native Web Audio nodes rather than replacing synthesis.

Covered: reference layout, five red keys, two slider knobs, offline/silent initialization, selection/caret editing, grapheme-safe deletion, physical/virtual Shift and Caps, keyboard activation, parameter events, pointer drag/reset/cancellation, finish state preservation, blur cleanup, opt-in audio and node teardown, multiple component instances, idempotent mounting, destroy, responsive containment, and hit-target reachability.

## Browser verification

The Codex in-app browser loaded `http://127.0.0.1:8765/typing-keyboard/`. Page identity, meaningful DOM content, runtime/overlay health, screenshots, and control response passed. Actual pointer interactions typed **Enochian**, the Volume slider reached **100**, and the Backlight slider reached **10**. The console reported no warnings or errors. Both material finishes were inspected at 1440×1000. At 390×844 the far-right arrow and knobs scrolled into view; the page itself did not overflow. Automated geometry checks also covered widths 280, 768, and 1440 with physical targets of at least 44 pixels.

The supplied 2048×1152 reference and the final browser captures were inspected as raster images. A 2048×1152 in-app-browser check measured the board at 2.54005:1, with both knob wrappers square. The component preserves the reference's 2.54:1 silhouette at an ordinary reusable UI size rather than reproducing its product-photo framing. Reference comparison points:

| Point | Result |
|---|---|
| Layout | Six rows, compact function row, long spacebar, stepped two-row ISO Enter, red inverted-T arrows, right-hand control rail. |
| Palette | Orange becomes Cinnabar `#CC0000`; case and key materials remain neutral gray/Ivory/Obsidian. |
| Knobs | Concentric raised caps, separate bases, dot tick scales, red bar and dot markers from the atlas dial vocabulary. |
| Key material | Dished caps, illuminated rims, deep deck sockets, homing bars, and visible three-pixel key travel. The ISO Enter cap was corrected to follow its stepped outline. |
| Type and icons | Key legends remain code-native, using the IBM Plex font stacks with local fallbacks. Arrow icons are inline SVG. |
| Display | Live local clock/date, red-to-white backlight, visible parameter readouts; clock remains legible when illumination is dimmed. |
| Responsive behavior | The hardware proportions and targets remain intact; horizontal panning replaces shrinking on small screens. |

The standalone page adds the demo textarea, finish/sound/clear controls, status, and a collapsed reuse guide. These are functional study controls. The reference's decorative cable/studio background is omitted. The bar and dot knobs replace its diagonal-ridge knobs. These are intentional adaptations for a usable Enochian UI element. No generated image is used as interface content.

Remaining limits: tested in Chromium, with pointer and simulated keyboard input. Real touch hardware, Safari/Firefox, external app integrations, and OS-level media commands were not exercised. Function/modifier keys emit events for application integration; the component does not execute OS commands. Virtual text edits do not implement an undo stack.
