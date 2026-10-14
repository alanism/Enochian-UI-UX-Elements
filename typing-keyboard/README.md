# Enochian Typing Keyboard

A standalone, reusable HTML/CSS/JavaScript typing keyboard based on the supplied compact mechanical-keyboard references. It has 79 keys, the stepped ISO Enter shape, a six-row layout, two Enochian rotary controls, and a narrow live-clock display. Cinnabar `#CC0000` replaces the reference's orange on Escape, the four arrows, the signal switch, and display. The knobs use the atlas's layered caps, tick rings, bar and dot position markers. Ivory and Obsidian finishes change the chassis, caps, ink, and knobs together.

Open [`index.html`](index.html) directly, or serve the repository and visit `http://127.0.0.1:8765/typing-keyboard/`. No build, dependencies, images, font downloads, network calls, or persistence are required. IBM Plex font stacks use local sans-serif/monospace fallbacks when Plex is unavailable.

## Interaction

- Tap the keys to edit the demo textarea at its selection/caret. Backspace/Delete handle Unicode graphemes. Arrow keys move the caret; up/down move between lines. The demo is plain text, with no undo stack for virtual edits.
- Type with a physical keyboard while the surface or textarea is focused. Native editing and shortcuts remain native in the textarea. Space/Enter activates a focused virtual key. Typing elsewhere on the page is unaffected.
- Caps toggles virtual capitalization. Shift applies to one virtual character; holding a physical Shift also modifies virtual typing. Fn + F1/F2 adjusts backlight, Fn + F10 toggles sound, and Fn + F11/F12 adjusts volume. Other function/modifier keys emit events for the host application; they do not control the OS or external media.
- Both knobs support vertical drag, arrows ±1, Page Up/Down ±10, Home/End, and double-click reset. Volume starts at 40; backlight at 80. Backlight changes the display illumination while the clock remains readable.
- Sound starts off. Explicitly enable it for a short synthesized triangle-wave key thock. Volume adjusts its level. Blur, hiding the page, and teardown release held keys and close the native audio context. There is no microphone, MIDI, or uploaded audio.
- On small screens, the board pans horizontally within its own region. Keys retain at least 44-pixel targets. Tab focus and scroll bring the right-hand controls into view. Reduced-motion preference disables key/illumination transitions.

## Add to the showcase

The gallery lives on another laptop. Add this page to its study-copy list and link the new study to `studies/typing-keyboard/`. A thumbnail can be captured from the actual rendered board. The current gallery and existing typing-keyboard card are unchanged by this standalone addition.

For an embedded demonstration, use `index.html?embedded`. That hides only the page heading, reuse guide, and footer. Finish controls, textarea, keyboard, and status remain visible. Use a roughly 700-pixel iframe height, with ordinary scrolling available for smaller viewports:

```html
<iframe src="studies/typing-keyboard/?embedded"
        title="Enochian Typing Keyboard"
        style="width:100%;height:700px;border:0"></iframe>
```

## Reuse the component in a project

Copy the marked `.mk-*` stylesheet, `<section data-enochian-keyboard>` markup, and reusable component script. Replace the final **demo mounting** line with your own call. The keyboard can edit its included textarea or a supplied native textarea:

```js
const root = document.querySelector('[data-enochian-keyboard]');
const keyboard = EnochianKeyboard.mount(root, document.querySelector('textarea'));

root.addEventListener('enochian:keyboard-input', ({ detail }) => {
  // {value, selectionStart, selectionEnd}
  saveDraft(detail.value);
});

root.addEventListener('enochian:keyboard-key', ({ detail }) => {
  // {code, key, shift, capsLock, fn}
  // Route function keys and modifiers to your own application actions.
});

root.addEventListener('enochian:keyboard-parameter', ({ detail }) => {
  // {parameter: 'volume' | 'backlight', value: 0..100}
  updateYourControl(detail.parameter, detail.value);
});

// On component removal:
keyboard.destroy();
```

Events bubble from each component root. Key events report semantic values such as `a`, `Enter`, and `ArrowRight` for virtual/board actions; direct native editing in a textarea keeps its ordinary browser keyboard events. Native `input` events also fire on the edited textarea. The component uses scoped selectors and no element IDs; multiple instances retain independent text, finishes, modifiers, and knobs. Mounting the same root twice returns its existing controller. `destroy()` aborts listeners, stops the clock, releases held keys, closes audio, and removes generated key markup so the root can be mounted again. Read-only/disabled textareas cannot be edited by virtual keys.

## Verification

```powershell
python -m unittest tests.test_typing_keyboard -q
```

Acceptance checks use real Chromium and include selection/caret editing, Unicode deletion, physical/virtual modifier interaction, native key activation, knob drag/keyboard/reset, finish state, responsive containment and hit targets, scoped mounting/cleanup, and genuine Web Audio opt-in/teardown. Existing harness files are unchanged.

Based on *Enochian UI UX Elements* by alanism / UnCommon Core, CC BY-NC 4.0. This is an independent reference-inspired interaction study.
