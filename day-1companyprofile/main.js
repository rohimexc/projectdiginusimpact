document.addEventListener('DOMContentLoaded', () => {
  // 1. Inisialisasi AOS (Animate On Scroll)
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true,
    offset: 70
  });

  // 2. Sticky Header & Tombol Scroll To Top
  const navbar = document.getElementById('navbar');
  const scrollTopBtn = document.getElementById('scrollTopBtn');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    if (navbar) {
      if (scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }

    if (scrollTopBtn) {
      if (scrollY > 300) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    }
  });

  // 3. Counter Statistics (Animasi Angka Berjalan)
  const counters = document.querySelectorAll('.counter');
  let counterStarted = false;

  const runCounter = () => {
    counters.forEach(counter => {
      const target = +counter.getAttribute('data-target');
      const count = +counter.innerText;
      const increment = Math.ceil(target / 40);

      if (count < target) {
        counter.innerText = Math.min(count + increment, target);
        setTimeout(runCounter, 30);
      } else {
        counter.innerText = target;
      }
    });
  };

  const statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    window.addEventListener('scroll', () => {
      const sectionPos = statsSection.getBoundingClientRect().top;
      const screenPos = window.innerHeight;
      if (sectionPos < screenPos && !counterStarted) {
        counterStarted = true;
        runCounter();
      }
    });
  }

  // 4. Interaksi Accordion Keunggulan & Pergantian Gambar Dinamis
  const accordionItems = document.querySelectorAll('.accordion-item');
  const previewImg = document.getElementById('accordionPreviewImg');

  accordionItems.forEach(item => {
    const header = item.querySelector('.accordion-header');

    header.addEventListener('click', () => {
      const isActive = item.classList.contains('active');

      // Tutup accordion lainnya
      accordionItems.forEach(acc => acc.classList.remove('active'));

      // Buka accordion yang diklik
      if (!isActive) {
        item.classList.add('active');

        // Ganti preview gambar dengan animasi transisi
        const newImgSrc = item.getAttribute('data-img');
        if (previewImg && newImgSrc) {
          previewImg.style.opacity = '0';
          previewImg.style.transform = 'scale(0.96)';

          setTimeout(() => {
            previewImg.src = newImgSrc;
            previewImg.style.opacity = '1';
            previewImg.style.transform = 'scale(1)';
          }, 180);
        }
      }
    });
  });

  // 5. Filter Portofolio
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-track .portfolio-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      portfolioCards.forEach(card => {
        const categories = card.getAttribute('data-category') || '';
        if (filterValue === 'all' || categories.includes(filterValue)) {
          card.classList.remove('hide');
        } else {
          card.classList.add('hide');
        }
      });
    });
  });

  // 6. Geser Carousel Portofolio (Tombol Panah Kiri & Kanan)
  const portfolioTrack = document.getElementById('portfolioTrack');
  const prevSlide = document.getElementById('prevSlide');
  const nextSlide = document.getElementById('nextSlide');

  if (portfolioTrack && prevSlide && nextSlide) {
    prevSlide.addEventListener('click', () => {
      portfolioTrack.scrollBy({ left: -370, behavior: 'smooth' });
    });

    nextSlide.addEventListener('click', () => {
      portfolioTrack.scrollBy({ left: 370, behavior: 'smooth' });
    });
  }

  // 7. Modal Portofolio
  const portfolioModal = document.getElementById('portfolioModal');
  const modalOverlay = document.getElementById('modalOverlay');
  const modalClose = document.getElementById('modalClose');
  const btnModalClose = document.getElementById('btnModalClose');
  const modalBadge = document.getElementById('modalBadge');
  const modalTitle = document.getElementById('modalTitle');
  const modalDomain = document.getElementById('modalDomain');
  const modalDesc = document.getElementById('modalDesc');

  const openPortfolioModal = (card) => {
    const badgeText = card.querySelector('.portfolio-badge')?.innerText || 'Portofolio';
    const titleText = card.querySelector('h3')?.innerText || 'Judul Portofolio';
    const domainHTML = card.querySelector('.portfolio-domain')?.innerHTML || '';
    const descText = card.querySelector('p')?.innerText || '';

    modalBadge.innerText = badgeText;
    modalTitle.innerText = titleText;
    modalDomain.innerHTML = domainHTML;
    modalDesc.innerText = descText;

    portfolioModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closePortfolioModal = () => {
    portfolioModal.classList.remove('active');
    document.body.style.overflow = '';
  };

  portfolioCards.forEach(card => {
    card.addEventListener('click', () => {
      openPortfolioModal(card);
    });
  });

  if (modalOverlay) modalOverlay.addEventListener('click', closePortfolioModal);
  if (modalClose) modalClose.addEventListener('click', closePortfolioModal);
  if (btnModalClose) btnModalClose.addEventListener('click', closePortfolioModal);

  // 8. Tombol Salin 1-Klik dengan Notifikasi Toast
  const copyBtns = document.querySelectorAll('.btn-copy');
  const toast = document.getElementById('toast');

  const showToast = (message) => {
    if (toast) {
      toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${message}`;
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 2500);
    }
  };

  copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy');
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showToast(`Berhasil disalin: ${textToCopy}`);
        });
      }
    });
  });
});