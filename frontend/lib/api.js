// Two different base URLs are needed for Docker Compose setups:
//
// - BROWSER_API_URL: used by code that runs in the user's browser (the
//   contact form, image src attributes). This must be a URL the browser
//   itself can reach, e.g. http://localhost:8000 published to the host.
//
// - SERVER_API_URL: used by getServerSideProps, which runs inside the
//   Next.js *server* container, not the browser. On Docker Compose this
//   should be the internal service name, e.g. http://backend:8000, since
//   "localhost" inside the frontend container would NOT reach Django.
//
// Outside Docker (plain `npm run dev`), both are simply http://127.0.0.1:8000,
// so a single NEXT_PUBLIC_API_URL in .env.local is all you need.

export const BROWSER_API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const SERVER_API_URL =
  process.env.INTERNAL_API_URL || BROWSER_API_URL;

// Kept for any existing code/imports that reference API_BASE_URL directly.
export const API_BASE_URL = BROWSER_API_URL;

export async function getProfile() {
  try {
    const res = await fetch(`${SERVER_API_URL}/api/profile/`, {
      // Always fetch fresh data from Django (SSR on every request).
      cache: 'no-store',
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch profile:', err);
    return null;
  }
}

export function mediaUrl(path) {
  if (!path) return null;
  if (path.startsWith('http')) return path;
  return `${BROWSER_API_URL}${path}`;
}

// Always resolvable — the backend serves either the uploaded CV file or a
// standard CV generated on the fly from the profile data, so this link
// works even before anything has been uploaded.
export function cvDownloadUrl() {
  return `${BROWSER_API_URL}/api/cv/download/`;
}

export async function sendContactMessage(payload) {
  const res = await fetch(`${BROWSER_API_URL}/api/contact/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to send message.');
  }
  return res.json();
}
