// netlify/functions/products.js

// Allow your site and local dev to call this function
const ALLOWED_ORIGINS = new Set([
  'https://urban123.netlify.app',
  'http://localhost:8888', // Netlify Dev
  'http://localhost:5173', // Vite dev (change if different)
  // 'https://YOUR-CUSTOM-DOMAIN.com',
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

// If your project is CommonJS (no "type":"module" in package.json), replace the next line with:
// exports.handler = async (event) => { ... }
export async function handler(event) {
  const headers = corsHeaders(event.headers.origin || '');

  // CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers };
  }

  try {
    const base = process.env.API_BASE; // set this in Netlify env vars
    if (!base) {
      return { statusCode: 500, headers, body: JSON.stringify({ error: 'Missing API_BASE' }) };
    }

    // Support three patterns using query params: all, by category, by id
    const url = new URL(event.rawUrl);
    const category = url.searchParams.get('category');
    const id = url.searchParams.get('id');

    let endpoint = `${base}/api/products`;
    if (id) endpoint = `${base}/api/products/${encodeURIComponent(id)}`;
    else if (category) endpoint = `${base}/api/products/category/${encodeURIComponent(category)}`;

    console.log("🔹 Fetching from:", endpoint);
const upstream = await fetch(endpoint);
const text = await upstream.text();
console.log("🔹 Upstream response:", text);

if (!upstream.ok) {
  return {
    statusCode: upstream.status,
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      error: 'Upstream error',
      status: upstream.status,
      requested_url: endpoint,
      body: text
    }),
  };
}


    if (!upstream.ok) {
      return {
        statusCode: upstream.status,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Upstream error', status: upstream.status, body: text }),
      };
    }

    return {
      statusCode: 200,
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: text,
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message || 'Server error' }),
    };
  }
}
