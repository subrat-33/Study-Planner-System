// Global Main Script

document.addEventListener('DOMContentLoaded', () => {
    // 1. Highlight active navigation link
    const path = window.location.pathname;
    const navItems = {
        '/dashboard': 'nav-dashboard',
        '/subjects': 'nav-subjects',
        '/schedule': 'nav-schedule',
        '/progress': 'nav-progress',
        '/analytics': 'nav-analytics'
    };
    
    const activeId = navItems[path];
    if (activeId) {
        document.getElementById(activeId)?.classList.add('active');
    }

    // 2. Check Authentication (except on login/register pages)
    const publicPages = ['/login', '/register', '/'];
    if (!publicPages.includes(path) && !auth.isAuthenticated()) {
        window.location.href = '/login';
        return;
    }

    // 3. Setup User Profile & Initials
    updateNavbarProfile();
    refreshUserData();

    // 4. Logout Handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            auth.logout();
        });
    }

    // 5. Populate Current Date/Time
    updateDateTime();
    setInterval(updateDateTime, 60000);

    // 6. Load Notifications
    loadNotificationsCount();

    // 7. Mobile Menu Toggle
    setupMobileMenu();
});

function setupMobileMenu() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const mobileNav = document.getElementById('mobile-nav');
    const closeBtn = document.getElementById('close-menu');
    
    if (!toggle || !mobileNav) return;

    // Create overlay if it doesn't exist
    let overlay = document.querySelector('.mobile-nav-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'mobile-nav-overlay';
        document.body.appendChild(overlay);
    }

    const openMenu = () => {
        mobileNav.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scroll
    };

    const closeMenu = () => {
        mobileNav.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = ''; // Restore scroll
    };

    toggle.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);

    // Close on link click
    mobileNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Handle logout link in mobile menu
    const logoutLink = mobileNav.querySelector('.logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            auth.logout();
        });
    }
}

function updateNavbarProfile() {
    const user = auth.getUser();
    if (user) {
        const initialEl = document.getElementById('user-initials');
        const nameEl = document.getElementById('user-name');
        const avatarContainer = document.getElementById('user-avatar-container');
        
        if (avatarContainer) {
            if (user.profile_picture_url) {
                avatarContainer.innerHTML = `<img src="${user.profile_picture_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: inherit;">`;
            } else if (initialEl) {
                const initials = user.full_name.split(' ').map(n => n[0]).join('').toUpperCase();
                initialEl.innerText = initials;
            }
        }
        
        if (nameEl) {
            nameEl.innerText = user.full_name;
        }
    }
}

async function refreshUserData() {
    if (!auth.isAuthenticated()) return;
    
    try {
        const user = await api.get('/user/profile');
        if (user) {
            auth.saveUser(user);
            updateNavbarProfile();
        }
    } catch (error) {
        console.error('Failed to refresh user data:', error);
    }
}

async function loadNotificationsCount() {
    if (!auth.isAuthenticated()) return;
    
    try {
        const data = await api.get('/notifications/total-count');
        const count = data.count || 0;
        const badge = document.getElementById('notification-count');
        
        if (badge) {
            if (count > 0) {
                badge.innerText = count > 99 ? '99+' : count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Failed to load notification count:', error);
    }
}

function updateDateTime() {
    const el = document.getElementById('current-date-time');
    if (el) {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        el.innerText = now.toLocaleDateString('en-US', options);
    }
}

// Global Toast Notification System
window.showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type} flex align-center gap-md`;
    
    const icon = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle');
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Fade in
    setTimeout(() => toast.classList.add('active'), 10);

    // Remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('active');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
};

// CSS for toasts (in case it wasn't in components.css)
const toastStyles = `
.toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.toast {
    background: white;
    padding: 16px 24px;
    border-radius: 8px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    min-width: 300px;
    border-left: 4px solid var(--primary);
    transform: translateX(120%);
    transition: transform 0.3s ease;
}
.toast.active { transform: translateX(0); }
.toast-success { border-left-color: var(--success); }
.toast-error { border-left-color: var(--danger); }
`;
const styleSheet = document.createElement("style");
styleSheet.innerText = toastStyles;
document.head.appendChild(styleSheet);
