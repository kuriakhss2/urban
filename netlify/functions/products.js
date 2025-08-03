// netlify/functions/products.js

const ALLOWED_ORIGINS = new Set([
  'https://urban123.netlify.app',
  'http://localhost:8888',
  'http://localhost:5173',
]);

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : 'https://urban123.netlify.app';
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'GET,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    Vary: 'Origin',
  };
}

// Adjust this if your backend’s category names differ.
// Example guesses shown; tweak once you see real values.
const CATEGORY_MAP = {
  clothes: 'Clothes',   // or 'clothing'
  socks: 'Socks',
  books: 'Books',
  shoes: 'Shoes',       // or 'footwear'
};

exports.handler = async (event) => {
  const headers = corsHeaders(event.headers.origin || '');
  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers };

  try {
    const base = process.env.API_BASE;
    if (!base) return { statusCode: 500, headers, body: JSON.stringify({ error: 'Missing API_BASE' }) };

    const url = new URL(event.rawUrl);
    const rawCategory = url.searchParams.get('category');
    const id = url.searchParams.get('id');
    const debug = url.searchParams.get('debug') === '1';

    // Normalize category for the upstream API
    const normalizedCategory = rawCategory
      ? (CATEGORY_MAP[rawCategory.toLowerCase()] ?? rawCategory)
      : null;

    // Build upstream endpoint
    let endpoint = `${base}/api/products`;
    if (id) {
      endpoint = `${base}/api/products/${encodeURIComponent(id)}`;
    } else if (normalizedCategory) {
      endpoint = `${base}/api/products/category/${encodeURIComponent(normalizedCategory)}`;
    }

    // Helper to fetch & parse JSON safely
    const fetchJson = async (ep) => {
      const res = await fetch(ep);
      const text = await res.text();
      let json;
      try { json = JSON.parse(text); } catch { json = null; }
      return { ok: res.ok, status: res.status, text, json };
    };

    // First attempt (direct category or id or all)
    const first = await fetchJson(endpoint);

    // If asking by category but got nothing (or non-array),
    // fallback: get ALL and filter locally (case-insensitive)
    if (rawCategory && (!first.ok || !Array.isArray(first.json) || first.json.length === 0)) {
      const allAttempt = await fetchJson(`${base}/api/products`);
      let filtered = [];
      if (Array.isArray(allAttempt.json)) {
        const want = rawCategory.toLowerCase();
        filtered = allAttempt.json.filter(p => {
          const c = (p.category || '').toString().toLowerCase();
          // match exact, or against normalized as backup
          return c === want || c === (normalizedCategory || '').toLowerCase();
        });
      }

      if (debug) {
        return {
          statusCode: 200,
          headers: { ...headers, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            mode: 'fallback-filter',
            requested_category: rawCategory,
            normalized_category: normalizedCategory,
            tried_endpoint: endpoint,
            upstream_first_status: first.status,
            upstream_first_sample: typeof first.json === 'object' ? (Array.isArray(first.json) ? first.json.slice(0, 2) : first.json) : first.text,
            upstream_all_status: allAttempt.status,
            count_after_filter: filtered.length,
            sample_after_filter: filtered.slice(0, 2),
          }),
        };
      }

      return {
        statusCode: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify(filtered),
      };
    }

    // Normal successful path
    if (first.ok) {
      if (debug) {
        return {
          statusCode: 200,
          headers: { ...headers, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            mode: 'direct',
            endpoint,
            status: first.status,
            is_array: Array.isArray(first.json),
            length: Array.isArray(first.json) ? first.json.length : undefined,
            sample: Array.isArray(first.json) ? first.json.slice(0, 2) : first.json ?? first.text,
          }),
        };
      }
      return {
        statusCode: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: Array.isArray(first.json) ? JSON.stringify(first.json) : first.text,
      };
    }

    // Upstream error
    return {
      statusCode: first.status || 502,
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Upstream error',
        requested_url: endpoint,
        status: first.status,
        body: first.text,
      }),
    };

  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message || 'Server error' }) };
  }
};
