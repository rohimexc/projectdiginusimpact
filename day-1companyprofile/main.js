document.addEventListener('DOMContentLoaded', () => {

  // 1. Inisialisasi library AOS
  AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true,
    offset: 70
  });

  // 2. Efek Scroll pada Navbar & Tombol Scroll-to-Top
  const navbar = document.getElementById('navbar');
  const scrollTopBtn = document.getElementById('scrollTopBtn');

  // Set initial state untuk scroll-top button
  if (scrollTopBtn) {
    scrollTopBtn.classList.add('opacity-0', 'pointer-events-none', 'translate-y-4', 'transition-all', 'duration-300');
  }

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    // Navbar shadow effect
    if (navbar) {
      if (scrollY > 40) {
        navbar.classList.add('shadow-md', 'bg-white/95');
        navbar.classList.remove('bg-white/90');
      } else {
        navbar.classList.remove('shadow-md', 'bg-white/95');
        navbar.classList.add('bg-white/90');
      }
    }

    // Scroll-to-top visibility
    if (scrollTopBtn) {
      if (scrollY > 300) {
        scrollTopBtn.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-4');
        scrollTopBtn.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
      } else {
        scrollTopBtn.classList.add('opacity-0', 'pointer-events-none', 'translate-y-4');
        scrollTopBtn.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
      }
    }
  });

  // Kembali ke atas saat tombol panah diklik
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 3. Animasi Angka Counter Statistik
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


// 4. Accordion Interaktif & Preview Gambar (Ultra Smooth Transition)
const accordionItems = document.querySelectorAll('.accordion-item');
const previewImg = document.getElementById('accordionPreviewImg');

accordionItems.forEach(item => {
  const header = item.querySelector('.accordion-header');
  const body = item.querySelector('.accordion-body');
  const arrow = item.querySelector('.acc-arrow');

  // Set kondisi awal: jika item aktif (default), set row 1fr, sisanya 0fr
  if (item.classList.contains('active')) {
    body.style.gridTemplateRows = '1fr';
    if (arrow) arrow.classList.add('rotate-180', 'text-brand-600');
  } else {
    body.style.gridTemplateRows = '0fr';
  }

  header.addEventListener('click', () => {
    const isCurrentlyOpen = body.style.gridTemplateRows === '1fr';

    // 1. Tutup SEMUA accordion
    accordionItems.forEach(acc => {
      const accBody = acc.querySelector('.accordion-body');
      const accArrow = acc.querySelector('.acc-arrow');

      acc.classList.remove('active', 'border-brand-500', 'ring-2', 'ring-brand-100');
      acc.classList.add('border-slate-200');

      if (accBody) {
        accBody.style.gridTemplateRows = '0fr';
      }

      if (accArrow) {
        accArrow.classList.remove('rotate-180', 'text-brand-600');
        accArrow.classList.add('text-slate-400');
      }
    });

    // 2. Buka item yang diklik JIKA sebelumnya tertutup
    if (!isCurrentlyOpen) {
      item.classList.add('active', 'border-brand-500', 'ring-2', 'ring-brand-100');
      item.classList.remove('border-slate-200');

      // Animasi buka (transisi halus karena CSS transition menangani pergerakan grid-template-rows)
      body.style.gridTemplateRows = '1fr';

      if (arrow) {
        arrow.classList.remove('text-slate-400');
        arrow.classList.add('rotate-180', 'text-brand-600');
      }

      // 3. Animasi ganti gambar preview
      const newImgSrc = item.getAttribute('data-img');
      if (previewImg && newImgSrc && previewImg.src !== newImgSrc) {
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

  // 5. Filter Kategori Kartu Portofolio
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Style aktif untuk button filter
      filterBtns.forEach(b => {
        b.className = 'filter-btn px-5 py-2 rounded-full text-xs font-semibold bg-white text-slate-600 border border-slate-200 hover:bg-slate-100 transition';
      });
      btn.className = 'filter-btn active px-5 py-2 rounded-full text-xs font-semibold bg-brand-600 text-white shadow-md transition';

      const filterValue = btn.getAttribute('data-filter');

      portfolioCards.forEach(card => {
        const categories = card.getAttribute('data-category') || '';
        if (filterValue === 'all' || categories.includes(filterValue)) {
          card.classList.remove('hidden');
          card.classList.add('flex');
        } else {
          card.classList.add('hidden');
          card.classList.remove('flex');
        }
      });
    });
  });

  // 6. Modal Popup Detail Portofolio
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

    if (modalBadge) modalBadge.innerText = badgeText;
    if (modalTitle) modalTitle.innerText = titleText;
    if (modalDomain) modalDomain.innerHTML = domainHTML;
    if (modalDesc) modalDesc.innerText = descText;

    if (portfolioModal) {
      portfolioModal.classList.remove('hidden');
      portfolioModal.classList.add('flex');
    }
    document.body.style.overflow = 'hidden';
  };

  const closePortfolioModal = () => {
    if (portfolioModal) {
      portfolioModal.classList.add('hidden');
      portfolioModal.classList.remove('flex');
    }
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

  // 7. Copy Nomor Legalitas & Toast Notification
  const copyBtns = document.querySelectorAll('.btn-copy');
  const toast = document.getElementById('toast');
  let toastTimer = null;

  const showToast = (message) => {
    if (toast) {
      toast.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400"></i> <span>${message}</span>`;
      toast.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-4');
      toast.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');

      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.add('opacity-0', 'pointer-events-none', 'translate-y-4');
        toast.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
      }, 2500);
    }
  };

  copyBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // Mencegah bubbling jika ada container pembungkus
      const textToCopy = btn.getAttribute('data-copy');
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showToast(`Berhasil disalin: ${textToCopy}`);
        });
      }
    });
  });

});