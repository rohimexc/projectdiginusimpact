import { portfolioData } from '../data/portfolioData.js';

export function initMarquee() {
    const mainContainer = document.getElementById('portfolio-main-container');

    if (!mainContainer) return;

    // Bersihkan kontainer utama sebelum dirender ulang
    mainContainer.innerHTML = '';

    // Tentukan jumlah maksimal kartu per baris
    const cardsPerGroup = 8;
    
    // Hitung total berapa baris yang dibutuhkan berdasarkan jumlah data
    const totalRows = Math.ceil(portfolioData.length / cardsPerGroup);

    // Loop untuk membuat setiap baris (row) marquee secara dinamis
    for (let i = 0; i < totalRows; i++) {
        // Ambil data sebanyak 8 item per baris (slice: 0-8, 8-16, dst)
        const rowData = portfolioData.slice(i * cardsPerGroup, (i + 1) * cardsPerGroup);

        // Buat pembungkus baris (marquee-wrapper)
        const wrapper = document.createElement('div');
        wrapper.className = 'marquee-wrapper';
        if (i > 0) wrapper.style.marginTop = '20px'; // Beri jarak antar baris

        // Buat jalur track marquee (baris genap gerak ke kanan, ganjil ke kiri biar estetik)
        const track = document.createElement('div');
        const directionClass = i % 2 === 0 ? 'track-right' : 'track-left';
        track.className = `marquee-track ${directionClass}`;

        // Masukkan kartu portofolio ke dalam track baris tersebut
        rowData.forEach(item => {
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
            track.appendChild(card);
        });

        // Duplikat isi track via JS untuk efek infinite loop yang mulus tanpa jeda
        const items = Array.from(track.children);
        items.forEach(item => {
            track.appendChild(item.cloneNode(true));
        });

        // Gabungkan elemen ke dalam DOM halaman
        wrapper.appendChild(track);
        mainContainer.appendChild(wrapper);
    }
}