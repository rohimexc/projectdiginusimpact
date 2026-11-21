import sqlite3
import os
from datetime import datetime

# Pilih lokasi database yang aktif
db_path = 'administrasi_public/db.sqlite3' if os.path.exists('administrasi_public/db.sqlite3') else 'db.sqlite3'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Data berita akademik resmi prodi
berita_list = [
    {
        'judul': 'Kuliah Tamu: Transformasi Digital dan Reformasi Birokrasi Menuju Smart Governance',
        'ringkasan': 'Program Studi Administrasi Publik FISIP Universitas Tadulako menghadirkan pakar kebijakan nasional guna membedah implementasi SPBE.',
        'konten': '<p>Palu – Program Studi Administrasi Publik FISIP Universitas Tadulako sukses menggelar kuliah tamu bertajuk "Transformasi Digital dan Reformasi Birokrasi Sektor Publik". Kegiatan ini membekali mahasiswa dengan wawasan praktis mengenai tata kelola pemerintahan modern berbasis teknologi informasi di era transformasi digital.</p>',
    },
    {
        'judul': 'Pengabdian Masyarakat: Penguatan Kapasitas Administrasi dan Akuntabilitas Desa',
        'ringkasan': 'Dosen dan mahasiswa Administrasi Publik menggelar pelatihan tata kelola arsip elektronik dan perumusan regulasi desa di Sulawesi Tengah.',
        'konten': '<p>Sebagai implementasi Tri Dharma Perguruan Tinggi, sivitas akademika Program Studi Administrasi Publik menyelenggarakan pelatihan tata kelola pelayanan publik dan penyusunan regulasi desa secara partisipatif dan transparan.</p>',
    },
    {
        'judul': 'Workshop Penulisan Skripsi dan Publikasi Artikel Ilmiah Mahasiswa',
        'ringkasan': 'Pembekalan riset kebijakan publik kontemporer guna meningkatkan kualitas kelulusan serta publikasi karya ilmiah mahasiswa.',
        'konten': '<p>Guna mengakselerasi masa studi mahasiswa tingkat akhir, Program Studi menyelenggarakan lokakarya metodologi penelitian kebijakan publik serta penulisan manuskrip jurnal ilmiah terakreditasi nasional.</p>',
    }
]

waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Cek berita yang sudah ada di database
cur.execute("SELECT id FROM core_berita ORDER BY id ASC")
existing_rows = cur.fetchall()
existing_ids = [row[0] for row in existing_rows]

for idx, item in enumerate(berita_list):
    if idx < len(existing_ids):
        # Update berita lama
        berita_id = existing_ids[idx]
        cur.execute("""
            UPDATE core_berita 
            SET judul = ?, ringkasan = ?, konten = ?, updated_at = ?, posted_at = ?
            WHERE id = ?
        """, (item['judul'], item['ringkasan'], item['konten'], waktu_sekarang, waktu_sekarang, berita_id))
    else:
        # Tambah berita baru lengkap dengan created_at
        cur.execute("""
            INSERT INTO core_berita (judul, ringkasan, konten, created_at, updated_at, posted_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (item['judul'], item['ringkasan'], item['konten'], waktu_sekarang, waktu_sekarang, waktu_sekarang))

con.commit()
con.close()
print("SUKSES! Data Berita berhasil diperbarui menjadi berita prodi resmi.")