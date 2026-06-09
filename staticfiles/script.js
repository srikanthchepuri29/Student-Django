// Theme and Accent Loader (handled by pre-rendering but fallback or updates)
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

// Fetch Students
async function getStudents() {
    try {
        const response = await fetch('/api/students/');
        const data = await response.json();
        return data.students || [];
    } catch (err) {
        console.error("Error fetching students:", err);
        return [];
    }
}

// Render Dashboard Counts
async function updateDashboardCounts() {
    try {
        const response = await fetch('/api/dashboard/stats/');
        const data = await response.json();

        const studentCountEl = document.getElementById('studentCount');
        if (studentCountEl) studentCountEl.textContent = data.student_count;

        const coursesCountEl = document.getElementById('coursesCount');
        if (coursesCountEl) coursesCountEl.textContent = data.course_count;

        const teachersCountEl = document.getElementById('teachersCount');
        if (teachersCountEl) teachersCountEl.textContent = data.teacher_count;
    } catch (err) {
        console.error("Error updating counts:", err);
    }
}

// Render Student Table
async function renderStudentTable() {
    const tableBody = document.getElementById('studentTable');
    if (!tableBody) return;

    const students = await getStudents();
    tableBody.innerHTML = '';

    students.forEach((student) => {
        const row = document.createElement('tr');
        const statusClass = student.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${student.student_id}</td>
            <td>${student.name}</td>
            <td>${student.email}</td>
            <td>${student.course}</td>
            <td>
                <span class="status ${statusClass}">
                    ${student.status}
                </span>
            </td>
            <td>
                <button class="edit-btn" onclick="editStudent(${student.id})">Edit</button>
                <button class="delete-btn" onclick="deleteStudent(${student.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    const studentCountEl = document.getElementById('studentCount');
    if (studentCountEl) studentCountEl.textContent = students.length;
}

// Add/Edit Student
async function addStudent() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const course = document.getElementById('course').value.trim();
    const status = document.getElementById('status').value;
    const editIndex = document.getElementById('editIndex').value;

    if (name === '' || email === '' || course === '') {
        alert('Please fill all fields');
        return;
    }

    let url = '/api/students/';
    let method = 'POST';
    const payload = { name, email, course, status };

    if (editIndex !== '') {
        url = `/api/students/${editIndex}/`;
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
                alert('Student details updated successfully!');
                document.getElementById('addBtn').innerHTML = 'Add Student';
                document.getElementById('editIndex').value = '';
            } else {
                alert('Student added successfully!');
            }
            clearForm();
            if (document.getElementById('studentTable')) {
                await renderStudentTable();
            }
            await updateDashboardCounts();
        } else {
            const err = await response.json();
            alert(err.error || 'Operation failed');
        }
    } catch (err) {
        console.error("Error saving student:", err);
        alert('An error occurred during submission.');
    }
}

// Populate fields for Editing
async function editStudent(id) {
    try {
        const response = await fetch(`/api/students/${id}/`);
        if (!response.ok) {
            alert('Failed to load student details');
            return;
        }
        const student = await response.json();

        document.getElementById('name').value = student.name;
        document.getElementById('email').value = student.email;
        document.getElementById('course').value = student.course;
        document.getElementById('status').value = student.status;
        document.getElementById('editIndex').value = student.id;

        document.getElementById('addBtn').innerHTML = 'Update Student';

        // Scroll smoothly to form
        document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        console.error("Error editing student:", err);
    }
}

// Delete Student
async function deleteStudent(id) {
    const confirmDelete = confirm('Delete this student permanently?');
    if (confirmDelete) {
        try {
            const response = await fetch(`/api/students/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            if (response.ok) {
                await renderStudentTable();
                await updateDashboardCounts();
            } else {
                alert('Failed to delete student');
            }
        } catch (err) {
            console.error("Error deleting student:", err);
        }
    }
}

// Clear Form fields
function clearForm() {
    document.getElementById('name').value = '';
    document.getElementById('email').value = '';
    document.getElementById('course').value = '';
    document.getElementById('status').value = 'Active';
    document.getElementById('editIndex').value = '';
    const addBtn = document.getElementById('addBtn');
    if (addBtn) addBtn.innerHTML = 'Add Student';
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', async () => {
    // Sync theme options from server details first
    try {
        const profileRes = await fetch('/api/profile/');
        if (profileRes.ok) {
            const profile = await profileRes.json();
            // sync settings locally for compatibility with pages that use client-side local values
            localStorage.setItem('adminName', profile.admin_name);
            localStorage.setItem('adminEmail', profile.admin_email);
            localStorage.setItem('adminAvatar', profile.admin_avatar);
        }
        
        await renderStudentTable();
        await updateDashboardCounts();
    } catch (e) {
        console.error(e);
    }

    // Setup Search Event Listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#studentTable tr');

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
});

// Helper utility to write to live activity logs
async function logActivity(action, details) {
    try {
        await fetch('/api/logs/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ action, details })
        });
    } catch (err) {
        console.error("Error logging activity:", err);
    }
}