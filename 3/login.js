document.addEventListener("DOMContentLoaded", () => {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const eyeIcon = document.getElementById("eyeIcon");
  const loginForm = document.getElementById("loginForm");

  // Toggle Password
  if (togglePassword && passwordInput && eyeIcon) {
    togglePassword.addEventListener("click", () => {
      const isPassword = passwordInput.type === "password";
      passwordInput.type = isPassword ? "text" : "password";
      eyeIcon.classList.toggle("bi-eye", !isPassword);
      eyeIcon.classList.toggle("bi-eye-slash", isPassword);
    });
  }

  // Redirect ke Topik1_10.html
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      window.location.href = "Topik1_10.html";
    });
  }
});