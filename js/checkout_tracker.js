/**
 * CafePulse — Checkout Parameters & Referral Tracking Script
 * Parses URL query parameters for referral codes (?ref=) and Hardware IDs (?hwid=),
 * persists them in localStorage, and dynamically appends them as order_id to DOKU links.
 */
document.addEventListener("DOMContentLoaded", function() {
    // 1. Capture query parameters from current URL
    const urlParams = new URLSearchParams(window.location.search);
    const refParam = urlParams.get('ref');
    const hwidParam = urlParams.get('hwid');

    // 2. Persist to localStorage if present in URL
    if (refParam) {
        localStorage.setItem('cafepulse_ref', refParam.trim().toUpperCase());
    }
    if (hwidParam) {
        localStorage.setItem('cafepulse_hwid', hwidParam.trim());
    }

    // 3. Retrieve stored values
    const storedRef = localStorage.getItem('cafepulse_ref') || 'NONE';
    const storedHwid = localStorage.getItem('cafepulse_hwid') || '';

    // 4. Locate and rewrite DOKU Payment Links
    const dokuLinks = document.querySelectorAll('a[href*="pay.doku.com"]');
    dokuLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        
        // Determine package tier based on DOKU link ID or path name
        let packageType = 'PRO';
        if (href.includes('GVF6iQnaY6') || window.location.pathname.includes('founder.html')) {
            packageType = 'FOUNDER';
        }

        // Determine mode based on presence of hardware ID
        let modePart = 'WEB';
        if (storedHwid) {
            modePart = 'HWID_' + storedHwid;
        }

        // Assemble order_id: CP-[PACKAGE]_[MODE]-[REF]
        const orderId = 'CP-' + packageType + '_' + modePart + '-' + storedRef;

        // Construct new URL by appending order_id query parameter
        const separator = href.includes('?') ? '&' : '?';
        const newHref = href + separator + 'order_id=' + encodeURIComponent(orderId);
        
        link.setAttribute('href', newHref);
        console.log('CafePulse Tracker: Rewrote checkout link for ' + packageType + ' to: ' + newHref);
    });
});
