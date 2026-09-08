document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirmPassword");

  // Toggle Password Utama
  const togglePassword = document.getElementById("togglePassword");
  const eyeIcon = document.getElementById("eyeIcon");
  if (togglePassword && passwordInput && eyeIcon) {
    togglePassword.addEventListener("click", () => {
      const isPassword = passwordInput.type === "password";
      passwordInput.type = isPassword ? "text" : "password";
      eyeIcon.classList.toggle("bi-eye", !isPassword);
      eyeIcon.classList.toggle("bi-eye-slash", isPassword);
    });
  }

  // Toggle Konfirmasi Password
  const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");
  const eyeConfirmIcon = document.getElementById("eyeConfirmIcon");
  if (toggleConfirmPassword && confirmPasswordInput && eyeConfirmIcon) {
    toggleConfirmPassword.addEventListener("click", () => {
      const isPassword = confirmPasswordInput.type === "password";
      confirmPasswordInput.type = isPassword ? "text" : "password";
      eyeConfirmIcon.classList.toggle("bi-eye", !isPassword);
      eyeConfirmIcon.classList.toggle("bi-eye-slash", isPassword);
    });
  }

  // Indikator Password Strength (3 Segmen)
  const bar1 = document.getElementById("bar1");
  const bar2 = document.getElementById("bar2");
  const bar3 = document.getElementById("bar3");
  const strengthLabel = document.getElementById("strengthLabel");

  passwordInput.addEventListener("input", (e) => {
    const val = e.target.value;
    const hasLength = val.length >= 8;
    const hasLetters = /[a-zA-Z]/.test(val);
    const hasNumbers = /[0-9]/.test(val);
    const hasSpecial = /[^a-zA-Z0-9]/.test(val);

    // Reset warna
    [bar1, bar2, bar3].forEach(b => {
      b.className = "rounded-full bg-slate-200 transition-colors duration-300";
    });
    strengthLabel.textContent = "";

    if (!val) return;

    let score = 0;
    if (val.length >= 6) score++;
    if (hasLength && hasLetters && hasNumbers) score++;
    if (hasLength && hasLetters && hasNumbers && hasSpecial) score++;

    if (score === 1) {
      bar1.classList.remove("bg-slate-200");
      bar1.classList.add("bg-rose-500");
      strengthLabel.textContent = "Lemah";
      strengthLabel.className = "font-semibold uppercase tracking-wider text-[10px] text-rose-500";
    } else if (score === 2) {
      bar1.classList.remove("bg-slate-200");
      bar2.classList.remove("bg-slate-200");
      bar1.classList.add("bg-amber-500");
      bar2.classList.add("bg-amber-500");
      strengthLabel.textContent = "Sedang";
      strengthLabel.className = "font-semibold uppercase tracking-wider text-[10px] text-amber-500";
    } else if (score >= 3) {
      [bar1, bar2, bar3].forEach(b => {
        b.classList.remove("bg-slate-200");
        b.classList.add("bg-emerald-500");
      });
      strengthLabel.textContent = "Kuat";
      strengthLabel.className = "font-semibold uppercase tracking-wider text-[10px] text-emerald-500";
    }
  });

  // Validasi Submit
  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (passwordInput.value !== confirmPasswordInput.value) {
        alert("Konfirmasi kata sandi tidak sesuai!");
        confirmPasswordInput.focus();
        return;
      }
      alert("Pendaftaran berhasil! Mengarahkan ke halaman login.");
      window.location.href = "login.html";
    });
  }
});