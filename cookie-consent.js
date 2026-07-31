// ── Cookie consent + Google Analytics (GA4) ──
// GA4 laadt pas na expliciete toestemming; vóór toestemming worden geen
// analytics-cookies gezet. Gedeeld tussen index.html en privacybeleid.html.
const GA_MEASUREMENT_ID = 'G-X9EZL4YZ9';
const COOKIE_CONSENT_KEY = 'jebeCookieConsent';

function loadAnalytics() {
  if (window.jebeAnalyticsLoaded || GA_MEASUREMENT_ID.includes('XXXX')) return;
  window.jebeAnalyticsLoaded = true;
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
  document.head.appendChild(script);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA_MEASUREMENT_ID, { anonymize_ip: true });
}

const cookieBanner = document.getElementById('cookie-banner');
const cookieAccept = document.getElementById('cookie-accept');
const cookieReject = document.getElementById('cookie-reject');
const cookieManageLink = document.getElementById('cookie-manage');

function setCookieConsent(value) {
  try { localStorage.setItem(COOKIE_CONSENT_KEY, value); } catch (e) {}
  cookieBanner.hidden = true;
  if (value === 'granted') loadAnalytics();
}

let storedConsent = null;
try { storedConsent = localStorage.getItem(COOKIE_CONSENT_KEY); } catch (e) {}

if (storedConsent === 'granted') {
  loadAnalytics();
} else if (storedConsent !== 'denied') {
  cookieBanner.hidden = false;
}

cookieAccept.addEventListener('click', () => setCookieConsent('granted'));
cookieReject.addEventListener('click', () => setCookieConsent('denied'));
cookieManageLink.addEventListener('click', (e) => {
  e.preventDefault();
  cookieBanner.hidden = false;
});
