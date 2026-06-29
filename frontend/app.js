// The only client-side logic: call the backend and show which pod answered.
// nginx proxies /api to the backend service (see nginx.conf), so this stays
// same-origin and needs no CORS handling in the browser.
const button = document.getElementById('call');
const out = document.getElementById('out');

button.addEventListener('click', async () => {
  out.textContent = 'Loading…';
  try {
    const res = await fetch('/api/info');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    out.textContent = `${data.message}\nserved by pod: ${data.hostname}`;
  } catch (err) {
    out.textContent = `Request failed: ${err.message}`;
  }
});
