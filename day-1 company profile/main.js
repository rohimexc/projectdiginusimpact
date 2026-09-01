document.addEventListener('DOMContentLoaded', () => {
  // 1. Inisialisasi Animate On Scroll (AOS)
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true,
    offset: 70
  });

  // 2. Navigasi Hamburger untuk Mobile
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link, .nav-btn');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const icon = hamburger.querySelector('i');
      if (navMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-xmark');
      } else {
        icon.classList.remove('fa-xmark');
        icon.classList.add('fa-bars');
      }
    });

    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const icon = hamburger.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        }
      });
    });
  }

  // 3. Efek Sticky Navbar, Scroll Top Button, dan Scroll Spy
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

    const sections = document.querySelectorAll('section[id]');
    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 130;
      const sectionId = section.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        document.querySelectorAll('.nav-link').forEach(a => a.classList.remove('active'));
        const currentLink = document.querySelector(`.nav-link[href*="${sectionId}"]`);
        if (currentLink) currentLink.classList.add('active');
      }
    });
  });

  // 4. Animasi Angka Berjalan (Counter Statistics)
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

  // 5. Filter Portofolio Interaktif
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
          card.style.opacity = '0';
          setTimeout(() => {
            card.style.opacity = '1';
          }, 50);
        } else {
          card.classList.add('hide');
        }
      });
    });
  });

  // 6. Modal / Pop-Up Mengambang Detail Portofolio
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

  // 7. Tombol Salin 1-Klik dengan Notifikasi Toast
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

  // 8. Pengiriman Form Kontak Interaktif
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value;
      const selectedService = document.querySelector('input[name="service_type"]:checked')?.value || 'Digital Services';
      
      showToast(`Terima kasih ${name}, pengajuan layanan ${selectedService} berhasil dikirim!`);
      contactForm.reset();
    });
  }
});