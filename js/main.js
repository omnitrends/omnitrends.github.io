// ===== MOBILE NAVIGATION =====
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
        navToggle.classList.toggle('active');
    });

    // Close menu when clicking on a link (but not dropdown toggles)
    const navLinks = document.querySelectorAll('.nav__link:not(.nav__dropdown-toggle)');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('show');
            navToggle.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('show');
            navToggle.classList.remove('active');
        }
    });
}

// ===== DROPDOWN NAVIGATION =====
const dropdownToggles = document.querySelectorAll('.nav__dropdown-toggle');

dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        e.preventDefault();
        
        // For mobile view
        if (window.innerWidth <= 768) {
            const dropdown = toggle.closest('.nav__dropdown');
            const isActive = dropdown.classList.contains('active');
            
            // Close all other dropdowns
            document.querySelectorAll('.nav__dropdown.active').forEach(activeDropdown => {
                if (activeDropdown !== dropdown) {
                    activeDropdown.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active', !isActive);
        }
    });
});

// Close dropdown when clicking on dropdown links in mobile
const dropdownLinks = document.querySelectorAll('.nav__dropdown-link');
dropdownLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            // Close mobile menu
            navMenu.classList.remove('show');
            navToggle.classList.remove('active');
            
            // Close all dropdowns
            document.querySelectorAll('.nav__dropdown.active').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
});

// Handle window resize to reset mobile dropdown states
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        // Reset mobile dropdown states on desktop
        document.querySelectorAll('.nav__dropdown.active').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});

// ===== NEWSLETTER FORM =====
const newsletterForm = document.querySelector('.newsletter__form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = e.target.querySelector('.newsletter__input').value;
        
        if (email) {
            // Here you would typically send the email to your backend
            // For now, we'll just show an alert
            alert('Thank you for subscribing! We\'ll keep you updated with the latest trends.');
            e.target.querySelector('.newsletter__input').value = '';
        }
    });
}

// ===== SMOOTH SCROLLING FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== LAZY LOADING IMAGES =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== SCROLL TO TOP BUTTON =====
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '↑';
scrollToTopBtn.className = 'scroll-to-top';
scrollToTopBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: white;
    border: none;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
    box-shadow: var(--shadow);
`;

document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTopBtn.style.opacity = '1';
        scrollToTopBtn.style.visibility = 'visible';
    } else {
        scrollToTopBtn.style.opacity = '0';
        scrollToTopBtn.style.visibility = 'hidden';
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===== READING PROGRESS BAR =====
function createReadingProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background-color: var(--accent-color);
        z-index: 1001;
        transition: width 0.1s ease;
    `;
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

// Only add reading progress bar on article pages
if (document.querySelector('.article-content')) {
    createReadingProgressBar();
}

// ===== SEARCH FUNCTIONALITY =====
// Search functionality is now handled in articles.js

// ===== PERFORMANCE OPTIMIZATION =====
// Preload critical resources
function preloadCriticalResources() {
    const criticalImages = document.querySelectorAll('img[data-preload="true"]');
    criticalImages.forEach(img => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = img.src;
        document.head.appendChild(link);
    });
}

// Call on page load
window.addEventListener('load', preloadCriticalResources);

// ===== ANALYTICS HELPER =====
function trackEvent(eventName, eventData = {}) {
    // Google Analytics 4 event tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    }
    
    // You can also add other analytics services here
    console.log('Event tracked:', eventName, eventData);
}

// Track newsletter signups
if (newsletterForm) {
    newsletterForm.addEventListener('submit', () => {
        trackEvent('newsletter_signup', {
            event_category: 'engagement',
            event_label: 'newsletter'
        });
    });
}

// Track article clicks
document.querySelectorAll('.article-card__link, .article-card__title a').forEach(link => {
    link.addEventListener('click', (e) => {
        trackEvent('article_click', {
            event_category: 'content',
            event_label: e.target.textContent.trim(),
            value: 1
        });
    });
});

// ===== ACCESSIBILITY ENHANCEMENTS =====
// Skip to main content link
function addSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-color);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
        transition: top 0.3s;
    `;
    
    skipLink.addEventListener('focus', () => {
        skipLink.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Add skip link on page load
document.addEventListener('DOMContentLoaded', addSkipLink);

// ===== ERROR HANDLING =====
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    // You could send this to an error tracking service
});

// ===== SERVICE WORKER REGISTRATION =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/js/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// ===== MOBILE OPTIMIZATIONS =====
// Prevent zoom on input focus for iOS
if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
    document.querySelectorAll('input, textarea, select').forEach(input => {
        input.addEventListener('focus', () => {
            input.style.fontSize = '16px';
        });
        input.addEventListener('blur', () => {
            input.style.fontSize = '';
        });
    });
}

// Improve mobile scroll performance
let ticking = false;
function updateScrollPosition() {
    // Any scroll-related updates here
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateScrollPosition);
        ticking = true;
    }
});

// Add passive event listeners for better performance
const addPassiveEventListener = (element, event, handler) => {
    element.addEventListener(event, handler, { passive: true });
};

// Use passive listeners for scroll and touch events
document.querySelectorAll('.article-card').forEach(card => {
    addPassiveEventListener(card, 'touchstart', () => {});
});

// Optimize images for mobile
function optimizeImagesForMobile() {
    if (window.innerWidth <= 768) {
        document.querySelectorAll('img').forEach(img => {
            // Add loading="lazy" if not already present
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }
            
            // Add decoding="async" for better performance
            img.setAttribute('decoding', 'async');
        });
    }
}

// Run on load and resize
window.addEventListener('load', optimizeImagesForMobile);
window.addEventListener('resize', optimizeImagesForMobile);