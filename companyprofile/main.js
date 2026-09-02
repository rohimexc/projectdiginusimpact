/**
 * ==========================================================================
 * DOKUMENTASI LOGIKA PEMROGRAMAN (main.js) - DIGINUS
 * Catatan: Berkas ini mengatur seluruh perilaku interaktif halaman web, 
 * meliputi inisialisasi animasi gulir, efek navigasi, gulir mulus (smooth scroll),
 * serta sistem akordeon eksklusif yang terhubung dengan gambar dinamis.
 * ==========================================================================
 */


/**
 * ==========================================================================
 * FUNGSI 1: INISIALISASI AOS & EFEK NAVBAR SAAT DIGULIR (SCROLL)
 * ==========================================================================
 * Fungsi ini berjalan otomatis setelah seluruh struktur HTML selesai dimuat.
 * Bertanggung jawab mengaktifkan pustaka animasi dan mendeteksi posisi layar.
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // Inisialisasi Pustaka AOS (Animate On Scroll) dengan konfigurasi kehalusan kustom
    AOS.init({
        duration: 800,              // Durasi animasi dalam milidetik
        easing: 'ease-out-cubic',   // Jenis kurva transisi gerakan yang lembut
        once: true,                 // Animasi hanya berjalan sekali saat elemen muncul
        offset: 40                  // Jarak piksel pemicu sebelum elemen terlihat
    });

    // Menangani perubahan gaya bilah navigasi (header) saat halaman digulir ke bawah
    const header = document.getElementById('header');
    window.addEventListener('scroll', function() {
        // Jika posisi gulir vertikal melebihi 30 piksel, tambahkan kelas 'scrolled'
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Menangani interaksi gulir roda tetikus (wheel) secara horizontal pada kartu portofolio
    const portfolioMarquee = document.querySelector('.portfolio-marquee');
    if (portfolioMarquee) {
        portfolioMarquee.addEventListener('wheel', (evt) => {
            if (evt.deltaY !== 0) {
                evt.preventDefault(); // Mencegah gulir vertikal default halaman
                portfolioMarquee.scrollLeft += evt.deltaY; // Mengubah arah gulir ke horizontal
            }
        });
    }
});


/**
 * ==========================================================================
 * FUNGSI 2: PENGGULIRAN HALUS MENU NAVIGASI (SMOOTH SCROLL TO TARGET)
 * ==========================================================================
 * @param {Event} event - Objek peristiwa klik pada tombol/tautan.
 * @param {string} targetId - Atribut ID elemen tujuan gulir (contoh: '#portofolio').
 * Catatan: Fungsi ini mencegah lompatan kasar halaman dan menggantinya dengan animasi gulir yang mulus.
 */
function smoothScrollTo(event, targetId) {
    event.preventDefault();
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth', // Mengaktifkan efek transisi gulir halus
            block: 'start'      // Menyelaraskan bagian atas elemen dengan bagian atas viewport
        });
    }
}


/**
 * ==========================================================================
 * FUNGSI 3: SISTEM AKORDEON EKSKLUSIF & SINKRONISASI GAMBAR DINAMIS
 * ==========================================================================
 * Fungsi ini mengelola bagian "Kenapa Harus DIGINUS". Ketika satu menu dibuka,
 * menu lainnya akan tertutup otomatis, dan gambar serta keterangan di sebelah kanan
 * akan berganti secara sinkron menggunakan efek pudar (fade).
 */
document.addEventListener("DOMContentLoaded", function() {
    const accordionItems = document.querySelectorAll('.why-diginus-grid .accordion-item');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    // Mengatur agar item akordeon pertama menyala/terbuka secara default saat halaman dimuat
    const firstItem = accordionItems[0];
    if (firstItem) {
        firstItem.classList.add('active');
        const body = firstItem.querySelector('.accordion-body');
        if (body) body.style.maxHeight = body.scrollHeight + "px";
    }

    // Menambahkan pemantau klik (click event listener) pada setiap item akordeon
    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        
        header.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // Langkah A: Menutup seluruh item akordeon terlebih dahulu (Penerapan Sistem Eksklusif)
            accordionItems.forEach(el => {
                el.classList.remove('active');
                const body = el.querySelector('.accordion-body');
                if (body) body.style.maxHeight = null;
            });

            // Langkah B: Jika item yang diklik sebelumnya tidak aktif, buka item tersebut
            if (!isActive) {
                item.classList.add('active');
                const body = item.querySelector('.accordion-body');
                if (body) {
                    body.style.maxHeight = body.scrollHeight + "px"; // Mengatur tinggi dinamis berdasarkan isi konten
                }

                // Mengambil data sumber gambar baru dan teks keterangan dari atribut HTML (data-img & data-caption)
                const newImgSrc = item.getAttribute('data-img');
                const newCaption = item.getAttribute('data-caption');

                // Langkah C: Menerapkan efek transisi pudar (fade) saat mengganti gambar di kolom kanan
                if (activeImg) {
                    activeImg.style.opacity = '0'; // Menyembunyikan gambar secara perlahan
                    setTimeout(() => {
                        activeImg.src = newImgSrc;  // Mengubah sumber berkas gambar
                        activeImg.style.opacity = '1'; // Memunculkan kembali gambar baru secara perlahan
                    }, 200);
                }

                // Langkah D: Memperbarui teks pada label badge keterangan di bawah gambar
                if (activeText) {
                    activeText.textContent = newCaption;
                }
            }
        });
    });
});

/**
 * ==========================================================================
 * LOGIKA OTOMATIS PEMBAGIAN BARIS PORTOFOLIO (> 8 CARD JADI 2 BARIS)
 * ==========================================================================
 */
document.addEventListener("DOMContentLoaded", function() {
    const row1Track = document.querySelector('#marquee-row-1 .marquee-track');
    const row2Wrapper = document.getElementById('marquee-row-2');
    const row2Track = document.getElementById('marquee-track-2');

    if (row1Track && row2Wrapper && row2Track) {
        const allCards = Array.from(row1Track.querySelectorAll('.portfolio-card'));
        
        // Jika total card portofolio lebih dari 8
        if (allCards.length > 8) {
            row2Wrapper.style.display = 'flex'; // Munculkan baris kedua

            // Ambil card mulai dari indeks ke-8 (card ke-9 dan seterusnya)
            const excessCards = allCards.slice(8);
            
            // Pindahkan card selebihnya ke baris kedua
            excessCards.forEach(card => {
                row2Track.appendChild(card.cloneNode(true)); // Gandakan ke baris 2
                card.remove(); // Hapus dari baris 1
            });
        } else {
            // Jika kurang atau pas 8, sembunyikan baris kedua
            row2Wrapper.style.display = 'none';
        }

        // Duplikat isi track secara otomatis di dalam JavaScript untuk efek infinite loop yang mulus
        [row1Track, row2Track].forEach(track => {
            if (track.children.length > 0) {
                const items = Array.from(track.children);
                items.forEach(item => {
                    track.appendChild(item.cloneNode(true));
                });
            }
        });
    }
});