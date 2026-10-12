import { whyDiginusData } from '../data/whyDiginusData.js';

export function initAccordion() {
    const accordionContainer = document.querySelector('.accordion-container');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    if (!accordionContainer) return;

    accordionContainer.innerHTML = '';

    whyDiginusData.forEach((item, index) => {
        const accordionItem = document.createElement('div');
        // Tambahkan class 'active' secara default khusus untuk item pertama
        const isFirst = index === 0;
        
        accordionItem.className = `border rounded-2xl mb-4 bg-white overflow-hidden transition-all duration-300 ${
            isFirst ? 'active border-indigo-600 shadow-lg shadow-indigo-600/10' : 'border-slate-200 shadow-sm'
        }`;
        accordionItem.setAttribute('data-img', item.img);
        accordionItem.setAttribute('data-caption', item.caption);

        accordionItem.innerHTML = `
            <div class="accordion-header px-6 py-5 font-bold text-slate-900 cursor-pointer flex justify-between items-center w-full text-left text-base">
                <span><i class="${item.icon} mr-2.5 text-blue-600"></i> ${item.title}</span>
                <i class="fas fa-chevron-down transition-transform duration-300 text-slate-500 ${isFirst ? 'rotate-180 text-blue-600' : ''}"></i>
            </div>
            <div class="accordion-body overflow-hidden transition-all duration-300 ease-in-out px-6 text-slate-600 text-sm leading-relaxed" style="max-height: ${isFirst ? '200px' : '0px'};">
                <p class="pb-6">${item.description}</p>
            </div>
        `;
        accordionContainer.appendChild(accordionItem);
    });

    // Set gambar & teks awal sesuai item pertama
    if (activeImg && whyDiginusData.length > 0) {
        activeImg.src = whyDiginusData[0].img;
        activeImg.setAttribute('loading', 'lazy');
    }
    if (activeText && whyDiginusData.length > 0) {
        activeText.textContent = whyDiginusData[0].caption;
    }

    const accordionItems = accordionContainer.querySelectorAll('.border');

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Tutup semua item
            accordionItems.forEach(el => {
                el.classList.remove('active', 'border-indigo-600', 'shadow-lg', 'shadow-indigo-600/10');
                el.classList.add('border-slate-200', 'shadow-sm');
                const body = el.querySelector('.accordion-body');
                const icon = el.querySelector('.fa-chevron-down');
                if (body) body.style.maxHeight = "0px";
                if (icon) icon.classList.remove('rotate-180', 'text-blue-600');
            });

            // Buka item yang diklik jika sebelumnya mati
            if (!isActive) {
                item.classList.add('active', 'border-indigo-600', 'shadow-lg', 'shadow-indigo-600/10');
                item.classList.remove('border-slate-200', 'shadow-sm');
                
                const body = item.querySelector('.accordion-body');
                const icon = item.querySelector('.fa-chevron-down');
                
                if (body) body.style.maxHeight = body.scrollHeight + "px";
                if (icon) icon.classList.add('rotate-180', 'text-blue-600');

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