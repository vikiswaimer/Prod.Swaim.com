/**
 * Hero live preview — same graph as ../index.html (niches.js), read-only.
 * SWA-42: not a wireframe; data-driven solo-digital-services map.
 */
(function () {
  function getActiveNiche() {
    const pack = window.TOOLMAP_NICHES;
    if (!pack || !pack.items) return null;
    const slug = pack.activeSlug;
    return pack.items.find(function (n) {
      return n.slug === slug;
    });
  }

  function render(svg, niche) {
    var nodes = niche.nodes || [];
    var edges = niche.edges || [];
    var byId = Object.fromEntries(
      nodes.map(function (n) {
        return [n.id, n];
      })
    );
    var ns = "http://www.w3.org/2000/svg";

    var defs = document.createElementNS(ns, "defs");
    var glow = document.createElementNS(ns, "radialGradient");
    glow.setAttribute("id", "hero-glow");
    glow.setAttribute("cx", "50%");
    glow.setAttribute("cy", "42%");
    glow.setAttribute("r", "58%");
    var stopA = document.createElementNS(ns, "stop");
    stopA.setAttribute("offset", "0%");
    stopA.setAttribute("stop-color", "#3ecfbf");
    stopA.setAttribute("stop-opacity", "0.18");
    var stopB = document.createElementNS(ns, "stop");
    stopB.setAttribute("offset", "100%");
    stopB.setAttribute("stop-color", "#0c1016");
    stopB.setAttribute("stop-opacity", "0");
    glow.appendChild(stopA);
    glow.appendChild(stopB);
    defs.appendChild(glow);
    svg.appendChild(defs);

    var bg = document.createElementNS(ns, "rect");
    bg.setAttribute("width", "100%");
    bg.setAttribute("height", "100%");
    bg.setAttribute("fill", "url(#hero-glow)");
    svg.appendChild(bg);

    edges.forEach(function (e) {
      var a = byId[e.from];
      var b = byId[e.to];
      if (!a || !b) return;
      var line = document.createElementNS(ns, "line");
      line.setAttribute("class", "preview-edge");
      line.setAttribute("x1", a.x);
      line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x);
      line.setAttribute("y2", b.y);
      svg.appendChild(line);
    });

    nodes.forEach(function (n) {
      var g = document.createElementNS(ns, "g");
      g.setAttribute("class", "preview-node");
      g.setAttribute("transform", "translate(" + (n.x - 70) + ", " + (n.y - 18) + ")");

      var rect = document.createElementNS(ns, "rect");
      rect.setAttribute("width", "140");
      rect.setAttribute("height", "36");
      rect.setAttribute("rx", "8");
      g.appendChild(rect);

      var text = document.createElementNS(ns, "text");
      text.setAttribute("x", "70");
      text.setAttribute("y", "23");
      text.setAttribute("text-anchor", "middle");
      text.textContent = n.label;
      g.appendChild(text);

      svg.appendChild(g);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var svg = document.getElementById("hero-map-preview");
    if (!svg) return;
    var niche = getActiveNiche();
    if (!niche || !niche.nodes) return;
    render(svg, niche);

    var label = document.getElementById("hero-niche-label");
    var eyebrow = document.getElementById("hero-niche-eyebrow");
    if (label) label.textContent = niche.label;
    if (eyebrow) eyebrow.textContent = niche.slug;

    var counts = document.querySelectorAll("[data-map-count]");
    counts.forEach(function (el) {
      var kind = el.getAttribute("data-map-count");
      if (kind === "nodes") el.textContent = String(niche.nodes.length);
      if (kind === "edges") el.textContent = String((niche.edges || []).length);
    });
  });
})();
