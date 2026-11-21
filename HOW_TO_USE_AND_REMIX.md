# How to use and remix

Every control in the atlas is plain HTML, CSS and JavaScript in a single file. There is nothing to install and no build step. This guide shows how to lift one control into your own project, and what a remix needs before it belongs in the atlas.

The work is licensed under [CC BY-NC 4.0](LICENSE.md). You can use and remix it for non-commercial work, with credit.

---

## 1. Look before you lift

1. Open `volume-2/index.html` or `volume-3/index.html` in a browser.
2. Find the control and try it with both the pointer and the keyboard. The grey hint line under each control lists its keys.
3. Turn on the **Code Veil** near the top of the page. Each card then shows the fragment that makes the control behave, usually the physics, the state logic or the CSS trick. That fragment is the idea. The full implementation is in the source.

## 2. Find the three pieces

Each control has three parts in the page source, and each part has a marked header.

| Part | Where | Look for |
|---|---|---|
| **Markup** | inside `<article class="unit">` | the control's `id`, e.g. `id="cp"` (Cadence Pads) or the card `id="c-jp"` (Joypad) |
| **Styles** | the `<style>` block | `/* ── Cadence Pads ── */` |
| **Behaviour** | the `<script>` block | `/* ═════════ Cadence Pads ═════════ */` in Volume II, `/* ── Joypad Controller ── */` in Volume III |

Copy everything from a control's header down to the next header.

## 3. Bring the shared core with it

Controls lean on a small core at the top of each page's script. Copy the parts your control uses.

| Helper | What it does | Needed by |
|---|---|---|
| `SNAP`, `HEAVY`, `PRESS` | spring constants used across the whole atlas | anything that moves |
| `class Spring` | a damped spring: `new Spring(value, SNAP, onUpdate)`, then `.to(target)` or `.set(value)` | anything that moves |
| `reduce` | `true` when the visitor prefers reduced motion. Springs jump straight to their target | everything |
| `$`, `$$`, `clamp`, `svgEl` | small DOM and maths helpers | everything |
| `addLoop`, `watch` | one shared animation loop that pauses when a control scrolls off-screen | meters, platter, transport, thermostat, physics toys |
| `audio()`, `click()`, `tick()`, `thock()`, `clack()` | short synthesized clicks that start only after the visitor interacts | anything that makes a sound |
| `MASTER`, `bands()` | Volume II only: the page-wide volume bus and analyser | Monitor Pair, Excursion Pair, the Cadence Pads drums |
| `bindFinish()` | the Ivory / Obsidian switch | every card in Volume II |
| `makeFader`, `makeKnob`, `makeRotary` | shared builders for faders, knobs and dials | Volume II faders, knobs and dials |
| `makeToggle`, `makeHSlider` | shared builders for toggles and horizontal sliders | Volume III switches and sliders |

### Tokens

Keep the root tokens, or map them onto your own design system:

```css
:root {
  --accent: #CC0000;   /* Cinnabar signal */
  --ink: #111; --muted: #6e6e6e; --tile: #f5f6f7; --paper: #fff;
  --sans: "IBM Plex Sans", sans-serif;
  --mono: "IBM Plex Mono", monospace;
  --serif: "IBM Plex Serif", serif;   /* Volume III */
}
```

Load the fonts from Google Fonts:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,500;1,400&display=swap">
```

## 4. Wire it to your app

Every control already reports its state. Hook into the place where it writes its readout:

- **ARIA first.** Sliders set `aria-valuenow` and `aria-valuetext`. Switches set `aria-checked`. Latches set `aria-pressed`. Watch those attributes or read them on submit.
- **Callbacks.** Builders take an `onChange` or `onInput` callback, for example `makeToggle(btn, knob, { travel: 44, onChange: on => save(on) })`.
- **Remove the demo.** Simulations such as the thermostat's room, the VU signal and the camera's scenes are there to show the control working. Replace them with your real data source.

## 5. Remix rules

A remix belongs in the atlas when it passes these checks:

- [ ] **Palette:** black, white and one signal accent. Other colours only on sensors and gauges, where colour carries meaning, such as heat and cool.
- [ ] **Type:** IBM Plex Sans, Mono or Serif only.
- [ ] **Finishes:** an Ivory and an Obsidian version, switched with `data-finish`.
- [ ] **State at a glance:** someone can tell the state without reading the label, from a lamp, a colour, depth, position or a printed symbol.
- [ ] **Keyboard:** it works fully without a pointer, and the hint line says how.
- [ ] **Reduced motion:** it still works, with motion skipped, when `prefers-reduced-motion` is set.
- [ ] **Self-contained:** no libraries and no network calls.
- [ ] **Credit:** a `lineage` line naming the hardware or design it comes from.

## 6. Share a remix

1. Fork the repository.
2. Add your control as a new `<article class="unit">` card in the volume it fits. Include the description, the finish switch, a readout, a hint line, a lineage line and a Code Veil snippet.
3. Rebuild the standalone page: `volume-N/index.html` is the root source file with a `<!doctype html>` and `<head>` wrapper added.
4. Open a pull request with a short clip or screenshot of both finishes.

When you use a control outside this repository, credit it like this:

> Based on *Enochian UI UX Elements* by alanism / UnCommon Core (https://github.com/alanism/Enochian-UI-UX-Elements), CC BY-NC 4.0.

## 7. Interface components

Open [Volume IV](volume-4/index.html#pattern-index) to browse and try all 66 patterns. Search by a catalog name or an original name such as “Binary Gate.” Each result jumps to its example, and **Find a component** offers the same lookup from anywhere in the volume. Patch changes and bench transcript attachments belong to the current page session.

### Coverage map

All 66 entries in the [shadcn/ui Components catalog](https://ui.shadcn.com/docs/components) have one primary family below. Volume IV implements 59 in native HTML, CSS, and JavaScript and embeds seven live originals from Volumes I and III.

| Family | Volume IV | Existing Enochian controls |
|---|---|---|
| [Forms](volume-4/index.html#forms) | Field, Label, Input, Input Group, Native Select, Textarea, Checkbox, Radio Group, Date Picker (native date field), Calendar (inline grid), Combobox (editable search), Input OTP, Select (custom popup), Questionnaire | Slider and Switch ([Signal Slider](volume-4/index.html#original-slider) and [Binary Gate](volume-4/index.html#original-switch)) |
| [Navigation](volume-4/index.html#navigation) | Breadcrumb, Navigation Menu (section links), Sidebar, Tabs, Pagination, Menubar | — |
| [Overlays](volume-4/index.html#overlays) | Alert Dialog, Command, Context Menu, Dialog, Drawer (bottom edge), Dropdown Menu, Hover Card, Popover (disclosure), Sheet (side edge), Tooltip | — |
| [Feedback](volume-4/index.html#feedback) | Alert, Empty, Progress, Skeleton, Spinner, Toast | — |
| [Data display](volume-4/index.html#data-display) | Attachment, Badge, Bubble, Chart (bar chart), Data Table, Marker, Message, Message Scroller, Table, Trace | Code Block ([Code Veil](volume-4/index.html#original-code-block)) |
| [Layout](volume-4/index.html#layout) | Accordion, Aspect Ratio (CSS), Avatar (initials), Card, Carousel, Collapsible, Direction (scoped reading direction), Item, Kbd, Resizable, Scroll Area, Separator, Typography | Button, Button Group, Toggle, Toggle Group ([Push Button](volume-4/index.html#original-button), [Three Keys](volume-4/index.html#original-button-group), [Hollow Gate](volume-4/index.html#original-toggle), [Triad Action Keys](volume-4/index.html#original-toggle-group)) |

### Reuse

- Hover a pattern or turn on **Copy controls** to show its **Copy** action. Paste the copied code into a new `.html` file. Each export includes the markup, styles, and behavior it needs to run offline. Related patterns share code when their interactions depend on the same example. If clipboard access is blocked, the dialog selects the source for a manual copy.
- The seven originals export from their source volumes and keep their own finishes. Use **Open Volume I** or **Open Volume III** to reach the canonical control. The three Volume I exports include the [Motion browser runtime](assets/motion-11.18.2.js) under its [MIT license](assets/motion-LICENSE.md).
- Use Cinnabar for a meaningful action or state. Binary Gate's keyboard focus outline uses neutral ink. The original Cinnabar Switch uses red fill to indicate on.
- In Volume IV, the raised edge on a key invites a press, and the inset on a field invites entry. Flat badges, avatars, and readouts display information. Keep borders where they separate controls, content groups, or overlays. `--ring` uses neutral ink for focus, `--signal` marks selected controls, progress, and primary actions, and `--error` marks validation failures.
- Copy the matching handler for interactive patterns. Keep field labels and validation messages connected, tabs paired with their panels, and native dialogs paired with their accessible titles. Replace the demo patch array with your own data when reusing the table, inspector, or chart.
- Use the transcript's message template for author and content layout, its attachment template for a local file, and the marker for a checkpoint between turns. The scroller preserves the current reading position when older notes are added, and local reports appear as soon as they are ready. **Preview loading** demonstrates the spinner and skeleton independently of the diagnostics result.

Run the offline browser checks with `python -m unittest tests.test_interface_components -q`. They exercise catalog navigation, all seven live originals, all 66 exports, the patch workflow, overlays, transcript, layout, and finish switching.
