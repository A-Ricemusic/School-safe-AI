// static/js/login.js
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.querySelector('.toggle-password');
    
    // Password visibility toggle
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            }
        });
    }

    // Form validation
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            const errors = [];

            // Email validation
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailInput.value)) {
                isValid = false;
                errors.push('Please enter a valid email address');
                emailInput.classList.add('error');
            } else {
                emailInput.classList.remove('error');
            }

            // Password validation
            if (passwordInput.value.length < 6) {
                isValid = false;
                errors.push('Password must be at least 6 characters long');
                passwordInput.classList.add('error');
            } else {
                passwordInput.classList.remove('error');
            }

            // If there are errors, prevent form submission and show errors
            if (!isValid) {
                e.preventDefault();
                showErrors(errors);
            }
        });
    }

    // Show error messages
    function showErrors(errors) {
        // Remove existing flash messages
        const existingFlashes = document.querySelector('.flash-messages');
        if (existingFlashes) {
            existingFlashes.remove();
        }

        // Create new flash messages container
        const flashMessages = document.createElement('div');
        flashMessages.className = 'flash-messages';

        errors.forEach(error => {
            const flashMessage = document.createElement('div');
            flashMessage.className = 'flash-message';
            flashMessage.innerHTML = `
                <i class="fas fa-exclamation-circle"></i>
                ${error}
            `;
            flashMessages.appendChild(flashMessage);
        });

        // Insert flash messages after the header
        const loginHeader = document.querySelector('.login-header');
        loginHeader.insertAdjacentElement('afterend', flashMessages);
    }

    // Input focus effects
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        // Add focus effect to input group
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            // Validate on blur
            validateInput(this);
        });

        // Real-time validation as user types
        input.addEventListener('input', function() {
            validateInput(this);
        });
    });

    // Input validation
    function validateInput(input) {
        if (input.type === 'email') {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(input.value) && input.value !== '') {
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        }

        if (input.type === 'password') {
            if (input.value.length < 6 && input.value !== '') {
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        }
    }

    // Remember email functionality
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail && emailInput) {
        emailInput.value = rememberedEmail;
    }

    // Save email when form is submitted
    if (loginForm) {
        loginForm.addEventListener('submit', function() {
            if (emailInput.value) {
                localStorage.setItem('rememberedEmail', emailInput.value);
            }
        });
    }

    // Add loading state to submit button
    const submitBtn = document.querySelector('.submit-btn');
    if (submitBtn) {
        loginForm.addEventListener('submit', function() {
            submitBtn.innerHTML = `
                <span>Logging in...</span>
                <i class="fas fa-spinner fa-spin"></i>
            `;
            submitBtn.disabled = true;
        });
    }
});