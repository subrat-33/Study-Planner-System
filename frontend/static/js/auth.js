// Authentication Handlers

async function handleLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await api.post('/auth/login', { email, password });
        
        auth.saveToken(response.access_token);
        auth.saveUser(response.user);
        
        showToast('Login successful! Redirecting...');
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 1000);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleRegister() {
    const fullName = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }

    try {
        await api.post('/auth/register', {
            full_name: fullName,
            email: email,
            password: password
        });
        
        showToast('Account created! You can now login.');
        setTimeout(() => {
            window.location.href = '/login';
        }, 1500);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Hook up register form if on register page
document.addEventListener('DOMContentLoaded', () => {
    const regForm = document.getElementById('register-form');
    if (regForm) {
        regForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleRegister();
        });
    }
});
