// Advanced JavaScript for Student Performance ML Project
// Modern ES6+ with animations, 3D effects, and interactive features

class StudentPerformanceApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupScrollAnimations();
        this.setupFormValidation();
        this.setupThemeToggle();
    }

    init() {
        console.log('🚀 Student Performance ML App Initialized');
        this.setupLoadingAnimation();
        this.setupCounterAnimations();
        this.setup3DEffects();
    }

    // Particle System
    createParticles() {
        // Particle system removed for a cleaner professional look.
    }

    createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random positioning and animation
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        particle.style.animationDelay = Math.random() * 2 + 's';
        
        container.appendChild(particle);

        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 8000);
    }

    // Scroll Animations
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Trigger counter animation for metrics
                    if (entry.target.classList.contains('metric-card')) {
                        this.animateCounter(entry.target);
                    }
                }
            });
        }, observerOptions);

        // Observe all fade-in elements
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });

        // Observe metric cards
        document.querySelectorAll('.metric-card').forEach(el => {
            observer.observe(el);
        });
    }

    // Counter Animation
    animateCounter(element) {
        const valueElement = element.querySelector('.metric-value');
        if (!valueElement || valueElement.dataset.animated) return;

        const finalValue = parseFloat(valueElement.textContent);
        const duration = 2000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutCubic = 1 - Math.pow(1 - progress, 3);
            const currentValue = finalValue * easeOutCubic;
            
            if (valueElement.textContent.includes('%')) {
                valueElement.textContent = Math.round(currentValue) + '%';
            } else if (valueElement.textContent.includes('.')) {
                valueElement.textContent = currentValue.toFixed(2);
            } else {
                valueElement.textContent = Math.round(currentValue);
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                valueElement.dataset.animated = 'true';
            }
        };

        requestAnimationFrame(animate);
    }

    // 3D Effects Setup
    setup3DEffects() {
        // 3D interactive card effects removed for a more minimal/professional UI.
    }

    // Form Validation with Visual Feedback
    setupFormValidation() {
        const form = document.querySelector('form');
        if (!form) return;

        const inputs = form.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearValidation(input));
        });

        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
                this.showFormErrors();
            } else {
                this.showLoadingState();
            }
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Remove existing validation classes
        field.classList.remove('valid', 'invalid');

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        } else if (field.type === 'number') {
            const num = parseFloat(value);
            const min = parseFloat(field.min) || 0;
            const max = parseFloat(field.max) || 100;
            
            if (isNaN(num) || num < min || num > max) {
                isValid = false;
                message = `Please enter a number between ${min} and ${max}`;
            }
        }

        // Apply validation styling
        field.classList.add(isValid ? 'valid' : 'invalid');
        
        // Show/hide error message
        this.showFieldError(field, isValid ? '' : message);
        
        return isValid;
    }

    showFieldError(field, message) {
        let errorElement = field.parentNode.querySelector('.field-error');
        
        if (message) {
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'field-error';
                field.parentNode.appendChild(errorElement);
            }
            errorElement.textContent = message;
            errorElement.style.opacity = '1';
        } else if (errorElement) {
            errorElement.style.opacity = '0';
            setTimeout(() => {
                if (errorElement.parentNode) {
                    errorElement.parentNode.removeChild(errorElement);
                }
            }, 300);
        }
    }

    clearValidation(field) {
        field.classList.remove('invalid');
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.style.opacity = '0';
        }
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    showFormErrors() {
        // Shake animation for invalid fields
        const invalidFields = document.querySelectorAll('.invalid');
        invalidFields.forEach(field => {
            field.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                field.style.animation = '';
            }, 500);
        });
    }

    // Loading State Management
    showLoadingState() {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        const originalText = submitBtn.textContent;
        submitBtn.innerHTML = '<div class="loading-spinner"></div> Processing...';
        submitBtn.disabled = true;

        // Simulate processing time (remove this in production)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 3000);
    }

    // Theme Toggle (Dark/Light Mode)
    setupThemeToggle() {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = '🌙';
        themeToggle.setAttribute('aria-label', 'Toggle dark mode');
        
        document.body.appendChild(themeToggle);

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            themeToggle.innerHTML = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
            
            // Save preference
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
        });

        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.innerHTML = '☀️';
        }
    }

    // Loading Animation
    setupLoadingAnimation() {
        // Page load animation
        window.addEventListener('load', () => {
            const loader = document.querySelector('.page-loader');
            if (loader) {
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                }, 500);
            }

            // Animate elements on load
            this.animateOnLoad();
        });
    }

    animateOnLoad() {
        const elements = document.querySelectorAll('.hero-title, .hero-subtitle, .feature-card');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(50px)';
            
            setTimeout(() => {
                el.style.transition = 'all 0.8s ease-out';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    // Counter Animations for Statistics
    setupCounterAnimations() {
        const counters = document.querySelectorAll('[data-counter]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-counter'));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            // Start counter when element is visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        updateCounter();
                        observer.unobserve(entry.target);
                    }
                });
            });

            observer.observe(counter);
        });
    }

    // Event Listeners
    setupEventListeners() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
        });

        // Button click effects
        document.addEventListener('click', (e) => {
            // support both legacy `.btn-3d` and new `.btn-modern` buttons
            const btn = e.target.closest('.btn-3d, .btn-modern');
            if (btn) {
                // pass the button and mouse coordinates for ripple positioning
                this.createRippleEffect(btn, e.clientX, e.clientY);
            }
        });

        // Form input focus effects
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('focus', () => {
                input.parentNode.classList.add('focused');
            });

            input.addEventListener('blur', () => {
                input.parentNode.classList.remove('focused');
            });
        });
    }

    // Ripple Effect for Buttons
    createRippleEffect(button, clientX, clientY) {
        if (!button) return;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = (clientX || (rect.left + rect.width / 2)) - rect.left - size / 2;
        const y = (clientY || (rect.top + rect.height / 2)) - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        // ensure button has position relative for ripple placement
        if (getComputedStyle(button).position === 'static') {
            button.style.position = 'relative';
        }

        button.appendChild(ripple);

        setTimeout(() => {
            if (ripple && ripple.parentNode) ripple.remove();
        }, 600);
    }

    // Prediction Result Animation
    animatePredictionResult(score) {
        const resultContainer = document.querySelector('.result-display');
        if (!resultContainer) return;

        // Create animated score display
        const scoreElement = resultContainer.querySelector('.result-score');
        if (scoreElement) {
            let currentScore = 0;
            const targetScore = parseFloat(score);
            const duration = 2000;
            const increment = targetScore / (duration / 16);

            const animateScore = () => {
                currentScore += increment;
                if (currentScore < targetScore) {
                    scoreElement.textContent = currentScore.toFixed(1);
                    requestAnimationFrame(animateScore);
                } else {
                    scoreElement.textContent = targetScore.toFixed(2);
                    
                    // Add celebration effect
                    this.celebratePrediction();
                }
            };

            animateScore();
        }
    }

    // Celebration Animation
    celebratePrediction() {
        // Disabled confetti celebration for a professional presentation.
    }

    createConfetti() {
        // Confetti removed.
    }

    getRandomColor() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
}

// Utility Functions
const utils = {
    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Throttle function for scroll events
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Format numbers with animations
    formatNumber(num, decimals = 0) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(num);
    }
};

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentPerformanceApp();
});

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .shake {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    .field-error {
        color: #ff6b6b;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .form-control.valid {
        border-color: #4ecdc4;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1);
    }

    .form-control.invalid {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
    }

    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
        cursor: pointer;
        z-index: 1001;
        transition: var(--transition);
        backdrop-filter: blur(10px);
    }

    .theme-toggle:hover {
        transform: scale(1.1) rotate(15deg);
    }

    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #ff6b6b;
        animation: confetti-fall linear forwards;
        z-index: 1000;
        pointer-events: none;
    }

    @keyframes confetti-fall {
        0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }

    .page-loader {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: opacity 0.5s ease;
    }

    .dark-theme {
        --primary-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --glass-bg: rgba(0, 0, 0, 0.2);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
`;

document.head.appendChild(style);

// Export for use in other scripts
window.StudentPerformanceApp = StudentPerformanceApp;
window.utils = utils;
