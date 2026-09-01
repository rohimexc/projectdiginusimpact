// Inisialisasi AOS (Animate On Scroll) Library
AOS.init({
    duration: 1000, 
    once: true,     
    offset: 80     
});

// Efek Navbar Berubah Warna Jadi Biru Saat Di-scroll
const header = document.getElementById('header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Toggle Mobile Navigation Menu
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.querySelector('nav');

mobileMenu.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    
    // Ubah icon hamburger menjadi 'X' (close) dan sebaliknya
    const icon = mobileMenu.querySelector('i');
    if (navLinks.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Tutup menu otomatis saat salah satu link diklik di perangkat mobile
document.querySelectorAll('nav ul li a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        const icon = mobileMenu.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// Simulasi Form Kontak Submit 
const formKontak = document.getElementById('form-kontak');
if (formKontak) {
    formKontak.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Terima kasih banyak! Pesan Anda sudah kami terima. Tim DIGINUS akan segera menghubungi Anda kembali.');
        formKontak.reset();
    });
}
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.borderColor = 'var(--primary-color)';
    });
    card.addEventListener('mouseleave', () => {
        card.style.borderColor = '#f1f5f9';
    });
});