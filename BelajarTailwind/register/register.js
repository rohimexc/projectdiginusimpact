document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('regName').value;
    alert(`Pendaftaran berhasil untuk ${name}! Selamat datang di versi Premium.`);
    window.location.href = 'login.html';
});

document.getElementById('registerForm').addEventListener('submit', function(e) {
    // Mencegah form agar tidak melakukan refresh halaman secara default
    e.preventDefault();

    // Mengambil nilai dari input form pendaftaran
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    // Validasi sederhana (opsional)
    if (!name || !email || !password) {
        alert('Mohon isi semua kolom yang tersedia!');
        return;
    }

    // Simulasi sukses pendaftaran
    alert(`Registrasi berhasil, ${name}! Silakan masuk menggunakan akun baru Anda.`);

    // Mengarahkan (redirect) otomatis ke halaman login
    // Sesuaikan path ../Login/login.html dengan struktur folder kamu
    window.location.href = '../Login/login.html';
});