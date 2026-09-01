document.addEventListener('DOMContentLoaded', () => {
  // 1. Inisialisasi Animate On Scroll (AOS)
  AOS.init({
    duration: 600,
    easing: 'ease-out',
    once: true,
    offset: 50
  });

  // 2. Efek Sticky Header & Scroll Top Button
  const navbar = document.getElementById('navbar');
  const scrollTopBtn = document.getElementById('scrollTopBtn');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    if (navbar) {
      if (scrollY > 30) {
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
      const increment = Math.ceil(target / 30);

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

  // 4. Filter Portofolio
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');

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

  // 5. Modal Portofolio
  const portfolioModal = document.getElementById('portfolioModal');
  const modalOverlay = document.getElementById('modalOverlay');
  const modalClose = document.getElementById('modalClose');
  const btnModalClose = document.getElementById('btnModalClose');
  const modalBadge = document.getElementById('modalBadge');
  const modalTitle = document.getElementById('modalTitle');
  const modalDomain = document.getElementById('modalDomain');
  const modalDesc = document.getElementById('modalDesc');

  const openPortfolioModal = (card) => {
    modalBadge.innerText = card.querySelector('.portfolio-badge')?.innerText || 'Portofolio';
    modalTitle.innerText = card.querySelector('h3')?.innerText || 'Judul Portofolio';
    modalDomain.innerHTML = card.querySelector('.portfolio-domain')?.innerHTML || '';
    modalDesc.innerText = card.querySelector('p')?.innerText || '';

    portfolioModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closePortfolioModal = () => {
    portfolioModal.classList.remove('active');
    document.body.style.overflow = '';
  };

  portfolioCards.forEach(card => {
    card.addEventListener('click', () => openPortfolioModal(card));
  });

  if (modalOverlay) modalOverlay.addEventListener('click', closePortfolioModal);
  if (modalClose) modalClose.addEventListener('click', closePortfolioModal);
  if (btnModalClose) btnModalClose.addEventListener('click', closePortfolioModal);

  // 6. Tombol Salin 1-Klik & Toast
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
          showToast(`Tersalin: ${textToCopy}`);
        });
      }
    });
  });

  // 7. Pengiriman Form Kontak
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value;
      const selectedService = document.querySelector('input[name="service_type"]:checked')?.value || 'Digital Services';
      
      showToast(`Terima kasih ${name}, pengajuan ${selectedService} terkirim!`);
      contactForm.reset();
    });
  }
});