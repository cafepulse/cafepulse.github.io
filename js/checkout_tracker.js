/**
 * CafePulse — Dynamic Checkout & Midtrans Snap Integration
 * Intercepts payment links, displays a modern cyber-dark checkout modal,
 * collects customer identity, requests a Snap transaction from Cloudflare Worker,
 * and handles secure redirection.
 */
document.addEventListener("DOMContentLoaded", function() {
    // 1. Capture query parameters from current URL & persist to localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const refParam = urlParams.get('ref');
    const hwidParam = urlParams.get('hwid');

    if (refParam) {
        localStorage.setItem('cafepulse_ref', refParam.trim().toUpperCase());
    }
    if (hwidParam) {
        localStorage.setItem('cafepulse_hwid', hwidParam.trim());
    }

    // 2. Add checkout modal CSS styles dynamically to the head
    const style = document.createElement('style');
    style.innerHTML = `
        .cp-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(8, 10, 15, 0.85);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .cp-modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .cp-modal-card {
            background: rgba(17, 24, 39, 0.95);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 16px;
            padding: 2.5rem;
            width: 90%;
            max-width: 460px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 50px rgba(56, 189, 248, 0.1);
            transform: scale(0.9) translateY(20px);
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            font-family: 'Outfit', 'Inter', sans-serif;
            color: #f3f4f6;
            position: relative;
        }
        .cp-modal-overlay.active .cp-modal-card {
            transform: scale(1) translateY(0);
        }
        .cp-modal-close {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            background: transparent;
            border: none;
            color: #9ca3af;
            font-size: 1.5rem;
            cursor: pointer;
            transition: color 0.2s ease;
            line-height: 1;
        }
        .cp-modal-close:hover {
            color: #38bdf8;
        }
        .cp-modal-header {
            margin-bottom: 1.75rem;
        }
        .cp-modal-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .cp-modal-desc {
            font-size: 0.9rem;
            color: #9ca3af;
            line-height: 1.5;
        }
        .cp-modal-form-group {
            margin-bottom: 1.25rem;
            text-align: left;
        }
        .cp-modal-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: #9ca3af;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .cp-modal-input {
            width: 100%;
            background: rgba(31, 41, 55, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            color: #ffffff;
            font-size: 0.95rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            box-sizing: border-box;
        }
        .cp-modal-input:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }
        .cp-modal-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 1rem;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }
        .cp-modal-btn:hover {
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .cp-modal-btn:active {
            transform: scale(0.98);
        }
        .cp-modal-btn:disabled {
            background: #374151;
            color: #9ca3af;
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }
        .cp-modal-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #f87171;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            margin-bottom: 1.25rem;
            display: none;
            line-height: 1.4;
            text-align: left;
        }
        .cp-spinner {
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top: 3px solid #ffffff;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            animation: cp-spin 0.8s linear infinite;
            display: none;
        }
        @keyframes cp-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // 3. Create Modal HTML elements
    const overlay = document.createElement('div');
    overlay.className = 'cp-modal-overlay';
    overlay.id = 'cpCheckoutModal';

    overlay.innerHTML = `
        <div class="cp-modal-card">
            <button class="cp-modal-close" id="cpModalCloseBtn">&times;</button>
            <div class="cp-modal-header">
                <div class="cp-modal-title" id="cpModalTitle">Checkout CafePulse</div>
                <div class="cp-modal-desc" id="cpModalDesc">Lengkapi formulir di bawah ini untuk melanjutkan pembayaran secara aman melalui Midtrans.</div>
            </div>
            <div class="cp-modal-error" id="cpModalError"></div>
            <form id="cpCheckoutForm" onsubmit="return false;">
                <div class="cp-modal-form-group">
                    <label class="cp-modal-label" for="cpCustomerName">Nama Lengkap</label>
                    <input type="text" id="cpCustomerName" class="cp-modal-input" placeholder="Masukkan nama lengkap Anda" required />
                </div>
                <div class="cp-modal-form-group">
                    <label class="cp-modal-label" for="cpCustomerEmail">Email</label>
                    <input type="email" id="cpCustomerEmail" class="cp-modal-input" placeholder="nama@email.com" required />
                </div>
                <button type="submit" class="cp-modal-btn" id="cpSubmitBtn">
                    <div class="cp-spinner" id="cpBtnSpinner"></div>
                    <span id="cpBtnText">Lanjutkan ke Pembayaran</span>
                </button>
            </form>
        </div>
    `;
    document.body.appendChild(overlay);

    // Modal Control Variables
    const closeBtn = document.getElementById('cpModalCloseBtn');
    const submitBtn = document.getElementById('cpSubmitBtn');
    const form = document.getElementById('cpCheckoutForm');
    const nameInput = document.getElementById('cpCustomerName');
    const emailInput = document.getElementById('cpCustomerEmail');
    const errorDiv = document.getElementById('cpModalError');
    const spinner = document.getElementById('cpBtnSpinner');
    const btnText = document.getElementById('cpBtnText');
    const modalTitle = document.getElementById('cpModalTitle');
    const modalDesc = document.getElementById('cpModalDesc');

    let activeProduct = 'PRO'; // Default
    let isFounder = false;

    // Open Modal Function
    function openCheckout(productType) {
        activeProduct = productType;
        isFounder = (productType === 'FOUNDER');

        if (isFounder) {
            modalTitle.innerText = "Join Founder Program";
            modalDesc.innerText = "Lengkapi nama dan email Anda untuk bergabung sebagai Founder CafePulse (Terbatas 100 pendukung).";
        } else {
            modalTitle.innerText = "Beli Lisensi Professional";
            modalDesc.innerText = "Lengkapi nama dan email Anda untuk melakukan pembayaran lisensi CafePulse Pro secara instan.";
        }

        errorDiv.style.display = 'none';
        nameInput.value = '';
        emailInput.value = '';
        overlay.classList.add('active');
        nameInput.focus();
    }

    // Close Modal Function
    function closeModal() {
        overlay.classList.remove('active');
    }

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) closeModal();
    });

    // 4. Intercept clicks on payment buttons
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link) {
            const href = link.getAttribute('href') || '';
            const isCheckoutTrigger = link.classList.contains('cp-checkout-trigger') || href.startsWith('#checkout-');
            if (isCheckoutTrigger) {
                e.preventDefault();

                // Determine package tier
                let packageType = link.getAttribute('data-package') || 'PRO';
                if (!link.getAttribute('data-package')) {
                    if (href.includes('founder') || window.location.pathname.includes('founder.html')) {
                        packageType = 'FOUNDER';
                    }
                }
                openCheckout(packageType);
            }
        }
    });

    // 5. Handle form submission (API Call)
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();

        if (!name || !email) {
            showError("Harap lengkapi semua kolom formulir.");
            return;
        }

        // Disable elements & show spinner
        submitBtn.disabled = true;
        nameInput.disabled = true;
        emailInput.disabled = true;
        spinner.style.display = 'block';
        btnText.innerText = "Memproses...";
        errorDiv.style.display = 'none';

        // Gather tracking variables from localStorage
        const referral = localStorage.getItem('cafepulse_ref') || 'NONE';
        const hwid = localStorage.getItem('cafepulse_hwid') || '';

        // API Endpoint routing logic: Sandbox/Localhost vs Production
        let apiUrl = "https://cafepulse-licensing.cafepulse-network.workers.dev/api/v1/create-payment";
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.protocol === "file:") {
            apiUrl = "http://127.0.0.1:8787/api/v1/create-payment";
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product: activeProduct,
                    customer_name: name,
                    customer_email: email,
                    hwid: hwid,
                    referral: referral,
                    founder: isFounder
                })
            });

            const data = await response.json();

            if (response.ok && data.success && data.checkout_url) {
                // Redirect to Midtrans snap checkout
                window.location.href = data.checkout_url;
            } else {
                showError(data.error || "Gagal membuat transaksi pembayaran. Silakan coba lagi.");
            }
        } catch (err) {
            console.error("Payment API Error:", err);
            showError("Terjadi kesalahan jaringan atau server tidak merespons. Silakan periksa koneksi internet Anda.");
        } finally {
            // Re-enable elements
            submitBtn.disabled = false;
            nameInput.disabled = false;
            emailInput.disabled = false;
            spinner.style.display = 'none';
            btnText.innerText = "Lanjutkan ke Pembayaran";
        }
    });

    function showError(message) {
        errorDiv.innerText = message;
        errorDiv.style.display = 'block';
    }
});
