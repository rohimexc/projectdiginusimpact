document.addEventListener("DOMContentLoaded", () => {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const eyeIcon = document.getElementById("eyeIcon");
  const loginForm = document.getElementById("loginForm");

  // Toggle show/hide password
  togglePassword.addEventListener("click", () => {
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";

    eyeIcon.classList.toggle("fa-eye", !isPassword);
    eyeIcon.classList.toggle("fa-eye-slash", isPassword);
  });

  // Handle submit form
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    console.log("Login data:", { email, password, rememberMe });
    alert(`Berhasil Login: ${email}`);
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const eyeIcon = document.getElementById("eyeIcon");
  const loginForm = document.getElementById("loginForm");

  // Toggle Password Visibility
  if (togglePassword) {
    togglePassword.addEventListener("click", () => {
      const isPassword = passwordInput.type === "password";
      passwordInput.type = isPassword ? "text" : "password";

      eyeIcon.classList.toggle("fa-eye", !isPassword);
      eyeIcon.classList.toggle("fa-eye-slash", isPassword);
    });
  }

  // Handle Form Submission & Redirect
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault(); // Mencegah reload halaman default

      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      console.log("Login submitted:", { email, password });

      // Pindah langsung ke file Topik1_10.html
      window.location.href = "Topik1_10.html";
    });
  }
});