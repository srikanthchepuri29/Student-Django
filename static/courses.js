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

// Load courses from SQLite
async function getCourses() {
    try {
        const response = await fetch('/api/courses/');
        const data = await response.json();
        return data.courses || [];
    } catch (err) {
        console.error("Error fetching courses:", err);
        return [];
    }
}

// Render course stats and table rows
async function renderCourses() {
    const tableBody = document.getElementById('courseTable');
    if (!tableBody) return;

    const courses = await getCourses();
    tableBody.innerHTML = '';
    let activeCount = 0;
    const categories = new Set();

    courses.forEach((course) => {
        if (course.status === 'Active') activeCount++;
        if (course.category) categories.add(course.category.trim().toLowerCase());

        const row = document.createElement('tr');
        const statusClass = course.status === 'Active' ? 'active' : 'inactive';
        row.innerHTML = `
            <td>${course.course_id}</td>
            <td><strong>${course.title}</strong></td>
            <td>${course.teacher}</td>
            <td><span style="font-weight:500;">${course.category}</span></td>
            <td>${course.duration}</td>
            <td><span class="status ${statusClass}">${course.status}</span></td>
            <td>
                <button class="edit-btn" onclick="editCourse(${course.id})">Edit</button>
                <button class="delete-btn" onclick="deleteCourse(${course.id})">Delete</button>
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
async function addCourse() {
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

    let url = '/api/courses/';
    let method = 'POST';
    const payload = { title, teacher, category, duration, status };

    if (editIndex !== '') {
        url = `/api/courses/${editIndex}/`;
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
                alert('Course details updated successfully!');
                document.getElementById('addBtn').innerHTML = 'Add Course';
                document.getElementById('editIndex').value = '';
            } else {
                alert('Course added successfully!');
            }
            clearForm();
            await renderCourses();
        } else {
            const err = await response.json();
            alert(err.error || 'Operation failed');
        }
    } catch (err) {
        console.error("Error saving course:", err);
        alert('An error occurred during submission.');
    }
}

// Populate form fields for edit
async function editCourse(id) {
    try {
        const response = await fetch(`/api/courses/${id}/`);
        if (!response.ok) {
            alert('Failed to load course details');
            return;
        }
        const course = await response.json();

        document.getElementById('courseTitle').value = course.title;
        document.getElementById('courseTeacher').value = course.teacher;
        document.getElementById('courseCategory').value = course.category;
        document.getElementById('courseDuration').value = course.duration;
        document.getElementById('courseStatus').value = course.status;
        document.getElementById('editIndex').value = course.id;

        document.getElementById('addBtn').innerHTML = 'Update Course';

        // Smooth scroll to form
        document.querySelector('.student-form').scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        console.error("Error editing course:", err);
    }
}

// Delete course
async function deleteCourse(id) {
    const confirmDelete = confirm('Delete this course permanently?');
    if (confirmDelete) {
        try {
            const response = await fetch(`/api/courses/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            if (response.ok) {
                await renderCourses();
            } else {
                alert('Failed to delete course');
            }
        } catch (err) {
            console.error("Error deleting course:", err);
        }
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

    await renderCourses();

    // Setup course search with Suggestions and Button Click
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
            const rows = document.querySelectorAll('#courseTable tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 1) {
                    const title = cells[1].textContent.toLowerCase();
                    const category = cells[3].textContent.toLowerCase();
                    const teacher = cells[2].textContent.toLowerCase();
                    row.style.display = (title.includes(filter) || category.includes(filter) || teacher.includes(filter)) ? '' : 'none';
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
                const rows = document.querySelectorAll('#courseTable tr');
                rows.forEach(row => row.style.display = '');
                return;
            }

            // Get course titles from courseTable rows
            const rows = document.querySelectorAll('#courseTable tr');
            const courseList = [];
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 1) {
                    const title = cells[1].textContent.trim();
                    courseList.push({ title });
                }
            });

            // Filter courses
            const matches = courseList.filter(c => c.title.toLowerCase().includes(filter));

            if (matches.length > 0) {
                suggestionsContainer.innerHTML = '';
                // Deduplicate matches
                const uniqueMatches = [];
                const seen = new Set();
                matches.forEach(m => {
                    if (!seen.has(m.title.toLowerCase())) {
                        seen.add(m.title.toLowerCase());
                        uniqueMatches.push(m);
                    }
                });

                uniqueMatches.slice(0, 5).forEach(match => {
                    const item = document.createElement('div');
                    item.className = 'suggestion-item';
                    item.innerHTML = `<i class="fa-solid fa-book"></i> <span>${match.title}</span>`;
                    item.addEventListener('click', function () {
                        searchInput.value = match.title;
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
