import { portfolioData } from '../data/portfolioData.js';

export function initMarquee() {
    const mainContainer = document.getElementById('portfolio-main-container');

    if (!mainContainer) return;

    mainContainer.innerHTML = '';

    if (!document.getElementById('dynamic-marquee-style')) {
        const style = document.createElement('style');
        style.id = 'dynamic-marquee-style';
        style.innerHTML = `
            @keyframes scrollRight {
                0% { transform: translateX(0); }
                100% { transform: translateX(-50%); }
            }
            @keyframes scrollLeft {
                0% { transform: translateX(-50%); }
                100% { transform: translateX(0); }
            }
            .anim-right {
                animation: scrollRight 40s linear infinite;
            }
            .anim-left {
                animation: scrollLeft 40s linear infinite;
            }
            .anim-right:hover, .anim-left:hover {
                animation-play-state: paused;
            }
        `;
        document.head.appendChild(style);
    }

    const cardsPerGroup = 8;
    const totalRows = Math.ceil(portfolioData.length / cardsPerGroup);

    for (let i = 0; i < totalRows; i++) {
        const rowData = portfolioData.slice(i * cardsPerGroup, (i + 1) * cardsPerGroup);

        // Tambah padding vertikal (py-4) di wrapper biar pas card hover naik ke atas, tidak terpotong overflow hidden
        const wrapper = document.createElement('div');
        wrapper.className = 'overflow-hidden relative w-full py-4';
        if (i > 0) wrapper.classList.add('mt-2');

        const track = document.createElement('div');
        const animClass = i % 2 === 0 ? 'anim-right' : 'anim-left';
        track.className = `flex gap-6 w-max ${animClass}`;

        rowData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'bg-white border border-slate-200 rounded-2xl p-6 w-[320px] flex-shrink-0 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-indigo-600 flex flex-col justify-between';
            card.innerHTML = `
                <div class="flex items-center justify-between mb-4">
                    <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl"><i class="${item.icon}"></i></div>
                    <span class="text-xs font-bold text-indigo-600 tracking-wider uppercase bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">${item.category}</span>
                </div>
                <div>
                    <h3 class="text-base font-bold text-slate-900 mb-2">${item.title}</h3>
                    <p class="text-xs text-slate-500 leading-relaxed">${item.desc}</p>
                </div>
            `;
            track.appendChild(card);
        });

        // Duplikat track untuk infinite loop mulus
        const items = Array.from(track.children);
        items.forEach(item => {
            track.appendChild(item.cloneNode(true));
        });

        wrapper.appendChild(track);
        mainContainer.appendChild(wrapper);
    }
}