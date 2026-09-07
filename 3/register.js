document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");

  // Toggle Password
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const eyeIcon = document.getElementById("eyeIcon");

  togglePassword.addEventListener("click", () => {
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";

    eyeIcon.classList.toggle("fa-eye", !isPassword);
    eyeIcon.classList.toggle("fa-eye-slash", isPassword);
  });

  // Toggle Confirm Password
  const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");
  const confirmPasswordInput = document.getElementById("confirmPassword");
  const eyeConfirmIcon = document.getElementById("eyeConfirmIcon");

  toggleConfirmPassword.addEventListener("click", () => {
    const isPassword = confirmPasswordInput.type === "password";
    confirmPasswordInput.type = isPassword ? "text" : "password";

    eyeConfirmIcon.classList.toggle("fa-eye", !isPassword);
    eyeConfirmIcon.classList.toggle("fa-eye-slash", isPassword);
  });

  // Form Submit & Validation
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const fullName = document.getElementById("fullName").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    const termsAccepted = document.getElementById("termsCheck").checked;

    // Validasi kesesuaian password
    if (password !== confirmPassword) {
      alert("Password dan konfirmasi password tidak cocok!");
      confirmPasswordInput.focus();
      return;
    }

    if (!termsAccepted) {
      alert("Harap setujui Syarat dan Ketentuan terlebih dahulu.");
      return;
    }

    console.log("Pendaftaran Berhasil:", { fullName, email, password });
    alert(`Pendaftaran berhasil untuk: ${fullName}! Silakan login.`);

    // Redirect ke login.html setelah sukses
    window.location.href = "login.html";
  });
});