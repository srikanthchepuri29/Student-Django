// Theme and Accent Loader
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedColor = localStorage.getItem('accentColor') || '#2563eb';
    const savedHover = localStorage.getItem('accentHover') || '#1d4ed8';

    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.style.setProperty('--sidebar-border', savedColor);
    document.documentElement.style.setProperty('--sidebar-active-bg', savedColor + '1a');
    document.documentElement.style.setProperty('--primary-color', savedColor);
    document.documentElement.style.setProperty('--primary-hover', savedHover);
}
document.addEventListener('DOMContentLoaded', initTheme);

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

// Load teachers from SQLite
async function getTeachers() {
    try {
        const response = await fetch('/api/teachers/');
        const data = await response.json();
        return data.teachers || [];
    } catch (err) {
        console.error("Error fetching teachers:", err);
        return [];
    }
}

// Render teachers stats and table rows
async function renderTeachers() {
    const tableBody = document.getElementById('teacherTable');
    if (!tableBody) return;

    const teachers = await getTeachers();
    tableBody.innerHTML = '';
    let activeCount = 0;
    let leaveCount = 0;

    teachers.forEach((teacher) => {
        if (teacher.status === 'Active') {
            activeCount++;
        } else {
            leaveCount++;
        }

        const row = document.createElement('tr');
        const statusClass = teacher.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${teacher.teacher_id}</td>
            <td><strong>${teacher.name}</strong></td>
            <td>${teacher.email}</td>
            <td>${teacher.spec}</td>
            <td>${teacher.exp}</td>
            <td><span class="status ${statusClass}">${teacher.status}</span></td>
            <td>
                <button class="edit-btn" onclick="editTeacher(${teacher.id})">Edit</button>
                <button class="delete-btn" onclick="deleteTeacher(${teacher.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Update Cards
    const totalTeachersEl = document.getElementById('totalTeachers');
    if (totalTeachersEl) totalTeachersEl.textContent = teachers.length;

    const activeTeachersEl = document.getElementById('activeTeachers');
    if (activeTeachersEl) activeTeachersEl.textContent = activeCount;

    const onLeaveTeachersEl = document.getElementById('onLeaveTeachers');
    if (onLeaveTeachersEl) onLeaveTeachersEl.textContent = leaveCount;
}

// Add or Edit teacher
async function addTeacher() {
    const name = document.getElementById('teacherName').value.trim();
    const email = document.getElementById('teacherEmail').value.trim();
    const spec = document.getElementById('teacherSpec').value.trim();
    const exp = document.getElementById('teacherExp').value.trim();
    const status = document.getElementById('teacherStatus').value;
    const editIndex = document.getElementById('editIndex').value;

    if (name === '' || email === '' || spec === '' || exp === '') {
        alert('Please fill all fields');
        return;
    }

    let url = '/api/teachers/';
    let method = 'POST';
    const payload = { name, email, spec, exp, status };

    if (editIndex !== '') {
        url = `/api/teachers/${editIndex}/`;
        method = 'PUT';
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            if (editIndex !== '') {
                alert('Teacher details updated successfully!');
                document.getElementById('addBtn').innerHTML = 'Add Teacher';
                document.getElementById('editIndex').value = '';
            } else {
                alert('Teacher registered successfully!');
            }
            clearForm();
            await renderTeachers();
        } else {
            const err = await response.json();
            alert(err.error || 'Operation failed');
        }
    } catch (err) {
        console.error("Error saving teacher:", err);
        alert('An error occurred during submission.');
    }
}

// Populate form fields for edit
async function editTeacher(id) {
    try {
        const response = await fetch(`/api/teachers/${id}/`);
        if (!response.ok) {
            alert('Failed to load teacher details');
            return;
        }
        const teacher = await response.json();

        document.getElementById('teacherName').value = teacher.name;
        document.getElementById('teacherEmail').value = teacher.email;
        document.getElementById('teacherSpec').value = teacher.spec;
        document.getElementById('teacherExp').value = teacher.exp;
        document.getElementById('teacherStatus').value = teacher.status;
        document.getElementById('editIndex').value = teacher.id;

        document.getElementById('addBtn').innerHTML = 'Update Teacher';

        // Smooth scroll to form
        document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        console.error("Error editing teacher:", err);
    }
}

// Delete teacher
async function deleteTeacher(id) {
    const confirmDelete = confirm('Delete this teacher record permanently?');
    if (confirmDelete) {
        try {
            const response = await fetch(`/api/teachers/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            if (response.ok) {
                await renderTeachers();
            } else {
                alert('Failed to delete teacher');
            }
        } catch (err) {
            console.error("Error deleting teacher:", err);
        }
    }
}

// Clear form inputs
function clearForm() {
    document.getElementById('teacherName').value = '';
    document.getElementById('teacherEmail').value = '';
    document.getElementById('teacherSpec').value = '';
    document.getElementById('teacherExp').value = '';
    document.getElementById('teacherStatus').value = 'Active';
    document.getElementById('editIndex').value = '';
    
    const addBtn = document.getElementById('addBtn');
    if (addBtn) addBtn.innerHTML = 'Add Teacher';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', async () => {
    // Sync header profile details locally
    try {
        const profileRes = await fetch('/api/profile/');
        if (profileRes.ok) {
            const profile = await profileRes.json();
            localStorage.setItem('adminName', profile.admin_name);
            localStorage.setItem('adminEmail', profile.admin_email);
            localStorage.setItem('adminAvatar', profile.admin_avatar);
            
            const nameEl = document.querySelector('.admin span');
            const avatarEl = document.querySelector('.admin img');
            if (nameEl) nameEl.textContent = profile.admin_name;
            if (avatarEl) avatarEl.src = profile.admin_avatar;
        }
    } catch (e) {
        console.error(e);
    }

    await renderTeachers();

    // Setup teacher search with Suggestions and Button Click
    const searchInput = document.getElementById('searchInput');
    const searchBox = document.querySelector('.search-box');
    
    if (searchInput && searchBox) {
        // Dynamically create suggestions container
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'search-suggestions';
        suggestionsContainer.id = 'searchSuggestions';
        searchBox.appendChild(suggestionsContainer);

        // Function to perform search
        const performSearch = () => {
            const filter = searchInput.value.toLowerCase();
            const rows = document.querySelectorAll('#teacherTable tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 1) {
                    const name = cells[1].textContent.toLowerCase();
                    const spec = cells[3].textContent.toLowerCase();
                    row.style.display = (name.includes(filter) || spec.includes(filter)) ? '' : 'none';
                } else {
                    const text = row.innerText.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                }
            });
            suggestionsContainer.style.display = 'none';
        };

        // Input listener for filtering suggestions
        searchInput.addEventListener('input', function () {
            const filter = this.value.trim().toLowerCase();
            if (filter.length === 0) {
                suggestionsContainer.style.display = 'none';
                // Reset search filter
                const rows = document.querySelectorAll('#teacherTable tr');
                rows.forEach(row => row.style.display = '');
                return;
            }

            // Get teacher names from teacherTable rows
            const rows = document.querySelectorAll('#teacherTable tr');
            const teacherList = [];
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 1) {
                    const name = cells[1].textContent.trim();
                    teacherList.push({ name });
                }
            });

            // Filter teachers
            const matches = teacherList.filter(t => t.name.toLowerCase().includes(filter));

            if (matches.length > 0) {
                suggestionsContainer.innerHTML = '';
                // Deduplicate matches
                const uniqueMatches = [];
                const seen = new Set();
                matches.forEach(m => {
                    if (!seen.has(m.name.toLowerCase())) {
                        seen.add(m.name.toLowerCase());
                        uniqueMatches.push(m);
                    }
                });

                uniqueMatches.slice(0, 5).forEach(match => {
                    const item = document.createElement('div');
                    item.className = 'suggestion-item';
                    item.innerHTML = `<i class="fa-solid fa-users"></i> <span>${match.name}</span>`;
                    item.addEventListener('click', function () {
                        searchInput.value = match.name;
                        performSearch();
                    });
                    suggestionsContainer.appendChild(item);
                });
                suggestionsContainer.style.display = 'block';
            } else {
                suggestionsContainer.style.display = 'none';
            }
        });

        // Click search button
        const searchBtn = searchBox.querySelector('button');
        if (searchBtn) {
            searchBtn.addEventListener('click', performSearch);
        }

        // Enter key in input
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchBox.contains(e.target)) {
                suggestionsContainer.style.display = 'none';
            }
        });
    }
});
