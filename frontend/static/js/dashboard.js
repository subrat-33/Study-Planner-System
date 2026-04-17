// Dashboard Logic

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    
    // Quick Generate Button
    const quickGen = document.getElementById('quick-generate');
    if (quickGen) {
        quickGen.addEventListener('click', async () => {
            quickGen.disabled = true;
            quickGen.innerText = 'Optimizing...';
            try {
                await api.post('/schedule/generate', {});
                showToast('Schedule optimized successfully!');
                loadDashboardData();
            } catch (error) {
                showToast(error.message, 'error');
            } finally {
                quickGen.disabled = false;
                quickGen.innerHTML = '<i class="fas fa-magic"></i> Optimize Schedule';
            }
        });
    }
});

async function loadDashboardData() {
    try {
        // In a real app, these would be separate calls or one aggregate call
        const stats = await api.get('/progress/summary');
        const subjects = await api.get('/subjects');
        const schedule = await api.get('/schedule');
        
        updateStats(stats, subjects.length);
        renderTodaySchedule(schedule);
        renderDeadlines(subjects);
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

function updateStats(stats, subjCount) {
    document.getElementById('stat-today-tasks').innerText = stats.today_tasks || 0;
    document.getElementById('stat-progress').innerText = (stats.overall_progress || 0) + '%';
    
    // Show days till next upcoming exam
    const daysEl = document.getElementById('stat-days-left');
    if (stats.days_until_exam !== null && stats.days_until_exam !== undefined) {
        daysEl.innerText = stats.days_until_exam;
    } else {
        daysEl.innerText = '—';
        daysEl.title = 'No upcoming exams';
    }
    
    document.getElementById('stat-total-subjects').innerText = subjCount;
}

function renderTodaySchedule(schedule) {
    const list = document.getElementById('today-schedule-list');
    if (!list) return;

    const todayStr = new Date().toISOString().split('T')[0];
    const todayItems = schedule.filter(it => it.date === todayStr);

    if (todayItems.length === 0) {
        // Keep the empty state defined in HTML
        return;
    }

    list.innerHTML = '';
    todayItems.forEach(item => {
        const row = document.createElement('div');
        row.className = 'card flex justify-between align-center';
        row.style.padding = '16px';
        row.style.borderLeft = `4px solid ${item.color}`;
        
        row.innerHTML = `
            <div>
                <strong style="display: block;">${item.subject_name}</strong>
                <span style="font-size: 0.85rem; color: var(--gray-500);">${item.topic_name}</span>
            </div>
            <div class="flex align-center gap-md">
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--gray-700);">${item.start_time.substring(0, 5)}</span>
                <button class="btn btn-outline btn-sm" onclick="markComplete(${item.topic_id})">
                    <i class="fas fa-check"></i>
                </button>
            </div>
        `;
        list.appendChild(row);
    });
}

function renderDeadlines(subjects) {
    const list = document.getElementById('deadlines-list');
    if (!list) return;

    // Sort by deadline
    const sorted = [...subjects].sort((a, b) => new Date(a.deadline) - new Date(b.deadline)).slice(0, 3);

    if (sorted.length === 0) return;

    list.innerHTML = '';
    sorted.forEach(subj => {
        const days = Math.ceil((new Date(subj.deadline) - new Date()) / (1000 * 60 * 60 * 24));
        const item = document.createElement('div');
        item.innerHTML = `
            <div class="flex justify-between" style="font-size: 0.85rem; margin-bottom: 4px;">
                <span>${subj.name}</span>
                <span class="badge ${days < 7 ? 'badge-hard' : 'badge-medium'}">${days} days left</span>
            </div>
            <div class="progress-container" style="height: 6px;">
                <div class="progress-bar" style="width: ${subj.progress}%"></div>
            </div>
        `;
        list.appendChild(item);
    });
}

async function markComplete(topicId) {
    try {
        await api.put(`/progress/${topicId}`, { status: 'Completed' });
        showToast('Task marked as completed! 🎉');
        loadDashboardData();
    } catch (error) {
        showToast(error.message, 'error');
    }
}
