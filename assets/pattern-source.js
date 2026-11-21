(() => {
  "use strict";
  function between(source, start, end) {
    const first = source.indexOf(start);
    const last = end ? source.indexOf(end, first + start.length) : source.length;
    if (first < 0 || last < 0) throw new Error("Source section is missing: " + start);
    return source.slice(first, last).trim();
  }

  function html(title, styles, markup, script = "", runtime = "") {
    const escapedTitle = title.replaceAll("&", "&amp;").replaceAll("<", "&lt;");
    const inline = value => "<script>\n" + value.replace(/<\/script/gi, "<\\/script") + "\n</" + "script>";
    return [
      "<!doctype html>",
      "<!-- Based on Enochian UI UX Elements by alanism / UnCommon Core. CC BY-NC 4.0. -->",
      '<html lang="en" data-finish="ivory">', "<head>", '<meta charset="utf-8">',
      '<meta name="viewport" content="width=device-width, initial-scale=1">',
      "<title>" + escapedTitle + " · Enochian Elements</title>",
      "<style>\n" + styles.trim() + "\n</style>", "</head>", "<body>", markup,
      runtime && inline(runtime), script && inline("(() => {\n" + script + "\n})();"),
      "</body>", "</html>", ""
    ].filter((line, index, lines) => line || index === lines.length - 1).join("\n");
  }

  // Shared examples stay together when their behavior uses the same demo state.
  const recipes = {
    Calendar: "calendar", Checkbox: "checkbox", Combobox: "combobox", "Date Picker": "date",
    Field: "patch", Input: "text", "Input Group": "patch", "Input OTP": "otp", Label: "text",
    "Native Select": "native", Questionnaire: "questionnaire", "Radio Group": "radio",
    Select: "select", Textarea: "textarea",
    Breadcrumb: "breadcrumb", Menubar: "overlays", "Navigation Menu": "navigation",
    Pagination: "patch", Sidebar: "navigation", Tabs: "tabs",
    "Alert Dialog": "overlays", Command: "command", "Context Menu": "overlays", Dialog: "overlays",
    Drawer: "overlays", "Dropdown Menu": "overlays", "Hover Card": "hover", Popover: "popover",
    Sheet: "overlays", Tooltip: "date",
    Alert: "alert", Empty: "patch", Progress: "diagnose", Skeleton: "diagnose",
    Spinner: "diagnose", Toast: "patch",
    Attachment: "transcript", Badge: "patch", Bubble: "transcript", Chart: "patch",
    "Data Table": "patch", Marker: "transcript", Message: "transcript",
    "Message Scroller": "transcript", Table: "patch", Trace: "transcript",
    Accordion: "notes", "Aspect Ratio": "studies", Avatar: "studies", Card: "studies",
    Carousel: "carousel", Collapsible: "notes", Direction: "panes", Item: "studies",
    Kbd: "notes", Resizable: "panes", "Scroll Area": "studies", Separator: "notes",
    Typography: "typography"
  };
  const samples = {
    checkbox: [["#patch-pin", "label"]],
    text: [["#patch-name", ".field"]],
    textarea: [["#notes", ".field"]],
    native: [["#bank", ".field"]],
    radio: ["#patch-source"],
    date: [["#review-date", ".field"]],
    otp: [["#bench-access", "article"]],
    questionnaire: [["#questionnaire", "article"]],
    tabs: [["#front-panel-tabs", "article"]],
    breadcrumb: ["#breadcrumb-trail"],
    hover: [["#hover-card-trigger", ".hover-preview"]],
    popover: [["#session-popover-trigger", "details"]],
    alert: ["#system-alert"],
    diagnose: [["#diagnose", "article"]],
    transcript: ["#bench-transcript", "#message-template", "#attachment-template"],
    carousel: ["#bank-carousel"],
    panes: [["#patch-panes", "article"]],
    notes: ["#build-notes"],
    studies: ["#related-study-card"],
    typography: [".intro > div"]
  };

  function native(name, { body, styles, script }) {
    const sample = recipes[name];
    if (!sample) throw new Error("No source recipe for " + name);
    const part = (start, end) => between(script, start, end);
    const nodes = [];
    function read(query) {
      const [selector, ancestor] = Array.isArray(query) ? query : [query];
      const node = body.querySelector(selector);
      if (!node) throw new Error("Example markup is missing: " + selector);
      return (ancestor ? node.closest(ancestor) : node).cloneNode(true);
    }
    const add = (...queries) => nodes.push(...queries.map(read));
    function section(id, ...queries) {
      const element = document.createElement("section");
      element.id = id;
      element.append(read("#" + id + "-title"), ...queries.map(read));
      nodes.push(element);
    }
    function fields(...queries) {
      const form = document.createElement("form");
      form.id = "patch-form";
      form.className = "panel stack";
      form.append(...queries.map(read));
      nodes.push(form);
    }
    const code = [];
    const use = (start, end) => code.push(part(start, end));
    const helpers = () => use('"use strict";', "const finishKey");
    const library = () => use("const starter =", "let nextId");
    const front = () => use("function renderFrontPanel()", "function renderTable()");
    const chart = () => use("function renderChart()", "function showNameError(");
    const picker = () => use("function bindPicker(", "const bankField");
    const jump = () => use("function jump(", 'window.addEventListener("hashchange"');
    const command = () => {
      use('const command = $("#command");', "const patternFamilies");
      use("function addCommand(", "for (const [family, entries]");
      for (const [label, id] of [["Forms", "forms"], ["Overlays", "overlays"], ["Data display", "data-display"]]) {
        code.push(`addCommand("${label}", "${id}", "${label.toLowerCase()}");`);
      }
      use('const commands = $$("button", commandResults);', "function bindMenu(");
    };

    if (samples[sample]) add(...samples[sample]);
    switch (sample) {
      case "patch":
      case "overlays":
        section("forms", "#patch-form");
        section("data-display", ".data-grid");
        add("#patch-row", "#chart-bar", "#toast", "#inspector");
        helpers();
        library();
        use("let nextId", 'const command = $("#command");');
        code.push('const command = $("#command");');
        jump();
        if (sample === "overlays") {
          section("overlays", "#overlays > .pair", "#overlays > .examples");
          add(["#patch-menubar", "article"], "#about", "#reset", "#drawer");
          use("function bindMenu(", 'const disclosure = $(".disclosure");');
          use('const drawerGrip = $(".drawer-grip");', "// Calendar:");
        }
        use('const disclosure = $(".disclosure");', 'const drawerGrip = $(".drawer-grip");');
        code.push("renderTable(); renderChart(); renderFrontPanel();");
        break;
      case "calendar":
        fields(["#review-date", ".field"]);
        add("#review-calendar");
        helpers();
        code.push('const form = $("#patch-form");');
        use("const reviewDate", "// Select and editable combobox");
        break;
      case "select":
        fields(["#bank", ".field"]);
        add(["#bank-picker", ".picker"]);
        helpers();
        picker();
        code.push('const form = $("#patch-form");');
        use("const bankField", '  bindPicker(\n    $("#patch-picker"),');
        break;
      case "combobox":
        add(["#patch-picker", ".picker"]);
        helpers();
        library();
        front();
        picker();
        use('  bindPicker(\n    $("#patch-picker"),', "// OTP uses");
        code.push("renderFrontPanel();");
        break;
      case "navigation":
        add("#catalog-sidebar", "#pattern-index > header");
        nodes[nodes.length - 1].id = "pattern-index";
        for (const id of ["forms", "navigation", "overlays", "feedback", "data-display", "layout"]) section(id);
        break;
      case "command":
        add("#command-trigger", "#command");
        section("forms", ["#patch-name", ".field"]);
        section("overlays", ["#session-popover-trigger", "details"]);
        section("data-display", "#system-alert");
        helpers();
        jump();
        command();
        use('const disclosure = $(".disclosure");', 'const drawerGrip = $(".drawer-grip");');
        break;
      case "date":
      case "hover":
      case "popover":
        helpers();
        code.push("const command = null;");
        use('const disclosure = $(".disclosure");', 'const drawerGrip = $(".drawer-grip");');
        break;
      case "tabs":
        helpers();
        library();
        front();
        use("const tabs =", "const starter =");
        code.push("renderFrontPanel();");
        break;
      case "otp":
        helpers();
        use('const code = $("#bench-code");', 'const questionnaire = $("#questionnaire");');
        break;
      case "questionnaire":
        helpers();
        use('const questionnaire = $("#questionnaire");', "// Transcript keeps");
        break;
      case "diagnose":
        helpers();
        library();
        use('const diagnose = $("#diagnose");', "  renderTable();\n  renderChart();");
        break;
      case "transcript":
        helpers();
        library();
        use('const transcript = $("#transcript");', 'const carousel = $("#bank-carousel");');
        break;
      case "carousel":
        helpers();
        library();
        chart();
        use('const carousel = $("#bank-carousel");', 'const panes = $("#patch-panes");');
        code.push("renderChart();");
        break;
      case "panes":
        helpers();
        library();
        front();
        use('const panes = $("#patch-panes");', 'const diagnose = $("#diagnose");');
        code.push("renderFrontPanel();");
        break;
    }
    const base = "https://github.com/alanism/Enochian-UI-UX-Elements/blob/main/";
    for (const node of nodes) for (const link of node.querySelectorAll('a[href^="../"]')) {
      link.href = base + link.getAttribute("href").slice(3);
    }
    return html(name, styles, '<main class="shell stack">\n' + nodes.map(node => node.outerHTML).join("\n") + "\n</main>", code.join("\n\n"));
  }

  function original(pattern, node, styles, script, motion) {
    const title = ({
      slider: "Signal Slider", switch: "Binary Gate", toggle: "Hollow Gate", "toggle-group": "Triad Action Keys",
      button: "Push Button", "button-group": "The Three Keys", "code-block": "Code Veil"
    })[pattern];
    const pick = (start, end) => between(script, start, end);
    const markup = node.cloneNode(true);
    const pieces = [];
    const use = (start, end) => pieces.push(pick(start, end));
    let body;
    if (motion) {
      use("const { animate }", "const ang =");
      body = node.previousElementSibling.outerHTML + "\n" + markup.outerHTML;
      if (pattern === "button") use("/* concave push button:", "/* arcade push-buttons: momentary");
      if (pattern === "button-group") {
        use("let AC=null, bedGain=null;", "function renderRadio(");
        use("/* arcade push-buttons: momentary", "/* Code Veil drives");
      }
      if (pattern === "code-block") {
        markup.querySelectorAll(".code-snippet").forEach(panel => panel.remove());
        body = node.previousElementSibling.outerHTML + "\n" + markup.outerHTML;
        use("function bindFinish(", 'bindFinish("darkDialFinish"');
        use('bindFinish("codeVeilFinish"', 'bindFinish("keyboardFinish"');
        use("const CODE_SPRING", "const CODE_SNIPPETS");
        pieces.push('const CODE_SNIPPETS = [\n' + pick('{id:"codeToggle"', '{id:"darkDial"') + "\n];");
        use("function addCodePanels()", "renderCodeLayer(true);");
        pieces.push("renderCodeLayer(true);");
      }
    } else {
      markup.querySelector(".code-snippet")?.remove();
      body = '<div class="page"><div class="grid">' + markup.outerHTML + "</div></div>";
      use("let MASTER=null", "const NS =");
      use("class Spring", "/* ── one shared frame loop");
      use("let AC=null, NB=null", "/* ── accent, sound, finishes");
      use('$$(".rthemes[data-target]")', "const PINCH");
      if (pattern === "slider") use("function makeHSlider(", "for(let i=0;i<=10;i++)");
      if (pattern === "switch") {
        use("const PINCH", "/* ── Seeker Orb");
        use('makeToggle($("std")', 'makeToggle($("col")');
      }
      if (pattern === "toggle") use('$("ccv").addEventListener', "/* ── Pulse Grid");
      if (pattern === "toggle-group") use("/* ── Triad Action Keys", "/* ── Cinnabar Key");
    }
    return html(title, styles, body, pieces.join("\n\n"), motion);
  }
  window.EnochianPatternSource = { native, original };
})();
