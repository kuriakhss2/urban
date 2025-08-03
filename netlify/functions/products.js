// netlify/functions/products.js

// --- CORS allow-list (add your custom domain when you have one) ---
const ALLOWED_ORIGINS = new Set([
  "https://urban123.netlify.app",
  "http://localhost:8888", // Netlify Dev
  "http://localhost:5173", // Vite dev server
]);

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : "https://urban123.netlify.app";
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    Vary: "Origin",
  };
}

// --- Prevent caching (avoid 304 Not Modified / stale empty responses) ---
const NO_CACHE = {
  "Content-Type": "application/json",
  "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
  Pragma: "no-cache",
  Expires: "0",
};

// --- Category synonyms/variants: adjust to match your backend values exactly ---
const ALT_NAMES = {
  clothes: ["clothes", "clothing", "apparel"],
  socks: ["socks", "sock"],
  books: ["books", "book"],
  shoes: ["shoes", "shoe", "footwear"],
};

// --- Helper: fetch and parse JSON safely (and keep the raw text) ---
async function fetchJson(endpoint) {
  const res = await fetch(endpoint);
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }
  return { ok: res.ok, status: res.status, json, text, endpoint };
}

exports.handler = async (event) => {
  const headers = corsHeaders(event.headers.origin || "");
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }

  try {
    const base = process.env.API_BASE;
    if (!base) {
      return {
        statusCode: 500,
        headers: { ...headers, ...NO_CACHE },
        body: JSON.stringify({ error: "Missing API_BASE" }),
      };
    }

    const url = new URL(event.rawUrl);
    const rawCategory = url.searchParams.get("category");
    const id = url.searchParams.get("id");
    const debug = url.searchParams.get("debug") === "1";

    // 1) Build the first upstream endpoint (try the raw category first)
    let endpoint = `${base}/api/products`;
    if (id) {
      endpoint = `${base}/api/products/${encodeURIComponent(id)}`;
    } else if (rawCategory) {
      endpoint = `${base}/api/products/category/${encodeURIComponent(rawCategory)}`;
    }

    // 2) First attempt: call upstream as-is
    const first = await fetchJson(endpoint);

    // 3) Fallback path: if category query returned nothing, fetch ALL and filter locally
    if (rawCategory && (!first.ok || !Array.isArray(first.json) || first.json.length === 0)) {
      const allAttempt = await fetchJson(`${base}/api/products`);
      let filtered = [];

      if (Array.isArray(allAttempt.json)) {
        const wantList =
          ALT_NAMES[(rawCategory || "").toLowerCase()] ||
          [(rawCategory || "").toLowerCase()];

        filtered = allAttempt.json.filter((p) => {
          const c = (p.category || "").toString().toLowerCase();
          return wantList.includes(c);
        });
      }

      if (debug) {
        return {
          statusCode: 200,
          headers: { ...headers, ...NO_CACHE },
          body: JSON.stringify({
            mode: "fallback-filter",
            requested_category: rawCategory,
            tried_endpoint: first.endpoint,
            upstream_first_status: first.status,
            upstream_all_status: allAttempt.status,
            wantList,
            count_after_filter: filtered.length,
            sample_after_filter: filtered.slice(0, 2),
          }),
        };
      }

      return {
        statusCode: 200,
        headers: { ...headers, ...NO_CACHE },
        body: JSON.stringify(filtered),
      };
    }

    // 4) Normal successful path
    if (first.ok) {
      if (debug) {
        return {
          statusCode: 200,
          headers: { ...headers, ...NO_CACHE },
          body: JSON.stringify({
            mode: "direct",
            endpoint: first.endpoint,
            status: first.status,
            is_array: Array.isArray(first.json),
            length: Array.isArray(first.json) ? first.json.length : undefined,
            sample: Array.isArray(first.json) ? first.json.slice(0, 2) : first.json ?? first.text,
          }),
        };
      }

      return {
        statusCode: 200,
        headers: { ...headers, ...NO_CACHE },
        body: Array.isArray(first.json) ? JSON.stringify(first.json) : first.text,
      };
    }

    // 5) Upstream error
    return {
      statusCode: first.status || 502,
      headers: { ...headers, ...NO_CACHE },
      body: JSON.stringify({
        error: "Upstream error",
        requested_url: first.endpoint,
        status: first.status,
        body: first.text,
      }),
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers: { ...headers, ...NO_CACHE },
      body: JSON.stringify({ error: err.message || "Server error" }),
    };
  }
};
