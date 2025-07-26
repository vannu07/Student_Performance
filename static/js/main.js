// Simple and Clean JavaScript for Student Performance Predictor

class StudentPredictorApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupAnimations();
    }

    init() {
        console.log('🚀 Student Predictor App Initialized');
        this.setupNavbarScroll();
        this.setupSmoothScrolling();
    }

    // Navbar scroll effect
    setupNavbarScroll() {
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
        });
    }

    // Smooth scrolling for anchor links
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Form validation with visual feedback
    setupFormValidation() {
        const form = document.querySelector('#predictionForm');
        if (!form) return;

        const inputs = form.querySelectorAll('input, select');
        
        // Real-time validation
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
                this.showFormErrors();
            } else {
                this.showLoadingState();
            }
        });
    }

    // Validate individual field
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Clear previous validation
        field.classList.remove('is-valid', 'is-invalid');
        this.clearFieldError(field);

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }
        // Number field validation
        else if (field.type === 'number' && value) {
            const num = parseFloat(value);
            const min = parseFloat(field.min) || 0;
            const max = parseFloat(field.max) || 100;
            
            if (isNaN(num)) {
                isValid = false;
                message = 'Please enter a valid number';
            } else if (num < min || num > max) {
                isValid = false;
                message = `Score must be between ${min} and ${max}`;
            }
        }

        // Apply validation styling
        if (value) { // Only show validation if field has content
            field.classList.add(isValid ? 'is-valid' : 'is-invalid');
            if (!isValid) {
                this.showFieldError(field, message);
            }
        }

        return isValid;
    }

    // Show field error message
    showFieldError(field, message) {
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
    }

    // Clear field error
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    // Validate entire form
    validateForm(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Show form validation errors
    showFormErrors() {
        const invalidFields = document.querySelectorAll('.is-invalid');
        
        if (invalidFields.length > 0) {
            // Scroll to first invalid field
            invalidFields[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            
            // Focus on first invalid field
            invalidFields[0].focus();
            
            // Show error message
            this.showNotification('Please fill in all required fields correctly', 'error');
        }
    }

    // Show loading state during form submission
    showLoadingState() {
        const submitBtn = document.querySelector('#submitBtn');
        if (!submitBtn) return;

        // Create loading overlay
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay show';
        loadingOverlay.innerHTML = `
            <div class="text-center">
                <div class="loading-spinner mb-3"></div>
                <h5>Processing your request...</h5>
                <p class="text-muted">Our AI is analyzing the student data</p>
            </div>
        `;
        document.body.appendChild(loadingOverlay);

        // Disable submit button
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div>Processing...';
        submitBtn.disabled = true;

        // Remove loading state after form submission (handled by server)
        // This is just for visual feedback during the request
    }

    // Show notification messages
    showNotification(message, type = 'info') {
        const alertClass = type === 'error' ? 'alert-danger' : 'alert-info';
        
        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Setup scroll animations
    setupAnimations() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.fade-in, .slide-up').forEach(el => {
            observer.observe(el);
        });

        // Add fade-in class to cards and sections
        document.querySelectorAll('.feature-card, .step-card, .info-card').forEach(el => {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    }

    // Setup event listeners
    setupEventListeners() {
        // Form field focus effects
        document.querySelectorAll('.form-control, .form-select').forEach(field => {
            field.addEventListener('focus', () => {
                field.parentNode.classList.add('focused');
            });
            
            field.addEventListener('blur', () => {
                field.parentNode.classList.remove('focused');
            });
        });

        // Button hover effects
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });

        // Card hover effects
        document.querySelectorAll('.feature-card, .info-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    // Utility function to format numbers
    formatNumber(num, decimals = 1) {
        return parseFloat(num).toFixed(decimals);
    }

    // Utility function to get performance level
    getPerformanceLevel(score) {
        if (score >= 90) return { level: 'Excellent', color: 'success' };
        if (score >= 80) return { level: 'Very Good', color: 'info' };
        if (score >= 70) return { level: 'Good', color: 'primary' };
        if (score >= 60) return { level: 'Average', color: 'warning' };
        return { level: 'Needs Improvement', color: 'danger' };
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentPredictorApp();
});

// Additional utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Form auto-save functionality (optional)
function setupAutoSave() {
    const form = document.querySelector('#predictionForm');
    if (!form) return;

    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            localStorage.setItem('studentFormData', JSON.stringify(data));
        });
    });

    // Load saved data
    const savedData = localStorage.getItem('studentFormData');
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && data[key]) {
                field.value = data[key];
            }
        });
    }
}

// Initialize auto-save
document.addEventListener('DOMContentLoaded', setupAutoSave);