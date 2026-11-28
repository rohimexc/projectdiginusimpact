import sqlite3
import os

db_path = 'administrasi_public/db.sqlite3' if os.path.exists('administrasi_public/db.sqlite3') else 'db.sqlite3'
con = sqlite3.connect(db_path)
cur = con.cursor()

data_tentang = [
    (
        'profil',
        'Profil Program Studi Administrasi Publik',
        '''<p>Program Studi Administrasi Publik merupakan salah satu program studi unggulan di bawah naungan Fakultas Ilmu Sosial dan Ilmu Politik (FISIP) Universitas Tadulako. Program studi ini berkomitmen untuk menyelenggarakan pendidikan tinggi berkualitas guna menghasilkan lulusan yang kompeten, berintegritas, serta berdaya saing global di bidang tata kelola sektor publik dan kebijakan publik.</p>
        <p>Kurikulum yang diterapkan dirancang secara adaptif dan relevan dengan perkembangan dinamika administrasi modern, transformasi digital sektor publik, serta prinsip tata kelola pemerintahan yang baik (good governance). Mahasiswa dibekali dengan pemahaman teori yang mendalam serta keterampilan praktis melalui kegiatan perkuliahan interaktif, penelitian berbasis isu strategis daerah dan nasional, serta program pengabdian kepada masyarakat yang berwawasan lingkungan dan berkelanjutan.</p>
        <p>Dengan dukungan tenaga pengajar profesional dan sarana akademik yang lengkap, Program Studi Administrasi Publik siap mencetak inovator, birokrat, perencana kebijakan, analis kebijakan publik, serta pemimpin masa depan yang berdedikasi bagi kemajuan bangsa dan kesejahteraan masyarakat madani.</p>'''
    ),
    (
        'sejarah',
        'Sejarah & Dasar Hukum',
        '''<p>Program Studi Administrasi Publik berawal dari pembentukan Jurusan Ilmu Administrasi di lingkungan Fakultas Ilmu Sosial dan Ilmu Politik Universitas Tadulako seiring dengan pengesahan pendirian universitas negeri di Sulawesi Tengah.</p>
        <p>Dalam perkembangannya, Program Studi Administrasi Publik secara berkala memperbarui izin operasional dan kurikulum berbasis kerangka kualifikasi nasional (KKNI) serta standar nasional pendidikan tinggi melalui Surat Keputusan Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi, menegaskan kedudukannya sebagai pilar pembina keilmuan administrasi negara/publik di kawasan timur Indonesia.</p>'''
    ),
    (
        'visi_misi',
        'Visi, Misi, dan Tujuan',
        '''<h3>Visi</h3>
        <p>Menjadi program studi yang unggul secara global dalam bidang ilmu administrasi publik sebagai mitra strategis untuk kehidupan yang lebih baik melalui pendidikan, penelitian, dan pelayanan tata kelola publik yang berwawasan lingkungan dan berkelanjutan.</p>
        <h3>Misi</h3>
        <ul>
          <li>Menyelenggarakan proses pembelajaran berkualitas, inovatif, dan relevan dengan kemajuan teknologi sektor publik.</li>
          <li>Mengembangkan riset-riset strategis dalam penyelesaian masalah tata kelola kebijakan lokal dan nasional.</li>
          <li>Melaksanakan pengabdian kepada masyarakat berbasis pemberdayaan sosial dan penguatan birokrasi daerah.</li>
        </ul>'''
    ),
    (
        'profil_lulusan',
        'Profil Lulusan Program Studi Administrasi Publik',
        '''<p>Lulusan Program Studi Administrasi Publik FISIP Universitas Tadulako dipersiapkan untuk berkarier di berbagai instansi pemerintahan pusat maupun daerah, lembaga legislatif, organisasi non-pemerintah (NGO/LSM), BUMN/BUMD, hingga lembaga riset publik.</p>
        <p><strong>Prospek Karier Lulusan:</strong></p>
        <ul>
          <li><strong>Analis Kebijakan Publik:</strong> Merumuskan, menganalisis, serta mengevaluasi rancangan kebijakan publik yang efektif dan berkeadilan.</li>
          <li><strong>Administrator Publik / Aparatur Sipil Negara:</strong> Mengelola manajemen birokrasi, tata usaha, serta pelayanan langsung kepada masyarakat.</li>
          <li><strong>Manajer Lembaga Nirlaba:</strong> Mengelola perencanaan strategis dan operasional lembaga swadaya masyarakat serta institusi sosial.</li>
          <li><strong>Peneliti & Konsultan Tata Kelola Publik:</strong> Menyediakan data analitis dan rekomendasi strategis bagi pengambil keputusan.</li>
        </ul>'''
    ),
    (
        'akreditasi',
        'Sertifikat Akreditasi Program Studi',
        '''<p>Program Studi Administrasi Publik FISIP Universitas Tadulako telah meraih predikat akreditasi resmi dari Badan Akreditasi Nasional Perguruan Tinggi (BAN-PT) / Lembaga Akreditasi Mandiri.</p>
        <p>Pengakuan akreditasi ini membuktikan komitmen mutu kurikulum, sarana pendidikan, kualitas dosen, serta capaian pembelajaran mahasiswa kami sesuai dengan standar mutu pendidikan tinggi nasional.</p>'''
    )
]

sql = """
INSERT OR REPLACE INTO core_halamantentang (kategori, judul, isi, updated_at)
VALUES (?, ?, ?, datetime('now'))
"""

for item in data_tentang:
    cur.execute(sql, item)

con.commit()
con.close()
print("SUKSES! Semua data menu Tentang berhasil diisi.")