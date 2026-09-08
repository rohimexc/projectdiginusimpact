import { whyDiginusData } from '../data/whyDiginusData.js';

export function initAccordion() {
    const accordionContainer = document.querySelector('.accordion-container');
    const activeImg = document.getElementById('active-feature-img');
    const activeText = document.getElementById('active-feature-text');

    if (!accordionContainer) return;

    accordionContainer.innerHTML = '';

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

    if (activeImg && whyDiginusData.length > 0) {
        activeImg.src = whyDiginusData[0].img;
        activeImg.setAttribute('loading', 'lazy');
    }
    if (activeText && whyDiginusData.length > 0) {
        activeText.textContent = whyDiginusData[0].caption;
    }

    const accordionItems = document.querySelectorAll('.why-diginus-grid .accordion-item');
    const firstItem = accordionItems[0];
    if (firstItem) {
        const body = firstItem.querySelector('.accordion-body');
        if (body) body.style.maxHeight = body.scrollHeight + "px";
    }

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            accordionItems.forEach(el => {
                el.classList.remove('active');
                const body = el.querySelector('.accordion-body');
                if (body) body.style.maxHeight = null;
            });

            if (!isActive) {
                item.classList.add('active');
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