// Menunggu semua struktur HTML selesai dimuat oleh browser sebelum menjalankan kode JavaScript di dalamnya
document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================================================
  // 1. INISIALISASI ANIMASI AOS (Animate On Scroll)
  // ==========================================================================
  // Mengecek apakah library AOS sudah terpasang; jika ada, aktifkan animasi
  // 'once: true' artinya animasi hanya berjalan sekali saat pertama kali halaman terbuka
  if (typeof AOS !== "undefined") {
    AOS.init({ once: true });
  }

  // ==========================================================================
  // 2. MENGAMBIL ELEMEN DARI HTML
  // ==========================================================================
  // Menghubungkan ID yang ada di file login.html ke variabel JavaScript
  const togglePassword = document.getElementById("togglePassword"); // Tombol ikon mata
  const passwordInput = document.getElementById("password");         // Kolom input kata sandi
  const eyeIcon = document.getElementById("eyeIcon");                 // Ikon mata di dalam tombol
  const loginForm = document.getElementById("loginForm");             // Formulir login utama

  // ==========================================================================
  // 3. FITUR INTIP / SEMBUNYIKAN KATA SANDI (Show/Hide Password)
  // ==========================================================================
  // Memastikan ketiga elemen password tersebut benar-benar ada di layar sebelum diberi fungsi klik
  if (togglePassword && passwordInput && eyeIcon) {
    togglePassword.addEventListener("click", () => {
      // Periksa apakah jenis input saat ini masih berupa titik-titik rahasia ("password")
      const isPassword = passwordInput.type === "password";
      
      // Jika ya ("password"), ubah ke "text" agar terlihat; jika tidak, kembalikan ke "password"
      passwordInput.type = isPassword ? "text" : "password";
      
      // Ganti bentuk ikon Bootstrap Icons:
      // - bi-eye       : Gambar mata terbuka (teks terlihat)
      // - bi-eye-slash : Gambar mata dicoret (teks tersembunyi)
      eyeIcon.classList.toggle("bi-eye", !isPassword);
      eyeIcon.classList.toggle("bi-eye-slash", isPassword);
    });
  }

  // ==========================================================================
  // 4. AKSI SAAT TOMBOL MASUK DITEKAN (Submit Form)
  // ==========================================================================
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      // Mencegah halaman refresh otomatis secara default saat tombol diklik
      e.preventDefault();
      
      // Mengarahkan pengguna langsung ke halaman catatan materi BelajarTailwind
      window.location.href = "Topik1_10.html";
    });
  }
});