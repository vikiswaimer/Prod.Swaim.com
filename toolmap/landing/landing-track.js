/**
 * Light PostHog tracking for landing variants.
 */
(function () {
  function capture(event, props) {
    if (window.posthog && typeof window.posthog.capture === "function") {
      window.posthog.capture(event, {
        surface: "landing",
        portrait: "founders-entrepreneurs",
        ...props,
      });
    } else {
      console.debug("[posthog stub]", event, props);
    }
  }

  function initPostHog() {
    const cfg = window.TOOLMAP_CONFIG || {};
    if (!cfg.posthogKey || String(cfg.posthogKey).includes("YOUR_KEY")) return;
    if (window.posthog && window.posthog.__loaded) return;
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
            (p.async = !0),
            (p.src = s.api_host.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js"),
            (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r);
          var u = e;
          void 0 !== a ? (u = e[a] = []) : (a = "posthog");
          u.people = u.people || [];
          o = "init capture".split(" ");
          for (n = 0; n < o.length; n++) g(u, o[n]);
          e._i.push([i, s, a]);
        }),
        (e.__SV = 1));
    })(document, window.posthog || []);
    window.posthog.init(cfg.posthogKey, {
      api_host: cfg.posthogHost || "https://eu.i.posthog.com",
      person_profiles: "identified_only",
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initPostHog();
    const variant =
      (document.body.className.match(/variant-([a-c])/) || [])[1] ||
      document.body.getAttribute("data-variant") ||
      "hub";
    capture("landing_viewed", { variant: variant, path: location.pathname });
    document.querySelectorAll("[data-cta]").forEach(function (el) {
      el.addEventListener("click", function () {
        const cta = el.getAttribute("data-cta");
        capture("landing_cta_clicked", { variant: variant, cta: cta });
        if (cta === "playbook") {
          capture("paid_cta_clicked", { variant: variant, surface: "landing", cta: cta });
        }
      });
    });
  });
})();
