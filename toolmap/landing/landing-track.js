/**
 * Light PostHog tracking for landing variants.
 */
(function () {
  const ATTR_KEY = "toolmap_attribution";

  function readStoredAttribution() {
    try {
      return JSON.parse(sessionStorage.getItem(ATTR_KEY) || "{}");
    } catch (err) {
      return {};
    }
  }

  function getCurrentAttribution() {
    const params = new URLSearchParams(location.search);
    const props = {};
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
      const value = params.get(key);
      if (value) props[key] = value;
    });
    if (document.referrer) props.referrer = document.referrer;
    return props;
  }

  function getAttributionProps() {
    const current = getCurrentAttribution();
    const merged = { ...readStoredAttribution(), ...current };
    try {
      if (Object.keys(merged).length) sessionStorage.setItem(ATTR_KEY, JSON.stringify(merged));
    } catch (err) {
      // Ignore storage issues and keep the current request flowing.
    }
    return merged;
  }

  function appendQueryToHref(href, query) {
    const url = new URL(href, location.href);
    query.forEach(function (value, key) {
      if (!url.searchParams.has(key)) url.searchParams.set(key, value);
    });
    return url.pathname + url.search + url.hash;
  }

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
      // Growth funnel starts on a public landing, so anonymous events must be captured.
      person_profiles: "always",
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initPostHog();
    const attribution = getAttributionProps();
    const currentQuery = new URLSearchParams(location.search);
    const variant =
      (document.body.className.match(/variant-([a-c])/) || [])[1] ||
      document.body.getAttribute("data-variant") ||
      "hub";
    document.querySelectorAll("a[data-cta]").forEach(function (el) {
      el.setAttribute("href", appendQueryToHref(el.getAttribute("href"), currentQuery));
    });
    capture("landing_viewed", { variant: variant, path: location.pathname, ...attribution });
    document.querySelectorAll("[data-cta]").forEach(function (el) {
      el.addEventListener("click", function () {
        capture("landing_cta_clicked", {
          variant: variant,
          cta: el.getAttribute("data-cta"),
          ...attribution,
        });
      });
    });
  });
})();
