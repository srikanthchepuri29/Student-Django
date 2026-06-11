// Common Student Portal JS Library

// Helper to extract CSRF tokens
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

// Fetch header details and statistics on dashboard loads
async function initStudentStats() {
    try {
        const response = await fetch('/api/student/stats/');
        if (!response.ok) return;
        const stats = await response.json();
        
        // Sync Topbar and sidebar header info
        const topbarName = document.getElementById('topbarName');
        if (topbarName) topbarName.textContent = stats.full_name;
        
        const topbarAvatar = document.getElementById('topbarAvatar');
        if (topbarAvatar && stats.profile_photo) {
            topbarAvatar.src = stats.profile_photo.startsWith('data:') ? stats.profile_photo : '/srikanth.png';
        }

        // Dashboard specific details
        const welcomeTitle = document.getElementById('welcomeTitle');
        if (welcomeTitle) welcomeTitle.textContent = `Welcome Back, ${stats.full_name}!`;

        const welcomeSubtitle = document.getElementById('welcomeSubtitle');
        if (welcomeSubtitle) welcomeSubtitle.textContent = `Course Enrolled: ${stats.course_name} | Batch: ${stats.batch_name} | ID: ${stats.student_id}`;

        const cardNotesCount = document.getElementById('cardNotesCount');
        if (cardNotesCount) cardNotesCount.textContent = stats.materials_count;

        const cardChallengesCount = document.getElementById('cardChallengesCount');
        if (cardChallengesCount) cardChallengesCount.textContent = stats.completed_challenges;

        const cardQuizzesCount = document.getElementById('cardQuizzesCount');
        if (cardQuizzesCount) cardQuizzesCount.textContent = stats.completed_quizzes;

        const cardAssignmentsCount = document.getElementById('cardAssignmentsCount');
        if (cardAssignmentsCount) cardAssignmentsCount.textContent = stats.pending_assignments;

        const upcomingClassText = document.getElementById('upcomingClassText');
        if (upcomingClassText) upcomingClassText.textContent = stats.upcoming_class;

        // Progress indicators
        const progressPercent = document.getElementById('progressPercent');
        if (progressPercent) progressPercent.textContent = `${stats.progress_percentage}%`;

        const progressCircleVal = document.querySelector('.progress-circle circle.val');
        if (progressCircleVal) {
            const r = 40; // radius of circle
            const circumference = 2 * Math.PI * r;
            progressCircleVal.style.strokeDasharray = circumference;
            const offset = circumference - (stats.progress_percentage / 100) * circumference;
            progressCircleVal.style.strokeDashoffset = offset;
        }
    } catch (err) {
        console.error("Error loading student stats:", err);
    }
}

// Fetch Announcements
async function loadAnnouncements() {
    const listContainer = document.getElementById('announcementsFeed');
    if (!listContainer) return;
    
    try {
        const response = await fetch('/api/student/announcements/');
        if (!response.ok) return;
        const data = await response.json();
        
        listContainer.innerHTML = '';
        if (data.announcements.length === 0) {
            listContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px 0;">No announcements published yet.</p>';
            return;
        }

        data.announcements.forEach(ann => {
            const item = document.createElement('div');
            item.className = 'feed-item';
            item.innerHTML = `
                <h4>${ann.title}</h4>
                <p>${ann.content}</p>
                <span class="feed-date">${ann.date}</span>
            `;
            listContainer.appendChild(item);
        });
    } catch (err) {
        console.error("Error loading announcements:", err);
    }
}

// Load profile details on profile page
async function loadStudentProfile() {
    const form = document.getElementById('studentProfileForm');
    if (!form) return;
    
    try {
        const response = await fetch('/api/student/profile/');
        if (!response.ok) return;
        const data = await response.json();
        
        document.getElementById('full_name').value = data.full_name;
        document.getElementById('student_id').value = data.student_id;
        document.getElementById('email').value = data.email;
        document.getElementById('mobile_number').value = data.mobile_number;
        document.getElementById('address').value = data.address;
        document.getElementById('date_of_birth').value = data.date_of_birth;
        document.getElementById('gender').value = data.gender;
        document.getElementById('educational_qualification').value = data.educational_qualification;
        document.getElementById('previous_study_details').value = data.previous_study_details;
        document.getElementById('college_university_name').value = data.college_university_name;
        document.getElementById('batch_name').value = data.batch_name;
        document.getElementById('course_name').value = data.course_name;
        document.getElementById('joining_date').value = data.joining_date;
        document.getElementById('emergency_contact').value = data.emergency_contact;
        
        const avatarImg = document.getElementById('profileAvatarImg');
        if (avatarImg && data.profile_photo) {
            avatarImg.src = data.profile_photo.startsWith('data:') ? data.profile_photo : '/srikanth.png';
        }
    } catch (err) {
        console.error("Error loading student profile:", err);
    }
}

// Handle profile form save
async function saveStudentProfile(e) {
    if (e) e.preventDefault();
    
    const payload = {
        mobile_number: document.getElementById('mobile_number').value.trim(),
        address: document.getElementById('address').value.trim(),
        date_of_birth: document.getElementById('date_of_birth').value.trim(),
        gender: document.getElementById('gender').value,
        educational_qualification: document.getElementById('educational_qualification').value.trim(),
        previous_study_details: document.getElementById('previous_study_details').value.trim(),
        college_university_name: document.getElementById('college_university_name').value.trim(),
        emergency_contact: document.getElementById('emergency_contact').value.trim()
    };
    
    try {
        const response = await fetch('/api/student/profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            alert('Profile updated successfully!');
            await initStudentStats();
        } else {
            const err = await response.json();
            alert(err.error || 'Failed to update profile');
        }
    } catch (err) {
        console.error(err);
        alert('An error occurred during submission.');
    }
}

// Handle avatar photo changes
function handleAvatarUpload(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            const base64 = e.target.result;
            const imgEl = document.getElementById('profileAvatarImg');
            if (imgEl) imgEl.src = base64;
            
            try {
                const response = await fetch('/api/student/profile/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ profile_photo: base64 })
                });
                
                if (response.ok) {
                    await initStudentStats();
                } else {
                    alert('Failed to save profile picture');
                }
            } catch (err) {
                console.error("Error uploading profile photo:", err);
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// LMS Modules page handlers
let allMaterials = [];
async function loadLMSMaterials() {
    const grid = document.getElementById('materialsGrid');
    if (!grid) return;
    
    try {
        const response = await fetch('/api/student/lms/');
        if (!response.ok) return;
        const data = await response.json();
        allMaterials = data.materials;
        filterMaterials('all');
    } catch (err) {
        console.error("Error loading LMS materials:", err);
    }
}

function filterMaterials(type) {
    const grid = document.getElementById('materialsGrid');
    if (!grid) return;
    
    // Update active tab styles
    document.querySelectorAll('.filter-tab').forEach(tab => {
        if (tab.getAttribute('data-type') === type) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    // Filter
    let filtered = allMaterials;
    if (type !== 'all') {
        filtered = allMaterials.filter(m => {
            const mType = m.material_type.toLowerCase();
            if (type === 'technical_notes') return mType.includes('technical notes');
            if (type === 'aptitude') return mType.includes('aptitude');
            if (type === 'english') return mType.includes('english');
            if (type === 'interview_q') return mType.includes('interview questions');
            if (type === 'assignments') return mType.includes('assignments') || mType.includes('tasks');
            if (type === 'mini_projects') return mType.includes('mini projects');
            if (type === 'mock_interview') return mType.includes('mock interview');
            return false;
        });
    }
    
    grid.innerHTML = '';
    if (filtered.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px 0;">No learning materials available in this section.</div>';
        return;
    }
    
    filtered.forEach(m => {
        const card = document.createElement('div');
        card.className = 'material-card';
        
        let typeIcon = 'fa-file-pdf';
        if (m.file_type.toLowerCase() === 'video') typeIcon = 'fa-circle-play';
        if (m.file_type.toLowerCase() === 'link') typeIcon = 'fa-link';
        if (m.file_type.toLowerCase() === 'document') typeIcon = 'fa-file-word';
        
        card.innerHTML = `
            <div class="material-meta">
                <span class="material-tag">${m.material_type}</span>
                <i class="fa-solid ${typeIcon} material-type-icon"></i>
            </div>
            <h4>${m.title}</h4>
            <p>${m.content}</p>
            <div class="material-footer">
                <span class="material-date">Uploaded: ${m.uploaded_at}</span>
                <a href="${m.file_url || '#'}" target="_blank" class="download-link" onclick="if(!this.getAttribute('href') || this.getAttribute('href')==='#'){alert('Material content: ' + '${m.content}'); return false;}">
                    <i class="fa-solid fa-download"></i> View
                </a>
            </div>
        `;
        grid.appendChild(card);
    });
}

// MCQ Quiz Module Handlers
let mcqData = [];
let mcqSelectedAnswers = {};
let activeMCQCategory = '';

async function loadMCQData() {
    const catsContainer = document.getElementById('mcqCategories');
    if (!catsContainer) return;
    
    try {
        const response = await fetch('/api/student/mcq/');
        if (!response.ok) return;
        const data = await response.json();
        
        mcqData = data.mcqs;
        
        // Group by category to build left list
        const categories = [...new Set(mcqData.map(q => q.category))];
        
        catsContainer.innerHTML = '';
        if (categories.length === 0) {
            catsContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">No MCQs available.</p>';
            return;
        }

        categories.forEach((cat, idx) => {
            const item = document.createElement('div');
            item.className = 'category-item';
            if (idx === 0) {
                item.className = 'category-item active';
                activeMCQCategory = cat;
            }
            item.innerHTML = `<span>${cat}</span> <i class="fa-solid fa-chevron-right"></i>`;
            item.onclick = () => selectMCQCategory(cat, item);
            catsContainer.appendChild(item);
        });

        // Render history
        renderMCQHistory(data.history);
        
        if (activeMCQCategory) {
            renderActiveQuiz();
        }
    } catch (err) {
        console.error("Error loading MCQs:", err);
    }
}

function selectMCQCategory(cat, element) {
    document.querySelectorAll('.category-item').forEach(item => item.classList.remove('active'));
    element.classList.add('active');
    activeMCQCategory = cat;
    mcqSelectedAnswers = {};
    renderActiveQuiz();
}

function renderActiveQuiz() {
    const container = document.getElementById('quizArena');
    if (!container) return;
    
    const filtered = mcqData.filter(q => q.category === activeMCQCategory);
    container.innerHTML = `<h3>${activeMCQCategory} Practice Quiz</h3>`;
    
    if (filtered.length === 0) {
        container.innerHTML += '<p style="color: var(--text-secondary); padding: 20px 0;">No questions found in this category.</p>';
        return;
    }

    filtered.forEach((q, index) => {
        const qBox = document.createElement('div');
        qBox.style.marginBottom = '30px';
        qBox.innerHTML = `
            <div class="quiz-question">${index + 1}. ${q.question_text}</div>
            <div class="quiz-options">
                <div class="quiz-option" id="opt-${q.id}-A" onclick="selectQuizOption(${q.id}, 'A')">
                    <span style="font-weight: 700;">A.</span> ${q.option_a}
                </div>
                <div class="quiz-option" id="opt-${q.id}-B" onclick="selectQuizOption(${q.id}, 'B')">
                    <span style="font-weight: 700;">B.</span> ${q.option_b}
                </div>
                <div class="quiz-option" id="opt-${q.id}-C" onclick="selectQuizOption(${q.id}, 'C')">
                    <span style="font-weight: 700;">C.</span> ${q.option_c}
                </div>
                <div class="quiz-option" id="opt-${q.id}-D" onclick="selectQuizOption(${q.id}, 'D')">
                    <span style="font-weight: 700;">D.</span> ${q.option_d}
                </div>
            </div>
        `;
        container.appendChild(qBox);
    });

    const submitBtn = document.createElement('button');
    submitBtn.className = 'submit-btn';
    submitBtn.style.marginTop = '10px';
    submitBtn.textContent = 'Submit Answers';
    submitBtn.onclick = submitQuizAnswers;
    container.appendChild(submitBtn);
}

function selectQuizOption(qId, optionVal) {
    // Deselect previous
    ['A', 'B', 'C', 'D'].forEach(opt => {
        const el = document.getElementById(`opt-${qId}-${opt}`);
        if (el) el.classList.remove('selected');
    });
    
    // Select current
    const targetEl = document.getElementById(`opt-${qId}-${optionVal}`);
    if (targetEl) targetEl.classList.add('selected');
    
    mcqSelectedAnswers[qId] = optionVal;
}

async function submitQuizAnswers() {
    const questionsCount = mcqData.filter(q => q.category === activeMCQCategory).length;
    const answeredCount = Object.keys(mcqSelectedAnswers).length;
    
    if (answeredCount < questionsCount) {
        if (!confirm('You have not answered all questions. Submit anyway?')) {
            return;
        }
    }
    
    try {
        const response = await fetch('/api/student/mcq/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                category: activeMCQCategory,
                answers: mcqSelectedAnswers
            })
        });
        
        if (response.ok) {
            const res = await response.json();
            alert(`Quiz Submitted!\nScore: ${res.score}/${res.total}\nPercentage: ${Math.round((res.score/res.total)*100)}%`);
            mcqSelectedAnswers = {};
            // Reload MCQs and history
            await loadMCQData();
            await initStudentStats();
        } else {
            alert('Failed to submit quiz score');
        }
    } catch (err) {
        console.error("Error submitting quiz:", err);
    }
}

function renderMCQHistory(history) {
    const historyBody = document.getElementById('mcqHistoryBody');
    if (!historyBody) return;
    
    historyBody.innerHTML = '';
    if (history.length === 0) {
        historyBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--text-secondary);">No previous attempts found.</td></tr>';
        return;
    }
    
    history.forEach(h => {
        const row = document.createElement('tr');
        const pct = Math.round((h.score / h.total) * 100);
        row.innerHTML = `
            <td><strong>${h.category}</strong></td>
            <td>${h.score} / ${h.total}</td>
            <td><span class="status-pill ${pct >= 70 ? 'success' : 'pending'}">${pct}%</span></td>
            <td style="font-size: 12px; color: var(--text-secondary);">${h.date}</td>
        `;
        historyBody.appendChild(row);
    });
}

// Coding Challenge Module Handlers
let codingChallenges = [];
let activeChallenge = null;

async function loadCodingChallenges() {
    const listContainer = document.getElementById('challengeList');
    if (!listContainer) return;
    
    try {
        const response = await fetch('/api/student/coding/');
        if (!response.ok) return;
        const data = await response.json();
        
        codingChallenges = data.challenges;
        filterCodingChallenges('all');
    } catch (err) {
        console.error("Error loading coding challenges:", err);
    }
}

function filterCodingChallenges(difficulty) {
    const listContainer = document.getElementById('challengeList');
    if (!listContainer) return;
    
    // Update active tab styles
    document.querySelectorAll('.filter-tab').forEach(tab => {
        if (tab.getAttribute('data-diff') === difficulty) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    let filtered = codingChallenges;
    if (difficulty !== 'all') {
        filtered = codingChallenges.filter(c => c.difficulty.toLowerCase() === difficulty.toLowerCase());
    }

    listContainer.innerHTML = '';
    if (filtered.length === 0) {
        listContainer.innerHTML = '<p style="color: var(--text-secondary); padding: 20px; text-align: center;">No challenges found.</p>';
        return;
    }

    filtered.forEach((c, idx) => {
        const item = document.createElement('div');
        item.className = `category-item ${activeChallenge && activeChallenge.id === c.id ? 'active' : ''}`;
        
        const isCompleted = c.status === 'Completed';
        const checkIcon = isCompleted ? '<i class="fa-solid fa-circle-check" style="color: var(--success); margin-left: 8px;"></i>' : '';
        const diffClass = c.difficulty.toLowerCase() === 'easy' ? 'success' : (c.difficulty.toLowerCase() === 'medium' ? 'warning' : 'danger');

        item.innerHTML = `
            <div>
                <span>${c.title}</span> ${checkIcon}
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Difficulty: <span class="status-pill ${diffClass}" style="padding: 1px 4px; font-size: 10px;">${c.difficulty}</span></div>
            </div>
            <i class="fa-solid fa-chevron-right"></i>
        `;
        
        item.onclick = () => selectChallenge(c, item);
        listContainer.appendChild(item);
        
        // Auto select first challenge initially if none selected
        if (idx === 0 && !activeChallenge) {
            selectChallenge(c, item);
        }
    });
}

function selectChallenge(c, element) {
    if (element) {
        document.querySelectorAll('#challengeList .category-item').forEach(item => item.classList.remove('active'));
        element.classList.add('active');
    }
    
    activeChallenge = c;
    
    const titleEl = document.getElementById('challengeTitle');
    const descEl = document.getElementById('challengeDesc');
    const inputEl = document.getElementById('challengeInputFormat');
    const outputEl = document.getElementById('challengeOutputFormat');
    const sampleInputEl = document.getElementById('challengeSampleInput');
    const sampleOutputEl = document.getElementById('challengeSampleOutput');
    const editor = document.getElementById('codingEditor');
    const solBtn = document.getElementById('showSolutionBtn');
    const solutionCard = document.getElementById('solutionCard');
    const solutionCode = document.getElementById('solutionCode');

    if (titleEl) titleEl.textContent = c.title;
    if (descEl) descEl.textContent = c.description;
    if (inputEl) inputEl.textContent = c.input_format;
    if (outputEl) outputEl.textContent = c.output_format;
    if (sampleInputEl) sampleInputEl.textContent = c.sample_input;
    if (sampleOutputEl) sampleOutputEl.textContent = c.sample_output;
    
    // Set custom editor placeholder or saved code
    if (editor) {
        editor.value = c.saved_code || `def ${c.title.toLowerCase().replace(/ /g, '_')}(s):\n    # Write your python code here\n    pass`;
    }

    if (solutionCard) solutionCard.style.display = 'none';
    if (solBtn) {
        if (c.sample_solution) {
            solBtn.style.display = 'inline-block';
            if (solutionCode) solutionCode.textContent = c.sample_solution;
        } else {
            solBtn.style.display = 'none';
        }
    }
}

function toggleChallengeSolution() {
    const solutionCard = document.getElementById('solutionCard');
    if (!solutionCard) return;
    
    if (solutionCard.style.display === 'none') {
        solutionCard.style.display = 'block';
    } else {
        solutionCard.style.display = 'none';
    }
}

async function submitCodingChallenge() {
    if (!activeChallenge) return;
    
    const code = document.getElementById('codingEditor').value;
    try {
        const response = await fetch('/api/student/coding/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                challenge_id: activeChallenge.id,
                code: code
            })
        });
        
        if (response.ok) {
            alert('Congratulations! Your solution passed all tests and has been submitted.');
            
            // Reload challenges
            const prevId = activeChallenge.id;
            await loadCodingChallenges();
            await initStudentStats();
            
            // Re-select challenge
            const updated = codingChallenges.find(c => c.id === prevId);
            if (updated) {
                selectChallenge(updated, null);
                // Also update matching category list active class
                loadCodingChallenges(); // Re-renders the list
            }
        } else {
            alert('Submission failed. Please check syntax/logic errors.');
        }
    } catch (err) {
        console.error("Error submitting code challenge:", err);
    }
}

// Class Schedule timtable loader
async function loadWeeklyClassSchedule() {
    const scheduleBody = document.getElementById('scheduleTableBody');
    if (!scheduleBody) return;
    
    try {
        const response = await fetch('/api/student/schedule/');
        if (!response.ok) return;
        const data = await response.json();
        
        scheduleBody.innerHTML = '';
        const schedule = data.schedule;
        
        // Form structure by slot
        const timeSlots = [
            '09:30 AM – 11:30 AM',
            '11:30 AM – 12:30 PM',
            '12:30 PM – 12:45 PM',
            '01:00 PM – 02:00 PM',
            '02:00 PM – 04:00 PM',
            '04:00 PM – 04:30 PM'
        ];
        
        timeSlots.forEach(slot => {
            const row = document.createElement('tr');
            row.innerHTML = `<td><strong>${slot}</strong></td>`;
            
            // Add cells for Mon-Fri
            schedule.forEach(daySched => {
                const daySlot = daySched.slots.find(s => {
                    const s1 = s.time.replace(/ /g, '').replace('–', '-');
                    const s2 = slot.replace(/ /g, '').replace('–', '-');
                    return s1 === s2;
                });
                
                if (daySlot) {
                    let cellClass = 'class';
                    if (daySlot.type.toLowerCase().includes('preparation') || daySlot.type.toLowerCase().includes('practice')) cellClass = 'practice';
                    if (daySlot.type.toLowerCase().includes('break')) cellClass = 'break';
                    if (daySlot.type.toLowerCase().includes('lunch')) cellClass = 'lunch';
                    
                    row.innerHTML += `
                        <td>
                            <div class="schedule-cell ${cellClass}">
                                ${daySlot.title}
                                <br>
                                <small style="font-size: 10px; opacity:0.8;">${daySlot.desc}</small>
                            </div>
                        </td>
                    `;
                } else {
                    row.innerHTML += `<td>-</td>`;
                }
            });
            
            scheduleBody.appendChild(row);
        });
    } catch (err) {
        console.error("Error loading class timetable:", err);
    }
}

// Assignments Module Handlers
let studentAssignments = [];
let activeAssignment = null;

async function loadStudentAssignments() {
    const listContainer = document.getElementById('assignmentsList');
    if (!listContainer) return;
    
    try {
        const response = await fetch('/api/student/assignments/');
        if (!response.ok) return;
        const data = await response.json();
        studentAssignments = data.assignments;
        
        listContainer.innerHTML = '';
        if (studentAssignments.length === 0) {
            listContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">No assignments found.</p>';
            return;
        }

        studentAssignments.forEach((assign, idx) => {
            const item = document.createElement('div');
            item.className = `category-item ${activeAssignment && activeAssignment.id === assign.id ? 'active' : ''}`;
            const isCompleted = assign.status === 'Submitted';
            const statusIcon = isCompleted ? '<i class="fa-solid fa-circle-check" style="color: var(--success); margin-left: 8px;"></i>' : '';
            
            item.innerHTML = `
                <div>
                    <span>${assign.title}</span> ${statusIcon}
                    <div style="font-size:11px; color:var(--text-secondary); margin-top:4px;">Due: ${assign.due_date}</div>
                </div>
                <i class="fa-solid fa-chevron-right"></i>
            `;
            item.onclick = () => selectAssignment(assign, item);
            listContainer.appendChild(item);
            
            if (idx === 0 && !activeAssignment) {
                selectAssignment(assign, item);
            }
        });
    } catch (err) {
        console.error("Error loading assignments:", err);
    }
}

function selectAssignment(assign, element) {
    if (element) {
        document.querySelectorAll('#assignmentsList .category-item').forEach(item => item.classList.remove('active'));
        element.classList.add('active');
    }
    
    activeAssignment = assign;
    
    const titleEl = document.getElementById('assignmentTitle');
    const descEl = document.getElementById('assignmentDesc');
    const dateEl = document.getElementById('assignmentDueDate');
    const editor = document.getElementById('assignmentContentInput');
    const statusPill = document.getElementById('assignmentStatusPill');

    if (titleEl) titleEl.textContent = assign.title;
    if (descEl) descEl.textContent = assign.description;
    if (dateEl) dateEl.textContent = assign.due_date;
    if (editor) {
        editor.value = assign.submission_content || '';
    }
    
    if (statusPill) {
        statusPill.textContent = assign.status;
        statusPill.className = `status-pill ${assign.status === 'Submitted' ? 'success' : 'pending'}`;
    }
}

async function submitStudentAssignment() {
    if (!activeAssignment) return;
    
    const content = document.getElementById('assignmentContentInput').value.trim();
    if (content === '') {
        alert('Please write some content before submitting.');
        return;
    }
    
    try {
        const response = await fetch('/api/student/assignments/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                assignment_id: activeAssignment.id,
                content: content
            })
        });
        
        if (response.ok) {
            alert('Assignment submitted successfully!');
            const prevId = activeAssignment.id;
            await loadStudentAssignments();
            await initStudentStats();
            
            const updated = studentAssignments.find(a => a.id === prevId);
            if (updated) {
                selectAssignment(updated, null);
            }
        } else {
            alert('Failed to submit assignment.');
        }
    } catch (err) {
        console.error("Error submitting assignment:", err);
    }
}

// Auto start dashboard operations on load
document.addEventListener('DOMContentLoaded', () => {
    initStudentStats();
    
    // Call specific loaders if target DOM nodes exist
    if (document.getElementById('announcementsFeed')) {
        loadAnnouncements();
    }
    if (document.getElementById('studentProfileForm')) {
        loadStudentProfile();
    }
    if (document.getElementById('materialsGrid')) {
        loadLMSMaterials();
    }
    if (document.getElementById('mcqCategories')) {
        loadMCQData();
    }
    if (document.getElementById('challengeList')) {
        loadCodingChallenges();
    }
    if (document.getElementById('scheduleTableBody')) {
        loadWeeklyClassSchedule();
    }
    if (document.getElementById('assignmentsList')) {
        loadStudentAssignments();
    }
});
