// Theme and Accent Loader (Loads and applies saved customizations on page start)
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedColor = localStorage.getItem('accentColor') || '#2563eb';
    const savedHover = localStorage.getItem('accentHover') || '#1d4ed8';

    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.style.setProperty('--sidebar-border', savedColor);
    document.documentElement.style.setProperty('--sidebar-active-bg', savedColor + '1a');
    document.documentElement.style.setProperty('--primary-color', savedColor);
    document.documentElement.style.setProperty('--primary-hover', savedHover);

    // Apply color dots active state on settings load
    const colorDots = document.querySelectorAll('.color-dot');
    colorDots.forEach(dot => {
        if (dot.getAttribute('data-color') === savedColor) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });

    // Sync Dark Mode Switch State
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.checked = (savedTheme === 'dark');
    }
}

// Temporary tracked states for appearance settings
let tempTheme = localStorage.getItem('theme') || 'light';
let tempColor = localStorage.getItem('accentColor') || '#2563eb';
let tempHover = localStorage.getItem('accentHover') || '#1d4ed8';

// Select Dark Mode (temporary track)
function selectDarkTheme(isDark) {
    tempTheme = isDark ? 'dark' : 'light';
}

// Select Accent Color (temporary track)
function selectAccentColor(element) {
    tempColor = element.getAttribute('data-color');
    tempHover = element.getAttribute('data-hover');

    // Update active circle dots visually first
    document.querySelectorAll('.color-dot').forEach(dot => {
        dot.classList.remove('active');
    });
    element.classList.add('active');
}

// Explicitly Apply and Save theme preferences
function applyAppearanceSettings() {
    localStorage.setItem('theme', tempTheme);
    localStorage.setItem('accentColor', tempColor);
    localStorage.setItem('accentHover', tempHover);

    // Apply globally instantly
    initTheme();

    // Log the action in real-time tracker
    logActivity('Appearance Changed', `Accent set to ${tempColor} and Theme set to ${tempTheme.toUpperCase()}`);

    // Premium visual feedback on button
    const btn = document.querySelector('button[onclick="applyAppearanceSettings()"]');
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Theme Applied Successfully! ✓';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 2500);
    }
}

// Base64 Admin Avatar Upload Handler
function initAvatarUpload() {
    const fileInput = document.getElementById('avatarUpload');
    const profileImg = document.getElementById('profileAvatar');
    const topbarImg = document.getElementById('topbarAvatar');

    if (!fileInput) return;

    // Load saved avatar if exists
    const savedAvatar = localStorage.getItem('adminAvatar');
    if (savedAvatar) {
        if (profileImg) profileImg.src = savedAvatar;
        if (topbarImg) topbarImg.src = savedAvatar;
    }

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const base64String = event.target.result;
                localStorage.setItem('adminAvatar', base64String);
                
                if (profileImg) profileImg.src = base64String;
                if (topbarImg) topbarImg.src = base64String;
                
                // Log action
                logActivity('Profile Avatar Updated', 'Uploaded new custom display photo');
                alert('Profile avatar updated successfully!');
            };
            reader.readAsDataURL(file);
        }
    });
}

// Save Admin Profile Details
function saveProfileSettings() {
    const name = document.getElementById('adminName').value.trim();
    const email = document.getElementById('adminEmail').value.trim();

    if (name === '' || email === '') {
        alert('Please enter a valid display name and email address');
        return;
    }

    localStorage.setItem('adminName', name);
    localStorage.setItem('adminEmail', email);

    // Update Topbar UI in real-time
    const topbarName = document.getElementById('topbarAdminName');
    if (topbarName) topbarName.textContent = name;

    // Log action
    logActivity('Profile Saved', `Display name updated to: ${name}`);

    // Premium visual feedback on button
    const btn = document.querySelector('button[onclick="saveProfileSettings()"]');
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Profile Details Updated! ✓';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 2500);
    }
}

// Load saved Profile details on page start
function loadProfileSettings() {
    const savedName = localStorage.getItem('adminName') || 'Admin';
    const savedEmail = localStorage.getItem('adminEmail') || 'admin@gmail.com';

    const nameInput = document.getElementById('adminName');
    const emailInput = document.getElementById('adminEmail');
    const topbarName = document.getElementById('topbarAdminName');

    if (nameInput) nameInput.value = savedName;
    if (emailInput) emailInput.value = savedEmail;
    if (topbarName) topbarName.textContent = savedName;
}

// Save switch selections for notification alerts
function saveNotificationSettings() {
    const email = document.getElementById('emailNotif').checked;
    const student = document.getElementById('studentNotif').checked;
    const digest = document.getElementById('digestNotif').checked;

    localStorage.setItem('notif_email', email);
    localStorage.setItem('notif_student', student);
    localStorage.setItem('notif_digest', digest);

    // Log action
    logActivity('Preferences Saved', 'Updated notification alerts preferences');

    // Premium visual feedback on button
    const btn = document.querySelector('button[onclick="saveNotificationSettings()"]');
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Preferences Saved! ✓';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 2500);
    }
}

// Load saved switches on page start
function loadNotificationSettings() {
    const email = localStorage.getItem('notif_email') !== 'false'; // default true
    const student = localStorage.getItem('notif_student') !== 'false'; // default true
    const digest = localStorage.getItem('notif_digest') === 'true'; // default false

    const emailEl = document.getElementById('emailNotif');
    const studentEl = document.getElementById('studentNotif');
    const digestEl = document.getElementById('digestNotif');

    if (emailEl) emailEl.checked = email;
    if (studentEl) studentEl.checked = student;
    if (digestEl) digestEl.checked = digest;
}

// Password Change Handler
function changeAdminPassword() {
    const current = document.getElementById('currentPass').value;
    const newPass = document.getElementById('newPass').value;
    const confirmPass = document.getElementById('confirmPass').value;

    if (current === '' || newPass === '' || confirmPass === '') {
        alert('Please fill out all credentials fields');
        return;
    }

    if (newPass !== confirmPass) {
        alert('Confirm password mismatch! Please verify.');
        return;
    }

    if (newPass.length < 6) {
        alert('Password must be at least 6 characters long');
        return;
    }

    // Save password
    localStorage.setItem('adminPassword', newPass);

    // Clear inputs
    document.getElementById('currentPass').value = '';
    document.getElementById('newPass').value = '';
    document.getElementById('confirmPass').value = '';

    // Log action
    logActivity('Security Updated', 'System administrator password credentials modified');

    // Premium visual feedback on button
    const btn = document.querySelector('button[onclick="changeAdminPassword()"]');
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Security Key Updated! ✓';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 2500);
    }
}

// Extra Premium Feature: Export System Backup Data
function exportSystemData() {
    const students = localStorage.getItem('students');
    const courses = localStorage.getItem('courses');
    const teachers = localStorage.getItem('teachers');
    const theme = localStorage.getItem('theme');
    const accentColor = localStorage.getItem('accentColor');
    const accentHover = localStorage.getItem('accentHover');
    const adminName = localStorage.getItem('adminName');
    const adminEmail = localStorage.getItem('adminEmail');
    const adminAvatar = localStorage.getItem('adminAvatar');

    const state = {
        students: students ? JSON.parse(students) : null,
        courses: courses ? JSON.parse(courses) : null,
        teachers: teachers ? JSON.parse(teachers) : null,
        preferences: {
            theme,
            accentColor,
            accentHover,
            adminName,
            adminEmail,
            adminAvatar
        }
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "student_dashboard_backup.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();

    // Log action
    logActivity('Backup Exported', 'Successfully downloaded student_dashboard_backup.json');

    // Premium visual feedback on button
    const btn = document.querySelector('button[onclick="exportSystemData()"]');
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Data Exported Successfully! ✓';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 2500);
    }
}

// Extra Premium Feature: Import System Backup Data
function importSystemData(input) {
    const file = input.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const state = JSON.parse(e.target.result);
            
            if (state.students) localStorage.setItem('students', JSON.stringify(state.students));
            if (state.courses) localStorage.setItem('courses', JSON.stringify(state.courses));
            if (state.teachers) localStorage.setItem('teachers', JSON.stringify(state.teachers));
            
            if (state.preferences) {
                const pref = state.preferences;
                if (pref.theme) localStorage.setItem('theme', pref.theme);
                if (pref.accentColor) localStorage.setItem('accentColor', pref.accentColor);
                if (pref.accentHover) localStorage.setItem('accentHover', pref.accentHover);
                if (pref.adminName) localStorage.setItem('adminName', pref.adminName);
                if (pref.adminEmail) localStorage.setItem('adminEmail', pref.adminEmail);
                if (pref.adminAvatar) localStorage.setItem('adminAvatar', pref.adminAvatar);
            }

            // Log action before reload
            logActivity('Backup Imported', 'Uploaded and applied new student_dashboard_backup.json system state');
            alert('System Backup successfully imported! Reloading the page to apply changes...');
            window.location.reload();
        } catch(err) {
            alert('Invalid backup file formatting! Please load a valid exported JSON file.');
        }
    };
    reader.readAsText(file);
}

// Extra Premium Feature: Reset Database State
function resetSystemData() {
    const confirmReset = confirm('Are you absolutely sure you want to delete all students, courses, teachers, and customizations? This action is permanent!');
    if (confirmReset) {
        localStorage.clear();
        alert('Database reset to defaults successfully! Reloading...');
        window.location.reload();
    }
}

// Real-time scenario logging utilities
function logActivity(action, details) {
    const logs = JSON.parse(localStorage.getItem('activityLogs')) || [];
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    logs.unshift({ action, details, timestamp });
    
    // Cap at 25 log entries
    if (logs.length > 25) logs.pop();
    
    localStorage.setItem('activityLogs', JSON.stringify(logs));
    renderActivityLogs();
}

function renderActivityLogs() {
    const logList = document.getElementById('activityLogList');
    if (!logList) return;

    const logs = JSON.parse(localStorage.getItem('activityLogs')) || [
        { action: "System Started", details: "Dashboard initialized. Ready to accept student records.", timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }
    ];

    logList.innerHTML = '';
    if (logs.length === 0) {
        logList.innerHTML = '<p style="font-size:12px; color:var(--card-text-secondary); text-align:center; padding: 20px 0;">No activities recorded yet.</p>';
        return;
    }

    logs.forEach(log => {
        const item = document.createElement('div');
        item.style.padding = '10px';
        item.style.borderRadius = '8px';
        item.style.background = 'rgba(0,0,0,0.02)';
        item.style.borderLeft = '4px solid var(--primary-color)';
        item.style.fontSize = '12px';
        item.style.transition = 'all 0.3s';
        
        let icon = '<i class="fa-solid fa-circle-info" style="color:var(--primary-color); margin-right:6px;"></i>';
        if (log.action.includes('Delete')) icon = '<i class="fa-solid fa-trash-can" style="color:#ef4444; margin-right:6px;"></i>';
        if (log.action.includes('Add') || log.action.includes('Register')) icon = '<i class="fa-solid fa-circle-plus" style="color:#10b981; margin-right:6px;"></i>';
        if (log.action.includes('Edit') || log.action.includes('Update') || log.action.includes('Profile') || log.action.includes('Security')) icon = '<i class="fa-solid fa-pen-to-square" style="color:#f59e0b; margin-right:6px;"></i>';
        if (log.action.includes('Backup') || log.action.includes('Appearance') || log.action.includes('Preferences')) icon = '<i class="fa-solid fa-sliders" style="color:#8b5cf6; margin-right:6px;"></i>';

        item.innerHTML = `
            <div style="display:flex; justify-content:space-between; font-weight:600; color:var(--card-text-primary); margin-bottom:4px;">
                <span>${icon}${log.action}</span>
                <span style="font-size:10px; color:var(--card-text-secondary); font-weight:normal;">${log.timestamp}</span>
            </div>
            <div style="color:var(--card-text-secondary); font-size: 11px;">${log.details}</div>
        `;
        logList.appendChild(item);
    });
}

function clearActivityLogs() {
    localStorage.removeItem('activityLogs');
    renderActivityLogs();
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initAvatarUpload();
    loadProfileSettings();
    loadNotificationSettings();
    renderActivityLogs();
});
