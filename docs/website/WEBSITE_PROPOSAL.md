# CafePulse GitHub Pages Update Proposal (Sprint 3)

Proposal teknis ini merinci perubahan kode HTML, CSS, dan JavaScript pada repositori `cafepulse/cafepulse.github.io` untuk mewujudkan *Download Experience* baru dan integrasi dokumentasi panduan pengguna lintas platform (Windows & Linux).

---

## 1. Modifikasi Navigasi Utama (Header)

### 1.1 Berkas yang Diubah: Semua berkas `.html` di root website
### 1.2 Kode Navigasi Baru (Ringkas & Efisien):
```html
<nav>
    <ul class="nav-links">
        <li><a href="./index.html">Home</a></li>
        <li><a href="./product.html">Features</a></li>
        <li><a href="./pricing.html">Pricing</a></li>
        <li><a href="./founder.html">Founder Program</a></li>
        <li><a href="./documentation.html">Docs</a></li>
        <li><a href="./download.html" class="btn btn-nav-dl">Download</a></li>
    </ul>
</nav>
```
*Catatan: About and Contact dipindahkan sepenuhnya ke footer link untuk mengurangi kepadatan menu.*

---

## 2. Pembaruan Halaman Unduhan (`download.html`)

### 2.1 Struktur Tab Sistem (Windows vs Linux)
Tambahkan tombol toggle tab di dalam kontainer utama halaman unduhan:
```html
<div class="tab-toggle-container">
    <button class="tab-btn active" onclick="switchPlatform('windows')">
        <img src="./assets/win-icon.svg" alt="Windows"> Windows Version
    </button>
    <button class="tab-btn" onclick="switchPlatform('linux')">
        <img src="./assets/linux-icon.svg" alt="Linux"> Linux Version
    </button>
</div>
```

### 2.2 Konten Unduhan Dinamis
#### A. Konten Tab Windows (`id="platform-windows"`)
Menampilkan kartu-kartu unduhan Windows Setup (.exe) and Portable (.zip) untuk edisi Free and Professional, serta perintah PowerShell:
```html
<div id="platform-windows" class="platform-content active">
    <!-- Kartu Free Setup -->
    <div class="dl-card">
        <h3>CafePulse Free Edition Setup</h3>
        <p>Windows 10 / 11 (64-bit) &bull; Installer &bull; ~56 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe" class="btn btn-primary">Download Setup (EXE)</a>
    </div>
    <!-- Kartu Free Portable -->
    <div class="dl-card">
        <h3>CafePulse Free Portable ZIP</h3>
        <p>Windows 10 / 11 (64-bit) &bull; Portable &bull; ~96 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Portable.zip" class="btn btn-secondary">Download Portable (ZIP)</a>
    </div>
    <!-- Kartu Pro Setup -->
    <div class="dl-card">
        <h3>CafePulse Professional Setup</h3>
        <p>Windows 10 / 11 (64-bit) &bull; Installer &bull; ~56 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional_Setup.exe" class="btn btn-primary-pro">Download Professional (EXE)</a>
    </div>
    <!-- Kartu Pro Portable -->
    <div class="dl-card">
        <h3>CafePulse Professional Portable ZIP</h3>
        <p>Windows 10 / 11 (64-bit) &bull; Portable &bull; ~96 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional_Portable.zip" class="btn btn-secondary-pro">Download Portable (ZIP)</a>
    </div>
</div>
```

#### B. Konten Tab Linux (`id="platform-linux"`)
Menampilkan kartu-kartu unduhan Linux AppImage untuk edisi Free and Professional, serta perintah Terminal Linux:
```html
<div id="platform-linux" class="platform-content">
    <!-- Kartu Free AppImage -->
    <div class="dl-card">
        <h3>CafePulse Free AppImage</h3>
        <p>Linux x86_64 &bull; Standalone Executable &bull; ~112 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage" class="btn btn-primary">Download AppImage</a>
    </div>
    <!-- Kartu Pro AppImage -->
    <div class="dl-card">
        <h3>CafePulse Professional AppImage</h3>
        <p>Linux x86_64 &bull; Standalone Executable &bull; ~112 MB</p>
        <a href="https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Professional.AppImage" class="btn btn-primary-pro">Download AppImage (Pro)</a>
    </div>
</div>
```

---

## 3. Tambahan CSS untuk Kerapian (`css/main.css`)

Tambahkan style berikut untuk mendukung layout baru, visual tab, and responsivitas mobile:
```css
/* Tab Navigation styling */
.tab-toggle-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.tab-btn {
    padding: 0.75rem 1.5rem;
    border: 1px solid var(--border-color);
    background: var(--bg-primary);
    color: var(--text-secondary);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tab-btn.active, .tab-btn:hover {
    background: var(--accent-blue);
    color: white;
    border-color: var(--accent-blue);
}

/* Platform Content visibility toggling */
.platform-content {
    display: none;
}

.platform-content.active {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

/* Professional Colors */
.btn-primary-pro {
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    color: white;
    border: none;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.2);
}
.btn-primary-pro:hover {
    background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
}
```

---

## 4. Tambahan Logika JavaScript (`js/main.js`)

Tambahkan fungsi pergantian tab dan salin command otomatis ke clipboard:
```javascript
// Switch platform tab
function switchPlatform(platform) {
    // Toggle active class on buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    // Toggle active class on content sections
    document.querySelectorAll('.platform-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`platform-${platform}`).classList.add('active');
    
    // Switch aside terminal code box content
    const codeBox = document.getElementById('terminal-command');
    if (platform === 'windows') {
        codeBox.innerText = 'Invoke-WebRequest -Uri "https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free_Setup.exe" -OutFile "CafePulse_Free_Setup.exe"; .\\CafePulse_Free_Setup.exe';
        document.getElementById('terminal-label').innerText = 'Windows PowerShell';
    } else {
        codeBox.innerText = 'wget https://github.com/cafepulse/cafepulse.github.io/releases/latest/download/CafePulse_Free.AppImage && chmod +x CafePulse_Free.AppImage && ./CafePulse_Free.AppImage';
        document.getElementById('terminal-label').innerText = 'Linux Terminal';
    }
}
```
