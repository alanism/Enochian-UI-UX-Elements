"""Acceptance gates for the standalone reference-inspired typing keyboard."""
from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
from tests.transport_native import NATIVE_AUDIT

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'typing-keyboard/index.html'


class TypingKeyboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.assertTrue(PAGE.is_file(), 'The standalone typing-keyboard page is missing')
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.page.set_default_timeout(1500)
        self.errors, self.remote = [], []
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))
        self.page.on('request', lambda r: self.remote.append(r.url) if r.url.startswith(('http:', 'https:')) else None)
        self.page.add_init_script("window.keyboardEvents=[];for(const name of ['input','key','parameter'])document.addEventListener('enochian:keyboard-'+name,e=>keyboardEvents.push({name,...e.detail}));")
        self.page.goto(PAGE.as_uri())
        self.root = self.page.locator('[data-enochian-keyboard]').first
        self.output = self.root.get_by_role('textbox', name='Keyboard text')

    def key(self, code):
        return self.root.locator(f'[data-code="{code}"]')

    def test_reference_structure_palette_and_offline_initialization(self):
        self.assertEqual(self.root.locator('.mk-key').count(), 79)
        self.assertEqual(self.root.locator('[data-accent]').count(), 5)
        self.assertEqual(self.root.locator('[role=slider]').count(), 2)
        self.assertEqual(self.root.get_attribute('data-finish'), 'ivory')
        self.assertEqual(self.page.get_by_role('button', name='Sound off').get_attribute('aria-pressed'), 'false')
        self.assertEqual(self.root.evaluate("e=>getComputedStyle(e).getPropertyValue('--mk-accent').trim().toLowerCase()"), '#cc0000')
        self.assertRegex(self.root.locator('[data-clock]').inner_text(), r'\d{1,2}:\d{2}')
        self.assertEqual(self.remote, [])
        self.assertEqual(self.errors, [])

    def test_board_keeps_the_reference_aspect_ratio_across_viewports(self):
        for width in [390, 1440, 2048]:
            self.page.set_viewport_size({'width':width,'height':1152})
            box = self.root.locator('.mk-board').bounding_box()
            self.assertAlmostEqual(box['width']/box['height'], 2.54, delta=.005)

    def test_right_arrow_shares_the_bottom_row_and_arrow_spacing(self):
        for width in [390, 1440, 2048]:
            self.page.set_viewport_size({'width':width,'height':1152})
            for finish in ['ivory', 'obsidian']:
                self.root.locator(f'[data-finish-choice={finish}]').click()
                left, down, right = [self.key(code).bounding_box() for code in ['ArrowLeft','ArrowDown','ArrowRight']]
                self.assertAlmostEqual(right['y'], down['y'], delta=.1)
                self.assertAlmostEqual(right['height'], down['height'], delta=.1)
                self.assertAlmostEqual(right['x']-down['x']-down['width'], down['x']-left['x']-left['width'], delta=.1)

    def test_display_is_clear_of_parameter_readouts(self):
        screen = self.root.locator('.mk-screen')
        self.assertEqual(screen.locator('.mk-levels,[data-volume-value],[data-light-value]').count(), 0)
        self.assertNotRegex(screen.inner_text(), r'(?i)\bvol(?:ume)?\b|\blight\b')
        self.assertRegex(screen.locator('[data-clock]').inner_text(), r'\d{1,2}:\d{2}')

    def test_virtual_typing_edits_the_caret_selection_and_modifiers(self):
        self.key('KeyA').click()
        self.key('KeyB').click()
        self.assertEqual(self.output.input_value(), 'ab')
        self.output.evaluate('e=>e.setSelectionRange(0,1)')
        self.key('KeyC').click()
        self.assertEqual(self.output.input_value(), 'cb')
        self.key('Backspace').click()
        self.assertEqual(self.output.input_value(), 'b')
        self.key('ShiftLeft').click()
        self.key('Digit1').click()
        self.assertEqual(self.output.input_value(), '!b')
        self.assertEqual(self.key('ShiftLeft').get_attribute('aria-pressed'), 'false')
        self.key('CapsLock').click()
        self.key('KeyA').click()
        self.key('ArrowRight').click()
        self.key('Delete').click()
        self.assertEqual(self.output.input_value(), '!Ab')
        self.key('Enter').click()
        self.assertEqual(self.output.input_value(), '!Ab\n')
        self.assertTrue(self.page.evaluate("keyboardEvents.some(e=>e.name==='input'&&e.value==='!Ab\\n')"))

    def test_physical_typing_native_editor_and_key_release(self):
        self.root.locator('.mk-board').focus()
        self.page.keyboard.down('a')
        self.assertEqual(self.key('KeyA').get_attribute('data-down'), 'true')
        self.assertEqual(self.output.input_value(), 'a')
        self.page.keyboard.up('a')
        self.assertEqual(self.key('KeyA').get_attribute('data-down'), 'false')
        self.output.fill('native')
        self.output.focus()
        self.page.keyboard.press('End')
        self.page.keyboard.press('x')
        self.assertEqual(self.output.input_value(), 'nativex')
        self.key('KeyZ').focus()
        self.page.keyboard.press('Enter')
        self.assertEqual(self.output.input_value(), 'nativexz')
        self.assertEqual(self.root.locator('[data-down=true]').count(), 0)
        self.assertEqual(self.errors, [])

    def test_knobs_keyboard_drag_reset_and_finish_preserve_state(self):
        volume = self.root.get_by_role('slider', name='Volume')
        light = self.root.get_by_role('slider', name='Backlight')
        volume.focus()
        self.page.keyboard.press('End')
        self.assertEqual(volume.get_attribute('aria-valuenow'), '100')
        light.focus()
        self.page.keyboard.press('Home')
        self.page.keyboard.press('PageUp')
        self.assertEqual(light.get_attribute('aria-valuenow'), '10')
        self.assertAlmostEqual(float(self.root.evaluate("e=>getComputedStyle(e).getPropertyValue('--mk-light')")), .172)
        box = light.bounding_box()
        self.page.mouse.move(box['x']+box['width']/2, box['y']+box['height']/2)
        self.page.mouse.down()
        self.page.mouse.move(box['x']+box['width']/2, box['y']+box['height']/2-60)
        self.page.mouse.up()
        self.assertGreater(int(light.get_attribute('aria-valuenow')), 10)
        light.dblclick()
        self.assertEqual(light.get_attribute('aria-valuenow'), '80')
        self.page.get_by_role('button', name='Obsidian', exact=True).click()
        self.assertEqual(self.root.get_attribute('data-finish'), 'obsidian')
        self.assertEqual(volume.get_attribute('aria-valuenow'), '100')
        self.assertEqual(volume.get_attribute('aria-valuetext'), '100 percent')
        self.assertTrue(self.page.evaluate("keyboardEvents.some(e=>e.name==='parameter'&&e.parameter==='volume'&&e.value===100)"))
        self.assertEqual(self.errors, [])

    def test_blur_releases_held_keys_and_cancelled_knob_drag(self):
        self.root.locator('.mk-board').focus()
        self.page.keyboard.down('a')
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        self.assertEqual(self.root.locator('[data-down=true]').count(), 0)
        self.page.keyboard.up('a')
        knob = self.root.get_by_role('slider', name='Volume')
        box = knob.bounding_box()
        x, y = box['x']+box['width']/2, box['y']+box['height']/2
        self.page.mouse.move(x,y)
        self.page.mouse.down()
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        self.page.mouse.move(x,y-30)
        self.page.mouse.up()
        self.assertEqual(knob.get_attribute('aria-valuenow'), '40')
        self.assertEqual(self.errors, [])

    def test_focused_mobile_scroll_region_uses_native_arrow_panning(self):
        self.page.set_viewport_size({'width':390,'height':844})
        region = self.root.locator('.mk-scroll')
        region.focus()
        self.page.keyboard.press('ArrowRight')
        self.page.wait_for_function("document.querySelector('.mk-scroll').scrollLeft>0", timeout=700)
        self.assertEqual(self.output.input_value(), '')

    def test_hardware_shift_applies_to_virtual_keys_and_native_caps_syncs(self):
        self.root.locator('.mk-board').focus()
        self.page.keyboard.down('Shift')
        self.key('KeyA').click()
        self.page.keyboard.up('Shift')
        self.assertEqual(self.output.input_value(), 'A')
        self.output.focus()
        self.page.keyboard.press('CapsLock')
        self.key('KeyB').click()
        self.assertEqual(self.output.input_value(), 'AB')

    def test_virtual_backspace_preserves_unicode_graphemes(self):
        self.output.fill('A👨‍👩‍👧‍👦')
        self.output.evaluate('e=>e.setSelectionRange(e.value.length,e.value.length)')
        self.key('Backspace').click()
        self.assertEqual(self.output.input_value(), 'A')

    def test_reuse_key_events_contain_semantic_keys_instead_of_rendered_icons(self):
        self.key('KeyA').click()
        self.key('ArrowRight').click()
        events = self.page.evaluate("keyboardEvents.filter(e=>e.name==='key')")
        self.assertEqual(events[-2]['key'], 'a')
        self.assertEqual(events[-1]['key'], 'ArrowRight')

    def test_sound_requires_opt_in_uses_native_audio_and_closes_on_blur(self):
        self.page.add_init_script(NATIVE_AUDIT)
        self.page.reload()
        self.key('KeyA').click()
        self.assertEqual(self.page.evaluate('__audioAudit.contexts.length'), 0)
        self.page.get_by_role('button', name='Sound off').click()
        self.key('KeyB').click()
        self.page.wait_for_function('__audioAudit.sources.some(s=>s.ended&&s.disconnected)')
        self.assertEqual(self.page.evaluate('__audioAudit.contexts.length'), 1)
        self.assertTrue(self.page.evaluate('__audioAudit.sources[0].started'))
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        self.page.wait_for_function("__audioAudit.contexts.every(c=>c.state==='closed')")
        self.assertEqual(self.page.get_by_role('button', name='Sound off').get_attribute('aria-pressed'), 'false')
        self.assertEqual(self.errors, [])

    def test_reuse_is_scoped_idempotent_and_can_be_destroyed(self):
        self.page.evaluate("""() => {
            const first=document.querySelector('[data-enochian-keyboard]');
            const second=first.cloneNode(true);
            second.querySelector('[data-keyboard-keys]').replaceChildren();
            second.querySelector('.mk-rail>.mk-key').remove();
            second.dataset.instance='second';
            first.after(second);
            EnochianKeyboard.mount(second);
            EnochianKeyboard.mount(second);
        }""")
        second = self.page.locator('[data-instance=second]')
        self.assertEqual(second.locator('.mk-key').count(), 79)
        second.locator('[data-code=KeyB]').click()
        self.assertEqual(second.get_by_role('textbox', name='Keyboard text').input_value(), 'b')
        self.assertEqual(self.output.input_value(), '')
        second.get_by_role('button', name='Obsidian', exact=True).click()
        self.assertEqual(self.root.get_attribute('data-finish'), 'ivory')
        self.page.evaluate("document.querySelector('[data-instance=second]').enochianKeyboard.destroy()")
        self.assertEqual(second.locator('.mk-key').count(), 0)
        self.key('KeyA').click()
        self.assertEqual(self.output.input_value(), 'a')
        self.assertEqual(self.errors, [])

    def test_mobile_contains_page_and_keeps_every_control_reachable(self):
        for width in [280, 390, 768, 1440]:
            with self.subTest(width=width):
                self.page.set_viewport_size({'width':width,'height':1000})
                self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth-innerWidth'), 0)
                small = self.root.locator('.mk-key,[role=slider]').evaluate_all("els=>els.filter(e=>{const r=e.getBoundingClientRect();return r.width<44||r.height<44}).map(e=>e.dataset.code||e.getAttribute('aria-label'))")
                self.assertEqual(small, [])
                for code in ['Escape', 'Enter', 'ArrowRight']:
                    button = self.key(code)
                    button.scroll_into_view_if_needed()
                    self.assertTrue(button.evaluate("e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}"))
        self.assertEqual(self.errors, [])


if __name__ == '__main__':
    unittest.main()
