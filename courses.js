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

// Default Courses Data
const defaultCourses = [
    { id: 1001, title: 'Python Full Stack', teacher: 'Vijay Kumar', category: 'Programming', duration: '6 Months', status: 'Active' },
    { id: 1002, title: 'Java Development', teacher: 'Prasad Roy', category: 'Programming', duration: '4 Months', status: 'Active' },
    { id: 1003, title: 'Web Development', teacher: 'Sneha Reddy', category: 'Design', duration: '3 Months', status: 'Active' },
    { id: 1004, title: 'React JS', teacher: 'Suresh Kumar', category: 'Development', duration: '2 Months', status: 'Active' },
    { id: 1005, title: 'Flutter Mobile App', teacher: 'Naveen Kumar', category: 'Mobile', duration: '3 Months', status: 'Active' }
];

// Load courses from LocalStorage
function getCourses() {
    const courses = localStorage.getItem('courses');
    if (!courses) {
        localStorage.setItem('courses', JSON.stringify(defaultCourses));
        return defaultCourses;
    }
    return JSON.parse(courses);
}

// Save courses to LocalStorage
function saveCourses(courses) {
    localStorage.setItem('courses', JSON.stringify(courses));
}

// Render course stats and table rows
function renderCourses() {
    const courses = getCourses();
    const tableBody = document.getElementById('courseTable');
    if (!tableBody) return;

    tableBody.innerHTML = '';
    let activeCount = 0;
    const categories = new Set();

    courses.forEach((course, index) => {
        if (course.status === 'Active') activeCount++;
        if (course.category) categories.add(course.category.trim().toLowerCase());

        const row = document.createElement('tr');
        const statusClass = course.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${course.id}</td>
            <td><strong>${course.title}</strong></td>
            <td>${course.teacher}</td>
            <td><span style="font-weight:500;">${course.category}</span></td>
            <td>${course.duration}</td>
            <td><span class="status ${statusClass}">${course.status}</span></td>
            <td>
                <button class="edit-btn" onclick="editCourse(${index})">Edit</button>
                <button class="delete-btn" onclick="deleteCourse(${index})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Update Cards
    const totalCoursesEl = document.getElementById('totalCourses');
    if (totalCoursesEl) totalCoursesEl.textContent = courses.length;

    const activeCoursesEl = document.getElementById('activeCourses');
    if (activeCoursesEl) activeCoursesEl.textContent = activeCount;

    const totalCategoriesEl = document.getElementById('totalCategories');
    if (totalCategoriesEl) totalCategoriesEl.textContent = categories.size;
}

// Add or Edit course
function addCourse() {
    const title = document.getElementById('courseTitle').value.trim();
    const teacher = document.getElementById('courseTeacher').value.trim();
    const category = document.getElementById('courseCategory').value.trim();
    const duration = document.getElementById('courseDuration').value.trim();
    const status = document.getElementById('courseStatus').value;
    const editIndex = document.getElementById('editIndex').value;

    if (title === '' || teacher === '' || category === '' || duration === '') {
        alert('Please fill all fields');
        return;
    }

    const courses = getCourses();

    if (editIndex !== '') {
        // Edit course
        const idx = parseInt(editIndex);
        courses[idx].title = title;
        courses[idx].teacher = teacher;
        courses[idx].category = category;
        courses[idx].duration = duration;
        courses[idx].status = status;

        document.getElementById('addBtn').innerHTML = 'Add Course';
        document.getElementById('editIndex').value = '';
        logActivity('Course Updated', `Updated details for course: ${title}`);
        alert('Course details updated successfully!');
    } else {
        // Add new course
        const newId = courses.length > 0 ? Math.max(...courses.map(c => c.id)) + 1 : 1001;
        courses.push({
            id: newId,
            title,
            teacher,
            category,
            duration,
            status
        });
        logActivity('Course Created', `Created new course: ${title} (Instructor: ${teacher})`);
        alert('Course added successfully!');
    }

    saveCourses(courses);
    clearForm();
    renderCourses();
}

// Populate form fields for edit
function editCourse(index) {
    const courses = getCourses();
    const course = courses[index];

    document.getElementById('courseTitle').value = course.title;
    document.getElementById('courseTeacher').value = course.teacher;
    document.getElementById('courseCategory').value = course.category;
    document.getElementById('courseDuration').value = course.duration;
    document.getElementById('courseStatus').value = course.status;
    document.getElementById('editIndex').value = index;

    document.getElementById('addBtn').innerHTML = 'Update Course';

    // Smooth scroll to form
    document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
}

// Delete course
function deleteCourse(index) {
    const confirmDelete = confirm('Delete this course permanently?');
    if (confirmDelete) {
        const courses = getCourses();
        const course = courses[index];
        logActivity('Course Removed', `Deleted course: ${course.title}`);
        courses.splice(index, 1);
        saveCourses(courses);
        renderCourses();
    }
}

// Clear form inputs
function clearForm() {
    document.getElementById('courseTitle').value = '';
    document.getElementById('courseTeacher').value = '';
    document.getElementById('courseCategory').value = '';
    document.getElementById('courseDuration').value = '';
    document.getElementById('courseStatus').value = 'Active';
    document.getElementById('editIndex').value = '';
    
    const addBtn = document.getElementById('addBtn');
    if (addBtn) addBtn.innerHTML = 'Add Course';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    renderCourses();

    // Setup course search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#courseTable tr');

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
