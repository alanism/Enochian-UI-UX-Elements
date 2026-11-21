(() => {
  const root = document.documentElement;
  const params = new URLSearchParams(location.search);
  const embedded = params.has("embedded");
  const pattern = params.get("pattern");
  const fonts = document.currentScript.dataset.fonts;
  const sourceTool = new URL("pattern-source.js", document.currentScript.src);
  if (embedded) root.classList.add("embedded");

  function loadFonts() {
    for (const origin of ["https://fonts.googleapis.com", "https://fonts.gstatic.com"]) {
      const link = document.createElement("link");
      link.rel = "preconnect";
      link.href = origin;
      if (origin.endsWith("gstatic.com")) link.crossOrigin = "anonymous";
      document.head.append(link);
    }
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = fonts;
    document.head.append(link);
  }
  if (!pattern || !/^[a-z-]+$/.test(pattern)) {
    loadFonts();
    return;
  }

  root.classList.add("embedded", "atlas-preview");
  const style = document.createElement("style");
  style.textContent = `
    html.atlas-preview:not([data-preview-ready]) body { visibility: hidden; }
    html.atlas-preview [hidden], html.atlas-preview .cap { display: none !important; }
    html.atlas-preview .page, html.atlas-preview .grid { margin: 0; padding: 0; max-width: none; }
    html.atlas-preview .grid { grid-template-columns: minmax(0, 1fr); }
    html.atlas-preview .card { min-width: 0; }
    html.atlas-preview .fx { max-width: 100%; }
    html.atlas-preview .d37-wrap { flex-wrap: wrap; justify-content: center; }
    html.atlas-preview .abtns { flex-wrap: wrap; gap: clamp(6px, 4vw, 44px); }
  `;
  document.head.append(style);

  document.addEventListener("DOMContentLoaded", () => {
    const original = document.querySelector(`[data-atlas-pattern="${pattern}"]`);
    if (!original) {
      root.classList.remove("atlas-preview");
      root.classList.toggle("embedded", embedded);
      loadFonts();
      return;
    }
    const sourceCopy = original.cloneNode(true);
    const detached = document.createElement("div");
    if (original.previousElementSibling?.classList.contains("cap")) {
      detached.append(original.previousElementSibling.cloneNode(true));
    }
    detached.append(sourceCopy);
    for (let node = original; node !== document.body; node = node.parentElement) {
      for (const sibling of node.parentElement.children) {
        if (sibling !== node) sibling.hidden = true;
      }
    }
    root.dataset.previewReady = "";
    if (window.parent === window) return;

    const localFile = location.protocol === "file:";
    const origin = localFile ? "*" : location.origin;
    const styles = document.querySelector("style[data-pattern-style]").textContent;
    const source = document.querySelector("script[data-pattern-script]").textContent;
    let engine;
    function loadSourceTool() {
      if (!engine) engine = new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = sourceTool.href;
        script.onload = () => resolve(window.EnochianPatternSource);
        script.onerror = reject;
        document.head.append(script);
      });
      return engine;
    }
    window.addEventListener("message", async event => {
      const sameOrigin = event.origin === location.origin || (localFile && event.origin === "null");
      if (event.source !== window.parent || !sameOrigin || event.data?.type !== "enochian-copy-source") return;
      let code;
      try {
        const exporter = await loadSourceTool();
        const installer = globalThis.installEnochianMotion;
        const motion = installer ? "(" + installer.toString() + ").call(globalThis);" : "";
        code = exporter.original(pattern, sourceCopy, styles, source, motion);
      } catch (error) {
        console.error(error);
      }
      window.parent.postMessage({ type: "enochian-pattern-source", code }, origin);
    });
    window.parent.postMessage({ type: "enochian-preview-ready" }, origin);
    new ResizeObserver(() => {
      window.parent.postMessage({
        type: "enochian-preview-size",
        height: Math.ceil(document.body.getBoundingClientRect().height)
      }, origin);
    }).observe(document.body);
  }, { once: true });
})();
