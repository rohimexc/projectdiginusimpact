**Catatan & Hal Penting Seputar Project DIGINUS**
**CV. Cendika Digital Nusantara**

**1. Urusan Tampilan & Logo Tab (Favicon)**
Atasi Logo Ilang di Mode Gelap (Dark Mode):
Ternyata tag standar HTML buat favicon nggak bisa langsung dipakein filter CSS inline karena browser ngerender ikonnya di luar elemen DOM biasa. Makanya, penting banget nyiapin file logo khusus (kayak LOGOONLY.jpeg atau versi warna terang) biar pas dibuka di browser ber-tema gelap, ikonnya nggak tenggelam alias tetep kelihatan jelas.

**2. Bikin User Experience (UX) & Interaksinya**
Akordeon (Buka-Tutup Otomatis):
Nerapin logika DOM yang otomatis ngehapus kelas aktif pas ada menu lain yang diklik. Hasilnya, kalau satu menu dibuka, menu yang lain bakal nutup sendiri secara otomatis, jadi tampilan web tetep rapi dan nggak numpuk-numpuk.

Ganti Gambar Otomatis Pakai Atribut Custom:
Memanfaatkan atribut data HTML (data-img dan data-caption) yang digabung sama event listener klik. Jadi pas menu keunggulan diklik, gambar ilustrasi di sebelah kanan bisa ikut keganti instan lengkap dengan efek pudar (fade) halus pakai settimeout.

Animasi Melayang yang Natural (Cubic-Bezier):
Daripada pake animasi lurus biasa yang kaku, kita pake fungsi kurva kecepatan cubic-bezier(0.165, 0.84, 0.44, 1) buat efek kartu hover-to-lift. Hasilnya gerakan naiknya kerasa jauh lebih luwes, enak dipandang, dan nggak kaku.

**3. Rapihin Layout & Navigasi Web**
Gulir Halus (Smooth Scroll):
Kombinasi antara CSS scroll-behavior: smooth sama fungsi script scrollIntoView bikin perpindahan dari satu bagian ke bagian lain di web jadi mulus banget tanpa ada lompatan kasar.

Efek Interaktif di Bagian Footer:
Nambahin efek geser naik tipis (translateY) plus perubahan warna jadi lebih terang pas kursor nyentuh teks alamat, email, atau nomor telpon di footer. Jadi kelihatan lebih interaktif dan profesional.