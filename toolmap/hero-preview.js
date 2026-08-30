/**
 * Hero live preview — same graph as map.html (niches.js), read-only.
 */
(function () {
  function getActiveNiche() {
    const pack = window.TOOLMAP_NICHES;
    if (!pack || !pack.items) return null;
    const slug = pack.activeSlug;
    return (
      pack.items.find(function (n) {
        return n.slug === slug;
      }) || null
    );
  }

  function render(svg, niche) {
    const nodes = niche.nodes || [];
    const edges = niche.edges || [];
    const byId = Object.fromEntries(
      nodes.map(function (n) {
        return [n.id, n];
      })
    );
    const ns = "http://www.w3.org/2000/svg";

    const defs = document.createElementNS(ns, "defs");
    const glow = document.createElementNS(ns, "radialGradient");
    glow.setAttribute("id", "hero-glow");
    glow.setAttribute("cx", "50%");
    glow.setAttribute("cy", "42%");
    glow.setAttribute("r", "58%");

    const stopA = document.createElementNS(ns, "stop");
    stopA.setAttribute("offset", "0%");
    stopA.setAttribute("stop-color", "#3ecfbf");
    stopA.setAttribute("stop-opacity", "0.18");

    const stopB = document.createElementNS(ns, "stop");
    stopB.setAttribute("offset", "100%");
    stopB.setAttribute("stop-color", "#0c1016");
    stopB.setAttribute("stop-opacity", "0");

    glow.appendChild(stopA);
    glow.appendChild(stopB);
    defs.appendChild(glow);
    svg.appendChild(defs);

    const bg = document.createElementNS(ns, "rect");
    bg.setAttribute("width", "100%");
    bg.setAttribute("height", "100%");
    bg.setAttribute("fill", "url(#hero-glow)");
    svg.appendChild(bg);

    edges.forEach(function (edge) {
      const from = byId[edge.from];
      const to = byId[edge.to];
      if (!from || !to) return;

      const line = document.createElementNS(ns, "line");
      line.setAttribute("class", "preview-edge");
      if (edge.id === "e2") line.classList.add("is-featured");
      line.setAttribute("x1", from.x);
      line.setAttribute("y1", from.y);
      line.setAttribute("x2", to.x);
      line.setAttribute("y2", to.y);
      svg.appendChild(line);
    });

    nodes.forEach(function (node) {
      const group = document.createElementNS(ns, "g");
      group.setAttribute("class", "preview-node");
      group.setAttribute("transform", "translate(" + (node.x - 70) + ", " + (node.y - 18) + ")");

      const rect = document.createElementNS(ns, "rect");
      rect.setAttribute("width", "140");
      rect.setAttribute("height", "36");
      rect.setAttribute("rx", "8");
      group.appendChild(rect);

      const text = document.createElementNS(ns, "text");
      text.setAttribute("x", "70");
      text.setAttribute("y", "23");
      text.setAttribute("text-anchor", "middle");
      text.textContent = node.label;
      group.appendChild(text);

      svg.appendChild(group);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    const svg = document.getElementById("hero-map-preview");
    if (!svg) return;

    const niche = getActiveNiche();
    if (!niche || !niche.nodes) {
      const fallback = document.getElementById("hero-map-fallback");
      if (fallback) fallback.hidden = false;
      return;
    }

    render(svg, niche);

    const label = document.getElementById("hero-niche-label");
    const eyebrow = document.getElementById("hero-niche-eyebrow");
    const trustSlug = document.getElementById("hero-niche-slug");
    if (label) label.textContent = niche.label;
    if (eyebrow) eyebrow.textContent = niche.slug;
    if (trustSlug) trustSlug.textContent = niche.slug;

    document.querySelectorAll("[data-map-count]").forEach(function (el) {
      const kind = el.getAttribute("data-map-count");
      if (kind === "nodes") el.textContent = String(niche.nodes.length);
      if (kind === "edges") el.textContent = String((niche.edges || []).length);
    });
  });
})();
