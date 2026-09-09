/* GA4 measurement: consent first; fixed events only; no form values or link text. */
(function () {
  'use strict';
  var ID = 'G-4G1QC1B639', KEY = 'ks_analytics_consent_v1';
  var enabled = false, started = false, progress = {}, activeSeconds = 0;
  var consent;
  try { consent = JSON.parse(localStorage.getItem(KEY)); } catch (_) {}
  if (!consent || Date.now() - consent.at > 180 * 86400000) consent = null;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  var canonical = document.querySelector('link[rel="canonical"]');
  var page = canonical ? canonical.href : 'https://khaqanshaheen.com/404.html';
  function origin(value) { try { return new URL(value).origin; } catch (_) { return ''; } }
  function event(name, parameters) {
    if (!enabled) return;
    gtag('event', name, Object.assign({page_location: page, page_referrer: origin(document.referrer)}, parameters || {}));
  }
  function start() {
    if (started) return;
    started = enabled = true;
    window['ga-disable-' + ID] = false;
    gtag('consent', 'default', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    gtag('js', new Date());
    var config = {send_page_view:false, page_location:page, page_referrer:origin(document.referrer), allow_google_signals:false, allow_ad_personalization_signals:false, cookie_expires:15552000};
    // Campaign labels only. Never forward arbitrary query parameters or URL fragments.
    var query = new URLSearchParams(location.search);
    [['utm_source','campaign_source'],['utm_medium','campaign_medium'],['utm_campaign','campaign_name']].forEach(function(pair) {
      var value = query.get(pair[0]);
      var knownSource = pair[0] === 'utm_source' && ['chatgpt.com','perplexity.ai','gemini.google.com','copilot.microsoft.com','claude.ai'].indexOf(value) !== -1;
      if (value && (/^[a-zA-Z0-9_-]{1,64}$/.test(value) || knownSource)) config[pair[1]] = value;
    });
    gtag('config', ID, config);
    event('page_view', {page_title:document.title});
    var script = document.createElement('script');
    script.async = true; script.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(script);
  }
  function clearCookies() {
    document.cookie.split(';').forEach(function(raw) {
      var name = raw.trim().split('=')[0];
      if (!/^_ga(?:_|$)/.test(name)) return;
      ['', ';domain=' + location.hostname, ';domain=.khaqanshaheen.com'].forEach(function(domain) {
        document.cookie = name + '=;Max-Age=0;path=/' + domain + ';SameSite=Lax;Secure';
      });
    });
  }
  function choose(value) {
    try { localStorage.setItem(KEY, JSON.stringify({value:value, at:Date.now()})); } catch (_) {}
    panel.hidden = true;
    if (value === 'granted') start();
    else {
      enabled = false;
      window['ga-disable-' + ID] = true;
      clearCookies();
      // Remove an already loaded Google tag from this document on withdrawal.
      if (started) location.reload();
    }
    settings.focus();
  }
  var style = document.createElement('style');
  style.textContent = '.ks-consent{position:fixed;bottom:16px;left:16px;right:16px;z-index:1000;max-width:640px;background:#fff;color:#0f1b2d;padding:20px;border:1px solid #64748b;border-radius:12px;box-shadow:0 4px 30px #0002;font:16px/1.5 system-ui}.ks-consent[hidden]{display:none}.ks-consent p{margin:0 0 12px}.ks-consent button,.ks-settings{font:inherit;cursor:pointer;border:1px solid #64748b;border-radius:6px;padding:8px 14px;background:#fff;color:#0f1b2d;margin:4px}.ks-consent a{color:#174ea6;text-decoration:underline}.ks-consent button:focus-visible,.ks-settings:focus-visible{outline:3px solid #1769c2;outline-offset:2px}';
  document.head.appendChild(style);
  var panel = document.createElement('section');
  panel.className = 'ks-consent'; panel.setAttribute('aria-label','Analytics cookie choice');
  panel.innerHTML = '<p><strong>Help improve this website</strong></p><p>With your permission, Google Analytics measures visits, traffic sources and interactions with services and booking links. It uses analytics cookies. Form answers are not collected.</p><p><a href="/privacy.html">Privacy and analytics details</a></p><button type="button" data-choice="granted">Accept analytics</button><button type="button" data-choice="denied">Reject analytics</button>';
  document.body.appendChild(panel);
  var settings = document.createElement('button');
  settings.type = 'button'; settings.className = 'ks-settings'; settings.textContent = 'Analytics preferences';
  (document.querySelector('footer .wrap') || document.querySelector('footer') || document.body).appendChild(settings);
  settings.addEventListener('click',function(){panel.hidden=false;panel.querySelector('button').focus();});
  panel.querySelectorAll('button[data-choice]').forEach(function(button){button.addEventListener('click',function(){choose(button.dataset.choice);});});
  panel.hidden = !!consent;
  if (consent && consent.value === 'granted') start();

  document.addEventListener('click', function(e) {
    var button = e.target.closest('button');
    if (button && !button.disabled && (button.id === 'bk-go' || button.id === 'bk-priority')) {
      event('booking_request_click', {request_type:button.id === 'bk-go' ? 'standard' : 'priority'});
      return;
    }
    var anchor = e.target.closest('a[href]');
    if (!anchor) return;
    var url; try { url = new URL(anchor.href, location.href); } catch (_) { return; }
    if (url.protocol === 'mailto:' || url.protocol === 'tel:') {event('contact_click',{contact_method:url.protocol === 'mailto:' ? 'email' : 'phone'});return;}
    if (!/^https?:$/.test(url.protocol)) return;
    if (/^(wa\.me|api\.whatsapp\.com)$/.test(url.hostname)) {event('contact_click',{contact_method:'whatsapp'});return;}
    if (url.origin !== location.origin) {event('outbound_click',{destination_domain:url.hostname});return;}
    if (/\/booking\.html$/.test(url.pathname)) event('booking_click');
    else if (url.hash === '#contact') event('contact_click',{contact_method:'contact_section'});
    else if (/\.(pdf|docx?|xlsx?|zip)$/i.test(url.pathname)) event('file_download',{file_extension:url.pathname.split('.').pop().toLowerCase()});
    else if (/\/services\.html$/.test(url.pathname)) event('service_click');
  }, true);
  var formStarted = false;
  document.addEventListener('input',function(e){
    if (enabled && !formStarted && /^bk-/.test(e.target.id || '')) {formStarted=true;event('booking_form_start');}
  });
  document.addEventListener('scroll', function() {
    if (!enabled) return;
    var height = document.documentElement.scrollHeight - innerHeight;
    if (height <= 0) return;
    var percent = Math.round(100 * scrollY / height);
    [25,50,75,90].forEach(function(n){if(percent >= n && !progress[n]){progress[n]=true;event('scroll_depth',{percent_scrolled:n});}});
  },{passive:true});
  setInterval(function(){
    if (!enabled || document.visibilityState !== 'visible' || !document.hasFocus()) return;
    activeSeconds += 5;
    if ([30,60,180].indexOf(activeSeconds) !== -1) event('engaged_read',{active_seconds:activeSeconds});
  },5000);
}());
