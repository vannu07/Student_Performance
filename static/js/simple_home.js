/**
 * Simple Home JavaScript - Student Performance Predictor
 * Handles form validation, progress tracking, and UI interactions
 */

class SimpleHomeApp {
    constructor() {
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupApp());
        } else {
            this.setupApp();
        }
    }

    setupApp() {
        console.log('🎓 Student Performance Predictor - Simple Home Initialized');
        
        // Get DOM elements
        this.form = document.getElementById('predictionForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.steps = document.querySelectorAll('.step');
        
        // Required form fields
        this.requiredFields = [
            'gender', 
            'ethnicity', 
            'parental_level_of_education', 
            'lunch', 
            'test_preparation_course', 
            'reading_score', 
            'writing_score'
        ];

        // Setup functionality
        this.setupFormValidation();
        this.setupProgressTracking();
        this.setupFormSubmission();
        this.setupResultsScrolling();
        
        // Initial progress check
        this.updateProgress();
    }

    /**
     * Setup form validation with real-time feedback
     */
    setupFormValidation() {
        // Add event listeners to all form fields
        this.requiredFields.forEach(fieldName => {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (field) {
                // Real-time validation
                field.addEventListener('input', () => this.updateProgress());
                field.addEventListener('change', () => this.updateProgress());
                
                // Individual field validation
                field.addEventListener('blur', () => this.validateField(field));
                field.addEventListener('focus', () => this.clearFieldError(field));
            }
        });
    }

    /**
     * Validate individual field
     */
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Check if required field is empty
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }
        
        // Validate number fields
        if (field.type === 'number' && value) {
            const num = parseFloat(value);
            const min = parseFloat(field.min) || 0;
            const max = parseFloat(field.max) || 100;
            
            if (isNaN(num)) {
                isValid = false;
                errorMessage = 'Please enter a valid number';
            } else if (num < min || num > max) {
                isValid = false;
                errorMessage = `Score must be between ${min} and ${max}`;
            }
        }

        // Apply validation styling
        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    }

    /**
     * Show field validation feedback
     */
    showFieldValidation(field, isValid, errorMessage) {
        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        // Add appropriate class
        if (field.value.trim()) {
            field.classList.add(isValid ? 'is-valid' : 'is-invalid');
        }

        // Show/hide error message
        if (!isValid && errorMessage) {
            this.showFieldError(field, errorMessage);
        } else {
            this.clearFieldError(field);
        }
    }

    /**
     * Show field error message
     */
    showFieldError(field, message) {
        // Remove existing error
        this.clearFieldError(field);

        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.color = '#dc3545';
        errorDiv.style.marginTop = '0.25rem';

        // Insert after field
        field.parentNode.appendChild(errorDiv);
    }

    /**
     * Clear field error message
     */
    clearFieldError(field) {
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    }

    /**
     * Setup progress tracking and step indicators
     */
    setupProgressTracking() {
        // Create progress elements if they don't exist
        if (!this.progressFill) {
            this.createProgressBar();
        }
    }

    /**
     * Create progress bar if it doesn't exist
     */
    createProgressBar() {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container mt-3';
        progressContainer.innerHTML = `
            <div class="progress-bar-custom">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="text-center mt-2">
                <small id="progressText" class="text-muted">0% Complete</small>
            </div>
        `;

        // Insert before submit button
        if (this.submitBtn) {
            this.submitBtn.parentNode.insertBefore(progressContainer, this.submitBtn);
            this.progressFill = document.getElementById('progressFill');
            this.progressText = document.getElementById('progressText');
        }
    }

    /**
     * Update progress based on filled fields
     */
    updateProgress() {
        let filledFields = 0;
        
        this.requiredFields.forEach(fieldName => {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (field && field.value.trim() !== '') {
                filledFields++;
            }
        });
        
        const progress = (filledFields / this.requiredFields.length) * 100;
        
        // Update progress bar
        if (this.progressFill) {
            this.progressFill.style.width = progress + '%';
        }
        
        // Update progress text
        if (this.progressText) {
            this.progressText.textContent = Math.round(progress) + '% Complete';
        }
        
        // Update step indicators
        this.updateSteps(progress);
        
        // Update submit button
        this.updateSubmitButton(progress);
    }

    /**
     * Update step indicators
     */
    updateSteps(progress) {
        if (!this.steps.length) return;

        const currentStep = Math.floor((progress / 100) * 3);
        
        this.steps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
            
            if (index < currentStep) {
                step.classList.add('completed');
            } else if (index === currentStep && progress > 0) {
                step.classList.add('active');
            }
        });
    }

    /**
     * Update submit button state
     */
    updateSubmitButton(progress) {
        if (!this.submitBtn) return;

        const isComplete = progress >= 100;
        this.submitBtn.disabled = !isComplete;
        
        if (isComplete) {
            this.submitBtn.innerHTML = '<i class="fas fa-magic"></i> Predict Math Score';
            this.submitBtn.className = 'btn btn-predict';
        } else {
            this.submitBtn.innerHTML = '<i class="fas fa-lock"></i> Complete all fields first';
            this.submitBtn.className = 'btn btn-predict disabled';
        }
    }

    /**
     * Setup form submission handling
     */
    setupFormSubmission() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => {
            // Validate all fields before submission
            let isFormValid = true;
            
            this.requiredFields.forEach(fieldName => {
                const field = document.querySelector(`[name="${fieldName}"]`);
                if (field && !this.validateField(field)) {
                    isFormValid = false;
                }
            });

            if (!isFormValid) {
                e.preventDefault();
                this.showFormError('Please fix the errors above before submitting.');
                return;
            }

            // Show loading state
            if (!this.submitBtn.disabled) {
                this.showLoadingState();
            }
        });
    }

    /**
     * Show form-level error message
     */
    showFormError(message) {
        // Remove existing error
        const existingError = this.form.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }

        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger form-error mt-3';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;

        // Insert before submit button
        this.submitBtn.parentNode.insertBefore(errorDiv, this.submitBtn);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    /**
     * Show loading state during form submission
     */
    showLoadingState() {
        if (!this.submitBtn) return;

        this.submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Predicting...';
        this.submitBtn.disabled = true;
        this.submitBtn.style.opacity = '0.7';
    }

    /**
     * Setup smooth scrolling to results
     */
    setupResultsScrolling() {
        // This will be called by the template if results exist
        window.scrollToResults = () => {
            setTimeout(() => {
                const resultCard = document.querySelector('.result-card');
                if (resultCard) {
                    resultCard.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }
            }, 100);
        };
    }

    /**
     * Utility method to show notifications
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.innerHTML = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the app
const simpleHomeApp = new SimpleHomeApp();

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SimpleHomeApp;
}