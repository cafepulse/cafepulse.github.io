/* ==========================================================================
   CafePulse Website Operations Engine — Vanilla JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDownloadMeta();
    initForms();
    initMarkdownLoader();
    initGlobalCopyBtns();
});

function initGlobalCopyBtns() {
    document.addEventListener('click', (e) => {
        if (e.target && e.target.classList.contains('copy-email-btn')) {
            const email = e.target.getAttribute('data-email');
            if (email) {
                navigator.clipboard.writeText(email);
                const confirmMsg = e.target.nextElementSibling;
                if (confirmMsg && confirmMsg.classList.contains('copy-confirm')) {
                    confirmMsg.style.display = 'block';
                    setTimeout(() => { confirmMsg.style.display = 'none'; }, 3000);
                } else {
                    // Fallback alert if no adjacent element
                    alert("Email address copied: " + email);
                }
            }
        }
    });
}

/* --------------------------------------------------------------------------
   1. Hamburger & Navigation Handler
   -------------------------------------------------------------------------- */
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav');

    if (hamburger && mobileNav) {
        hamburger.addEventListener('click', () => {
            mobileNav.classList.toggle('open');
            hamburger.innerHTML = mobileNav.classList.contains('open') ? '&times;' : '&#9776;';
        });
    }
}

/* --------------------------------------------------------------------------
   2. GitHub Releases API Downloader Info
   -------------------------------------------------------------------------- */
function initDownloadMeta() {
    const metaVer = document.getElementById('meta-ver');
    const metaDate = document.getElementById('meta-date');

    // Only run on download page
    if (metaVer && metaDate) {
        fetch('https://api.github.com/repos/cafepulse/CafePulse/releases/latest')
            .then(res => {
                if (!res.ok) throw new Error('API Rate Limit or Network Error');
                return res.json();
            })
            .then(data => {
                if (data.tag_name) {
                    metaVer.textContent = data.tag_name;
                    
                    // Format Date
                    const pubDate = new Date(data.published_at);
                    const options = { year: 'numeric', month: 'long' };
                    metaDate.textContent = pubDate.toLocaleDateString('en-US', options);

                    // Update download button URLs based on assets if matched
                    const assets = data.assets || [];
                    const winExe = assets.find(a => a.name.endsWith('.exe'));
                    const winZip = assets.find(a => a.name.endsWith('.zip'));
                    const linApp = assets.find(a => a.name.endsWith('.AppImage'));

                    if (winExe) document.getElementById('btn-win-dl').href = winExe.browser_download_url;
                    if (winZip) document.getElementById('btn-win-portable').href = winZip.browser_download_url;
                    if (linApp) document.getElementById('btn-linux-dl').href = linApp.browser_download_url;
                }
            })
            .catch(err => {
                console.warn('Falling back to static download paths:', err.message);
                // Fallbacks are already hardcoded in HTML template
            });
    }
}

/* --------------------------------------------------------------------------
   3. Contact & Bug Forms Handler
   -------------------------------------------------------------------------- */
function initForms() {
    const contactForm = document.getElementById('contact-form');
    const contactStatus = document.getElementById('contact-status-msg');

    if (contactForm && contactStatus) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name    = (document.getElementById('contact-name')?.value    || '').trim();
            const email   = (document.getElementById('contact-email')?.value   || '').trim();
            const subject = (document.getElementById('contact-subject')?.value || '').trim();
            const message = (document.getElementById('contact-msg')?.value     || '').trim();

            // Build a mailto: link that pre-populates the email client
            const to      = 'cafepulse.network@gmail.com';
            const sub     = encodeURIComponent(`[CafePulse] ${subject || 'Support Inquiry'}`);
            const body    = encodeURIComponent(
                `Name: ${name}\nEmail: ${email}\n\n${message}\n\n---\nSent from cafepulse website`
            );
            const mailto  = `mailto:${to}?subject=${sub}&body=${body}`;

            // Open email client
            window.location.href = mailto;

            // Friendly status message with fallbacks
            contactStatus.style.color = 'var(--color-success)';
            contactStatus.innerHTML = `
                <div style="margin-top: 15px; color: var(--text-primary); text-align: center;">
                    <p style="margin-bottom: 10px; font-weight: normal; font-size: 0.9rem;">Your email client has been opened. If it didn't open automatically, use these alternatives:</p>
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${to}&su=${sub}&body=${body}" target="_blank" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Open in Gmail</a>
                        <button type="button" class="btn btn-secondary copy-email-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" data-email="${to}">Copy Email Address</button>
                        <div class="copy-confirm" style="color: var(--color-success); font-size: 0.85rem; display: none; width: 100%;">Email address copied.</div>
                    </div>
                </div>
            `;
            contactStatus.style.display = 'block';
        });
    }

    const betaForm = document.getElementById('beta-report-form');
    const betaStatus = document.getElementById('beta-status-msg');

    if (betaForm && betaStatus) {
        betaForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name    = (document.getElementById('beta-name')?.value    || '').trim();
            const email   = (document.getElementById('beta-email')?.value   || '').trim();
            const subject = (document.getElementById('beta-subject')?.value || 'Beta Bug Report').trim();
            const message = (document.getElementById('beta-msg')?.value     || '').trim();

            const to   = 'cafepulse.network@gmail.com';
            const sub  = encodeURIComponent(`[CafePulse Beta] ${subject}`);
            const body = encodeURIComponent(
                `Name: ${name}\nEmail: ${email}\n\n${message}\n\n---\nSent from CafePulse Beta program page`
            );
            const mailto = `mailto:${to}?subject=${sub}&body=${body}`;

            window.location.href = mailto;

            betaStatus.style.color = 'var(--color-success)';
            betaStatus.innerHTML = `
                <div style="margin-top: 15px; color: var(--text-primary); text-align: center;">
                    <p style="margin-bottom: 10px; font-weight: normal; font-size: 0.9rem;">Your email client has been opened. If it didn't open automatically, use these alternatives:</p>
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${to}&su=${sub}&body=${body}" target="_blank" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Open in Gmail</a>
                        <button type="button" class="btn btn-secondary copy-email-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" data-email="${to}">Copy Email Address</button>
                        <div class="copy-confirm" style="color: var(--color-success); font-size: 0.85rem; display: none; width: 100%;">Email address copied.</div>
                    </div>
                </div>
            `;
            betaStatus.style.display = 'block';
        });
    }
}


/* --------------------------------------------------------------------------
   4. Markdown Parser & Document Loader
   -------------------------------------------------------------------------- */
function initMarkdownLoader() {
    const contentArea = document.getElementById('docs-content');
    if (!contentArea) return; // Only run on documentation page

    // Map URL queries to repository docs paths
    const docMapping = {
        'privacy_policy': './docs/legal/privacy_policy.md',
        'terms_of_service': './docs/legal/terms_of_service.md',
        'eula': './docs/legal/eula.md',
        'refund_policy': './docs/legal/refund_policy.md',
        'trademark_notes': './docs/legal/trademark_notes.md',
        'routeros_config': './docs/routeros_config.md',
        'user_manual_structure': './docs/product/user_manual_structure.md'
    };

    const urlParams = new URLSearchParams(window.location.search);
    const docKey = urlParams.get('doc');

    if (docKey && docMapping[docKey]) {
        // Update sidebar highlights
        document.querySelectorAll('.docs-sidebar a').forEach(a => a.classList.remove('active'));
        const activeLink = document.getElementById(`link-${docKey}`);
        if (activeLink) activeLink.classList.add('active');

        contentArea.innerHTML = '<p style="color: var(--text-secondary);">Loading official policy document...</p>';

        // Fetch markdown content
        fetch(docMapping[docKey])
            .then(res => {
                if (!res.ok) throw new Error(`Failed to load document: ${res.statusText}`);
                return res.text();
            })
            .then(text => {
                contentArea.innerHTML = parseMarkdown(text);
            })
            .catch(err => {
                contentArea.innerHTML = `<h2 style="color: var(--color-danger);">Document Load Failure</h2><p style="color: var(--text-secondary);">${err.message}</p>`;
            });
    }
}

/* --- Core Markdown to HTML Parsing Subsystem --- */
function parseMarkdown(md) {
    let html = '';
    const lines = md.split('\n');
    let inList = false;
    let inCodeBlock = false;
    let inTable = false;
    let tableHeaders = [];
    let tableRows = [];

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        // Code blocks switcher
        if (line.trim().startsWith('```')) {
            if (inCodeBlock) {
                html += '</code></pre>\n';
                inCodeBlock = false;
            } else {
                html += '<pre><code>';
                inCodeBlock = true;
            }
            continue;
        }

        if (inCodeBlock) {
            html += escapeHtml(line) + '\n';
            continue;
        }

        // Table parser
        if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
            if (line.includes('---') || line.includes(':---')) {
                continue; // Skip the markdown column separation markers
            }
            const parts = line.split('|').map(x => x.trim()).filter((x, idx, arr) => idx > 0 && idx < arr.length - 1);
            if (!inTable) {
                inTable = true;
                tableHeaders = parts;
            } else {
                tableRows.push(parts);
            }
            continue;
        } else if (inTable) {
            // Write compiled table block
            html += '<table><thead><tr>';
            tableHeaders.forEach(h => html += `<th>${parseInline(h)}</th>`);
            html += '</tr></thead><tbody>';
            tableRows.forEach(row => {
                html += '<tr>';
                row.forEach(cell => html += `<td>${parseInline(cell)}</td>`);
                html += '</tr>';
            });
            html += '</tbody></table>\n';
            inTable = false;
            tableHeaders = [];
            tableRows = [];
        }

        // Markdown Headers
        if (line.startsWith('# ')) {
            html += `<h1>${parseInline(line.substring(2))}</h1>\n`;
            continue;
        }
        if (line.startsWith('## ')) {
            html += `<h2>${parseInline(line.substring(3))}</h2>\n`;
            continue;
        }
        if (line.startsWith('### ')) {
            html += `<h3>${parseInline(line.substring(4))}</h3>\n`;
            continue;
        }

        // Markdown blockquotes & alert tags support
        if (line.startsWith('>')) {
            let quote = line.substring(1).trim();
            if (quote.startsWith('[!NOTE]') || quote.startsWith('[!IMPORTANT]') || quote.startsWith('[!WARNING]') || quote.startsWith('[!TIP]')) {
                const matchType = quote.match(/\[!(.*)\]/);
                const type = matchType ? matchType[1].toLowerCase() : 'note';
                quote = quote.replace(/\[!.*\]/, '').trim();
                html += `<blockquote class="badge badge-info" style="display: block; border-left: 4px solid var(--accent-blue); padding: 1rem; margin-bottom: 1.5rem; text-transform: none; text-align: left; font-size: 0.95rem; font-weight: normal; background-color: var(--bg-tertiary);"><strong>${type.toUpperCase()}:</strong> ${parseInline(quote)}</blockquote>\n`;
            } else {
                html += `<blockquote style="border-left: 4px solid var(--text-muted); padding-left: 1rem; margin-bottom: 1.5rem; color: var(--text-secondary); font-style: italic;">${parseInline(quote)}</blockquote>\n`;
            }
            continue;
        }

        // List item parser
        if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
            if (!inList) {
                html += '<ul style="margin-left: 1.5rem; margin-bottom: 1.5rem;">\n';
                inList = true;
            }
            html += `<li>${parseInline(line.trim().substring(2))}</li>\n`;
            continue;
        } else if (inList && !line.trim().startsWith('- ') && !line.trim().startsWith('* ')) {
            html += '</ul>\n';
            inList = false;
        }

        // Normal paragraph matching
        if (line.trim() !== '') {
            html += `<p style="margin-bottom: 1rem;">${parseInline(line)}</p>\n`;
        }
    }

    if (inList) html += '</ul>\n';
    return html;
}

function parseInline(text) {
    // Escape standard XML chars
    text = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    // Bold parsing
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Inline code parsing
    text = text.replace(/`(.*?)`/g, '<code style="font-family: var(--font-mono); color: var(--accent-blue); background-color: var(--bg-tertiary); padding: 0.2rem 0.4rem; border-radius: var(--radius-sm); font-size: 0.85em;">$1</code>');
    
    // Hyperlinks mapping [link text](url)
    text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" style="color: var(--accent-blue); text-decoration: none;">$1</a>');
    
    // De-escape formatting tags inside links/bold
    text = text.replace(/&lt;strong&gt;/g, '<strong>').replace(/&lt;\/strong&gt;/g, '</strong>');
    text = text.replace(/&lt;code(.*?)&gt;/g, '<code$1>').replace(/&lt;\/code&gt;/g, '</code>');
    text = text.replace(/&lt;a(.*?)&gt;/g, '<a$1>').replace(/&lt;\/a&gt;/g, '</a>');
    
    return text;
}

function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
