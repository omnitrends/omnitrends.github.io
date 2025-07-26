// Service Worker for OmniTrends
// This enables offline functionality and improves performance

const CACHE_NAME = 'omnitrends-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/about.html',
    '/contact.html',
    '/css/style.css',
    '/js/main.js',
    '/articles/ai-revolution-2024.html',
    '/articles/sustainable-living-guide.html',
    '/articles/remote-work-trends.html'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});