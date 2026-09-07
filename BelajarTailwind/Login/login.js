document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    alert(`Login berhasil untuk email: ${email}`);
});

document.getElementById('loginForm').addEventListener('submit', function(e) {
    // Mencegah form melakukan refresh halaman bawaan HTML
    e.preventDefault();

    // (Opsional) Ambil nilai email jika ingin divalidasi dulu
    const email = document.getElementById('loginEmail').value;

    // Menampilkan alert sukses sebentar (opsional)
    alert(`Login berhasil untuk ${email}! Selamat datang kembali.`);

    // Perintah untuk memindahkan halaman ke dashboard atau halaman utama kamu
    // Ganti 'dashboard.html' dengan nama file tujuan kamu berikutnya
    window.location.href = '../BelajarTailwind/topik1_10.html'; // Contoh redirect ke halaman Topik1-10
});