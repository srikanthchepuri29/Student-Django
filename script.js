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

// Default Student Data
const defaultStudents = [
    { id: 101, name: 'Srikanth', email: 'srikanth@gmail.com', course: 'Python Full Stack', status: 'Active' },
    { id: 102, name: 'Rahul', email: 'rahul@gmail.com', course: 'Java', status: 'Inactive' },
    { id: 103, name: 'Anjali', email: 'anjali@gmail.com', course: 'Web Development', status: 'Active' },
    { id: 104, name: 'praveen', email: 'srikanth@gmail.com', course: 'Python Full Stack', status: 'Active' },
    { id: 105, name: 'Sravani', email: 'sravani@gmail.com', course: 'Python Full Stack', status: 'Active' },
    { id: 106, name: 'premm', email: 'prem@gmail.com', course: 'React', status: 'Active' },
    { id: 107, name: 'sai', email: 'sai@gmail.com', course: 'Python Full Stack', status: 'Active' },
    { id: 108, name: 'ganesh', email: 'ganesh@gmail.com', course: 'flutter', status: 'Active' },
    { id: 109, name: 'mahesh', email: 'mahesh@gmail.com', course: 'Java', status: 'Active' },
    { id: 110, name: 'vinay', email: 'vinay@gmail.com', course: 'Java', status: 'Active' }
];

// Initialize State
function getStudents() {
    const students = localStorage.getItem('students');
    if (!students) {
        localStorage.setItem('students', JSON.stringify(defaultStudents));
        return defaultStudents;
    }
    return JSON.parse(students);
}

function saveStudents(students) {
    localStorage.setItem('students', JSON.stringify(students));
}

// Render Dashboard Counts
function updateDashboardCounts() {
    const students = getStudents();
    const courses = JSON.parse(localStorage.getItem('courses')) || [
        { id: 1, title: 'Python Full Stack', teacher: 'Vijay Kumar', category: 'Programming', duration: '6 Months', status: 'Active' },
        { id: 2, title: 'Java Development', teacher: 'Prasad Roy', category: 'Programming', duration: '4 Months', status: 'Active' },
        { id: 3, title: 'Web Development', teacher: 'Sneha Reddy', category: 'Design', duration: '3 Months', status: 'Active' },
        { id: 4, title: 'React JS', teacher: 'Suresh Kumar', category: 'Development', duration: '2 Months', status: 'Active' },
        { id: 5, title: 'Flutter Mobile App', teacher: 'Naveen Kumar', category: 'Mobile', duration: '3 Months', status: 'Active' }
    ];
    const teachers = JSON.parse(localStorage.getItem('teachers')) || [
        { id: 1, name: 'Vijay Kumar', email: 'vijay@gmail.com', spec: 'Python Full Stack', exp: '8 Years', status: 'Active' },
        { id: 2, name: 'Prasad Roy', email: 'prasad@gmail.com', spec: 'Java Development', exp: '10 Years', status: 'Active' },
        { id: 3, name: 'Sneha Reddy', email: 'sneha@gmail.com', spec: 'Web Development', exp: '5 Years', status: 'Active' },
        { id: 4, name: 'Suresh Kumar', email: 'suresh@gmail.com', spec: 'React JS', exp: '6 Years', status: 'Active' },
        { id: 5, name: 'Naveen Kumar', email: 'naveen@gmail.com', spec: 'Flutter Mobile App', exp: '4 Years', status: 'Active' }
    ];

    const studentCountEl = document.getElementById('studentCount');
    if (studentCountEl) studentCountEl.textContent = students.length;

    const coursesCountEl = document.getElementById('coursesCount');
    if (coursesCountEl) coursesCountEl.textContent = courses.length;

    const teachersCountEl = document.getElementById('teachersCount');
    if (teachersCountEl) teachersCountEl.textContent = teachers.length;
}

// Render Student Table
function renderStudentTable() {
    const tableBody = document.getElementById('studentTable');
    if (!tableBody) return; // Not on student directory page

    const students = getStudents();
    tableBody.innerHTML = '';

    students.forEach((student, index) => {
        const row = document.createElement('tr');
        const statusClass = student.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.email}</td>
            <td>${student.course}</td>
            <td>
                <span class="status ${statusClass}">
                    ${student.status}
                </span>
            </td>
            <td>
                <button class="edit-btn" onclick="editStudent(${index})">Edit</button>
                <button class="delete-btn" onclick="deleteStudent(${index})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    const studentCountEl = document.getElementById('studentCount');
    if (studentCountEl) studentCountEl.textContent = students.length;
}

// Add/Edit Student
function addStudent() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const course = document.getElementById('course').value.trim();
    const status = document.getElementById('status').value;
    const editIndex = document.getElementById('editIndex').value;

    if (name === '' || email === '' || course === '') {
        alert('Please fill all fields');
        return;
    }

    const students = getStudents();

    if (editIndex !== '') {
        // Edit Mode
        const idx = parseInt(editIndex);
        students[idx].name = name;
        students[idx].email = email;
        students[idx].course = course;
        students[idx].status = status;

        document.getElementById('addBtn').innerHTML = 'Add Student';
        document.getElementById('editIndex').value = '';
        logActivity('Student Updated', `Updated details for student: ${name}`);
        alert('Student details updated successfully!');
    } else {
        // Add Mode
        const newId = students.length > 0 ? Math.max(...students.map(s => s.id)) + 1 : 101;
        students.push({
            id: newId,
            name,
            email,
            course,
            status
        });
        logActivity('Student Enrolled', `Enrolled new student: ${name} (Course: ${course})`);
        alert('Student added successfully!');
    }

    saveStudents(students);
    clearForm();

    if (document.getElementById('studentTable')) {
        renderStudentTable();
    } else {
        // If on Dashboard page, update counts
        updateDashboardCounts();
    }
}

// Populate fields for Editing
function editStudent(index) {
    const students = getStudents();
    const student = students[index];

    document.getElementById('name').value = student.name;
    document.getElementById('email').value = student.email;
    document.getElementById('course').value = student.course;
    document.getElementById('status').value = student.status;
    document.getElementById('editIndex').value = index;

    document.getElementById('addBtn').innerHTML = 'Update Student';

    // Scroll smoothly to form
    document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
}

// Delete Student
function deleteStudent(index) {
    const confirmDelete = confirm('Delete this student permanently?');
    if (confirmDelete) {
        const students = getStudents();
        const student = students[index];
        logActivity('Student Removed', `Deleted profile of student: ${student.name}`);
        students.splice(index, 1);
        saveStudents(students);
        renderStudentTable();
        updateDashboardCounts();
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
document.addEventListener('DOMContentLoaded', () => {
    getStudents();
    renderStudentTable();
    updateDashboardCounts();

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
function logActivity(action, details) {
    const logs = JSON.parse(localStorage.getItem('activityLogs')) || [];
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    logs.unshift({ action, details, timestamp });
    if (logs.length > 25) logs.pop();
    localStorage.setItem('activityLogs', JSON.stringify(logs));
}