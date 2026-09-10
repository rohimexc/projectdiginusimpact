import { whyDiginusData } from '../data/whyDiginusData.js';

export function initAccordion() {
    const accordionContainer = document.querySelector('.accordion-container');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    if (!accordionContainer) return;

    accordionContainer.innerHTML = '';

    whyDiginusData.forEach((item) => {
        const accordionItem = document.createElement('div');
        accordionItem.className = 'border border-slate-200 rounded-2xl mb-4 bg-white overflow-hidden transition-all duration-300 shadow-sm';
        accordionItem.setAttribute('data-img', item.img);
        accordionItem.setAttribute('data-caption', item.caption);

        accordionItem.innerHTML = `
            <div class="accordion-header px-6 py-5 font-bold text-slate-900 cursor-pointer flex justify-between items-center w-full text-left text-base">
                <span><i class="${item.icon}"></i> ${item.title}</span>
                <i class="fas fa-chevron-down transition-transform duration-300"></i>
            </div>
            <div class="accordion-body overflow-hidden transition-all duration-500 ease-in-out px-6 text-slate-600 text-sm leading-relaxed" style="max-height: 0px;">
                <p class="pb-6">${item.description}</p>
            </div>
        `;
        accordionContainer.appendChild(accordionItem);
    });

    if (activeImg && whyDiginusData.length > 0) {
        activeImg.src = whyDiginusData[0].img;
        activeImg.setAttribute('loading', 'lazy');
    }
    if (activeText && whyDiginusData.length > 0) {
        activeText.textContent = whyDiginusData[0].caption;
    }

    // Ambil langsung dari accordionContainer yang baru di-generate
    const accordionItems = accordionContainer.querySelectorAll('.border');

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Tutup semua item secara halus
            accordionItems.forEach(el => {
                el.classList.remove('active', 'border-indigo-600', 'shadow-lg', 'shadow-indigo-600/10');
                el.classList.add('border-slate-200', 'shadow-sm');
                const body = el.querySelector('.accordion-body');
                if (body) body.style.maxHeight = "0px";
            });

            // Jika sebelumnya tidak aktif, buka yang diklik dengan mulus
            if (!isActive) {
                item.classList.add('active', 'border-indigo-600', 'shadow-lg', 'shadow-indigo-600/10');
                item.classList.remove('border-slate-200', 'shadow-sm');
                
                const body = item.querySelector('.accordion-body');
                if (body) body.style.maxHeight = body.scrollHeight + "px";

                const newImgSrc = item.getAttribute('data-img');
                const newCaption = item.getAttribute('data-caption');

                if (activeImg) {
                    activeImg.style.opacity = '0';
                    setTimeout(() => {
                        activeImg.src = newImgSrc;
                        activeImg.style.opacity = '1';
                    }, 200);
                }
                if (activeText) activeText.textContent = newCaption;
            }
        });
    });
}