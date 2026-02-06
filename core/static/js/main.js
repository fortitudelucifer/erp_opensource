document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle Logic
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            
            // Optional: Toggle icon state if we had one
            const isExpanded = navLinks.classList.contains('active');
            mobileBtn.setAttribute('aria-expanded', isExpanded);
        });
    }

    // Auto-dismiss flashes after 5 seconds
    const flashes = document.querySelectorAll('.status-badge.warning');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => {
                flash.style.opacity = '0';
                flash.style.transition = 'opacity 0.5s ease';
                setTimeout(() => flash.remove(), 500);
            });
        }, 5000);
    }
});
