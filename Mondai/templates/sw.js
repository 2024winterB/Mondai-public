var CACHE_NAME = 'my-pwa-cache-v1';
var urlsToCache = [
  '/mondai/login',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
];

self.addEventListener('install', function(event) {
  // キャッシュを開いて、指定したURLを保存する
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

// フェッチイベントでネットワークファーストの戦略を実行する
self.addEventListener("fetch", function (event) {
  event.respondWith(
    fetch(event.request)
      .then(function (response) {
        // ネットワークからリソースを取得できた場合
        // 新しいキャッシュを開いてリソースを保存する
        return caches.open(CACHE_NAME).then(function (cache) {
          cache.put(event.request, response.clone());
          return response;
        });
      })
      .catch(function () {
        // ネットワークからリソースを取得できなかった場合
        // キャッシュからリソースを探す
        return caches.match(event.request);
      })
  );
});

// アクティベートイベントで古いキャッシュを削除する
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys
          .filter(function (key) {
            // 現在のキャッシュ名と異なるキャッシュを削除する
            return key !== CACHE_NAME;
          })
          .map(function (key) {
            return caches.delete(key);
          })
      );
    })
  );
});