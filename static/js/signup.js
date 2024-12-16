// signup.js (for signup functionality)
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.querySelector('.signup-form');
    
    if (signupForm) {
        // Email validation
        signupForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value;
            const confirmEmail = document.getElementById('confirm_email').value;
            
            if (email !== confirmEmail) {
                e.preventDefault();
                alert('Email addresses do not match!');
            }
        });

        // Password visibility toggle
        const togglePassword = document.querySelector('.toggle-password');
        if (togglePassword) {
            togglePassword.addEventListener('click', function() {
                const passwordInput = document.getElementById('password');
                const icon = this;
                
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                }
            });
        }
    }
});