// Fungsi untuk toggle show/hide password
function togglePassword(fieldId, iconId) {
    const passwordField = document.getElementById(fieldId);
    const icon = document.getElementById(iconId);
    if (!passwordField || !icon) return;
    
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />`;
    } else {
        passwordField.type = "password";
        icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />`;
    }
}

// Fungsi indikator kekuatan password
function checkPasswordStrength(password) {
    const bar1 = document.getElementById('strengthBar1');
    const bar2 = document.getElementById('strengthBar2');
    const bar3 = document.getElementById('strengthBar3');
    const text = document.getElementById('strengthText');

    if (!bar1 || !bar2 || !bar3 || !text) return;

    // Reset warna bar
    bar1.className = "bg-slate-200 rounded-full transition-all duration-300 h-1.5";
    bar2.className = "bg-slate-200 rounded-full transition-all duration-300 h-1.5";
    bar3.className = "bg-slate-200 rounded-full transition-all duration-300 h-1.5";

    if (password.length === 0) {
        text.innerText = "Gunakan minimal 8 karakter dengan kombinasi huruf dan angka.";
        text.className = "text-[11px] text-slate-400";
        return;
    }

    // Evaluasi kekuatan password yang lebih masuk akal (tanpa wajib simbol/spasi)
    let hasLetter = /[a-zA-Z]/.test(password);
    let hasNumber = /[0-9]/.test(password);
    let isLongEnough = password.length >= 8;

    if (password.length < 6) {
        // 1. LEMAH (Merah) - Kurang dari 6 karakter
        bar1.className = "bg-red-500 rounded-full transition-all duration-300 h-1.5";
        text.innerText = "Sandi Lemah: Terlalu pendek.";
        text.className = "text-[11px] text-red-500 font-medium";
    } else if (!isLongEnough || !(hasLetter && hasNumber)) {
        // 2. SEDANG (Kuning) - 6-7 karakter atau cuma huruf/angka doang
        bar1.className = "bg-yellow-500 rounded-full transition-all duration-300 h-1.5";
        bar2.className = "bg-yellow-500 rounded-full transition-all duration-300 h-1.5";
        text.innerText = "Sandi Sedang: Tambahkan panjang atau kombinasi angka.";
        text.className = "text-[11px] text-yellow-600 font-medium";
    } else {
        // 3. KUAT (Hijau) - Minimal 8 karakter + ada huruf & angka
        bar1.className = "bg-emerald-500 rounded-full transition-all duration-300 h-1.5";
        bar2.className = "bg-emerald-500 rounded-full transition-all duration-300 h-1.5";
        bar3.className = "bg-emerald-500 rounded-full transition-all duration-300 h-1.5";
        text.innerText = "Sandi Kuat: Sangat aman!";
        text.className = "text-[11px] text-emerald-600 font-medium";
    }
}

// Event listener saat form disubmit
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    if (!name || !email || !password || !confirmPassword) {
        alert('Mohon isi semua kolom yang tersedia!');
        return;
    }

    if (password !== confirmPassword) {
        alert('Konfirmasi password tidak sama! Silakan periksa kembali.');
        return;
    }

    alert(`Registrasi berhasil, ${name}! Silakan masuk menggunakan akun baru Anda.`);
    window.location.href = '../Login/login.html';
});