/**
 * ==========================================================================
 * DOKUMENTASI LOGIKA PEMROGRAMAN (main.js) - DIGINUS
 * Catatan: Berkas ini mengatur seluruh perilaku interaktif halaman web, 
 * termasuk database lokal (array data) untuk akordeon dan portofolio dinamis.
 * ==========================================================================
 */


/**
 * ==========================================================================
 * DATABASE LOKAL (SUMBER DATA KONTEN DINAMIS)
 * ==========================================================================
 */

// 1. Database untuk Menu Akordeon & Gambar Dinamis (Keunggulan)
const whyDiginusData = [
    {
        title: "01. Solusi Terintegrasi",
        icon: "fas fa-cubes",
        caption: "Solusi Terintegrasi & Komprehensif",
        img: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
        description: "Menggabungkan course, service, dan produk digital dalam satu kesatuan kohesif untuk transformasi menyeluruh."
    },
    {
        title: "02. Praktis & Berbasis Kebutuhan Riil",
        icon: "fas fa-bullseye",
        caption: "Praktis & Berbasis Kebutuhan Riil",
        img: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80",
        description: "Berakar pada analisis kebutuhan pasar nyata, memastikan solusi langsung aplikatif di industri."
    },
    {
        title: "03. Berorientasi Dampak & Kapasitas",
        icon: "fas fa-chart-line",
        caption: "Berorientasi Dampak & Kapasitas",
        img: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
        description: "Membangun kapasitas dan kompetensi jangka panjang bagi setiap individu maupun organisasi."
    },
    {
        title: "04. Fleksibilitas Tinggi",
        icon: "fas fa-sliders-h",
        caption: "Fleksibilitas Tinggi & Kustomisasi",
        img: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80",
        description: "Layanan dirancang personal agar dapat disesuaikan dengan kebutuhan unik dan tujuan bisnis Anda."
    },
    {
        title: "05. Komitmen Inklusivitas",
        icon: "fas fa-hands-helping",
        caption: "Komitmen Inklusivitas",
        img: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
        description: "Teknologi dan produk yang dihadirkan bersifat berkelanjutan serta mudah diakses berbagai lapisan masyarakat."
    },
    {
        title: "06. Pelayanan Profesional & Terdampingi",
        icon: "fas fa-user-shield",
        caption: "Pelayanan Profesional & Terdampingi",
        img: "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=80",
        description: "Menjamin komunikasi jelas, komitmen tenggat waktu, serta pendampingan intensif yang optimal."
    },
    {
        title: "07. Layanan Daring & Luring",
        icon: "fas fa-laptop-house",
        caption: "Layanan Daring & Luring",
        img: "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=800&q=80",
        description: "Fleksibilitas penuh melalui opsi online, offline, maupun in-house training dengan tenaga profesional."
    }
];

// 2. Database untuk Kartu Portofolio (Bisa ditambah lebih dari 8 item untuk tes 2 baris)
const portfolioData = [
    { title: "Kantor Pertanahan Palu", category: "Digital Service", icon: "fas fa-landmark", desc: "<strong>Official Website BPN Kota Palu:</strong> Portal resmi layanan publik." },
    { title: "SITAMPAN UNTAD", category: "Produk Digital", icon: "fas fa-university", desc: "<strong>Sistem Informasi Terpadu MBKM:</strong> Pendukung Magang & PLP." },
    { title: "Website Teknik Geofisika", category: "Digital Service", icon: "fas fa-laptop", desc: "<strong>FMIPA Untad:</strong> Penjadwalan akademik real-time." },
    { title: "SMART - Audit Mutu", category: "Produk Digital", icon: "fas fa-shield-alt", desc: "<strong>Universitas Tadulako:</strong> Manajemen audit mutu internal." },
    { title: "Website PMM UNTAD", category: "Digital Service", icon: "fas fa-globe", desc: "<strong>Pusat Mobilitas Mahasiswa:</strong> Portal strategis program kampus." },
    { title: "Website Prodi Sains Data", category: "Produk Digital", icon: "fas fa-chart-pie", desc: "<strong>Universitas Tadulako:</strong> Portal pengolahan data & AI." },
    { title: "Prodi Administrasi Publik", category: "Digital Service", icon: "fas fa-book-reader", desc: "<strong>FISIP Untad:</strong> Sarana komunikasi akuntabilitas." },
    { title: "Pesantren Insan Cita", category: "Produk Digital", icon: "fas fa-school", desc: "Platform resmi pesantren & integrasi PPDB online." },
    { title: "Kantor Pertanahan Palu", category: "Digital Service", icon: "fas fa-landmark", desc: "<strong>Official Website BPN Kota Palu:</strong> Portal resmi layanan publik." },
    { title: "SITAMPAN UNTAD", category: "Produk Digital", icon: "fas fa-university", desc: "<strong>Sistem Informasi Terpadu MBKM:</strong> Pendukung Magang & PLP." },
    { title: "Website Teknik Geofisika", category: "Digital Service", icon: "fas fa-laptop", desc: "<strong>FMIPA Untad:</strong> Penjadwalan akademik real-time." },
    { title: "SMART - Audit Mutu", category: "Produk Digital", icon: "fas fa-shield-alt", desc: "<strong>Universitas Tadulako:</strong> Manajemen audit mutu internal." },
    { title: "Website PMM UNTAD", category: "Digital Service", icon: "fas fa-globe", desc: "<strong>Pusat Mobilitas Mahasiswa:</strong> Portal strategis program kampus." },
    { title: "Website Prodi Sains Data", category: "Produk Digital", icon: "fas fa-chart-pie", desc: "<strong>Universitas Tadulako:</strong> Portal pengolahan data & AI." },
    { title: "Prodi Administrasi Publik", category: "Digital Service", icon: "fas fa-book-reader", desc: "<strong>FISIP Untad:</strong> Sarana komunikasi akuntabilitas." },
    { title: "Pesantren Insan Cita", category: "Produk Digital", icon: "fas fa-school", desc: "Platform resmi pesantren & integrasi PPDB online." }
];


/**
 * ==========================================================================
 * FUNGSI UTAMA: INISIALISASI HALAMAN & RENDER KONTEN DINAMIS
 * ==========================================================================
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // Inisialisasi Pustaka AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 40
    });

    // Efek Header saat Digulir
    const header = document.getElementById('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // ----------------------------------------------------
    // RENDER OTOMATIS AKORDEON (KEUNGGULAN)
    // ----------------------------------------------------
    const accordionContainer = document.querySelector('.accordion-container');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    if (accordionContainer) {
        accordionContainer.innerHTML = ''; // Kosongkan kontainer dulu

        whyDiginusData.forEach((item, index) => {
            const accordionItem = document.createElement('div');
            accordionItem.className = `accordion-item ${index === 0 ? 'active' : ''}`;
            accordionItem.setAttribute('data-img', item.img);
            accordionItem.setAttribute('data-caption', item.caption);

            accordionItem.innerHTML = `
                <div class="accordion-header">
                    <span><i class="${item.icon}"></i> ${item.title}</span>
                    <i class="fas fa-chevron-down"></i>
                </div>
                <div class="accordion-body">
                    <p>${item.description}</p>
                </div>
            `;
            accordionContainer.appendChild(accordionItem);
        });

        // Set gambar awal default (item pertama)
        if (activeImg && whyDiginusData.length > 0) {
            activeImg.src = whyDiginusData[0].img;
            activeImg.setAttribute('loading', 'lazy');
        }
        if (activeText && whyDiginusData.length > 0) {
            activeText.textContent = whyDiginusData[0].caption;
        }

        // Logika Interaksi Akordeon & Sinkronisasi Gambar Dinamis (dengan Fade-In)
        const accordionItems = document.querySelectorAll('.why-diginus-grid .accordion-item');
        
        // Buka item pertama secara default
        const firstItem = accordionItems[0];
        if (firstItem) {
            const body = firstItem.querySelector('.accordion-body');
            if (body) body.style.maxHeight = body.scrollHeight + "px";
        }

        accordionItems.forEach(item => {
            const header = item.querySelector('.accordion-header');
            
            header.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                accordionItems.forEach(el => {
                    el.classList.remove('active');
                    const body = el.querySelector('.accordion-body');
                    if (body) body.style.maxHeight = null;
                });

                if (!isActive) {
                    item.classList.add('active');
                    const body = item.querySelector('.accordion-body');
                    if (body) {
                        body.style.maxHeight = body.scrollHeight + "px";
                    }

                    const newImgSrc = item.getAttribute('data-img');
                    const newCaption = item.getAttribute('data-caption');

                    // Efek transisi pudar (fade-in) pada gambar dinamis
                    if (activeImg) {
                        activeImg.style.opacity = '0';
                        setTimeout(() => {
                            activeImg.src = newImgSrc;
                            activeImg.style.opacity = '1';
                        }, 200);
                    }

                    if (activeText) {
                        activeText.textContent = newCaption;
                    }
                }
            });
        });
    }

    // ----------------------------------------------------
    // RENDER OTOMATIS PORTOFOLIO & LOGIKA DUAL MARQUEE (> 8 CARD)
    // ----------------------------------------------------
    const row1Track = document.getElementById('marquee-track-1');
    const row2Wrapper = document.getElementById('marquee-row-2');
    const row2Track = document.getElementById('marquee-track-2');

    if (row1Track) {
        row1Track.innerHTML = '';
        if (row2Track) row2Track.innerHTML = '';

        // Masukkan data portofolio dari database JS ke baris 1
        portfolioData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'portfolio-card';
            card.innerHTML = `
                <div class="portfolio-card-top">
                    <div class="portfolio-icon-box"><i class="${item.icon}"></i></div>
                    <span class="portfolio-badge">${item.category}</span>
                </div>
                <div class="portfolio-content">
                    <h3>${item.title}</h3>
                    <p>${item.desc}</p>
                </div>
            `;
            row1Track.appendChild(card);
        });

        const allCards = Array.from(row1Track.querySelectorAll('.portfolio-card'));

        // Jika total card lebih dari 8, pindahkan sisanya ke baris 2 (berlawanan arah)
        if (allCards.length > 8 && row2Wrapper && row2Track) {
            row2Wrapper.style.display = 'flex';
            const excessCards = allCards.slice(8);
            
            excessCards.forEach(card => {
                row2Track.appendChild(card); // Pindah ke baris 2
            });
        } else if (row2Wrapper) {
            row2Wrapper.style.display = 'none';
        }

        // Duplikat isi track via JS untuk efek infinite loop yang mulus
        const activeTracks = [row1Track];
        if (allCards.length > 8 && row2Track) {
            activeTracks.push(row2Track);
        }

        activeTracks.forEach(track => {
            const items = Array.from(track.children);
            items.forEach(item => {
                track.appendChild(item.cloneNode(true));
            });
        });
    }
});


/**
 * ==========================================================================
 * FUNGSI: PENGGULIRAN HALUS MENU NAVIGASI (SMOOTH SCROLL TO TARGET)
 * ==========================================================================
 */
function smoothScrollTo(event, targetId) {
    event.preventDefault();
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}