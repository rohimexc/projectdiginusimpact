// Menunggu semua elemen HTML selesai dimuat sebelum menjalankan perintah
document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================================================
  // 1. AKTIFKAN ANIMASI AOS
  // ==========================================================================
  if (typeof AOS !== "undefined") {
    AOS.init({ once: true });
  }

  // ==========================================================================
  // 2. MENGAMBIL ELEMEN INPUT & TOMBOL MATA DARI HTML
  // ==========================================================================
  const passwordInput = document.getElementById("password");
  const togglePassword = document.getElementById("togglePassword");
  const eyeIcon = document.getElementById("eyeIcon");

  const confirmPasswordInput = document.getElementById("confirmPassword");
  const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");
  const eyeIconConfirm = document.getElementById("eyeIconConfirm");

  // Elemen Bar Indikator Kekuatan Sandi
  const bar1 = document.getElementById("strengthBar1");
  const bar2 = document.getElementById("strengthBar2");
  const bar3 = document.getElementById("strengthBar3");
  const strengthText = document.getElementById("strengthText");

  const registerForm = document.getElementById("registerForm");

  // ==========================================================================
  // 3. FUNGSI INTIP / SEMBUNYIKAN KATA SANDI (GANDA)
  // ==========================================================================
  const setupToggle = (button, input, icon) => {
    if (!button || !input || !icon) return;
    button.addEventListener("click", () => {
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      icon.classList.toggle("bi-eye", !isPassword);
      icon.classList.toggle("bi-eye-slash", isPassword);
    });
  };

  // Terapkan fungsi toggle ke kolom password dan konfirmasi password
  setupToggle(togglePassword, passwordInput, eyeIcon);
  setupToggle(toggleConfirmPassword, confirmPasswordInput, eyeIconConfirm);

  // ==========================================================================
  // 4. LOGIKA PENGUKUR KEKUATAN SANDI (Merah=Lemah, Kuning=Sedang, Hijau=Kuat)
  // ==========================================================================
  if (passwordInput) {
    passwordInput.addEventListener("input", (e) => {
      const val = e.target.value;
      const hasLength = val.length >= 8;
      const hasLetter = /[a-zA-Z]/.test(val);
      const hasNumber = /[0-9]/.test(val);
      const hasSpecial = /[^a-zA-Z0-9]/.test(val);

      // Kembalikan 3 bar ke warna abu-abu default
      bar1.className = "h-1.5 rounded-full bg-slate-200 transition-colors duration-300";
      bar2.className = "h-1.5 rounded-full bg-slate-200 transition-colors duration-300";
      bar3.className = "h-1.5 rounded-full bg-slate-200 transition-colors duration-300";

      // Jika kolom kosong, hilangkan teks status
      if (val.length === 0) {
        strengthText.textContent = "";
        return;
      }

      // Hitung skor kekuatan sandi
      let score = 0;
      if (val.length >= 6) score++;
      if (hasLength && hasLetter && hasNumber) score++;
      if (hasLength && hasLetter && hasNumber && hasSpecial) score++;

      // Ubah warna batang berdasarkan skor
      if (score <= 1) {
        // 1 Batang Merah = Lemah
        bar1.classList.replace("bg-slate-200", "bg-rose-500");
        strengthText.textContent = "Lemah";
        strengthText.className = "font-semibold text-rose-500 text-[11px]";
      } else if (score === 2) {
        // 2 Batang Kuning = Sedang
        bar1.classList.replace("bg-slate-200", "bg-amber-400");
        bar2.classList.replace("bg-slate-200", "bg-amber-400");
        strengthText.textContent = "Sedang";
        strengthText.className = "font-semibold text-amber-500 text-[11px]";
      } else {
        // 3 Batang Hijau = Kuat
        bar1.classList.replace("bg-slate-200", "bg-emerald-500");
        bar2.classList.replace("bg-slate-200", "bg-emerald-500");
        bar3.classList.replace("bg-slate-200", "bg-emerald-500");
        strengthText.textContent = "Kuat";
        strengthText.className = "font-semibold text-emerald-600 text-[11px]";
      }
    });
  }

  // ==========================================================================
  // 5. VALIDASI KECOCOKAN KATA SANDI & PINDAH HALAMAN
  // ==========================================================================
  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();

      // Cek apakah kolom sandi dan konfirmasi sama persis
      if (passwordInput.value !== confirmPasswordInput.value) {
        alert("Konfirmasi kata sandi tidak cocok dengan kata sandi!");
        confirmPasswordInput.focus();
        return;
      }

      // Berhasil registrasi -> arahkan ke halaman modul pembelajaran
      window.location.href = "login.html";
    });
  }
});