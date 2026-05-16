/* Service worker — met en cache l’app pour une utilisation hors ligne après la première visite (HTTP/HTTPS ou localhost). */
'use strict';

var CACHE_NAME = 'acrosport-offline-v4';
var PRECACHE_URLS = [
  './index.html',
  './sw.js',
  './manifest.webmanifest',
  './icon-source.png',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon-32x32.png'
];

function precache() {
  return caches.open(CACHE_NAME).then(function (cache) {
    return Promise.all(
      PRECACHE_URLS.map(function (url) {
        var r = new Request(url, { cache: 'reload' });
        return cache.add(r).catch(function () {
          return cache.add(url);
        });
      })
    );
  });
}

self.addEventListener('install', function (event) {
  event.waitUntil(precache().then(function () {
    return self.skipWaiting();
  }));
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (key) {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then(function (hit) {
      if (hit) return hit;
      return fetch(req).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            try {
              cache.put(req, copy);
            } catch (_) {}
          });
        }
        return res;
      }).catch(function () {
        var wantsDoc = req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') !== -1;
        if (wantsDoc) {
          return caches.match('./index.html', { ignoreSearch: true }).then(function (page) {
            return page || caches.match('index.html', { ignoreSearch: true });
          });
        }
        return caches.match(req, { ignoreSearch: true });
      });
    })
  );
});
