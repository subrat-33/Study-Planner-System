// Subjects and Syllabus Management Script

document.addEventListener('DOMContentLoaded', () => {
    loadSubjects();

    // Subject Form Handler
    const subjectForm = document.getElementById('subject-form');
    if (subjectForm) {
        subjectForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await saveSubject();
        });
    }

    // Topic Form Handler
    const topicForm = document.getElementById('topic-form');
    if (topicForm) {
        topicForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await saveTopic();
        });
    }
});

let currentSubjectId = null;

async function loadSubjects() {
    try {
        const subjects = await api.get('/subjects');
        renderSubjects(subjects);
    } catch (error) {
        console.error('Failed to load subjects:', error);
    }
}

function renderSubjects(subjects) {
    const container = document.getElementById('subjects-container');
    const emptyState = document.getElementById('empty-subjects');
    
    if (!container) return;

    // Clear existing (except empty state)
    const cards = container.querySelectorAll('.subject-card');
    cards.forEach(c => c.remove());

    if (subjects.length === 0) {
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    
    subjects.forEach(subject => {
        const card = document.createElement('div');
        card.className = 'card subject-card';
        card.style.borderTop = `4px solid ${subject.color || '#4F46E5'}`;
        
        const progress = subject.progress || 0;
        
        card.innerHTML = `
            <div class="card-header">
                <h3 style="margin-bottom: 0;">${subject.name}</h3>
                <span class="badge badge-${subject.difficulty.toLowerCase()}">${subject.difficulty}</span>
            </div>
            <div style="margin-bottom: 16px;">
                <p style="font-size: 0.85rem; color: var(--gray-500);">Deadline: ${new Date(subject.deadline).toLocaleDateString()}</p>
                <div class="flex justify-between" style="font-size: 0.85rem; margin-top: 8px;">
                    <span>Progress</span>
                    <span>${progress}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: ${progress}%"></div>
                </div>
            </div>
            <div class="flex justify-between align-center" style="margin-top: 20px;">
                <div style="font-size: 0.85rem; color: var(--gray-600);">
                    <i class="fas fa-clock"></i> ${subject.weekly_hours} hrs/week
                </div>
                <div class="flex gap-sm">
                    <button class="btn btn-outline btn-sm" onclick="openTopicsDrawer(${subject.id}, '${subject.name}')">
                        <i class="fas fa-list-ul"></i> Topics
                    </button>
                    <button class="btn btn-secondary btn-sm" onclick="editSubject(${JSON.stringify(subject).replace(/"/g, '&quot;')})">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

function toggleSubjectModal(show) {
    const modal = document.getElementById('subject-modal');
    if (show) {
        modal.classList.add('active');
    } else {
        modal.classList.remove('active');
        document.getElementById('subject-form').reset();
        document.getElementById('subj-id').value = '';
    }
}

async function saveSubject() {
    const id = document.getElementById('subj-id').value;
    const data = {
        name: document.getElementById('subj-name').value,
        difficulty: document.getElementById('subj-difficulty').value,
        deadline: document.getElementById('subj-deadline').value,
        weekly_hours: document.getElementById('subj-hours').value,
        description: document.getElementById('subj-desc').value
    };

    try {
        if (id) {
            await api.put(`/subjects/${id}`, data);
            showToast('Subject updated successfully!');
        } else {
            await api.post('/subjects', data);
            showToast('Subject added successfully!');
        }
        toggleSubjectModal(false);
        loadSubjects();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function editSubject(subject) {
    document.getElementById('subj-id').value = subject.id;
    document.getElementById('subj-name').value = subject.name;
    document.getElementById('subj-difficulty').value = subject.difficulty;
    document.getElementById('subj-deadline').value = subject.deadline.split('T')[0];
    document.getElementById('subj-hours').value = subject.weekly_hours;
    document.getElementById('hours-val').innerText = subject.weekly_hours;
    document.getElementById('subj-desc').value = subject.description || '';
    
    document.getElementById('modal-title').innerText = 'Edit Subject';
    toggleSubjectModal(true);
}

// Topics Logic
function openTopicsDrawer(id, name) {
    currentSubjectId = id;
    document.getElementById('drawer-subject-name').innerText = name;
    document.getElementById('topics-drawer').classList.add('active');
    loadTopics(id);
}

function toggleTopicsDrawer(show) {
    const drawer = document.getElementById('topics-drawer');
    if (show) drawer.classList.add('active');
    else drawer.classList.remove('active');
}

async function loadTopics(subjectId) {
    try {
        const topics = await api.get(`/subjects/${subjectId}/topics`);
        renderTopics(topics);
    } catch (error) {
        console.error('Failed to load topics:', error);
    }
}

function renderTopics(topics) {
    const list = document.getElementById('topics-list');
    list.innerHTML = '';
    
    if (topics.length === 0) {
        list.innerHTML = '<p style="text-align:center; color: var(--gray-400); padding: 20px;">No topics added yet.</p>';
        return;
    }

    topics.forEach(topic => {
        const item = document.createElement('div');
        item.className = 'flex justify-between align-center card';
        item.style.padding = '12px 16px';
        item.style.marginBottom = '8px';
        
        item.innerHTML = `
            <div>
                <h4 style="margin: 0; font-size: 0.95rem;">${topic.name}</h4>
                <div style="font-size: 0.75rem; color: var(--gray-500); margin-top: 4px;">
                    <span class="badge badge-medium" style="font-size: 0.65rem;">${topic.priority} Priority</span>
                    <span style="margin-left: 8px;">${topic.estimated_hours} hrs</span>
                </div>
            </div>
            <div class="flex gap-sm">
                <button class="btn btn-outline btn-sm" style="padding: 4px 8px;" onclick="deleteTopic(${topic.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        list.appendChild(item);
    });
}

function showAddTopicForm() {
    document.getElementById('add-topic-section').style.display = 'block';
}

function hideAddTopicForm() {
    document.getElementById('add-topic-section').style.display = 'none';
    document.getElementById('topic-form').reset();
}

async function saveTopic() {
    const data = {
        name: document.getElementById('topic-name').value,
        estimated_hours: document.getElementById('topic-hours').value,
        priority: document.getElementById('topic-priority').value
    };

    try {
        await api.post(`/subjects/${currentSubjectId}/topics`, data);
        showToast('Topic added!');
        hideAddTopicForm();
        loadTopics(currentSubjectId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function deleteTopic(id) {
    if (!confirm('Are you sure you want to delete this topic?')) return;
    try {
        await api.delete(`/subjects/${currentSubjectId}/topics/${id}`);
        showToast('Topic deleted');
        loadTopics(currentSubjectId);
    } catch (error) {
        showToast(error.message, 'error');
    }
}
