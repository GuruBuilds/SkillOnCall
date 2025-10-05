// Mobile menu toggle
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');
const navButtons = document.querySelector('.nav-buttons');

mobileMenuBtn.addEventListener('click', () => {
    const isOpen = navLinks.style.display === 'flex';
    
    if (isOpen) {
        navLinks.style.display = 'none';
        navButtons.style.display = 'none';
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
    } else {
        navLinks.style.display = 'flex';
        navButtons.style.display = 'flex';
        mobileMenuBtn.innerHTML = '<i class="fas fa-times"></i>';
        
        // Stack vertically on mobile
        if (window.innerWidth <= 768) {
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '80px';
            navLinks.style.left = '0';
            navLinks.style.width = '100%';
            navLinks.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
            navLinks.style.padding = '2rem';
            navLinks.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
            
            navButtons.style.flexDirection = 'column';
            navButtons.style.position = 'absolute';
            navButtons.style.top = 'calc(80px + 240px)';
            navButtons.style.left = '2rem';
            navButtons.style.gap = '1rem';
            
            // Change link colors for mobile menu
            document.querySelectorAll('.nav-links a').forEach(link => {
                link.style.color = '#263238';
            });
        }
    }
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            navLinks.style.display = 'none';
            navButtons.style.display = 'none';
            mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Close mobile menu if open
            if (window.innerWidth <= 768 && navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
                navButtons.style.display = 'none';
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            }
        }
    });
});

// Initialize Swiper sliders
const professionalSwiper = new Swiper('.professionals .swiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    pagination: {
        el: '.professionals .swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        640: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    }
});

const testimonialSwiper = new Swiper('.testimonials .swiper', {
    slidesPerView: 1,
    spaceBetween: 30,
    pagination: {
        el: '.testimonials .swiper-pagination',
        clickable: true,
    },
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
});

// Animate elements when scrolling
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.service-card, .step, .professional-card');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        
        if (elementPosition < screenPosition) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

// Set initial state for animated elements
document.querySelectorAll('.service-card, .step, .professional-card').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
});

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);
