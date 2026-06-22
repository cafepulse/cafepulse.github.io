import sys
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 20)
        self.set_text_color(16, 185, 129) # CafePulse Green
        self.cell(0, 15, "CafePulse: Strategic Roadmap & Future Direction", border=0, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 41, 59)
        self.line(10, 25, 200, 25)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} - Official Internal Document", align="C")

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(56, 189, 248) # Blue
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(5)

    def add_bullet(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.set_x(15)
        self.multi_cell(0, 6, "- " + text)

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # Executive Summary
    pdf.chapter_title("Executive Summary")
    pdf.chapter_body(
        "Setelah berhasil mencapai 'Licensing Freeze' dengan arsitektur RSA-First yang kokoh, stabil, "
        "dan aman, pengembangan inti (core) CafePulse kini memasuki fase transisi krusial dari "
        "'Development' menuju 'Deployment & Community Building'. Dokumen ini merangkum arah "
        "strategis CafePulse di kuartal mendatang berdasarkan fondasi yang telah dibangun."
    )
    
    # Phase 1
    pdf.chapter_title("Fase 1: Konsolidasi & Infrastruktur (Terdekat)")
    pdf.chapter_body("Mempersiapkan infrastruktur kolaborasi dan penampungan rilis resmi:")
    pdf.add_bullet("GitHub Private Repository Setup: Mengamankan seluruh source code, menyusun CI/CD pipeline, Wiki internal, dan Issue Tracker.")
    pdf.add_bullet("Discord Community Setup: Peluncuran server Discord resmi dengan integrasi peran otomatis (Founder, Beta Tester, Commercial).")
    pdf.ln(5)
    
    # Phase 2
    pdf.chapter_title("Fase 2: Pengujian Dunia Nyata (Beta Phase)")
    pdf.chapter_body("Melibatkan kelompok pertama dalam pengujian operasional:")
    pdf.add_bullet("Beta Tester Program: Distribusi rilis perdana (Release Candidate) kepada kelompok uji terbatas (RC Cohorts).")
    pdf.add_bullet("Pengujian Skalabilitas: Menguji kompabilitas pada berbagai varian RouterOS v6 dan v7 di lapangan nyata.")
    pdf.add_bullet("Validasi HWID & Offline Mode: Memastikan sistem 'Automatic Downgrade' ke Free Edition berjalan mulus saat masa uji coba habis tanpa menyebabkan lockout.")
    pdf.ln(5)
    
    # Phase 3
    pdf.chapter_title("Fase 3: Adopsi Awal & Monetisasi (Founder Phase)")
    pdf.chapter_body("Mengamankan pangsa pasar awal dan penyokong proyek:")
    pdf.add_bullet("Founder Program Launch: Penjualan lisensi seumur hidup eksklusif untuk penyokong dana awal dengan jaminan update tak terbatas.")
    pdf.add_bullet("Commercial Rollout: Rilis versi stabil 1.0.0.0 ke pasar umum, memposisikan CafePulse sebagai software manajemen MikroTik Desktop-First tanpa SaaS.")
    pdf.add_bullet("Depresiasi Legacy: Secara bertahap menonaktifkan aktivasi berbasis Serial Key lama menuju ekosistem RSA penuh.")
    pdf.ln(5)

    # Phase 4
    pdf.chapter_title("Fase 4: Ekspansi Fitur Lanjutan (Post-Release)")
    pdf.chapter_body("Meskipun sistem lisensi telah dibekukan, pengembangan fitur inti jaringan akan diteruskan:")
    pdf.add_bullet("Advanced Network DNA Radar: Deteksi anomali cerdas untuk memonitor lalu lintas (bandwidth hogs, mitigasi DDoS).")
    pdf.add_bullet("Multi-Router Fleet Management: Pemantauan multi-RB secara simultan dari satu antarmuka dasbor (Fleet Dashboard).")
    pdf.add_bullet("Plugin Ecosystem: Penyediaan API lokal bagi komunitas untuk mengembangkan plugin integrasi buatan sendiri.")

    import os
    output_path = os.path.join(os.path.dirname(__file__), "..", "artifacts", "compiled_pdfs", "CafePulse_Strategic_Roadmap.pdf")
    pdf.output(output_path)
    print(f"PDF Report Generated Successfully as {output_path}")

if __name__ == "__main__":
    create_pdf()
