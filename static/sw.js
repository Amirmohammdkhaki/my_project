// static/sw.js

const CACHE_NAME = 'myblog-v1.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/index.js',
    '/static/images/favicon.ico',
    '/offline/'
];

// نصب Service Worker
self.addEventListener('install', function(event) {
    console.log('🔄 Service Worker installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('✅ Opened cache');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('✅ All resources cached');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ Cache installation failed:', error);
            })
    );
});

// فعال‌سازی Service Worker
self.addEventListener('activate', function(event) {
    console.log('🔄 Service Worker activating...');
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('✅ Service Worker activated');
            return self.clients.claim();
        })
    );
});

// مدیریت درخواست‌ها
self.addEventListener('fetch', function(event) {
    // فقط درخواست‌های GET را مدیریت کن
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // اگر فایل در کش وجود دارد، برگردان
                if (response) {
                    return response;
                }

                // در غیر این صورت از شبکه بگیر
                return fetch(event.request)
                    .then(function(response) {
                        // بررسی که پاسخ معتبر است
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // پاسخ را برای استفاده آینده در کش ذخیره کن
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(function(cache) {
                                cache.put(event.request, responseToCache);
                            });

                        return response;
                    })
                    .catch(function(error) {
                        console.log('❌ Fetch failed; returning offline page:', error);
                        
                        // برای صفحات HTML، صفحه آفلاین نشان بده
                        if (event.request.headers.get('accept').includes('text/html')) {
                            return caches.match('/offline/');
                        }
                        
                        // برای سایر فایل‌ها، null برگردان
                        return null;
                    });
            })
    );
});

// مدیریت push notifications
self.addEventListener('push', function(event) {
    if (!event.data) return;

    const data = event.data.json();
    const options = {
        body: data.body || 'مطلب جدیدی در وبلاگ منتشر شده است!',
        icon: '/static/images/favicon.ico',
        badge: '/static/images/favicon.ico',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(data.title || 'وبلاگ امیرمحمد', options)
    );
});

// کلیک روی notification
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    event.waitUntil(
        clients.matchAll({type: 'window'})
            .then(function(clientList) {
                // اگر یک تب باز از سایت داریم، آن را فعال کن
                for (const client of clientList) {
                    if (client.url === event.notification.data.url && 'focus' in client) {
                        return client.focus();
                    }
                }
                
                // در غیر این صورت، یک تب جدید باز کن
                if (clients.openWindow) {
                    return clients.openWindow(event.notification.data.url);
                }
            })
    );
});

// همگام‌سازی background
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        console.log('🔄 Background sync started');
        // اینجا می‌توانید داده‌های آفلاین را همگام کنید
    }
});

// مدیریت وضعیت آفلاین
function isOnline() {
    return self.navigator.onLine;
}

// گوش دادن به تغییرات وضعیت آنلاین/آفلاین
self.addEventListener('online', function() {
    console.log('✅ Application is online');
    // می‌توانید نوتیفیکیشن بفرستید یا داده‌ها را همگام کنید
});

self.addEventListener('offline', function() {
    console.log('⚠️ Application is offline');
});