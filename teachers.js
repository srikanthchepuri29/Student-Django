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

// Default Teachers Data
const defaultTeachers = [
    { id: 201, name: 'Vijay Kumar', email: 'vijay@gmail.com', spec: 'Python Full Stack', exp: '8 Years', status: 'Active' },
    { id: 202, name: 'Prasad Roy', email: 'prasad@gmail.com', spec: 'Java Development', exp: '10 Years', status: 'Active' },
    { id: 203, name: 'Sneha Reddy', email: 'sneha@gmail.com', spec: 'Web Development', exp: '5 Years', status: 'Active' },
    { id: 204, name: 'Suresh Kumar', email: 'suresh@gmail.com', spec: 'React JS', exp: '6 Years', status: 'Active' },
    { id: 205, name: 'Naveen Kumar', email: 'naveen@gmail.com', spec: 'Flutter Mobile App', exp: '4 Years', status: 'Active' }
];

// Load teachers from LocalStorage
function getTeachers() {
    const teachers = localStorage.getItem('teachers');
    if (!teachers) {
        localStorage.setItem('teachers', JSON.stringify(defaultTeachers));
        return defaultTeachers;
    }
    return JSON.parse(teachers);
}

// Save teachers to LocalStorage
function saveTeachers(teachers) {
    localStorage.setItem('teachers', JSON.stringify(teachers));
}

// Render teachers stats and table rows
function renderTeachers() {
    const teachers = getTeachers();
    const tableBody = document.getElementById('teacherTable');
    if (!tableBody) return;

    tableBody.innerHTML = '';
    let activeCount = 0;
    let leaveCount = 0;

    teachers.forEach((teacher, index) => {
        if (teacher.status === 'Active') {
            activeCount++;
        } else {
            leaveCount++;
        }

        const row = document.createElement('tr');
        const statusClass = teacher.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${teacher.id}</td>
            <td><strong>${teacher.name}</strong></td>
            <td>${teacher.email}</td>
            <td>${teacher.spec}</td>
            <td>${teacher.exp}</td>
            <td><span class="status ${statusClass}">${teacher.status}</span></td>
            <td>
                <button class="edit-btn" onclick="editTeacher(${index})">Edit</button>
                <button class="delete-btn" onclick="deleteTeacher(${index})">Delete</button>
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
function addTeacher() {
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

    const teachers = getTeachers();

    if (editIndex !== '') {
        // Edit teacher
        const idx = parseInt(editIndex);
        teachers[idx].name = name;
        teachers[idx].email = email;
        teachers[idx].spec = spec;
        teachers[idx].exp = exp;
        teachers[idx].status = status;

        document.getElementById('addBtn').innerHTML = 'Add Teacher';
        document.getElementById('editIndex').value = '';
        logActivity('Teacher Updated', `Updated profile for teacher: ${name}`);
        alert('Teacher details updated successfully!');
    } else {
        // Add new teacher
        const newId = teachers.length > 0 ? Math.max(...teachers.map(t => t.id)) + 1 : 201;
        teachers.push({
            id: newId,
            name,
            email,
            spec,
            exp,
            status
        });
        logActivity('Teacher Registered', `Registered new teacher: ${name} (Spec: ${spec})`);
        alert('Teacher registered successfully!');
    }

    saveTeachers(teachers);
    clearForm();
    renderTeachers();
}

// Populate form fields for edit
function editTeacher(index) {
    const teachers = getTeachers();
    const teacher = teachers[index];

    document.getElementById('teacherName').value = teacher.name;
    document.getElementById('teacherEmail').value = teacher.email;
    document.getElementById('teacherSpec').value = teacher.spec;
    document.getElementById('teacherExp').value = teacher.exp;
    document.getElementById('teacherStatus').value = teacher.status;
    document.getElementById('editIndex').value = index;

    document.getElementById('addBtn').innerHTML = 'Update Teacher';

    // Smooth scroll to form
    document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
}

// Delete teacher
function deleteTeacher(index) {
    const confirmDelete = confirm('Delete this teacher record permanently?');
    if (confirmDelete) {
        const teachers = getTeachers();
        const teacher = teachers[index];
        logActivity('Teacher Removed', `Removed profile of teacher: ${teacher.name}`);
        teachers.splice(index, 1);
        saveTeachers(teachers);
        renderTeachers();
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
document.addEventListener('DOMContentLoaded', () => {
    renderTeachers();

    // Setup teacher search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#teacherTable tr');

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
});

// Helper utility to write to live activity logs
function logActivity(action, details) {
    const logs = JSON.parse(localStorage.getItem('activityLogs')) || [];
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    logs.unshift({ action, details, timestamp });
    if (logs.length > 25) logs.pop();
    localStorage.setItem('activityLogs', JSON.stringify(logs));
}
