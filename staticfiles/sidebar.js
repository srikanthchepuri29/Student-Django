// Sidebar Common JS Library - Handles Theme, Profile Sync and Submenus

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initThemeAndProfile() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedColor = localStorage.getItem('accentColor') || '#3b82f6';
    const savedHover = localStorage.getItem('accentHover') || '#2563eb';

    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.style.setProperty('--sidebar-border', savedColor);
    document.documentElement.style.setProperty('--sidebar-active-bg', savedColor + '1a');
    document.documentElement.style.setProperty('--primary-color', savedColor);
    document.documentElement.style.setProperty('--primary-hover', savedHover);

    // Sync admin details from local storage or defaults
    const adminName = localStorage.getItem('adminName') || 'Admin';
    const adminAvatar = localStorage.getItem('adminAvatar') || 'srikanth.png';

    const nameEl = document.querySelector('.admin span');
    const avatarEl = document.querySelector('.admin img');
    if (nameEl) nameEl.textContent = adminName;
    if (avatarEl) {
        avatarEl.src = adminAvatar.startsWith('data:') ? adminAvatar : '/srikanth.png';
    }
}

function initSubmenus() {
    const toggles = document.querySelectorAll('.submenu-toggle');
    toggles.forEach(toggle => {
        const parent = toggle.parentElement;
        const submenu = parent.querySelector('.submenu');
        if (!submenu) return;
        
        // Determine if any link inside is the active page
        const currentPath = window.location.pathname;
        const subLinks = submenu.querySelectorAll('a');
        let shouldBeOpen = false;
        
        subLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href)) {
                link.parentElement.classList.add('active');
                shouldBeOpen = true;
            }
        });
        
        if (shouldBeOpen) {
            parent.classList.add('open');
            submenu.style.display = 'flex';
            submenu.style.flexDirection = 'column';
        } else {
            parent.classList.remove('open');
            submenu.style.display = 'none';
        }
        
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const isOpen = parent.classList.contains('open');
            if (isOpen) {
                parent.classList.remove('open');
                submenu.style.display = 'none';
            } else {
                parent.classList.add('open');
                submenu.style.display = 'flex';
                submenu.style.flexDirection = 'column';
            }
        });
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initThemeAndProfile();
    initSubmenus();
    
    // Fetch fresh profile data to update local cache
    fetch('/api/profile/')
        .then(res => {
            if (res.ok) return res.json();
        })
        .then(profile => {
            if (profile) {
                localStorage.setItem('adminName', profile.admin_name);
                localStorage.setItem('adminEmail', profile.admin_email);
                localStorage.setItem('adminAvatar', profile.admin_avatar);
                
                const nameEl = document.querySelector('.admin span');
                const avatarEl = document.querySelector('.admin img');
                if (nameEl) nameEl.textContent = profile.admin_name;
                if (avatarEl) {
                    avatarEl.src = profile.admin_avatar.startsWith('data:') ? profile.admin_avatar : '/srikanth.png';
                }
            }
        })
        .catch(err => console.error("Error fetching profile:", err));
});
