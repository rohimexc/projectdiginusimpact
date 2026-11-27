import { initHeader } from './components/header.js';
import { initAccordion } from './components/accordion.js';
import { initMarquee } from './components/marquee.js';
import { initSmoothScroll } from './utils/smoothScroll.js';

document.addEventListener("DOMContentLoaded", () => {
    // Inisialisasi Pustaka AOS
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 40
    });

    // Panggil semua fungsi modul fitur
    initHeader();
    initAccordion();
    initMarquee();
    initSmoothScroll();
});