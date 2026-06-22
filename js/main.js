/* ==========================================================================
   CafePulse Website Operations Engine — Vanilla JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDownloadMeta();
    initForms();
    initMarkdownLoader();
    initGlobalCopyBtns();
    initReferrals();
    initTiltEffect();
    initHero3D();
    initLightbox();
    initAbout3D();
    initStorytellingExperience();
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
        // Intercept local testing to use local compiled builds
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.protocol === "file:") {
            const btnWinDl = document.getElementById('btn-win-dl');
            const btnWinPortable = document.getElementById('btn-win-portable');
            if (btnWinDl) btnWinDl.href = "./exports/CafePulse_Free_Setup.exe";
            if (btnWinPortable) btnWinPortable.href = "./exports/CafePulse_Free_Portable.zip";
            metaVer.textContent = "v1.0.0-local";
            metaDate.textContent = "Local Compile";
            return;
        }

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
                `Name: ${name}\nEmail: ${email}\n\n${message}\n\n---\n${(window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_footer) || 'Sent from cafepulse website'}`
            );
            const mailto  = `mailto:${to}?subject=${sub}&body=${body}`;

            // Open email client
            window.location.href = mailto;

            // Friendly status message with fallbacks
            contactStatus.style.color = 'var(--color-success)';
            const statusText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_status) || "Your email client has been opened. If it didn't open automatically, use these alternatives:";
            const openGmailText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.open_gmail) || "Open in Gmail";
            const copyEmailText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.copy_email) || "Copy Email Address";
            const emailCopiedText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_copied) || "Email address copied.";
            
            contactStatus.innerHTML = `
                <div style="margin-top: 15px; color: var(--text-primary); text-align: center;">
                    <p style="margin-bottom: 10px; font-weight: normal; font-size: 0.9rem;">${statusText}</p>
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${to}&su=${sub}&body=${body}" target="_blank" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">${openGmailText}</a>
                        <button type="button" class="btn btn-secondary copy-email-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" data-email="${to}">${copyEmailText}</button>
                        <div class="copy-confirm" style="color: var(--color-success); font-size: 0.85rem; display: none; width: 100%;">${emailCopiedText}</div>
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
                `Name: ${name}\nEmail: ${email}\n\n${message}\n\n---\n${(window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_footer) || 'Sent from CafePulse Beta program page'}`
            );
            const mailto = `mailto:${to}?subject=${sub}&body=${body}`;

            window.location.href = mailto;

            betaStatus.style.color = 'var(--color-success)';
            const statusText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_status) || "Your email client has been opened. If it didn't open automatically, use these alternatives:";
            const openGmailText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.open_gmail) || "Open in Gmail";
            const copyEmailText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.copy_email) || "Copy Email Address";
            const emailCopiedText = (window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.email_copied) || "Email address copied.";
            
            betaStatus.innerHTML = `
                <div style="margin-top: 15px; color: var(--text-primary); text-align: center;">
                    <p style="margin-bottom: 10px; font-weight: normal; font-size: 0.9rem;">${statusText}</p>
                    <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                        <a href="https://mail.google.com/mail/?view=cm&fs=1&to=${to}&su=${sub}&body=${body}" target="_blank" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">${openGmailText}</a>
                        <button type="button" class="btn btn-secondary copy-email-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" data-email="${to}">${copyEmailText}</button>
                        <div class="copy-confirm" style="color: var(--color-success); font-size: 0.85rem; display: none; width: 100%;">${emailCopiedText}</div>
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
        'user_manual_structure': './docs/product/user_manual_structure.md',
        'installation_guide': './docs/installation_guide.md',
        'first_launch_guide': './docs/first_launch_guide.md',
        'system_requirements': './docs/system_requirements.md',
        'changelog': './docs/changelog.md',
        'known_issues': './docs/known_issues.md',
        'product_overview': './docs/product/product_overview.md',
        'editions_comparison': './docs/product/editions_comparison.md',
        'pricing_and_licensing': './docs/pricing_and_licensing.md',
        'bug_reporting_guide': './docs/bug_reporting_guide.md',
        'beta_tester_program': './docs/beta_tester_program.md'
    };

    const urlParams = new URLSearchParams(window.location.search);
    const docKey = urlParams.get('doc');

    if (docKey && docMapping[docKey]) {
        // Update sidebar highlights
        document.querySelectorAll('.docs-sidebar a').forEach(a => a.classList.remove('active'));
        const activeLink = document.getElementById(`link-${docKey}`);
        if (activeLink) activeLink.classList.add('active');

        contentArea.innerHTML = `<p style="color: var(--text-secondary);">${(window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.loading_doc) || 'Loading official policy document...'}</p>`;

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
                contentArea.innerHTML = `<h2 style="color: var(--color-danger);">${(window.__i18nStrings && window.__i18nStrings.forms && window.__i18nStrings.forms.load_error) || 'Document Load Failure'}</h2><p style="color: var(--text-secondary);">${err.message}</p>`;
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

/* --------------------------------------------------------------------------
   5. Referral & Hardware ID Integration
   -------------------------------------------------------------------------- */
function initReferrals() {
    const urlParams = new URLSearchParams(window.location.search);
    const ref = urlParams.get('ref');
    const hwid = urlParams.get('hwid');

    if (ref) {
        localStorage.setItem('cafepulse_ref', ref);
    }
    if (hwid) {
        localStorage.setItem('cafepulse_hwid', hwid);
    }

    const savedRef = localStorage.getItem('cafepulse_ref') || 'NONE';
    const savedHwid = localStorage.getItem('cafepulse_hwid') || 'WEB';

    // Checkout link handling is now dynamically managed by checkout_tracker.js with Midtrans Snap integration.
}

/* --------------------------------------------------------------------------
   6. 3D Hover Tilt Effect for Mockups & Screenshots
   -------------------------------------------------------------------------- */
function initTiltEffect() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    const cards = document.querySelectorAll('.tilt-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const xc = rect.width / 2;
            const yc = rect.height / 2;
            const maxAngle = 8; // gentle, professional tilt
            const angleX = ((yc - y) / yc) * maxAngle;
            const angleY = ((x - xc) / xc) * maxAngle;
            
            card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
        });
    });
}

/* --------------------------------------------------------------------------
   7. 3D WebGL Network Topology Scene (Three.js)
   -------------------------------------------------------------------------- */
function initHero3D() {
    const canvas = document.getElementById('hero-3d-canvas');
    if (!canvas) return; // Only runs on the homepage with the WebGL canvas

    // Stop WebGL on mobile devices (< 1024px) for performance and battery life
    if (window.innerWidth <= 1024) {
        return; 
    }

    // Wait for Three.js library to finish lazy loading
    if (typeof THREE === 'undefined') {
        setTimeout(initHero3D, 150);
        return;
    }

    // Respect system-wide reduced motion settings
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    try {
        // Hide fallback SVG as WebGL initializes successfully
        const fallbackSvg = document.querySelector('.hero-fallback-svg');
        if (fallbackSvg) {
            fallbackSvg.style.transition = 'opacity 0.5s ease';
            fallbackSvg.style.opacity = '0';
            setTimeout(() => { fallbackSvg.style.display = 'none'; }, 500);
        }

        // 1. Scene Setup
        const scene = new THREE.Scene();

        // 2. Camera Setup
        const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
        camera.position.set(0, 0, 7.5);

        // 3. Renderer Setup (with transparency for the background gradient)
        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // cap at 2 for performance

        // 4. Lighting Configuration
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.35);
        scene.add(ambientLight);

        const mainLight = new THREE.DirectionalLight(0x38bdf8, 1.2);
        mainLight.position.set(5, 8, 5);
        scene.add(mainLight);

        const glowLight = new THREE.PointLight(0x38bdf8, 1.5, 8);
        glowLight.position.set(0, 0, 0.5);
        scene.add(glowLight);

        // 5. Build Procedural 3D Network Router (Enterprise Rack Style)
        const routerGroup = new THREE.Group();

        // Router main chassis
        const chassisGeo = new THREE.BoxGeometry(2.4, 0.35, 1.5);
        const chassisMat = new THREE.MeshPhongMaterial({
            color: 0x1e2535,
            specular: 0x38bdf8,
            shininess: 40
        });
        const chassis = new THREE.Mesh(chassisGeo, chassisMat);
        routerGroup.add(chassis);

        // Router rack ears/brackets (enterprise detail)
        const earGeo = new THREE.BoxGeometry(0.1, 0.37, 0.2);
        const earMat = new THREE.MeshPhongMaterial({ color: 0x475569 });
        const leftEar = new THREE.Mesh(earGeo, earMat);
        leftEar.position.set(-1.22, 0, 0.5);
        const rightEar = new THREE.Mesh(earGeo, earMat);
        rightEar.position.set(1.22, 0, 0.5);
        routerGroup.add(leftEar);
        routerGroup.add(rightEar);

        // Antenna on the back left and right
        const antBaseGeo = new THREE.CylinderGeometry(0.06, 0.06, 0.08, 8);
        const antBaseMat = new THREE.MeshPhongMaterial({ color: 0x0f172a });
        const antRodGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.9, 8);
        const antRodMat = new THREE.MeshPhongMaterial({ color: 0x334155 });

        // Left antenna assembly
        const antBaseL = new THREE.Mesh(antBaseGeo, antBaseMat);
        antBaseL.position.set(-1.0, 0.2, -0.6);
        const antRodL = new THREE.Mesh(antRodGeo, antRodMat);
        antRodL.position.set(-1.0, 0.6, -0.6);
        antRodL.rotation.z = 0.15; // angled outwards slightly
        routerGroup.add(antBaseL);
        routerGroup.add(antRodL);

        // Right antenna assembly
        const antBaseR = new THREE.Mesh(antBaseGeo, antBaseMat);
        antBaseR.position.set(1.0, 0.2, -0.6);
        const antRodR = new THREE.Mesh(antRodGeo, antRodMat);
        antRodR.position.set(1.0, 0.6, -0.6);
        antRodR.rotation.z = -0.15;
        routerGroup.add(antBaseR);
        routerGroup.add(antRodR);

        // Glowing status LEDs on front panel
        const ledGeo = new THREE.SphereGeometry(0.035, 8, 8);
        const greenLedMat = new THREE.MeshBasicMaterial({ color: 0x22c55e });
        const blueLedMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
        
        const leds = [];
        for (let i = 0; i < 6; i++) {
            const led = new THREE.Mesh(ledGeo, i % 2 === 0 ? greenLedMat : blueLedMat);
            led.position.set(-0.8 + (i * 0.32), 0, 0.76); // face forward on front panel
            routerGroup.add(led);
            leds.push({
                mesh: led,
                blinkSpeed: 0.05 + (i * 0.02),
                baseColor: i % 2 === 0 ? 0x22c55e : 0x38bdf8
            });
        }

        scene.add(routerGroup);

        // 6. Define Surrounding Client Nodes (Server, Laptop, IoT device)
        const nodeGroup = new THREE.Group();
        scene.add(nodeGroup);

        const clientNodes = [];
        const nodePositions = [
            new THREE.Vector3(-2.6, 1.4, 0.5),    // Top-Left (Server)
            new THREE.Vector3(2.6, 1.2, -0.5),    // Top-Right (Desktop)
            new THREE.Vector3(0.3, -2.0, 0.8)     // Bottom-Center (Smart TV/IoT)
        ];

        const nodeMaterials = [
            new THREE.MeshPhongMaterial({ color: 0x0ea5e9, emissive: 0x082f49 }), // cyan
            new THREE.MeshPhongMaterial({ color: 0x22c55e, emissive: 0x052e16 }), // green
            new THREE.MeshPhongMaterial({ color: 0x38bdf8, emissive: 0x0c4a6e })  // blue-cyan
        ];

        // Client 1 node (Server Rack Box)
        const node1Geo = new THREE.BoxGeometry(0.35, 0.35, 0.35);
        const node1 = new THREE.Mesh(node1Geo, nodeMaterials[0]);
        node1.position.copy(nodePositions[0]);
        nodeGroup.add(node1);
        clientNodes.push(node1);

        // Client 2 node (Laptop Cylinder)
        const node2Geo = new THREE.CylinderGeometry(0.2, 0.2, 0.35, 6);
        const node2 = new THREE.Mesh(node2Geo, nodeMaterials[1]);
        node2.position.copy(nodePositions[1]);
        nodeGroup.add(node2);
        clientNodes.push(node2);

        // Client 3 node (IoT Sphere)
        const node3Geo = new THREE.SphereGeometry(0.22, 12, 12);
        const node3 = new THREE.Mesh(node3Geo, nodeMaterials[2]);
        node3.position.copy(nodePositions[2]);
        nodeGroup.add(node3);
        clientNodes.push(node3);

        // 7. Establish Connections and Particle Data Flow
        const connectionLines = [];
        const dataPackets = [];

        const packetGeo = new THREE.SphereGeometry(0.045, 8, 8);
        const packetMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        nodePositions.forEach((nodePos, idx) => {
            // Draw connection line from Node to Router
            const linePoints = [new THREE.Vector3(0, 0, 0), nodePos];
            const lineGeo = new THREE.BufferGeometry().setFromPoints(linePoints);
            const lineMat = new THREE.LineDashedMaterial({
                color: 0x38bdf8,
                dashSize: 0.2,
                gapSize: 0.1,
                transparent: true,
                opacity: 0.25
            });
            const line = new THREE.Line(lineGeo, lineMat);
            line.computeLineDistances(); // required for dashed line
            scene.add(line);
            connectionLines.push(line);

            // Create flowing data packets (2 per connection path for continuity)
            for (let p = 0; p < 2; p++) {
                const packetMesh = new THREE.Mesh(packetGeo, packetMat);
                scene.add(packetMesh);
                dataPackets.push({
                    mesh: packetMesh,
                    startPos: nodePos.clone(),
                    endPos: new THREE.Vector3(0, 0, 0),
                    progress: p * 0.5, // staggered starts
                    speed: 0.006 + Math.random() * 0.004
                });
            }
        });

        // 8. Interactive Camera Parallax on Mouse Move
        let targetX = 0;
        let targetY = 0;
        let currentX = 0;
        let currentY = 0;

        const heroGrid = document.querySelector('.hero-grid');
        if (heroGrid) {
            heroGrid.addEventListener('mousemove', (e) => {
                const rect = heroGrid.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                // Move limits: -0.8 to 0.8
                targetX = (x - 0.5) * 1.6;
                targetY = (y - 0.5) * 1.6;
            });
            
            heroGrid.addEventListener('mouseleave', () => {
                targetX = 0;
                targetY = 0;
            });
        }

        // 9. Window Resizing Handler
        function onResize() {
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height, false);
        }
        window.addEventListener('resize', onResize);

        // 10. IntersectionObserver to Halt render loop when offscreen (High Performance optimization)
        let isSceneVisible = true;
        const visibilityObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                isSceneVisible = entry.isIntersecting;
            });
        }, { threshold: 0.05 });
        visibilityObserver.observe(canvas);

        // 11. Core Animation Render Loop
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            // Only update rendering calculations if the element is inside the viewport
            if (isSceneVisible) {
                const elapsedTime = clock.getElapsedTime();

                // Damped camera movement (mouse tracking parallax)
                currentX += (targetX - currentX) * 0.06;
                currentY += (targetY - currentY) * 0.06;
                camera.position.x = currentX;
                camera.position.y = -currentY + Math.sin(elapsedTime * 0.5) * 0.08; // slow vertical drift
                camera.lookAt(new THREE.Vector3(0, 0, 0));

                // Slow rotation of router group
                routerGroup.rotation.y = elapsedTime * 0.08;
                routerGroup.rotation.x = Math.sin(elapsedTime * 0.3) * 0.08;

                // Animate orbiting Client Nodes slightly in waves
                clientNodes.forEach((node, idx) => {
                    node.rotation.x += 0.008;
                    node.rotation.y += 0.01;
                    node.position.y = nodePositions[idx].y + Math.sin(elapsedTime * 1.2 + idx) * 0.08;
                });

                // Animate data flow packets
                dataPackets.forEach(packet => {
                    packet.progress += packet.speed;
                    if (packet.progress >= 1.0) {
                        packet.progress = 0.0;
                    }
                    // Interpolate packet position between Client Node and Router Central Node
                    packet.mesh.position.lerpVectors(packet.startPos, packet.endPos, packet.progress);
                    // Add slight sine oscillation to simulate signal wave
                    const wave = Math.sin(packet.progress * Math.PI) * 0.15;
                    packet.mesh.position.y += wave;
                    
                    // Strobe effect on packet scale representing data activity
                    const scale = 0.7 + Math.sin(elapsedTime * 8 + packet.progress) * 0.3;
                    packet.mesh.scale.set(scale, scale, scale);
                });

                // Animate/Flicker router status LEDs
                leds.forEach(led => {
                    const noise = Math.sin(elapsedTime * (1.0 / led.blinkSpeed)) * 0.5 + 0.5;
                    // Switch state based on noise threshold
                    if (noise > 0.65) {
                        led.mesh.material.color.setHex(0x0f172a); // dark / OFF
                    } else {
                        led.mesh.material.color.setHex(led.baseColor); // colored / ON
                    }
                });

                renderer.render(scene, camera);
            }
        }

        // Trigger loop start
        animate();

    } catch (err) {
        console.warn('WebGL Initialization failed or was blocked by browser policies.', err);
    }
}

/* --------------------------------------------------------------------------
   8. Professional Screenshot Lightbox Modal (Zoom)
   -------------------------------------------------------------------------- */
function initLightbox() {
    const zoomableImages = document.querySelectorAll('.tilt-card img');
    if (zoomableImages.length === 0) return; // Exit if no zoomable images on page

    // 1. Create and Append Lightbox Overlay dynamically to DOM
    let overlay = document.getElementById('lightbox-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'lightbox-overlay';
        overlay.className = 'lightbox-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-hidden', 'true');
        overlay.setAttribute('tabindex', '-1');
        overlay.setAttribute('aria-label', (window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.aria_dialog) || 'Screenshot detail view');

        overlay.innerHTML = `
            <button class="lightbox-close" aria-label="${(window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.aria_close) || 'Close detail view'}">&times;</button>
            <button class="lightbox-arrow lightbox-prev" aria-label="${(window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.aria_prev) || 'Previous screenshot'}" style="display: none;">&#10094;</button>
            <div class="lightbox-content">
                <img class="lightbox-img" src="" alt="" tabindex="0">
                <div class="lightbox-caption"></div>
            </div>
            <button class="lightbox-arrow lightbox-next" aria-label="${(window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.aria_next) || 'Next screenshot'}" style="display: none;">&#10095;</button>
        `;
        document.body.appendChild(overlay);
    }

    const closeBtn = overlay.querySelector('.lightbox-close');
    const prevBtn = overlay.querySelector('.lightbox-prev');
    const nextBtn = overlay.querySelector('.lightbox-next');
    const lightboxImg = overlay.querySelector('.lightbox-img');
    const caption = overlay.querySelector('.lightbox-caption');

    let currentIndex = 0;
    let triggerElement = null;

    // Helper: Extract caption from page context
    function getCaption(img) {
        // Try getting closest card title
        const cardTitle = img.closest('.card')?.querySelector('.card-title')?.innerText;
        if (cardTitle) return cardTitle;
        // Fallback to section header
        const sectionHeader = img.closest('section')?.querySelector('h2')?.innerText;
        if (sectionHeader && sectionHeader.length < 50) return sectionHeader;
        // Fallback to alt text or screenshot
        return img.getAttribute('alt') || (window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.caption_fallback) || 'Screenshot Details';
    }

    // Helper: Update Lightbox Image Source & Caption with a smooth transition
    function updateLightbox(index) {
        currentIndex = index;
        const targetImg = zoomableImages[currentIndex];

        // Smooth fade-out before loading new source
        lightboxImg.style.opacity = '0';
        
        setTimeout(() => {
            lightboxImg.src = targetImg.src;
            lightboxImg.alt = targetImg.alt || (window.__i18nStrings && window.__i18nStrings.lightbox && window.__i18nStrings.lightbox.alt_fallback) || 'Enlarged Screenshot';
            caption.innerText = getCaption(targetImg);
            
            lightboxImg.onload = () => {
                lightboxImg.style.opacity = '1';
            };
        }, 120);
    }

    // Open Lightbox Action
    function openLightbox(index, triggerEl) {
        triggerElement = triggerEl;
        overlay.classList.add('active');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
        
        // Show/Hide navigation buttons depending on image count
        if (zoomableImages.length > 1) {
            prevBtn.style.display = 'flex';
            nextBtn.style.display = 'flex';
        } else {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        }

        updateLightbox(index);
        
        // Focus container or close button for accessibility
        setTimeout(() => {
            closeBtn.focus();
        }, 50);
    }

    // Close Lightbox Action
    function closeLightbox() {
        overlay.classList.remove('active');
        overlay.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');
        
        // Return focus to trigger button
        if (triggerElement) {
            triggerElement.focus();
        }
    }

    // Navigate to next index
    function showNext() {
        if (zoomableImages.length <= 1) return;
        const nextIdx = (currentIndex + 1) % zoomableImages.length;
        updateLightbox(nextIdx);
    }

    // Navigate to previous index
    function showPrev() {
        if (zoomableImages.length <= 1) return;
        const prevIdx = (currentIndex - 1 + zoomableImages.length) % zoomableImages.length;
        updateLightbox(prevIdx);
    }

    // Bind click events on all zoomable images
    zoomableImages.forEach((img, idx) => {
        // Style wrapper pointer and accessibility elements
        img.style.cursor = 'zoom-in';
        img.setAttribute('role', 'button');
        img.setAttribute('tabindex', '0');
        img.setAttribute('aria-haspopup', 'dialog');

        const triggerOpen = (e) => {
            e.preventDefault();
            openLightbox(idx, img);
        };

        img.addEventListener('click', triggerOpen);
        img.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                triggerOpen(e);
            }
        });
    });

    // Close on buttons or backdrop click
    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', showPrev);
    nextBtn.addEventListener('click', showNext);

    overlay.addEventListener('click', (e) => {
        // Close if click hits the dark overlay directly (not content/arrows)
        if (e.target === overlay) {
            closeLightbox();
        }
    });

    // Keyboard Navigation & Focus Trap Listener
    document.addEventListener('keydown', (e) => {
        if (!overlay.classList.contains('active')) return;

        // Escape to close
        if (e.key === 'Escape') {
            closeLightbox();
            e.preventDefault();
        }

        // Left Arrow
        if (e.key === 'ArrowLeft') {
            showPrev();
            e.preventDefault();
        }

        // Right Arrow
        if (e.key === 'ArrowRight') {
            showNext();
            e.preventDefault();
        }

        // Tab Focus Trap
        if (e.key === 'Tab') {
            // Find all focusable elements inside the modal
            const focusables = Array.from(overlay.querySelectorAll('button, img[tabindex="0"]'))
                .filter(el => el.style.display !== 'none');
            
            const firstFocusable = focusables[0];
            const lastFocusable = focusables[focusables.length - 1];

            if (e.shiftKey) { // Shift + Tab
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else { // Tab
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

/* --------------------------------------------------------------------------
   9. 3D WebGL About Pulse Core Scene (Three.js + Scroll-Bound Camera Easing)
   -------------------------------------------------------------------------- */
function initAbout3D() {
    const canvas = document.getElementById('about-3d-canvas');
    if (!canvas) return; // Only runs on pages with the about canvas

    if (window.innerWidth <= 1024) {
        return; // Disable on tablet/mobile screens
    }

    if (typeof THREE === 'undefined') {
        setTimeout(initAbout3D, 150);
        return;
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    try {
        // Hide fallback SVG as WebGL mounts successfully
        const fallback = document.querySelector('.about-fallback-svg');
        if (fallback) {
            fallback.style.transition = 'opacity 0.5s ease';
            fallback.style.opacity = '0';
            setTimeout(() => { fallback.style.display = 'none'; }, 500);
        }

        // 1. Scene & Setup
        const scene = new THREE.Scene();

        // 2. Camera Setup
        const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
        
        // Target and current camera/lookAt vectors for smooth LERP transitions
        const cameraPos = new THREE.Vector3(0, 0, 7.0);
        const cameraTargetPos = new THREE.Vector3(0, 0, 7.0);
        const cameraLookAt = new THREE.Vector3(0, 0, 0);
        const cameraTargetLookAt = new THREE.Vector3(0, 0, 0);
        
        camera.position.copy(cameraPos);

        // 3. Renderer Setup (transparent)
        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        // 4. Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.35);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x38bdf8, 1.8, 10);
        pointLight.position.set(0, 0, 1.0);
        scene.add(pointLight);

        const dirLight = new THREE.DirectionalLight(0x38bdf8, 0.8);
        dirLight.position.set(2, 4, 3);
        scene.add(dirLight);

        // 5. Central Node Group (CafePulse Core)
        const coreGroup = new THREE.Group();
        scene.add(coreGroup);

        const outerCoreGeo = new THREE.IcosahedronGeometry(0.8, 1);
        const outerCoreMat = new THREE.MeshPhongMaterial({
            color: 0x38bdf8,
            wireframe: true,
            transparent: true,
            opacity: 0.75
        });
        const outerCore = new THREE.Mesh(outerCoreGeo, outerCoreMat);
        coreGroup.add(outerCore);

        const innerCoreGeo = new THREE.SphereGeometry(0.24, 16, 16);
        const innerCoreMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
        const innerCore = new THREE.Mesh(innerCoreGeo, innerCoreMat);
        coreGroup.add(innerCore);

        // 6. Orbiting Satellites (DHCP, Voucher, Diagnostics, Monitoring)
        const satellites = [];
        const satGroup = new THREE.Group();
        scene.add(satGroup);

        // Define 4 satellite configurations matching page modules
        const satConfigs = [
            {
                name: 'Monitoring',
                pos: new THREE.Vector3(0, 2.0, 0),
                color: 0x22c55e, // green
                geo: new THREE.SphereGeometry(0.2, 12, 12),
                id: 'about-sec-vision'
            },
            {
                name: 'DHCP',
                pos: new THREE.Vector3(-2.0, 0, 0),
                color: 0xeab308, // yellow
                geo: new THREE.CylinderGeometry(0.14, 0.14, 0.35, 6),
                id: 'about-sec-offline'
            },
            {
                name: 'Voucher',
                pos: new THREE.Vector3(0, -2.0, 0),
                color: 0x0ea5e9, // blue-cyan
                geo: new THREE.BoxGeometry(0.3, 0.3, 0.3),
                id: 'about-sec-voucher'
            },
            {
                name: 'Diagnostics',
                pos: new THREE.Vector3(2.0, 0, 0),
                color: 0xef4444, // red
                geo: new THREE.TorusGeometry(0.14, 0.05, 8, 16),
                id: 'about-sec-builder'
            }
        ];

        const lineMat = new THREE.LineDashedMaterial({
            color: 0x38bdf8,
            dashSize: 0.15,
            gapSize: 0.08,
            transparent: true,
            opacity: 0.2
        });

        satConfigs.forEach((config) => {
            const meshMat = new THREE.MeshPhongMaterial({
                color: config.color,
                emissive: config.color,
                emissiveIntensity: 0.1,
                shininess: 30
            });
            const mesh = new THREE.Mesh(config.geo, meshMat);
            mesh.position.copy(config.pos);
            satGroup.add(mesh);

            // Connect satellite to core with a dashed line
            const points = [new THREE.Vector3(0, 0, 0), config.pos];
            const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
            const line = new THREE.Line(lineGeo, lineMat);
            line.computeLineDistances();
            scene.add(line);

            satellites.push({
                mesh: mesh,
                config: config,
                baseScale: 1.0,
                targetScale: 1.0,
                baseIntensity: 0.1,
                targetIntensity: 0.1
            });
        });

        // 7. Data Flow Particles along active paths
        const dataPackets = [];
        const packetGeo = new THREE.SphereGeometry(0.04, 8, 8);
        const packetMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        satConfigs.forEach((config) => {
            const packet = new THREE.Mesh(packetGeo, packetMat);
            scene.add(packet);
            dataPackets.push({
                mesh: packet,
                startPos: config.pos.clone(),
                endPos: new THREE.Vector3(0, 0, 0),
                progress: Math.random(),
                speed: 0.008 + Math.random() * 0.004,
                active: true
            });
        });

        // 8. Defining Cinematic Camera States for Scroll triggers
        const cameraStates = {
            'about-sec-problem': { posX: 0, posY: 0.4, posZ: 6.8, lookX: 0, lookY: 0, lookZ: 0, highlightId: null },
            'about-sec-offline': { posX: -1.0, posY: 0.8, posZ: 4.8, lookX: -1.8, lookY: 0, lookZ: 0, highlightId: 'about-sec-offline' },
            'about-sec-voucher': { posX: 1.0, posY: -0.8, posZ: 4.8, lookX: 0, lookY: -1.8, lookZ: 0, highlightId: 'about-sec-voucher' },
            'about-sec-builder': { posX: 1.2, posY: 0.2, posZ: 4.8, lookX: 1.8, lookY: 0, lookZ: 0, highlightId: 'about-sec-builder' },
            'about-sec-vision': { posX: 0, posY: 0.8, posZ: 4.8, lookX: 0, lookY: 1.8, lookZ: 0, highlightId: 'about-sec-vision' }
        };

        let activeState = cameraStates['about-sec-problem'];

        // 9. IntersectionObserver Setup on Sub-Sections
        const textSections = document.querySelectorAll('.about-scroll-section');
        const scrollObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    if (cameraStates[id]) {
                        activeState = cameraStates[id];
                        
                        // Update satellite highlight target states
                        satellites.forEach(sat => {
                            if (sat.config.id === activeState.highlightId) {
                                sat.targetScale = 1.35;
                                sat.targetIntensity = 0.8;
                            } else {
                                sat.targetScale = 1.0;
                                sat.targetIntensity = 0.1;
                            }
                        });
                    }
                }
            });
        }, { threshold: 0.45 });

        textSections.forEach(section => scrollObserver.observe(section));

        // 10. Interactive Mouse Move Parallax
        let mouseX = 0, mouseY = 0;
        const splitContainer = document.querySelector('.about-split-container');
        if (splitContainer) {
            splitContainer.addEventListener('mousemove', (e) => {
                const rect = splitContainer.getBoundingClientRect();
                mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 1.2;
                mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 1.2;
            });
            
            splitContainer.addEventListener('mouseleave', () => {
                mouseX = 0;
                mouseY = 0;
            });
        }

        // 11. Responsive Handler
        function onResize() {
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height, false);
        }
        window.addEventListener('resize', onResize);

        // 12. Visibility Optimization Observer
        let isSceneVisible = true;
        const visibilityObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                isSceneVisible = entry.isIntersecting;
            });
        }, { threshold: 0.05 });
        visibilityObserver.observe(canvas);

        // 13. Render Loop
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            if (isSceneVisible) {
                const elapsedTime = clock.getElapsedTime();

                // LERP Camera Position (incorporating mouse move offsets)
                const currentTargetX = activeState.posX + mouseX;
                const currentTargetY = activeState.posY - mouseY;
                const currentTargetZ = activeState.posZ;

                cameraPos.x += (currentTargetX - cameraPos.x) * 0.05;
                cameraPos.y += (currentTargetY - cameraPos.y) * 0.05;
                cameraPos.z += (currentTargetZ - cameraPos.z) * 0.05;
                camera.position.copy(cameraPos);

                // LERP lookAt Vector
                cameraTargetLookAt.x += (activeState.lookX - cameraTargetLookAt.x) * 0.05;
                cameraTargetLookAt.y += (activeState.lookY - cameraTargetLookAt.y) * 0.05;
                cameraTargetLookAt.z += (activeState.lookZ - cameraTargetLookAt.z) * 0.05;
                camera.lookAt(cameraTargetLookAt);

                // Pulse the central core wireframe geometry
                const corePulse = 1.0 + Math.sin(elapsedTime * 1.5) * 0.08;
                coreGroup.scale.set(corePulse, corePulse, corePulse);
                coreGroup.rotation.y = elapsedTime * 0.15;
                coreGroup.rotation.x = Math.cos(elapsedTime * 0.2) * 0.1;

                // Animate orbiting satellites
                satellites.forEach(sat => {
                    // Slow idle spin of meshes
                    sat.mesh.rotation.y += 0.01;
                    sat.mesh.rotation.x += 0.008;

                    // Interpolate highlights (emissive glow & scale)
                    const currentScale = sat.mesh.scale.x;
                    const nextScale = currentScale + (sat.targetScale - currentScale) * 0.08;
                    sat.mesh.scale.set(nextScale, nextScale, nextScale);

                    const currentIntensity = sat.mesh.material.emissiveIntensity;
                    sat.mesh.material.emissiveIntensity = currentIntensity + (sat.targetIntensity - currentIntensity) * 0.08;

                    // Wave node height when highlighted
                    if (sat.config.id === activeState.highlightId) {
                        sat.mesh.position.y = sat.config.pos.y + Math.sin(elapsedTime * 2.5) * 0.05;
                    } else {
                        sat.mesh.position.y = sat.config.pos.y;
                    }
                });

                // Animate packets flowing along connections
                dataPackets.forEach((packet, idx) => {
                    const sat = satellites[idx];
                    const isHighlighted = (sat.config.id === activeState.highlightId);

                    // Speed up packet flows if the node is active
                    packet.progress += packet.speed * (isHighlighted ? 1.5 : 0.6);
                    if (packet.progress >= 1.0) {
                        packet.progress = 0.0;
                    }

                    // Lerp position
                    packet.mesh.position.lerpVectors(packet.startPos, packet.endPos, packet.progress);
                    
                    // Emphasize glowing packet when active
                    const scaleFactor = (isHighlighted ? 1.4 : 0.7);
                    packet.mesh.scale.set(scaleFactor, scaleFactor, scaleFactor);
                });

                renderer.render(scene, camera);
            }
        }

        animate();

    } catch (err) {
        console.warn('WebGL Initialization failed in About page context.', err);
    }
}

/* --------------------------------------------------------------------------
   10. Inside CafePulse (Interactive Product Storytelling Experience) (Three.js)
   -------------------------------------------------------------------------- */
function initStorytellingExperience() {
    const canvas = document.getElementById('story-3d-canvas');
    if (!canvas) return; // Only runs on the homepage with the storytelling WebGL canvas

    // Stop WebGL on mobile devices (< 1024px) for performance and battery life
    if (window.innerWidth <= 1024) {
        return; 
    }

    // Wait for Three.js library to finish lazy loading
    if (typeof THREE === 'undefined') {
        setTimeout(initStorytellingExperience, 150);
        return;
    }

    // Respect system-wide reduced motion settings
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    try {
        // 1. Scene Setup
        const scene = new THREE.Scene();

        // 2. Camera Setup
        const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
        
        // Initial state values
        let currentSceneFloat = 0;
        let targetSceneFloat = 0;

        // Camera Keyframes (Position & LookAt) for 10 scenes (0 to 9)
        const cameraKeyframes = [
            { posX: 0, posY: 1.2, posZ: 6.5, lookX: 0, lookY: 0, lookZ: 0 },      // Scene 1: Reality of Net Ops (chaos)
            { posX: 0, posY: 0.5, posZ: 4.5, lookX: 0, lookY: 0, lookZ: 0 },      // Scene 2: Visibility Problem (faded)
            { posX: 0.5, posY: 0.5, posZ: 5.0, lookX: 0, lookY: 0, lookZ: 0 },    // Scene 3: Monitoring (bright cyan flow)
            { posX: -1.0, posY: 0.5, posZ: 4.5, lookX: -0.5, lookY: 0, lookZ: 0 }, // Scene 4: DHCP Leases (zoom left)
            { posX: 1.0, posY: -0.5, posZ: 4.5, lookX: 0.8, lookY: -0.2, lookZ: 0 },// Scene 5: Hotspot Vouchers (zoom right-down)
            { posX: 0.5, posY: 0.2, posZ: 4.0, lookX: 1.2, lookY: -0.5, lookZ: 0 }, // Scene 6: Diagnostics (focus red node)
            { posX: 0, posY: 1.0, posZ: 8.5, lookX: 0, lookY: 0, lookZ: 0 },      // Scene 7: Local First Architecture (zoom out, boundary)
            { posX: 0, posY: 0.3, posZ: 5.5, lookX: 0, lookY: 0, lookZ: 0 },      // Scene 8: Chaos vs Integrated (UI frame)
            { posX: -0.5, posY: 0.4, posZ: 5.0, lookX: 0, lookY: 0.1, lookZ: 0 },  // Scene 9: Operator Experience (UI glow)
            { posX: 0.2, posY: 0.6, posZ: 6.0, lookX: 0, lookY: 0, lookZ: 0 }       // Scene 10: Future of CafePulse (expansion)
        ];

        // 3. Renderer Setup (transparent)
        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        // 4. Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x38bdf8, 2.0, 12);
        pointLight.position.set(0, 0, 1.5);
        scene.add(pointLight);

        const dirLight = new THREE.DirectionalLight(0x38bdf8, 1.0);
        dirLight.position.set(3, 5, 4);
        scene.add(dirLight);

        // 5. Central Router Box
        const routerGroup = new THREE.Group();
        const chassisGeo = new THREE.BoxGeometry(1.2, 0.18, 0.8);
        const chassisMat = new THREE.MeshPhongMaterial({
            color: 0x1e2535,
            specular: 0x38bdf8,
            shininess: 50
        });
        const chassis = new THREE.Mesh(chassisGeo, chassisMat);
        routerGroup.add(chassis);

        // LED indicators
        const ledGeo = new THREE.SphereGeometry(0.02, 8, 8);
        const greenLedMat = new THREE.MeshBasicMaterial({ color: 0x22c55e });
        const blueLedMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
        const leds = [];
        for (let i = 0; i < 4; i++) {
            const led = new THREE.Mesh(ledGeo, i % 2 === 0 ? greenLedMat : blueLedMat);
            led.position.set(-0.4 + (i * 0.25), 0, 0.41);
            routerGroup.add(led);
            leds.push({ mesh: led, baseColor: i % 2 === 0 ? 0x22c55e : 0x38bdf8, blinkSpeed: 0.05 + i * 0.03 });
        }
        scene.add(routerGroup);

        // 6. Client Nodes (arranged in topology ring/grid)
        const clientGroup = new THREE.Group();
        scene.add(clientGroup);

        const clientPositions = [
            new THREE.Vector3(-1.8, 1.0, 0),     // Top-Left (Server)
            new THREE.Vector3(1.8, 0.8, -0.5),   // Top-Right (Desktop)
            new THREE.Vector3(1.2, -1.0, 0.5),   // Bottom-Right (Phone) -> will represent diagnostics error
            new THREE.Vector3(-1.4, -0.8, -0.2), // Bottom-Left (Laptop)
            new THREE.Vector3(0, 1.3, -0.6),     // Top-Center (AP)
            new THREE.Vector3(-0.8, -1.3, -0.4)  // Bottom-Center (Smart TV)
        ];

        const nodeMats = [
            new THREE.MeshPhongMaterial({ color: 0x38bdf8, shininess: 30 }),
            new THREE.MeshPhongMaterial({ color: 0x22c55e, shininess: 30 }),
            new THREE.MeshPhongMaterial({ color: 0xeab308, shininess: 30 }),
            new THREE.MeshPhongMaterial({ color: 0x38bdf8, shininess: 30 }),
            new THREE.MeshPhongMaterial({ color: 0x22c55e, shininess: 30 }),
            new THREE.MeshPhongMaterial({ color: 0xeab308, shininess: 30 })
        ];

        const nodeGeometries = [
            new THREE.BoxGeometry(0.24, 0.24, 0.24),
            new THREE.CylinderGeometry(0.12, 0.12, 0.24, 6),
            new THREE.SphereGeometry(0.14, 12, 12),
            new THREE.BoxGeometry(0.22, 0.22, 0.22),
            new THREE.CylinderGeometry(0.12, 0.12, 0.24, 6),
            new THREE.SphereGeometry(0.13, 12, 12)
        ];

        const clientNodes = [];
        const lines = [];

        const lineDashedMat = new THREE.LineDashedMaterial({
            color: 0x38bdf8,
            dashSize: 0.12,
            gapSize: 0.08,
            transparent: true,
            opacity: 0.25
        });

        clientPositions.forEach((pos, idx) => {
            const mesh = new THREE.Mesh(nodeGeometries[idx % nodeGeometries.length], nodeMats[idx % nodeMats.length].clone());
            mesh.position.copy(pos);
            clientGroup.add(mesh);
            clientNodes.push(mesh);

            // Connection line
            const points = [new THREE.Vector3(0, 0, 0), pos];
            const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
            const line = new THREE.Line(lineGeo, lineDashedMat);
            line.computeLineDistances();
            scene.add(line);
            lines.push(line);
        });

        // 7. Data Flow Packets (flowing along connections)
        const dataPackets = [];
        const packetGeo = new THREE.SphereGeometry(0.035, 8, 8);
        const packetMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
        
        clientPositions.forEach((pos, idx) => {
            for (let p = 0; p < 2; p++) {
                const mesh = new THREE.Mesh(packetGeo, packetMat);
                scene.add(mesh);
                dataPackets.push({
                    mesh: mesh,
                    startPos: pos.clone(),
                    endPos: new THREE.Vector3(0, 0, 0),
                    progress: p * 0.5,
                    speed: 0.007 + Math.random() * 0.004
                });
            }
        });

        // 8. Voucher Stack
        const voucherGroup = new THREE.Group();
        const sheetGeo = new THREE.BoxGeometry(0.35, 0.008, 0.5);
        const sheetMat = new THREE.MeshPhongMaterial({
            color: 0xf8fafc,
            transparent: true,
            opacity: 0.9,
            shininess: 10
        });
        for (let i = 0; i < 6; i++) {
            const sheet = new THREE.Mesh(sheetGeo, sheetMat);
            sheet.position.y = i * 0.03;
            sheet.rotation.y = (i * 0.08) - 0.2;
            voucherGroup.add(sheet);
        }
        voucherGroup.position.set(1.0, -0.6, 0.3);
        voucherGroup.scale.set(0.001, 0.001, 0.001); // hidden initially
        scene.add(voucherGroup);

        // 9. SQLite Database Cylinder
        const dbGroup = new THREE.Group();
        const dbDiscGeo = new THREE.CylinderGeometry(0.2, 0.2, 0.08, 16);
        const dbDiscMat = new THREE.MeshPhongMaterial({ color: 0x38bdf8, shininess: 40 });
        for (let i = 0; i < 3; i++) {
            const disc = new THREE.Mesh(dbDiscGeo, dbDiscMat);
            disc.position.y = (i - 1) * 0.11;
            dbGroup.add(disc);
        }
        dbGroup.position.set(-1.0, -0.5, 0.3);
        dbGroup.scale.set(0.001, 0.001, 0.001); // hidden initially
        scene.add(dbGroup);

        // 10. Local Cage Boundary Box
        const cageGeo = new THREE.BoxGeometry(3.6, 2.8, 3.6);
        const cageMat = new THREE.MeshBasicMaterial({
            color: 0x22c55e,
            wireframe: true,
            transparent: true,
            opacity: 0
        });
        const localCage = new THREE.Mesh(cageGeo, cageMat);
        scene.add(localCage);

        // 11. Cloud Node (external/internet dependency)
        const cloudNode = new THREE.Mesh(
            new THREE.SphereGeometry(0.25, 12, 12),
            new THREE.MeshPhongMaterial({ color: 0x475569, transparent: true, opacity: 0 })
        );
        cloudNode.position.set(4.2, 2.2, -3.0);
        scene.add(cloudNode);

        const cloudLinePoints = [new THREE.Vector3(0, 0, 0), cloudNode.position];
        const cloudLine = new THREE.Line(
            new THREE.BufferGeometry().setFromPoints(cloudLinePoints),
            new THREE.LineDashedMaterial({ color: 0xef4444, dashSize: 0.1, gapSize: 0.1, transparent: true, opacity: 0 })
        );
        cloudLine.computeLineDistances();
        scene.add(cloudLine);

        // 12. Diagnostics Alert Ring (Expanding wave)
        const alertRing = new THREE.Mesh(
            new THREE.RingGeometry(0.04, 0.2, 32),
            new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 0 })
        );
        alertRing.rotation.x = Math.PI / 2;
        scene.add(alertRing);

        // 13. UI Wireframe / Dashboard Frame
        const uiGroup = new THREE.Group();
        const uiFrame = new THREE.Mesh(
            new THREE.BoxGeometry(3.4, 2.2, 0.04),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0 })
        );
        uiGroup.add(uiFrame);
        uiGroup.position.set(0, 0, 1.2);
        uiGroup.scale.set(0.001, 0.001, 0.001); // hidden initially
        scene.add(uiGroup);

        // 14. Chaos Elements (Spreadsheet, winbox, notepad boxes)
        const chaosGroup = new THREE.Group();
        const chaosBoxes = [];
        const boxGeo = new THREE.BoxGeometry(0.22, 0.22, 0.22);
        const boxMat = new THREE.MeshPhongMaterial({ color: 0x94a3b8, wireframe: true, transparent: true, opacity: 0.4 });
        
        const chaosTargets = [
            new THREE.Vector3(-1.8, 0.2, 0.8),
            new THREE.Vector3(1.6, -0.4, 0.6),
            new THREE.Vector3(0.5, 1.4, -0.6),
            new THREE.Vector3(-0.9, -1.0, 0.7)
        ];
        
        for (let i = 0; i < 4; i++) {
            const box = new THREE.Mesh(boxGeo, boxMat.clone());
            box.position.copy(chaosTargets[i]);
            chaosGroup.add(box);
            chaosBoxes.push({
                mesh: box,
                basePos: chaosTargets[i].clone(),
                driftSeed: Math.random() * 10
            });
        }
        scene.add(chaosGroup);

        // 15. Track Interactive Mouse Move Parallax
        let mouseX = 0, mouseY = 0;
        const storytellingSection = document.getElementById('storytelling');

        storytellingSection.addEventListener('mousemove', (e) => {
            const rect = storytellingSection.getBoundingClientRect();
            mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 1.5;
            mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 1.5;
        });

        storytellingSection.addEventListener('mouseleave', () => {
            mouseX = 0;
            mouseY = 0;
        });

        // 16. Window resizing handler
        function onResize() {
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height, false);
        }
        window.addEventListener('resize', onResize);

        // 17. IntersectionObserver to Halt render loop when offscreen
        let isSceneVisible = true;
        const visibilityObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                isSceneVisible = entry.isIntersecting;
            });
        }, { threshold: 0.05 });
        visibilityObserver.observe(canvas);

        // 18. Scroll Monitor Logic
        function updateScrollState() {
            const rect = storytellingSection.getBoundingClientRect();
            const totalScrollableHeight = storytellingSection.scrollHeight - window.innerHeight;
            
            // Calculate scrolled offset within storytelling section bounds
            const scrolled = -rect.top;
            let progress = scrolled / totalScrollableHeight;
            progress = Math.max(0, Math.min(1, progress)); // clamp between 0.0 and 1.0

            targetSceneFloat = progress * 9.0; // maps progress 0.0-1.0 to scene index float 0.0-9.0

            // Toggle active classes on text cards
            const sceneIndex = Math.min(Math.floor(progress * 10.0), 9);
            const cards = storytellingSection.querySelectorAll('.story-card');
            cards.forEach((card, idx) => {
                if (idx === sceneIndex) {
                    card.classList.add('active');
                } else {
                    card.classList.remove('active');
                }
            });
        }
        window.addEventListener('scroll', updateScrollState);
        updateScrollState(); // initial calculation

        // 19. Animation Loop
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            if (isSceneVisible) {
                const elapsedTime = clock.getElapsedTime();

                // LERP scroll float state
                currentSceneFloat += (targetSceneFloat - currentSceneFloat) * 0.08;

                // Resolve Interpolated Camera State
                const baseIdx = Math.floor(currentSceneFloat);
                const nextIdx = Math.min(baseIdx + 1, 9);
                const alpha = currentSceneFloat - baseIdx;

                const baseKF = cameraKeyframes[baseIdx];
                const nextKF = cameraKeyframes[nextIdx];

                // Camera Position Interpolation
                const targetCamX = baseKF.posX + (nextKF.posX - baseKF.posX) * alpha + mouseX * 0.5;
                const targetCamY = baseKF.posY + (nextKF.posY - baseKF.posY) * alpha - mouseY * 0.5;
                const targetCamZ = baseKF.posZ + (nextKF.posZ - baseKF.posZ) * alpha;

                camera.position.x += (targetCamX - camera.position.x) * 0.08;
                camera.position.y += (targetCamY - camera.position.y) * 0.08;
                camera.position.z += (targetCamZ - camera.position.z) * 0.08;

                // LookAt Interpolation
                const targetLookX = baseKF.lookX + (nextKF.lookX - baseKF.lookX) * alpha;
                const targetLookY = baseKF.lookY + (nextKF.lookY - baseKF.lookY) * alpha;
                const targetLookZ = baseKF.lookZ + (nextKF.lookZ - baseKF.lookZ) * alpha;
                
                if (!window._storyCamLookAt) {
                    window._storyCamLookAt = new THREE.Vector3(0, 0, 0);
                }
                window._storyCamLookAt.x += (targetLookX - window._storyCamLookAt.x) * 0.08;
                window._storyCamLookAt.y += (targetLookY - window._storyCamLookAt.y) * 0.08;
                window._storyCamLookAt.z += (targetLookZ - window._storyCamLookAt.z) * 0.08;
                camera.lookAt(window._storyCamLookAt);

                // --- RESOLVE SCENE-SPECIFIC OBJECT PROPERTIES ---
                // Fades out chaos boxes from Scene 1 to Scene 3
                let chaosOpacity = 0.4;
                if (currentSceneFloat > 1.0) {
                    chaosOpacity = Math.max(0, 0.4 * (2.0 - currentSceneFloat));
                }
                let uiMergeAlpha = 0;
                if (currentSceneFloat > 7.0) {
                    uiMergeAlpha = Math.min(1.0, currentSceneFloat - 7.0);
                    chaosOpacity = 0.3 * uiMergeAlpha;
                }

                chaosBoxes.forEach((cb, idx) => {
                    cb.mesh.material.opacity = chaosOpacity;
                    
                    if (uiMergeAlpha > 0) {
                        const corners = [
                            new THREE.Vector3(-1.6, 1.0, 1.2),
                            new THREE.Vector3(1.6, 1.0, 1.2),
                            new THREE.Vector3(-1.6, -1.0, 1.2),
                            new THREE.Vector3(1.6, -1.0, 1.2)
                        ];
                        cb.mesh.position.lerpVectors(cb.basePos, corners[idx], uiMergeAlpha);
                        cb.mesh.rotation.y = elapsedTime * 0.5 * uiMergeAlpha;
                    } else {
                        const t = elapsedTime + cb.driftSeed;
                        cb.mesh.position.x = cb.basePos.x + Math.sin(t * 0.5) * 0.15;
                        cb.mesh.position.y = cb.basePos.y + Math.cos(t * 0.4) * 0.15;
                        cb.mesh.position.z = cb.basePos.z + Math.sin(t * 0.3) * 0.15;
                        cb.mesh.rotation.x += 0.005;
                        cb.mesh.rotation.y += 0.006;
                    }
                });

                // Scene 2: Network dimming/fading
                let netBrightness = 1.0;
                if (currentSceneFloat > 0.5 && currentSceneFloat <= 1.5) {
                    netBrightness = 1.0 - (0.85 * Math.sin((currentSceneFloat - 0.5) * Math.PI));
                } else if (currentSceneFloat > 1.5 && currentSceneFloat <= 2.0) {
                    netBrightness = 0.15 + 0.85 * (currentSceneFloat - 1.5) / 0.5;
                }

                clientNodes.forEach((node, idx) => {
                    node.material.color.setHex(nodeMats[idx % nodeMats.length].color.getHex());
                    node.material.color.multiplyScalar(netBrightness);
                    
                    node.position.y = clientPositions[idx].y + Math.sin(elapsedTime * 1.5 + idx) * 0.06;
                    node.rotation.y += 0.008;
                });

                lines.forEach((line) => {
                    line.material.opacity = 0.25 * netBrightness;
                });

                // Scene 3: Monitoring flow speeds
                let packetSpeedMultiplier = 1.0;
                if (currentSceneFloat >= 1.5 && currentSceneFloat <= 3.0) {
                    packetSpeedMultiplier = 1.0 + 1.5 * (currentSceneFloat - 1.5) / 1.5;
                } else if (currentSceneFloat > 3.0) {
                    packetSpeedMultiplier = 1.2;
                }
                let packetOpacity = 1.0;
                if (currentSceneFloat > 0.5 && currentSceneFloat <= 1.5) {
                    packetOpacity = Math.max(0, 1.0 - (currentSceneFloat - 0.5) / 0.5);
                }

                dataPackets.forEach(p => {
                    p.mesh.material.opacity = packetOpacity;
                    if (packetOpacity > 0) {
                        p.progress += p.speed * packetSpeedMultiplier;
                        if (p.progress >= 1.0) {
                            p.progress = 0;
                        }
                        p.mesh.position.lerpVectors(p.startPos, p.endPos, p.progress);
                        const wave = Math.sin(p.progress * Math.PI) * 0.12;
                        p.mesh.position.y += wave;
                    }
                });

                // Scene 4: DHCP Lease Zoom Target scale
                clientNodes.forEach((node, idx) => {
                    if (idx === 3 && currentSceneFloat > 2.5 && currentSceneFloat <= 4.0) {
                        const scale = 1.0 + 0.4 * Math.sin((currentSceneFloat - 2.5) * Math.PI / 1.5);
                        node.scale.set(scale, scale, scale);
                    } else if (idx !== 3) {
                        node.scale.set(1.0, 1.0, 1.0);
                    }
                });

                // Scene 5: Hotspot Voucher stack rises
                let voucherScale = 0.001;
                if (currentSceneFloat > 3.5 && currentSceneFloat <= 5.0) {
                    voucherScale = 0.001 + 0.999 * (currentSceneFloat - 3.5) / 1.5;
                } else if (currentSceneFloat > 5.0 && currentSceneFloat <= 6.0) {
                    voucherScale = Math.max(0.001, 1.0 - (currentSceneFloat - 5.0));
                }
                voucherGroup.scale.set(voucherScale, voucherScale, voucherScale);
                if (voucherScale > 0.01) {
                    voucherGroup.children.forEach((sheet, i) => {
                        sheet.position.y = (i * 0.03) + Math.sin(elapsedTime * 3.0 + i) * 0.01;
                    });
                }

                // Scene 6: Diagnostics blinking & alert ring
                let alertRingOpacity = 0;
                if (currentSceneFloat > 4.5 && currentSceneFloat <= 6.0) {
                    const blink = Math.sin(elapsedTime * 12) * 0.5 + 0.5;
                    const nodeColor = new THREE.Color(0xeab308);
                    const redColor = new THREE.Color(0xef4444);
                    clientNodes[2].material.color.lerpColors(nodeColor, redColor, blink);
                    
                    const pulse = (elapsedTime * 1.5) % 1.0;
                    alertRing.position.copy(clientNodes[2].position);
                    alertRing.scale.set(0.5 + pulse * 2.5, 0.5 + pulse * 2.5, 1);
                    alertRingOpacity = 0.8 * (1.0 - pulse);
                } else {
                    clientNodes[2].material.color.setHex(nodeMats[2].color.getHex());
                }
                alertRing.material.opacity = alertRingOpacity;

                // Scene 7: Local First Database Cylinder & Boundary Cage
                let localFirstAlpha = 0;
                if (currentSceneFloat > 5.5 && currentSceneFloat <= 7.0) {
                    localFirstAlpha = (currentSceneFloat - 5.5) / 1.5;
                } else if (currentSceneFloat > 7.0) {
                    localFirstAlpha = Math.max(0, 1.0 - (currentSceneFloat - 7.0) / 1.0);
                }

                const dbScale = Math.max(0.001, localFirstAlpha);
                dbGroup.scale.set(dbScale, dbScale, dbScale);
                dbGroup.rotation.y = elapsedTime * 0.4;
                
                localCage.material.opacity = 0.45 * localFirstAlpha;
                cloudNode.material.opacity = 0.5 * localFirstAlpha;
                cloudLine.material.opacity = 0.4 * localFirstAlpha;
                cloudNode.rotation.y += 0.005;

                // Scene 8 & 9: Operator UI Frame
                let uiAlpha = 0;
                if (currentSceneFloat > 6.8 && currentSceneFloat <= 8.5) {
                    uiAlpha = (currentSceneFloat - 6.8) / 1.7;
                } else if (currentSceneFloat > 8.5) {
                    uiAlpha = 1.0;
                }
                const uiScale = Math.max(0.001, uiAlpha);
                uiGroup.scale.set(uiScale, uiScale, uiScale);
                uiFrame.material.opacity = 0.35 * uiAlpha;

                // Scene 10: Future expansion
                let futureAlpha = 0;
                if (currentSceneFloat > 8.0) {
                    futureAlpha = Math.min(1.0, (currentSceneFloat - 8.0) / 1.0);
                }
                clientNodes[4].scale.set(futureAlpha, futureAlpha, futureAlpha);
                clientNodes[5].scale.set(futureAlpha, futureAlpha, futureAlpha);
                lines[4].material.opacity = 0.25 * futureAlpha;
                lines[5].material.opacity = 0.25 * futureAlpha;

                // Slow rotation of central router Group
                routerGroup.rotation.y = elapsedTime * 0.12;
                routerGroup.rotation.x = Math.sin(elapsedTime * 0.4) * 0.08;

                // Slowly blink/flicker LEDs
                leds.forEach(led => {
                    const noise = Math.sin(elapsedTime * (1.0 / led.blinkSpeed)) * 0.5 + 0.5;
                    if (noise > 0.65) {
                        led.mesh.material.color.setHex(0x0f172a); // OFF
                    } else {
                        led.mesh.material.color.setHex(led.baseColor); // ON
                    }
                });

                renderer.render(scene, camera);
            }
        }
        animate();

    } catch (err) {
        console.warn('WebGL Initialization failed inside Inside CafePulse storytelling context.', err);
    }
}

// Switch platform tab
function switchPlatform(platform) {
    // Toggle active class on buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    // Handle inline click binding
    if (window.event && window.event.currentTarget) {
        window.event.currentTarget.classList.add('active');
    }
    
    // Toggle active class on content sections
    document.querySelectorAll('.platform-content').forEach(content => {
        content.classList.remove('active');
    });
    const targetContent = document.getElementById(`platform-${platform}`);
    if (targetContent) {
        targetContent.classList.add('active');
    }
    
    // Switch aside terminal code box content
    const codeBox = document.getElementById('terminal-command');
    const labelBox = document.getElementById('terminal-label');
    if (codeBox && labelBox) {
        if (platform === 'windows') {
            codeBox.innerText = '$ProgressPreference = \'SilentlyContinue\'; Invoke-WebRequest -Uri "https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe" -OutFile "CafePulse_Free_Setup.exe"; .\\CafePulse_Free_Setup.exe';
            labelBox.innerText = 'Windows PowerShell';
        } else {
            codeBox.innerText = 'wget -O CafePulse_Free.AppImage "https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage" && chmod +x CafePulse_Free.AppImage && ./CafePulse_Free.AppImage';
            labelBox.innerText = 'Linux Terminal';
        }
    }
}
