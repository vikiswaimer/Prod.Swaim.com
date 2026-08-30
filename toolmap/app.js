/**
 * Tool Map — loads active niche from niches.js (portrait: founders/entrepreneurs).
 */
(function () {
  const params = new URLSearchParams(window.location.search);
  const embedPreview = params.get("embed") === "1";

  function getActiveNiche() {
    const pack = window.TOOLMAP_NICHES;
    if (!pack || !pack.items) return null;
    const slug = pack.activeSlug;
    return pack.items.find((n) => n.slug === slug) || null;
  }

  function capture(event, props) {
    const niche = (window.TOOLMAP_NICHES && window.TOOLMAP_NICHES.activeSlug) || "unknown";
    if (window.posthog && typeof window.posthog.capture === "function") {
      window.posthog.capture(event, { niche, portrait: "founders-entrepreneurs", ...props });
    } else {
      console.debug("[posthog stub]", event, { niche, ...props });
    }
  }

  function initPostHog() {
    const cfg = window.TOOLMAP_CONFIG || {};
    if (!cfg.posthogKey || cfg.posthogKey.includes("YOUR_KEY")) {
      console.warn("PostHog: нет config.local.js — события только в console.");
      return;
    }
    !(function (t, e) {
      var o, n, p, r;
      e.__SV ||
        ((window.posthog = e),
        (e._i = []),
        (e.init = function (i, s, a) {
          function g(t, e) {
            var o = e.split(".");
            2 == o.length && ((t = t[o[0]]), (e = o[1]));
            t[e] = function () {
              t.push([e].concat(Array.prototype.slice.call(arguments, 0)));
            };
          }
          ((p = t.createElement("script")).type = "text/javascript"),
            (p.crossOrigin = "anonymous"),
            (p.async = !0),
            (p.src = s.api_host.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js"),
            (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r);
          var u = e;
          void 0 !== a ? (u = e[a] = []) : (a = "posthog");
          u.people = u.people || [];
          u.toString = function (t) {
            var e = "posthog";
            return "posthog" !== a && (e += "." + a), t || (e += " (stub)"), e;
          };
          u.people.toString = function () {
            return u.toString(1) + ".people (stub)";
          };
          o = "init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property get_session_property createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(
            " "
          );
          for (n = 0; n < o.length; n++) g(u, o[n]);
          e._i.push([i, s, a]);
        }),
        (e.__SV = 1));
    })(document, window.posthog || []);

    window.posthog.init(cfg.posthogKey, {
      api_host: cfg.posthogHost || "https://eu.i.posthog.com",
      person_profiles: "identified_only",
      persistence: "localStorage+cookie",
    });
  }

  function clearActive(svg) {
    svg.querySelectorAll(".active").forEach((el) => el.classList.remove("active"));
  }

  function showDetail(title, body) {
    document.getElementById("detail-title").textContent = title;
    document.getElementById("detail-body").textContent = body;
  }

  function render(niche) {
    const nodes = niche.nodes || [];
    const edges = niche.edges || [];
    const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
    const svg = document.getElementById("map-svg");
    const ns = "http://www.w3.org/2000/svg";
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    edges.forEach((e) => {
      const a = byId[e.from];
      const b = byId[e.to];
      if (!a || !b) return;
      const line = document.createElementNS(ns, "line");
      line.setAttribute("class", "edge");
      line.setAttribute("data-edge", e.id);
      line.setAttribute("x1", a.x);
      line.setAttribute("y1", a.y);
      line.setAttribute("x2", b.x);
      line.setAttribute("y2", b.y);
      line.addEventListener("click", (ev) => {
        ev.stopPropagation();
        clearActive(svg);
        line.classList.add("active");
        showDetail(e.title, e.example);
        capture("edge_clicked", { edge_id: e.id, from: e.from, to: e.to });
      });
      svg.appendChild(line);
    });

    nodes.forEach((n) => {
      const g = document.createElementNS(ns, "g");
      g.setAttribute("class", "node");
      g.setAttribute("data-node", n.id);
      g.setAttribute("transform", `translate(${n.x - 70}, ${n.y - 18})`);

      const rect = document.createElementNS(ns, "rect");
      rect.setAttribute("width", "140");
      rect.setAttribute("height", "36");
      g.appendChild(rect);

      const text = document.createElementNS(ns, "text");
      text.setAttribute("x", "70");
      text.setAttribute("y", "23");
      text.setAttribute("text-anchor", "middle");
      text.textContent = n.label;
      g.appendChild(text);

      g.addEventListener("click", (ev) => {
        ev.stopPropagation();
        clearActive(svg);
        g.classList.add("active");
        showDetail(n.label, n.blurb);
        capture("node_clicked", { tool: n.id, tool_label: n.label });
      });
      svg.appendChild(g);
    });

    svg.addEventListener("click", () => {
      clearActive(svg);
      showDetail(
        "Кликните узел или связь",
        "Узлы — инструменты. Линии — как стыковать в этой нише. Ниши меняем по тестам; портрет — фаундеры."
      );
    });
  }

  function wireCta(niche) {
    const btn = document.getElementById("paid-cta");
    const href = "playbook.html?niche=" + encodeURIComponent(niche.slug);
    if (btn.tagName === "A") btn.setAttribute("href", href);
    btn.addEventListener("click", () => {
      capture("paid_cta_clicked", { surface: "map_footer", niche: niche.slug });
    });
  }

  function fillMeta(niche, portrait) {
    document.getElementById("niche-label").textContent = niche.label;
    const portraitEl = document.getElementById("portrait-label");
    if (portraitEl && portrait) portraitEl.textContent = portrait.label;
    const statusEl = document.getElementById("niche-status");
    if (statusEl) statusEl.textContent = niche.status || "testing";
    document.title = "Tool Map — " + niche.label;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const pack = window.TOOLMAP_NICHES;
    const niche = getActiveNiche();
    if (!niche || !niche.nodes) {
      showDetail("Нет данных ниши", "Добавьте nodes/edges в niches.js для activeSlug.");
      return;
    }
    if (embedPreview) document.body.classList.add("embed-preview");
    fillMeta(niche, pack && pack.portrait);
    if (!embedPreview) initPostHog();
    render(niche);
    wireCta(niche);
    if (!embedPreview) {
      capture("map_viewed", { surface: "toolmap_v0", niche_status: niche.status });
    }
  });
})();
