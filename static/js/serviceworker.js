var staticCacheName = 'sigr-v1';

// Arquivos que serão salvos no cache assim que o app abrir pela primeira vez
var filesToCache = [
    '/',
    '/static/images/icon-160x160.png',
    '/static/images/icon-512x512.png',
    // Adicione aqui caminhos para CSS ou JS globais se quiser, ex:
    // '/static/css/base.css',
];

// 1. Instalação do Service Worker
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll(filesToCache);
        })
    );
});

// 2. Intercepta as requisições (A mágica acontece aqui)
self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
            .then(function(response) {
                // Se a internet funcionar:
                // 1. Faz uma cópia da página para o cache
                // 2. Entrega a página para o usuário
                if (event.request.method === 'GET') {
                    var responseClone = response.clone();
                    caches.open(staticCacheName).then(function(cache) {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(function() {
                // Se a internet falhar (Offline):
                // Tenta entregar o que tem no cache
                return caches.match(event.request).then(function(response) {
                    if (response) {
                        return response;
                    }
                    // Se não tiver nada no cache, poderia retornar uma página de offline personalizada aqui
                    // Por enquanto, não retorna nada (o navegador mostra o dinossauro)
                });
            })
    );
});

// 3. Limpeza de caches antigos (Quando você mudar a versão do app)
self.addEventListener('activate', function(event) {
    var cacheWhitelist = [staticCacheName];
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});