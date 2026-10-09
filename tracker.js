/**
 * Spirit Adventures - Real-Time Universal Visitor & Traffic Analytics Tracker
 * Real visitor tracking, real-time multi-tab session heartbeats, and cloud sync.
 */

(function (window) {
    'use strict';

    const STORAGE_KEY = 'spirit_visitor_stats';
    const SESSION_KEY = 'spirit_session_active';
    const HEARTBEAT_KEY = 'spirit_active_heartbeats';
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

    // Unique Tab Session ID for real concurrent visitor heartbeat
    let tabSessionId = '';
    try {
        tabSessionId = sessionStorage.getItem('spirit_tab_session_id');
        if (!tabSessionId) {
            tabSessionId = 'tab_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);
            sessionStorage.setItem('spirit_tab_session_id', tabSessionId);
        }
    } catch (e) {
        tabSessionId = 'tab_' + Date.now();
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

    // Helper: Detect Referrer / Traffic Source
    function detectReferrerSource() {
        const ref = (document.referrer || '').toLowerCase();
        if (!ref) return 'direct';
        if (ref.includes('google')) return 'google';
        if (ref.includes('instagram') || ref.includes('facebook') || ref.includes('youtube') || ref.includes('tiktok') || ref.includes('twitter') || ref.includes('t.co')) return 'social';
        if (ref.includes('whatsapp') || ref.includes('wa.me')) return 'whatsapp';
        return 'referral';
    }

    // Helper: Format date as YYYY-MM-DD
    function getTodayKey() {
        return new Date().toISOString().split('T')[0];
    }

    // Helper: Extract visitor count from visitorbadge.io SVG string
    function parseCountFromSvg(svgText) {
        if (!svgText) return null;
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

    // Real-Time Heartbeat Management for Concurrent Active Visitors
    function sendHeartbeat(page) {
        try {
            let beats = JSON.parse(localStorage.getItem(HEARTBEAT_KEY) || '{}');
            const now = Date.now();
            // Purge dead sessions older than 30 seconds
            for (const id in beats) {
                if (!beats[id] || (now - (beats[id].lastSeen || 0) > 30000)) {
                    delete beats[id];
                }
            }
            beats[tabSessionId] = {
                id: tabSessionId,
                page: page || detectCurrentPage(),
                device: detectDeviceType(),
                lastSeen: now
            };
            localStorage.setItem(HEARTBEAT_KEY, JSON.stringify(beats));
        } catch (e) {}
    }

    function removeHeartbeat() {
        try {
            let beats = JSON.parse(localStorage.getItem(HEARTBEAT_KEY) || '{}');
            if (beats[tabSessionId]) {
                delete beats[tabSessionId];
                localStorage.setItem(HEARTBEAT_KEY, JSON.stringify(beats));
            }
            if (syncChannel) {
                syncChannel.postMessage({ type: 'SESSION_CLOSED', id: tabSessionId });
            }
        } catch (e) {}
    }

    // Start heartbeat
    sendHeartbeat();
    setInterval(() => sendHeartbeat(), 10000);
    window.addEventListener('beforeunload', removeHeartbeat);

    // Public Tracker Object
    const SpiritTracker = {
        // Record visit for current page
        recordVisit: async function (pageOverride) {
            const page = pageOverride || detectCurrentPage();
            const device = detectDeviceType();
            const source = detectReferrerSource();
            const today = getTodayKey();
            const timestamp = Date.now();
            const isNewSession = !sessionStorage.getItem(SESSION_KEY);

            if (isNewSession) {
                sessionStorage.setItem(SESSION_KEY, 'active_' + timestamp);
            }

            // 1. Update Local Real Visitor Cache
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
            if (!stats.sources) stats.sources = { direct: 0, google: 0, social: 0, whatsapp: 0, referral: 0 };

            stats.dates[today].views = (stats.dates[today].views || 0) + 1;
            if (isNewSession) {
                stats.dates[today].uniques = (stats.dates[today].uniques || 0) + 1;
            }

            // Real device breakdown
            if (device === 'Smart TV') stats.devices.tv = (stats.devices.tv || 0) + 1;
            else if (device === 'Tablet') stats.devices.tablet = (stats.devices.tablet || 0) + 1;
            else if (device === 'Mobile') stats.devices.mobile = (stats.devices.mobile || 0) + 1;
            else stats.devices.desktop = (stats.devices.desktop || 0) + 1;

            // Real page breakdown
            stats.pages[page] = (stats.pages[page] || 0) + 1;

            // Real traffic source breakdown
            stats.sources[source] = (stats.sources[source] || 0) + 1;

            stats.lastUpdated = timestamp;

            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(stats));
            } catch (e) {}

            // Send real heartbeat
            sendHeartbeat(page);

            // 2. Broadcast real visit event across tabs & windows (instant admin sync)
            const eventPayload = {
                type: 'VISIT_HIT',
                page: page,
                device: device,
                source: source,
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
            let cloudTodayHits = null;
            let cloudTotalHits = null;

            try {
                const todayClean = today.replace(/-/g, '');
                const todayUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_${todayClean}`;
                const totalUrl = `https://api.visitorbadge.io/api/visitors?path=${CLOUD_NAMESPACE}_total`;

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
                source,
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

        // Get currently active online visitors (REAL heartbeats of active sessions)
        getActiveOnlineNow: function () {
            try {
                const beats = JSON.parse(localStorage.getItem(HEARTBEAT_KEY) || '{}');
                const now = Date.now();
                let count = 0;
                for (const id in beats) {
                    if (beats[id] && (now - (beats[id].lastSeen || 0) <= 30000)) {
                        count++;
                    }
                }
                return count;
            } catch (e) {
                return 0;
            }
        },

        // Get device category
        getDeviceType: detectDeviceType,

        // Subscribe to live broadcast traffic events
        onLiveTraffic: function (callback) {
            if (syncChannel && typeof callback === 'function') {
                syncChannel.onmessage = (event) => {
                    if (event.data && (event.data.type === 'VISIT_HIT' || event.data.type === 'SESSION_CLOSED')) {
                        callback(event.data);
                    }
                };
            }
        }
    };

    // Auto-record visit on customer pages (skip recording page view count on admin page itself, but maintain heartbeat)
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
