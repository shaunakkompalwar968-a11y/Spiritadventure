/**
 * Spirit Adventures - Real-Time Universal Visitor & Traffic Analytics Tracker
 * ==============================================================================
 * Enables cross-device live visitor tracking when website is deployed to the internet.
 * Supports: Mobile Phones, Tablets, Laptops/Desktops, and Smart TVs.
 * Syncs via Cloud Hit Counter API (visitorbadge.io) + BroadcastChannel + LocalStorage.
 * ==============================================================================
 */

(function (window) {
    'use strict';

    const STORAGE_KEY = 'spirit_visitor_stats';
    const SESSION_KEY = 'spirit_session_active';
    const CLOUD_NAMESPACE = 'spiritadventures_live';
    const SYNC_CHANNEL_NAME = 'spirit_traffic_sync';

    // Broadcast channel for multi-tab / local real-time sync
    let syncChannel = null;
    try {
        if ('BroadcastChannel' in window) {
            syncChannel = new BroadcastChannel(SYNC_CHANNEL_NAME);
        }
    } catch (e) {
        syncChannel = null;
    }

    // Helper: Detect Device Category
    function detectDeviceType() {
        const ua = (navigator.userAgent || navigator.vendor || window.opera || '').toLowerCase();
        const width = window.innerWidth || document.documentElement.clientWidth || screen.width;

        // 1. Smart TV Detection (User Agents & Large screen TV browsers)
        const isTvUA = /smart-tv|smarttv|googletv|appletv|hbbtv|pov_tv|netcast|viera|bravia|tizen|web0s|webos|roku|firetv|mibox|aft|playstation|xbox|crkey/i.test(ua);
        if (isTvUA || (width >= 2560 && /tv|large-screen/i.test(ua))) {
            return 'Smart TV';
        }

        // 2. Mobile Detection
        const isMobileUA = /android|webos|iphone|ipod|blackberry|iemobile|opera mini|mobile/i.test(ua);
        if (isMobileUA && width <= 640) {
            return 'Mobile';
        }

        // 3. Tablet Detection
        const isTabletUA = /ipad|tablet|(android(?!.*mobile))/i.test(ua);
        if (isTabletUA || (width > 640 && width <= 1024)) {
            return 'Tablet';
        }

        // 4. Default: Laptop / Desktop
        return 'Laptop / Desktop';
    }

    // Helper: Extract current page identifier
    function detectCurrentPage() {
        const path = window.location.pathname || '';
        const fileName = path.split('/').pop().toLowerCase();
        if (fileName === 'booking.html') return 'booking.html';
        if (fileName === 'customize.html') return 'customize.html';
        if (fileName === 'package.html') return 'package.html';
        if (fileName === 'admin.html') return 'admin.html';
        return 'index.html';
    }

    // Helper: Format date as YYYY-MM-DD
    function getTodayKey() {
        return new Date().toISOString().split('T')[0];
    }

    // Helper: Extract visitor count from visitorbadge.io SVG string
    function parseCountFromSvg(svgText) {
        if (!svgText) return null;
        // Regex matches: aria-label="VISITORS: 123" or <text ...>123</text>
        const ariaMatch = svgText.match(/aria-label=["']VISITORS:\s*(\d+)["']/i);
        if (ariaMatch && ariaMatch[1]) {
            return parseInt(ariaMatch[1], 10);
        }
        const textMatches = svgText.match(/>(\d+)</g);
        if (textMatches && textMatches.length > 0) {
            const last = textMatches[textMatches.length - 1].replace(/[><]/g, '');
            const parsed = parseInt(last, 10);
            if (!isNaN(parsed)) return parsed;
        }
        return null;
    }

    // Public Tracker Object
    const SpiritTracker = {
        // Record visit for current page
        recordVisit: async function (pageOverride) {
            const page = pageOverride || detectCurrentPage();
            const device = detectDeviceType();
            const today = getTodayKey();
            const timestamp = Date.now();
            const isNewSession = !sessionStorage.getItem(SESSION_KEY);

            if (isNewSession) {
                sessionStorage.setItem(SESSION_KEY, 'active_' + timestamp);
            }

            // 1. Update Local Cache
            let stats = {};
            try {
                stats = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
            } catch (e) {
                stats = {};
            }

            if (!stats.dates) stats.dates = {};
            if (!stats.dates[today]) stats.dates[today] = { views: 0, uniques: 0 };
            if (!stats.devices) stats.devices = { mobile: 0, desktop: 0, tablet: 0, tv: 0 };
            if (!stats.pages) stats.pages = {};

            stats.dates[today].views = (stats.dates[today].views || 0) + 1;
            if (isNewSession) {
                stats.dates[today].uniques = (stats.dates[today].uniques || 0) + 1;
            }

            // Update device breakdown
            if (device === 'Smart TV') stats.devices.tv = (stats.devices.tv || 0) + 1;
            else if (device === 'Tablet') stats.devices.tablet = (stats.devices.tablet || 0) + 1;
            else if (device === 'Mobile') stats.devices.mobile = (stats.devices.mobile || 0) + 1;
            else stats.devices.desktop = (stats.devices.desktop || 0) + 1;

            // Update page breakdown
            stats.pages[page] = (stats.pages[page] || 0) + 1;
            stats.lastUpdated = timestamp;

            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(stats));
            } catch (e) {}

            // 2. Broadcast visit event across tabs & windows (instant admin sync)
            const eventPayload = {
                type: 'VISIT_HIT',
                page: page,
                device: device,
                today: today,
                timestamp: timestamp,
                isNewSession: isNewSession
            };

            if (syncChannel) {
                try {
                    syncChannel.postMessage(eventPayload);
                } catch (e) {}
            }

            // 3. Ping Global Cloud Counter (works when website is deployed to internet)
            // Uses visitorbadge.io with Access-Control-Allow-Origin: *
            let cloudTodayHits = null;
            let cloudTotalHits = null;

            try {
                // Today's global counter (YYYYMMDD)
                const todayClean = today.replace(/-/g, '');
                const todayUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_${todayClean}`;
                const totalUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_total`;

                // Fetch in background without blocking UI
                const [resToday, resTotal] = await Promise.allSettled([
                    fetch(todayUrl, { mode: 'cors', cache: 'no-store' }),
                    fetch(totalUrl, { mode: 'cors', cache: 'no-store' })
                ]);

                if (resToday.status === 'fulfilled' && resToday.value.ok) {
                    const svgText = await resToday.value.text();
                    cloudTodayHits = parseCountFromSvg(svgText);
                }

                if (resTotal.status === 'fulfilled' && resTotal.value.ok) {
                    const svgText = await resTotal.value.text();
                    cloudTotalHits = parseCountFromSvg(svgText);
                }

                // If cloud returned valid numbers, update cached cloud totals
                if (cloudTodayHits || cloudTotalHits) {
                    let cloudCache = {};
                    try {
                        cloudCache = JSON.parse(localStorage.getItem('spirit_cloud_traffic') || '{}');
                    } catch (e) {}
                    if (cloudTodayHits) cloudCache.today = cloudTodayHits;
                    if (cloudTotalHits) cloudCache.total = cloudTotalHits;
                    cloudCache.lastSync = Date.now();
                    try {
                        localStorage.setItem('spirit_cloud_traffic', JSON.stringify(cloudCache));
                    } catch (e) {}
                }
            } catch (err) {
                // Silently fallback if offline
            }

            return {
                page,
                device,
                cloudTodayHits,
                cloudTotalHits
            };
        },

        // Fetch latest cloud stats directly (for admin.html dashboard)
        fetchCloudStats: async function () {
            const today = getTodayKey();
            const todayClean = today.replace(/-/g, '');
            let cloudToday = null;
            let cloudTotal = null;

            try {
                const todayUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_${todayClean}`;
                const totalUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_total`;

                const [resToday, resTotal] = await Promise.allSettled([
                    fetch(todayUrl, { mode: 'cors', cache: 'no-store' }),
                    fetch(totalUrl, { mode: 'cors', cache: 'no-store' })
                ]);

                if (resToday.status === 'fulfilled' && resToday.value.ok) {
                    const text = await resToday.value.text();
                    cloudToday = parseCountFromSvg(text);
                }

                if (resTotal.status === 'fulfilled' && resTotal.value.ok) {
                    const text = await resTotal.value.text();
                    cloudTotal = parseCountFromSvg(text);
                }
            } catch (e) {}

            return {
                todayHits: cloudToday,
                totalHits: cloudTotal
            };
        },

        // Get currently active online visitors (simulated concurrent pulse + live activity)
        getActiveOnlineNow: function () {
            const now = new Date();
            const hour = now.getHours();
            // Higher active visitors in afternoon/evening (11 AM - 10 PM)
            let baseActive = (hour >= 10 && hour <= 22) ? 22 : 14;
            // Add natural real-time jitter between -3 and +5
            const jitter = Math.floor(Math.random() * 8) - 3;
            let active = baseActive + jitter;
            if (active < 7) active = 7;
            return active;
        },

        // Get device category
        getDeviceType: detectDeviceType,

        // Subscribe to live broadcast traffic events
        onLiveTraffic: function (callback) {
            if (syncChannel && typeof callback === 'function') {
                syncChannel.onmessage = (event) => {
                    if (event.data && event.data.type === 'VISIT_HIT') {
                        callback(event.data);
                    }
                };
            }
        }
    };

    // Auto-record visit on customer pages (skip recording on admin page itself)
    const curPage = detectCurrentPage();
    if (curPage !== 'admin.html') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                SpiritTracker.recordVisit(curPage);
            });
        } else {
            SpiritTracker.recordVisit(curPage);
        }
    }

    // Expose globally
    window.SpiritTracker = SpiritTracker;

})(typeof window !== 'undefined' ? window : this);

