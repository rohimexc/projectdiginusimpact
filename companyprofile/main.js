/* AOS & Custom Minimalist Animation Script */
document.addEventListener("DOMContentLoaded", function() {
    // Inisialisasi AOS Library dengan konfigurasi halus & smooth
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 40
    });

    // Efek Navbar Berubah Warna Saat Di-scroll
    const header = document.getElementById('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Interaksi tambahan untuk kartu portofolio (Auto-scroll smooth horizontal drag/wheel optional or subtle hover enhancement)
    const portfolioMarquee = document.querySelector('.portfolio-marquee');
    if (portfolioMarquee) {
        portfolioMarquee.addEventListener('wheel', (evt) => {
            if (evt.deltaY !== 0) {
                evt.preventDefault();
                portfolioMarquee.scrollLeft += evt.deltaY;
            }
        });
    }
});
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
/* =========================================
   LOGIKA JAVASCRIPT ACCORDION EKSKLUSIF
   ========================================= */
document.addEventListener("DOMContentLoaded", function() {
    const accordionItems = document.querySelectorAll('.why-diginus-grid .accordion-item');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    // Set item pertama menyala secara default saat halaman dimuat
    const firstItem = accordionItems[0];
    if (firstItem) {
        firstItem.classList.add('active');
        const body = firstItem.querySelector('.accordion-body');
        if (body) body.style.maxHeight = body.scrollHeight + "px";
    }

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        
        header.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // Tutup semua accordion item
            accordionItems.forEach(el => {
                el.classList.remove('active');
                const body = el.querySelector('.accordion-body');
                if (body) body.style.maxHeight = null;
            });

            // Jika item yang diklik tadi belum aktif, maka buka dan ganti gambarnya
            if (!isActive) {
                item.classList.add('active');
                const body = item.querySelector('.accordion-body');
                if (body) {
                    body.style.maxHeight = body.scrollHeight + "px";
                }

                // Ambil data gambar dan teks dari atribut HTML
                const newImgSrc = item.getAttribute('data-img');
                const newCaption = item.getAttribute('data-caption');

                // Efek transisi pudar (fade) saat ganti gambar
                if (activeImg) {
                    activeImg.style.opacity = '0';
                    setTimeout(() => {
                        activeImg.src = newImgSrc;
                        activeImg.style.opacity = '1';
                    }, 200);
                }

                // Ganti teks pada badge bawah gambar
                if (activeText) {
                    activeText.textContent = newCaption;
                }
            }
        });
    });
});