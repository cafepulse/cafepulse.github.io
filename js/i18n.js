/* ==========================================================================
   CafePulse Internationalization (i18n) Engine — Vanilla JS
   ========================================================================== */

const i18nConfig = {
    defaultLang: 'en',
    availableLangs: ['en', 'id', 'es'],
    storageKey: 'cafepulse_lang'
};

document.addEventListener('DOMContentLoaded', () => {
    initI18n();
});

function initI18n() {
    const activeLang = getActiveLanguage();
    
    // Set HTML lang attribute
    document.documentElement.lang = activeLang;
    
    // Bind click events on all language selectors in UI
    initLanguageSelectors(activeLang);

    // If active language is English (default), the page is already in English
    // No need to fetch translation JSON file, providing a fast native loading path
    if (activeLang === i18nConfig.defaultLang) {
        return;
    }

    // Load language dictionary and translate DOM
    loadTranslations(activeLang);
}

function getActiveLanguage() {
    // 1. Check URL path (e.g., /id/ or /es/) for pre-rendered pages
    const pathname = window.location.pathname;
    if (pathname.includes('/id/')) {
        return 'id';
    }
    if (pathname.includes('/es/')) {
        return 'es';
    }

    // 2. Check URL parameters (e.g. ?lang=id)
    const urlParams = new URLSearchParams(window.location.search);
    const urlLang = urlParams.get('lang');
    if (urlLang && i18nConfig.availableLangs.includes(urlLang)) {
        localStorage.setItem(i18nConfig.storageKey, urlLang);
        return urlLang;
    }

    // 3. Check localStorage
    const savedLang = localStorage.getItem(i18nConfig.storageKey);
    if (savedLang && i18nConfig.availableLangs.includes(savedLang)) {
        return savedLang;
    }

    // 4. Fallback to browser language
    const browserLang = (navigator.language || navigator.userLanguage).slice(0, 2);
    if (i18nConfig.availableLangs.includes(browserLang)) {
        return browserLang;
    }

    // 5. Default fallback
    return i18nConfig.defaultLang;
}

function loadTranslations(lang) {
    // Dynamically determine relative path prefix to the root website directory
    const pathname = window.location.pathname;
    const isInSubdir = /^\/(id|es)(\/|$)/.test(pathname);
    const pathPrefix = isInSubdir ? '../' : './';
    
    fetch(`${pathPrefix}lang/${lang}.json`)
        .then(res => {
            if (!res.ok) throw new Error(`Could not load translations for: ${lang}`);
            return res.json();
        })
        .then(translations => {
            translatePage(translations);
        })
        .catch(err => {
            console.warn('i18n Error:', err.message);
        });
}

function translatePage(translations) {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translatedValue = getNestedValue(translations, key);
        
        if (translatedValue) {
            // If the element is an input, translate its placeholder attribute
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.setAttribute('placeholder', translatedValue);
            } else {
                // Use innerHTML to support span styling within headers/texts
                el.innerHTML = translatedValue;
            }
        }
    });

    // Translate global page description meta tag for SEO
    const pageDesc = getNestedValue(translations, 'hero.subtitle') || getNestedValue(translations, 'footer.desc');
    const metaDesc = document.querySelector('meta[name="description"]');
    if (pageDesc && metaDesc) {
        metaDesc.setAttribute('content', pageDesc);
    }
}

// Helper: Traverse nested JSON keys (e.g., "hero.title")
function getNestedValue(obj, keyPath) {
    return keyPath.split('.').reduce((acc, part) => {
        return acc ? acc[part] : null;
    }, obj);
}

function initLanguageSelectors(activeLang) {
    // Look for both desktop and mobile select triggers
    const selectors = document.querySelectorAll('.lang-selector-btn');
    
    // Highlight the active option in switcher UI
    selectors.forEach(btn => {
        const langCode = btn.getAttribute('data-lang');
        if (langCode === activeLang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (langCode && i18nConfig.availableLangs.includes(langCode)) {
                localStorage.setItem(i18nConfig.storageKey, langCode);
                
                // Calculate target redirect path matching the folder structure
                const pathname = window.location.pathname;
                
                // Remove existing language folder prefix (/id/ or /es/)
                let cleanPath = pathname.replace(/^\/(id|es)\//, '/');
                
                // If cleanPath didn't start with / because of some relative path environment
                if (!cleanPath.startsWith('/')) {
                    cleanPath = '/' + cleanPath;
                }
                
                let targetPath;
                if (langCode === i18nConfig.defaultLang) {
                    targetPath = cleanPath;
                } else {
                    targetPath = `/${langCode}${cleanPath}`;
                }
                
                // Retain search queries (like ?doc=eula) or hash hashes if any
                const search = window.location.search;
                const hash = window.location.hash;
                
                window.location.href = window.location.origin + targetPath + search + hash;
            }
        });
    });
}
