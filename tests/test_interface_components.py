"""Browser acceptance checks for the standalone interface volume."""
from pathlib import Path
import unittest

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]


class InterfaceComponentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(offline=True, reduced_motion='reduce')
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.addCleanup(lambda: self.assertEqual(self.errors, []))
        self.page.goto((ROOT / 'index.html').as_uri())
        self.page.get_by_role('link', name='Interface components').click(timeout=2000)
        expect(self.page.get_by_role('heading', name='Interface components', exact=True)).to_be_visible()

    def test_form_validation_save_and_library_states(self):
        page = self.page
        name = page.get_by_role('textbox', name='Patch name')
        page.get_by_role('button', name='Save patch').click()
        expect(name).to_be_focused()
        expect(name).to_have_attribute('aria-invalid', 'true')
        name.fill('9th harmonic')
        expect(name).not_to_have_attribute('aria-invalid', 'true')
        page.get_by_label('Bank', exact=True).select_option('Rhythm')
        page.get_by_role('radio', name='External').check()
        page.get_by_role('checkbox', name='Pin to front panel').check()
        page.get_by_role('button', name='Save patch').click()
        expect(page.get_by_role('status').filter(has_text='9th harmonic saved.')).to_be_visible()

        search = page.get_by_role('searchbox', name='Filter patches')
        search.fill('9th harmonic')
        patch = page.get_by_role('button', name='9th harmonic')
        expect(patch).to_be_visible()
        patch.click()
        inspector = page.get_by_role('dialog', name='Patch inspector')
        expect(inspector.get_by_text('External', exact=True)).to_be_visible()
        expect(inspector.get_by_text('Pinned')).to_be_visible()
        page.keyboard.press('Escape')
        expect(patch).to_be_focused()
        search.fill('no such patch')
        expect(page.get_by_role('heading', name='No matching patches')).to_be_visible()
        page.get_by_role('button', name='Clear filter', exact=True).click()
        expect(search).to_be_focused()
        page.get_by_role('button', name='Next page').click()
        expect(page.get_by_text('Page 2 of 2', exact=True)).to_be_visible()
        page.get_by_role('button', name='Sort by patch name').click()
        expect(page.get_by_role('columnheader', name='Sort by patch name')).to_have_attribute('aria-sort', 'descending')

    def test_catalog_indexes_every_pattern_and_jumps_to_exact_examples(self):
        page = self.page
        catalog = page.get_by_role('region', name='Browse all 66 patterns')
        links = catalog.get_by_role('link')
        expect(links).to_have_count(66, timeout=2000)
        names = [link.inner_text().strip() for link in links.all()]
        self.assertEqual(len(set(names)), 66)
        for link in links.all():
            self.assertEqual(page.locator(link.get_attribute('href')).count(), 1)
        lookup = catalog.get_by_role('searchbox', name='Search patterns')
        lookup.fill('Binary Gate')
        expect(links).to_have_count(1)
        expect(links.first).to_have_text('Switch')
        lookup.fill('combobox')
        links.first.click()
        expect(page.get_by_role('combobox', name='Find a patch')).to_be_focused()
        page.get_by_role('button', name='Find a component').click()
        command = page.get_by_role('dialog', name='Find a component')
        command.get_by_role('searchbox').fill('Carousel')
        command.get_by_role('button', name='Carousel', exact=True).click()
        expect(page.get_by_role('region', name='Bank carousel')).to_be_focused()

    def test_catalog_keeps_secondary_copy_actions_quiet_until_requested(self):
        page = self.page
        page.mouse.move(0, 0)
        catalog = page.get_by_role('region', name='Browse all 66 patterns')
        copies = catalog.get_by_role('button', name='Copy Code for')
        expect(copies).to_have_count(0, timeout=1500)
        expect(catalog.locator('.pattern-group').first).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

        calendar = catalog.get_by_role('link', name='Calendar', exact=True)
        calendar.hover()
        action = catalog.get_by_role('button', name='Copy Code for Calendar')
        expect(action).to_be_visible()
        expect(action).to_have_css('box-shadow', 'none')
        page.mouse.move(0, 0)
        expect(action).to_be_hidden()

        toggle = catalog.get_by_role('button', name='Copy controls')
        toggle.press('Space')
        expect(toggle).to_have_attribute('aria-pressed', 'true')
        expect(copies).to_have_count(66)
        page.set_viewport_size({'width': 320, 'height': 844})
        self.assertTrue(page.evaluate('document.documentElement.scrollWidth === innerWidth'))
        toggle.press('Space')
        expect(copies).to_have_count(0)

    def test_rail_tracks_visible_section_after_scrolling_away_from_a_link(self):
        page = self.page
        navigation = page.get_by_role('navigation', name='Component families')
        layout = navigation.get_by_role('link', name='Layout', exact=True)
        layout.click()
        expect(layout).to_have_attribute('aria-current', 'location')
        page.locator('#pattern-index').evaluate("(el) => el.scrollIntoView({block: 'start'})")
        expect(navigation.get_by_role('link', name='Browse all', exact=True)).to_have_attribute('aria-current', 'location', timeout=1500)
        self.assertTrue(page.url.endswith('#layout'))

    def test_seven_original_controls_work_in_offline_previews(self):
        page = self.page
        page.set_viewport_size({'width': 390, 'height': 844})
        requests = []
        page.on('request', lambda request: requests.append(request.url) if request.url.startswith(('https:', 'http:')) else None)
        catalog = page.get_by_role('region', name='Browse all 66 patterns')
        cases = [
            ('Slider', 'Signal Slider', '#trk', 'aria-valuenow', '36', 'ArrowRight'),
            ('Switch', 'Binary Gate', '#std', 'aria-checked', 'true', 'Space'),
            ('Code Block', 'Code Veil', '#codeToggle', 'aria-checked', 'true', 'Enter'),
            ('Button', 'Push Button', '#concaveButton', 'aria-pressed', 'true', None),
            ('Button Group', 'The Three Keys', '#abtns .ab-red', 'aria-pressed', 'true', 'Space'),
            ('Toggle', 'Hollow Gate', '#ccv', 'aria-pressed', 'true', 'Enter'),
            ('Toggle Group', 'Triad Action Keys', '#tpb [aria-label="Record"]', 'aria-pressed', 'true', 'Space'),
        ]
        self.assertEqual(page.locator('iframe[src]').count(), 0)
        for name, title, selector, attribute, value, key in cases:
            with self.subTest(pattern=name):
                catalog.get_by_role('link', name=name, exact=True).click(timeout=2000)
                frame_element = page.locator(f'iframe[title="{title}"]')
                expect(frame_element).to_be_visible()
                frame = frame_element.content_frame
                control = frame.locator(selector)
                expect(control).to_be_visible()
                expect(frame.locator('header').first).not_to_be_visible()
                self.assertTrue(frame.locator('body').evaluate('(el) => el.scrollWidth <= innerWidth'))
                if name == 'Button Group':
                    frame.get_by_role('button', name='latch', exact=True).click()
                if key:
                    control.press(key)
                    expect(control).to_have_attribute(attribute, value)
                else:
                    control.focus()
                    page.keyboard.down('Space')
                    expect(control).to_have_attribute(attribute, value)
                    page.keyboard.up('Space')
                    expect(frame.get_by_text('1 press', exact=True)).to_be_visible()
                if name == 'Code Block':
                    expect(frame.get_by_role('button', name='COPY', exact=True)).to_be_visible()
                    preview = page.locator('#original-code-block')
                    preview.locator('summary').click()
                    expect(frame_element).not_to_be_visible()
                    preview.locator('summary').click()
                    expect(control).to_have_attribute('aria-checked', 'true')
        self.assertEqual(requests, [])

    def test_binary_gate_uses_original_materials_and_neutral_focus(self):
        page = self.page
        page.get_by_text('Obsidian', exact=True).click()
        page.locator('#pattern-groups a[href="#original-switch"]').click()
        frame = page.frame_locator('#original-switch iframe')
        control = frame.get_by_role('switch', name='Binary Gate')
        control.focus(timeout=2000)
        expect(control).to_have_css('outline-color', 'rgb(17, 17, 17)', timeout=1500)
        expect(frame.locator('#c-std .card')).to_have_css('background-color', 'rgb(245, 246, 247)')
        frame.get_by_role('button', name='OBSIDIAN', exact=True).click()
        control.press('ArrowRight')
        expect(control).to_have_css('outline-color', 'rgb(247, 247, 248)')
        expect(control).to_have_attribute('aria-checked', 'true')

    def test_volume_four_uses_neutral_focus_and_reserves_red_for_signals(self):
        page = self.page
        for finish, ink, muted, error in [
            ('Ivory', 'rgb(23, 23, 25)', 'rgb(93, 94, 100)', 'rgb(204, 0, 0)'),
            ('Obsidian', 'rgb(247, 247, 248)', 'rgb(173, 174, 181)', 'rgb(255, 101, 101)'),
        ]:
            with self.subTest(finish=finish):
                page.get_by_text(finish, exact=True).click()
                field = page.get_by_role('textbox', name='Patch name')
                field.focus()
                expect(field).to_have_css('outline-color', ink, timeout=1500)

                page.get_by_role('button', name='Save patch').click()
                expect(field).to_have_css('border-top-color', error)
                expect(field).to_have_css('outline-color', ink)
                expect(page.get_by_text('Enter a patch name.')).to_have_css('color', error)

                code = page.get_by_role('textbox', name='Bench code')
                code.focus()
                expect(page.locator('.otp [data-active]')).to_have_css('outline-color', ink)

                picker = page.get_by_role('combobox', name='Select patch bank')
                picker.press('ArrowDown')
                expect(page.locator('#bank-options [data-active]')).to_have_css('outline-color', ink)
                picker.press('Escape')

                page.get_by_role('grid', name='Review calendar').locator('button[tabindex="0"]').press('Enter')
                selected = page.locator('#calendar-days [aria-selected="true"] button')
                expect(selected).to_have_css('background-color', 'rgb(204, 0, 0)')
                expect(page.locator('#chart .bar span').first).to_have_css('background-color', muted)

                transcript = page.locator('.message[data-author="you"] .message-bubble').first
                self.assertEqual(
                    transcript.evaluate('(el) => getComputedStyle(el).borderInlineEndColor'),
                    transcript.evaluate('(el) => getComputedStyle(el).borderInlineStartColor'),
                )

    def test_copy_code_exports_runnable_source_for_all_catalog_patterns(self):
        page = self.page
        page.evaluate("""Object.defineProperty(navigator, 'clipboard', { value: {
            writeText: async value => { window.copiedPattern = value; }
        } })""")
        catalog = page.get_by_role('region', name='Browse all 66 patterns')
        catalog.get_by_role('button', name='Copy controls').click()
        buttons = catalog.get_by_role('button', name='Copy Code for')
        expect(buttons).to_have_count(66)
        example = self.context.new_page()
        errors = []
        external = []
        example.on('pageerror', lambda error: errors.append(str(error)))
        example.on('request', lambda request: external.append(request.url))
        originals = {
            'Slider': '#trk', 'Switch': '#std', 'Button': '#concaveButton',
            'Button Group': '#abtns', 'Code Block': '#codeToggle',
            'Toggle': '#ccv', 'Toggle Group': '#tpb'
        }
        for button in buttons.all():
            name = button.get_attribute('aria-label').removeprefix('Copy Code for ')
            with self.subTest(pattern=name):
                page.evaluate('window.copiedPattern = null')
                button.evaluate('(el) => el.click()')
                page.wait_for_function('typeof window.copiedPattern === "string"', timeout=6000)
                code = page.evaluate('window.copiedPattern')
                self.assertTrue(code.startswith('<!doctype html>'))
                example.set_content(code, wait_until='domcontentloaded')
                self.assertEqual(example.locator('#pattern-index input').count(), 0)
                if name in originals:
                    expect(example.locator(originals[name])).to_be_visible()
                else:
                    self.assertEqual(
                        example.locator('html').evaluate("(el) => getComputedStyle(el).getPropertyValue('--ring').trim()"),
                        '#171719',
                    )
                if name == 'Slider':
                    control = example.locator('#trk')
                    control.press('End')
                    expect(control).to_have_attribute('aria-valuenow', '100')
                elif name == 'Switch':
                    control = example.get_by_role('switch', name='Binary Gate')
                    control.press('ArrowRight')
                    expect(control).to_have_attribute('aria-checked', 'true')
                    expect(control).to_have_css('outline-color', 'rgb(17, 17, 17)')
                elif name == 'Button':
                    example.locator('#concaveButton').press('Space')
                    expect(example.get_by_text('1 press', exact=True)).to_be_visible()
                elif name == 'Button Group':
                    example.get_by_role('button', name='latch', exact=True).click()
                    control = example.locator('#abtns .ab-red')
                    control.press('Space')
                    expect(control).to_have_attribute('aria-pressed', 'true')
                elif name == 'Toggle':
                    control = example.locator('#ccv')
                    control.press('Enter')
                    expect(control).to_have_attribute('aria-pressed', 'true')
                elif name == 'Toggle Group':
                    control = example.get_by_role('button', name='Record', exact=True)
                    control.press('Space')
                    expect(control).to_have_attribute('aria-pressed', 'true')
                elif name == 'Code Block':
                    example.locator('#codeToggle').press('Space')
                    expect(example.get_by_role('button', name='COPY', exact=True)).to_be_visible()
                elif name == 'Combobox':
                    control = example.get_by_role('combobox', name='Find a patch')
                    control.fill('cad')
                    control.press('ArrowDown')
                    control.press('Enter')
                    expect(control).to_have_value('Cadence Kit')
                elif name == 'Spinner':
                    example.get_by_role('button', name='Preview loading').click()
                    expect(example.locator('#diagnostic-placeholder .spinner')).to_be_visible()
                    example.get_by_role('button', name='Run diagnostics').click()
                    expect(example.locator('#diagnostic-placeholder')).to_be_hidden()
                elif name == 'Avatar':
                    expect(example.locator('.avatar').first).to_have_css('box-shadow', 'none')
                self.assertEqual(errors, [])
        self.assertEqual(external, [])
        example.close()

    def test_copy_code_offers_selectable_source_when_clipboard_is_blocked(self):
        page = self.page
        page.evaluate("""Object.defineProperty(navigator, 'clipboard', { value: {
            writeText: async () => { throw new Error('Clipboard denied'); }
        } })""")
        page.get_by_role('button', name='Copy controls').click()
        page.get_by_role('button', name='Copy Code for Checkbox', exact=True).click()
        dialog = page.get_by_role('dialog', name='Copy Code')
        text = dialog.get_by_role('textbox', name='Pattern source code')
        expect(text).to_be_focused()
        self.assertIn('type="checkbox"', text.input_value())
        self.assertTrue(text.evaluate('(el) => el.selectionEnd - el.selectionStart === el.value.length'))

    def test_keyboard_tabs_command_and_confirmation_restore_focus(self):
        page = self.page
        page.get_by_role('tab', name='Signal').focus()
        page.keyboard.press('ArrowRight')
        expect(page.get_by_role('tab', name='Routing')).to_be_focused()
        expect(page.get_by_role('tabpanel', name='Routing')).to_be_visible()

        launcher = page.get_by_role('button', name='Find a component')
        launcher.click()
        command = page.get_by_role('dialog', name='Find a component')
        query = command.get_by_role('searchbox')
        expect(query).to_be_focused()
        query.fill('layout')
        page.keyboard.press('ArrowDown')
        expect(command.get_by_role('button', name='Layout')).to_be_focused()
        page.keyboard.press('Enter')
        expect(command).not_to_be_visible()
        expect(page.get_by_role('heading', name='Layout', exact=True, level=2)).to_be_focused()

        page.set_viewport_size({'width': 880, 'height': 800})
        menu = page.get_by_role('button', name='Patch actions')
        menu.focus()
        page.keyboard.press('ArrowDown')
        expect(page.get_by_role('menuitem', name='Create a patch')).to_be_focused()
        page.keyboard.press('ArrowDown')
        expect(page.get_by_role('menuitem', name='Browse library')).to_be_focused()
        self.assertTrue(page.evaluate('document.documentElement.scrollWidth === innerWidth'))
        page.keyboard.press('Escape')
        expect(menu).to_be_focused()

        trigger = page.get_by_role('button', name='Reset library')
        trigger.click()
        confirmation = page.get_by_role('alertdialog', name='Reset the patch library?')
        expect(confirmation.get_by_role('button', name='Keep patches')).to_be_focused()
        page.keyboard.press('Escape')
        expect(trigger).to_be_focused()
        trigger.click()
        confirmation.get_by_role('button', name='Reset demo').click()
        expect(page.get_by_text('Library reset.')).to_be_visible()

    def test_finish_persistence_mobile_and_feedback(self):
        page = self.page
        page.set_viewport_size({'width': 390, 'height': 844})
        page.get_by_text('Obsidian', exact=True).click()
        page.reload()
        expect(page.get_by_role('radio', name='Obsidian')).to_be_checked()
        expect(page.locator('html')).to_have_attribute('data-finish', 'obsidian')
        self.assertTrue(page.evaluate('document.documentElement.scrollWidth === innerWidth'))
        page.get_by_role('radio', name='Obsidian').focus()
        page.keyboard.press('ArrowLeft')
        expect(page.get_by_role('radio', name='Ivory')).to_be_checked()
        expect(page.locator('html')).to_have_attribute('data-finish', 'ivory')

        page.get_by_role('button', name='Run diagnostics').click()
        expect(page.get_by_role('progressbar', name='Diagnostics progress')).to_be_visible()
        expect(page.get_by_text('Diagnostics complete.')).to_be_visible()
        expect(page.get_by_role('progressbar', name='Diagnostics progress')).to_have_attribute('value', '100')

    def test_depth_supports_controls_and_loading_is_a_preview(self):
        page = self.page
        for finish in ('Ivory', 'Obsidian'):
            with self.subTest(finish=finish):
                page.get_by_text(finish, exact=True).click()
                for selector in ('#related-study-list .avatar', '#signal-panel', '#chart .bar', '.menubar'):
                    expect(page.locator(selector).first).to_have_css('box-shadow', 'none', timeout=1500)
                expect(page.locator('#diagnostic-value')).to_have_css('border-top-width', '0px')
                expect(page.get_by_role('textbox', name='Patch name')).not_to_have_css('box-shadow', 'none')
                expect(page.get_by_role('button', name='Save patch')).not_to_have_css('box-shadow', 'none')

        preview = page.get_by_role('button', name='Preview loading')
        placeholder = page.locator('#diagnostic-placeholder')
        expect(placeholder).to_be_hidden()
        preview.press('Space')
        expect(preview).to_have_attribute('aria-pressed', 'true')
        expect(placeholder.locator('.spinner')).to_be_visible()
        expect(placeholder.locator('.spinner')).to_have_css('animation-name', 'none')
        expect(placeholder.locator('.skeleton').first).to_be_visible()

        snapshot = page.get_by_role('button', name='Run diagnostics').evaluate("""button => {
            button.click();
            return {
                progress: document.querySelector('#progress').value,
                result: document.querySelector('#diagnostic-status').textContent,
                previewHidden: document.querySelector('#diagnostic-placeholder').hidden,
            };
        }""")
        self.assertEqual(snapshot, {
            'progress': 100,
            'result': 'Diagnostics complete. 6 patches checked.',
            'previewHidden': True,
        })
        expect(preview).to_have_attribute('aria-pressed', 'false')

    def test_calendar_select_combobox_otp_and_questionnaire(self):
        page = self.page
        calendar = page.get_by_role('grid', name='Review calendar')
        day = calendar.locator('button[tabindex="0"]')
        day.focus(timeout=2000)
        page.keyboard.press('ArrowRight')
        selected_date = calendar.locator('button:focus').get_attribute('data-date')
        page.keyboard.press('Enter')
        expect(page.locator('#review-date')).to_have_value(selected_date)
        month = page.locator('#calendar-month').inner_text()
        page.get_by_role('button', name='Next month').click()
        expect(page.locator('#calendar-month')).not_to_have_text(month)

        select = page.get_by_role('combobox', name='Select patch bank')
        select.press('ArrowDown')
        select.press('End')
        select.press('Enter')
        expect(page.get_by_label('Bank', exact=True)).to_have_value('Utility')
        combo = page.get_by_role('combobox', name='Find a patch')
        combo.fill('cad')
        expect(page.get_by_role('option', name='Cadence Kit')).to_be_visible()
        combo.press('ArrowDown')
        combo.press('Enter')
        expect(combo).to_have_value('Cadence Kit')
        expect(page.get_by_role('tabpanel', name='Signal')).to_contain_text('Cadence Kit')

        access = page.get_by_role('textbox', name='Bench code')
        access.fill('314-159')
        expect(access).to_have_value('314159')
        page.get_by_role('button', name='Verify code').click()
        expect(page.get_by_text('Bench code accepted.')).to_be_visible()

        questionnaire = page.get_by_role('form', name='Inspection setup')
        questionnaire.get_by_role('button', name='Next step').click()
        expect(questionnaire.get_by_text('Choose a bank to continue.')).to_be_visible()
        questionnaire.get_by_role('radio', name='Signal').check()
        questionnaire.get_by_role('button', name='Next step').click()
        questionnaire.get_by_role('checkbox', name='Check routing').check()
        questionnaire.get_by_role('button', name='Back', exact=True).click()
        expect(questionnaire.get_by_role('radio', name='Signal')).to_be_checked()
        questionnaire.get_by_role('button', name='Next step').click()
        expect(questionnaire.get_by_role('checkbox', name='Check routing')).to_be_checked()
        questionnaire.get_by_role('button', name='Skip checks').click()
        questionnaire.get_by_role('textbox', name='Inspection notes').fill('Check the front panel.')
        questionnaire.get_by_role('button', name='Save inspection').click()
        expect(questionnaire.get_by_text('Check the front panel.', exact=True)).to_be_visible()
        expect(questionnaire.get_by_text('No checks selected.')).to_be_visible()

    def test_menubar_context_menu_drawer_and_hover_card(self):
        page = self.page
        menubar = page.get_by_role('menubar', name='Patch workbench')
        patch_menu = menubar.get_by_role('menuitem', name='Patch', exact=True)
        patch_menu.focus(timeout=2000)
        page.keyboard.press('ArrowRight')
        view_menu = menubar.get_by_role('menuitem', name='View', exact=True)
        expect(view_menu).to_be_focused()
        page.keyboard.press('ArrowDown')
        expect(page.get_by_role('menuitem', name='Browse library')).to_be_focused()
        page.keyboard.press('Escape')
        expect(view_menu).to_be_focused()

        context = page.get_by_role('button', name='Patch card context menu')
        context.click(button='right')
        expect(page.get_by_role('menuitem', name='Inspect selected patch')).to_be_focused()
        page.keyboard.press('Escape')
        expect(context).to_be_focused()
        page.keyboard.press('Shift+F10')
        expect(page.get_by_role('menu', name='Patch card context menu')).to_be_visible()
        page.get_by_role('menuitem', name='Toggle front-panel pin').click()
        expect(page.get_by_text('Aether Receiver unpinned.')).to_be_visible()
        expect(context).to_be_focused()

        drawer_trigger = page.get_by_role('button', name='Open patch drawer')
        drawer_trigger.click()
        drawer = page.get_by_role('dialog', name='Patch drawer')
        expect(drawer).to_be_visible()
        expect(drawer.get_by_role('button', name='Close drawer')).to_be_focused()
        page.keyboard.press('Escape')
        expect(drawer_trigger).to_be_focused()

        preview = page.get_by_role('link', name='Preview the typing keyboard')
        preview.focus()
        card = page.get_by_text('Tactile text entry with a live display and two finishes.')
        expect(card).to_be_visible()
        page.keyboard.press('Escape')
        expect(card).not_to_be_visible()
        preview.click()
        expect(page.get_by_role('group', name='Enochian mechanical keyboard')).to_be_visible(timeout=1500)

    def test_transcript_file_bubble_marker_and_trace(self):
        page = self.page
        thread = page.get_by_role('region', name='Session transcript')
        expect(thread.get_by_role('log')).to_be_visible(timeout=2000)
        older = page.get_by_role('button', name='Load earlier notes')
        older.click()
        expect(thread.get_by_text('Bench powered on.')).to_be_attached()
        page.get_by_role('button', name='Add session marker').click()
        expect(thread.get_by_text('Session checkpoint', exact=True)).to_be_visible()

        file = page.get_by_label('Attach a local file')
        file.set_input_files({'name': 'patch.txt', 'mimeType': 'text/plain', 'buffer': b'Local patch test'})
        expect(page.get_by_role('button', name='Remove attachment')).to_be_visible()
        page.get_by_role('textbox', name='Bench note').fill('Check my signal patch.')
        reply = page.get_by_role('button', name='Send bench note').evaluate("""button => {
            button.click();
            return document.querySelector('#transcript-log li:last-child .message-bubble').textContent;
        }""")
        self.assertEqual(reply, 'Patch report ready.')
        expect(thread.locator('.message-bubble').get_by_text('Check my signal patch.')).to_be_visible()
        expect(thread.get_by_role('link', name='patch.txt')).to_have_attribute('download', 'patch.txt')
        expect(thread.get_by_text('Patch report ready.')).to_be_visible()
        thread.get_by_text('Read the selected patch').click()
        expect(thread.get_by_text('Aether Receiver · Signal bank', exact=True)).to_be_visible()
        page.get_by_role('button', name='Jump to latest note').click()
        self.assertTrue(thread.evaluate('(el) => el.scrollHeight - el.clientHeight - el.scrollTop < 3'))

    def test_carousel_direction_and_resizable(self):
        page = self.page
        carousel = page.get_by_role('region', name='Bank carousel')
        carousel.get_by_role('button', name='Next bank').click(timeout=2000)
        expect(carousel.get_by_role('heading', name='Rhythm bank')).to_be_visible()
        carousel.get_by_role('button', name='Previous bank').press('ArrowLeft')
        expect(carousel.get_by_role('heading', name='Signal bank')).to_be_visible()
        grip = page.get_by_role('separator', name='Resize patch panes')
        grip.press('ArrowRight')
        expect(grip).to_have_attribute('aria-valuenow', '55')
        page.get_by_role('radio', name='Right to left').check()
        expect(page.locator('#patch-panes')).to_have_attribute('dir', 'rtl')
        grip.press('ArrowLeft')
        expect(grip).to_have_attribute('aria-valuenow', '60')
        box = grip.bounding_box()
        x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x + 35, y)
        page.mouse.up()
        expect(grip).not_to_have_attribute('aria-valuenow', '60')


if __name__ == '__main__':
    unittest.main()
