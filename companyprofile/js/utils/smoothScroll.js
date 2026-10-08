export function initSmoothScroll() {
    window.smoothScrollTo = function(event, targetId) {
        event.preventDefault();
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    };
}