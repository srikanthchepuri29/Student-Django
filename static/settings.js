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

// Helper for Django CSRF
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
async function applyAppearanceSettings() {
    localStorage.setItem('theme', tempTheme);
    localStorage.setItem('accentColor', tempColor);
    localStorage.setItem('accentHover', tempHover);

    try {
        const response = await fetch('/api/theme/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                theme: tempTheme,
                accentColor: tempColor,
                accentHover: tempHover
            })
        });

        if (response.ok) {
            initTheme();
            await renderActivityLogs();

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
        } else {
            alert('Failed to save appearance settings to server.');
        }
    } catch (err) {
        console.error(err);
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
            reader.onload = async function(event) {
                const base64String = event.target.result;
                
                try {
                    const response = await fetch('/api/profile/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({ admin_avatar: base64String })
                    });

                    if (response.ok) {
                        localStorage.setItem('adminAvatar', base64String);
                        if (profileImg) profileImg.src = base64String;
                        if (topbarImg) topbarImg.src = base64String;
                        
                        alert('Profile avatar updated successfully!');
                        await renderActivityLogs();
                    } else {
                        alert('Failed to upload avatar to server.');
                    }
                } catch (err) {
                    console.error(err);
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

// Save Admin Profile Details
async function saveProfileSettings() {
    const name = document.getElementById('adminName').value.trim();
    const email = document.getElementById('adminEmail').value.trim();

    if (name === '' || email === '') {
        alert('Please enter a valid display name and email address');
        return;
    }

    try {
        const response = await fetch('/api/profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                admin_name: name,
                admin_email: email
            })
        });

        if (response.ok) {
            localStorage.setItem('adminName', name);
            localStorage.setItem('adminEmail', email);

            // Update Topbar UI in real-time
            const topbarName = document.getElementById('topbarAdminName');
            if (topbarName) topbarName.textContent = name;

            await renderActivityLogs();

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
        } else {
            alert('Failed to update profile details.');
        }
    } catch (err) {
        console.error(err);
    }
}

// Load saved Profile details on page start
async function loadProfileSettings() {
    try {
        const response = await fetch('/api/profile/');
        if (response.ok) {
            const profile = await response.json();
            
            const nameInput = document.getElementById('adminName');
            const emailInput = document.getElementById('adminEmail');
            const topbarName = document.getElementById('topbarAdminName');
            const profileImg = document.getElementById('profileAvatar');
            const topbarImg = document.getElementById('topbarAvatar');

            if (nameInput) nameInput.value = profile.admin_name;
            if (emailInput) emailInput.value = profile.admin_email;
            if (topbarName) topbarName.textContent = profile.admin_name;
            
            if (profile.admin_avatar) {
                localStorage.setItem('adminAvatar', profile.admin_avatar);
                if (profileImg) profileImg.src = profile.admin_avatar;
                if (topbarImg) topbarImg.src = profile.admin_avatar;
            }

            localStorage.setItem('adminName', profile.admin_name);
            localStorage.setItem('adminEmail', profile.admin_email);
        }
    } catch (err) {
        console.error(err);
    }
}

// Save switch selections for notification alerts
async function saveNotificationSettings() {
    const email = document.getElementById('emailNotif').checked;
    const student = document.getElementById('studentNotif').checked;
    const digest = document.getElementById('digestNotif').checked;

    try {
        const response = await fetch('/api/notifications/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ email, student, digest })
        });

        if (response.ok) {
            localStorage.setItem('notif_email', email);
            localStorage.setItem('notif_student', student);
            localStorage.setItem('notif_digest', digest);

            await renderActivityLogs();

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
        } else {
            alert('Failed to save notification preferences.');
        }
    } catch (err) {
        console.error(err);
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
async function changeAdminPassword() {
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

    try {
        const response = await fetch('/api/change-password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ current, newPass })
        });

        if (response.ok) {
            // Clear inputs
            document.getElementById('currentPass').value = '';
            document.getElementById('newPass').value = '';
            document.getElementById('confirmPass').value = '';

            await renderActivityLogs();

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
        } else {
            const err = await response.json();
            alert(err.error || 'Failed to update credentials.');
        }
    } catch (err) {
        console.error(err);
    }
}

// Extra Premium Feature: Export System Backup Data
async function exportSystemData() {
    try {
        const response = await fetch('/api/backup/export/');
        if (response.ok) {
            const state = await response.json();

            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "student_dashboard_backup.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();

            await renderActivityLogs();

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
        } else {
            alert('Failed to export system backup.');
        }
    } catch (err) {
        console.error(err);
    }
}

// Extra Premium Feature: Import System Backup Data
function importSystemData(input) {
    const file = input.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async function(e) {
        try {
            const state = JSON.parse(e.target.result);
            
            const response = await fetch('/api/backup/import/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(state)
            });

            if (response.ok) {
                // Sync settings locally as well
                if (state.preferences) {
                    const pref = state.preferences;
                    if (pref.theme) localStorage.setItem('theme', pref.theme);
                    if (pref.accentColor) localStorage.setItem('accentColor', pref.accentColor);
                    if (pref.accentHover) localStorage.setItem('accentHover', pref.accentHover);
                    if (pref.adminName) localStorage.setItem('adminName', pref.adminName);
                    if (pref.adminEmail) localStorage.setItem('adminEmail', pref.adminEmail);
                    if (pref.adminAvatar) localStorage.setItem('adminAvatar', pref.adminAvatar);
                }

                alert('System Backup successfully imported! Reloading the page to apply changes...');
                window.location.reload();
            } else {
                alert('Server rejected backup formatting.');
            }
        } catch(err) {
            alert('Invalid backup file formatting! Please load a valid exported JSON file.');
        }
    };
    reader.readAsText(file);
}

// Extra Premium Feature: Reset Database State
async function resetSystemData() {
    const confirmReset = confirm('Are you absolutely sure you want to delete all students, courses, teachers, and customizations? This action is permanent!');
    if (confirmReset) {
        try {
            const response = await fetch('/api/reset/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (response.ok) {
                localStorage.clear();
                alert('Database reset to defaults successfully! Reloading...');
                window.location.reload();
            } else {
                alert('Failed to reset database.');
            }
        } catch (err) {
            console.error(err);
        }
    }
}

// Render activity logs
async function renderActivityLogs() {
    const logList = document.getElementById('activityLogList');
    if (!logList) return;

    try {
        const response = await fetch('/api/logs/');
        if (!response.ok) return;
        const data = await response.json();
        const logs = data.logs;

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
            if (log.action.includes('Delete') || log.action.includes('Removed') || log.action.includes('Reset') || log.action.includes('Clear')) {
                icon = '<i class="fa-solid fa-trash-can" style="color:#ef4444; margin-right:6px;"></i>';
            } else if (log.action.includes('Add') || log.action.includes('Register') || log.action.includes('Create') || log.action.includes('Enroll')) {
                icon = '<i class="fa-solid fa-circle-plus" style="color:#10b981; margin-right:6px;"></i>';
            } else if (log.action.includes('Edit') || log.action.includes('Update') || log.action.includes('Profile') || log.action.includes('Security') || log.action.includes('Save')) {
                icon = '<i class="fa-solid fa-pen-to-square" style="color:#f59e0b; margin-right:6px;"></i>';
            } else if (log.action.includes('Backup') || log.action.includes('Appearance') || log.action.includes('Preferences') || log.action.includes('Theme')) {
                icon = '<i class="fa-solid fa-sliders" style="color:#8b5cf6; margin-right:6px;"></i>';
            }

            item.innerHTML = `
                <div style="display:flex; justify-content:space-between; font-weight:600; color:var(--card-text-primary); margin-bottom:4px;">
                    <span>${icon}${log.action}</span>
                    <span style="font-size:10px; color:var(--card-text-secondary); font-weight:normal;">${log.timestamp}</span>
                </div>
                <div style="color:var(--card-text-secondary); font-size: 11px;">${log.details}</div>
            `;
            logList.appendChild(item);
        });
    } catch (err) {
        console.error(err);
    }
}

async function clearActivityLogs() {
    try {
        const response = await fetch('/api/logs/', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            await renderActivityLogs();
        } else {
            alert('Failed to clear logs.');
        }
    } catch (err) {
        console.error(err);
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    initAvatarUpload();
    await loadProfileSettings();
    loadNotificationSettings();
    await renderActivityLogs();
});
