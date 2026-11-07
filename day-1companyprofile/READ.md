### (Materi Pengenalan DIGINUS)

### 1. Pengembangan Komponen Accordion Dinamis Berbasis Showcase
Integrasi Konten dengan Gambar: Saya mempelajari cara mengaitkan daftar teks accordion dengan preview gambar di sisi kolom lainnya secara interaktif. Dengan memanfaatkan atribut `data-img` pada HTML serta manipulasi DOM melalui JavaScript, tampilan gambar di sisi kanan dapat berganti secara dinamis dan halus (*fade transition*) sesuai poin keunggulan yang dipilih oleh pengguna.
Transisi CSS yang Halus: Memahami teknik pengaturan `max-height` dan `overflow: hidden` untuk menghasilkan efek ekspansi accordion yang natural tanpa pergeseran tata letak yang kaku.

### 2. Penerapan Micro-Interactions Minimalis pada Elemen UI
Transisi Visual yang Proporsional: Sebelumnya beberapa elemen animasi ikon bergerak cukup agresif (rotasi miring dan loncatan jauh). Melalui penyesuaian ini, saya belajar menerapkan prinsip clean & corporate UI, di mana animasi interaksi dibuat lebih tenang menggunakan subtle elevation (`translateY(-2px)`) dan perubahan warna lembut saat kursor diarahkan (hover).
Konsistensi Kartu Portofolio: Mengubah pergeseran ikon panah dan tautan menjadi penyesuaian skala mikro (`scale`) agar kartu informasi tetap seimbang, stabil, serta nyaman dibaca.

### 3. Optimasi Tampilan Responsif (Mobile Layout Optimization)
Penanganan Teks Panjang (Word-Break): Pada pengujian di layar ponsel, alamat email yang panjang berisiko menabrak batas kotak atau merusak struktur kartu. Saya mempelajari solusi penggunaan properti `word-break: break-word` dan `overflow-wrap: anywhere` agar teks dapat turun ke baris berikutnya secara rapi tanpa memotong kata secara janggal.
Penyelarasan Komponen Fleksibel (Flexbox Alignment): Mengatur `align-items: flex-start` pada media query perangkat mobile untuk memastikan ikon kontak tetap sejajar rapi di sudut kiri atas saat teks keterangan di sampingnya memanjang menjadi beberapa baris.

### 4. Konfigurasi Favicon dan Identitas Halaman Web
Pengaturan Metadata Head: Memahami penerapan tag `<link rel="icon">` dan `<title>` pada dokumen HTML untuk membangun identitas tab peramban yang konsisten dengan brand identity resmi DIGINUS.
Manajemen Cache Peramban: Memahami karakteristik peramban (browser) yang kerap menyimpan aset *favicon* lama pada memori cache, sehingga diperlukan langkah hard refresh untuk memuat aset visual yang baru diperbarui.

### 5. Pengelolaan Versi Kode Melalui Git & Terminal
Pemahaman Jalur Direktori Terminal: Memahami struktur path direktori aktif pada Git Bash, di mana perintah `cd` harus merujuk pada folder yang tepat dan perintah `cd ..` digunakan untuk kembali ke direktori induk (root project).
Manajemen Staging Perubahan Berkas: Mempelajari fungsi `git add -A` dalam merekam seluruh perubahan riwayat berkas, termasuk mendeteksi berkas yang berganti nama atau dipindahkan, sehingga status branch kerja (`dev-anggitamaharani`) tetap sinkron dan bersih saat dikirim ke repositori GitHub.