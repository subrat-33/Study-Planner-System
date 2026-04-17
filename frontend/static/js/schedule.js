// Timetable Display Logic

document.addEventListener('DOMContentLoaded', () => {
    loadSchedule();

    const exportBtn = document.getElementById('btn-export-pdf');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            window.print();
        });
    }
});

let currentSchedule = [];

async function loadSchedule() {
    try {
        const schedule = await api.get('/schedule');
        currentSchedule = schedule;
        
        if (schedule.length === 0) {
            document.getElementById('empty-state').style.display = 'block';
            document.getElementById('weekly-view').style.display = 'none';
        } else {
            document.getElementById('empty-state').style.display = 'none';
            document.getElementById('weekly-view').style.display = 'block';
            renderWeeklyGrid(schedule);
            renderDailyView(schedule);
            renderSubjectView(schedule);
        }
    } catch (error) {
        console.error('Failed to load schedule:', error);
    }
}

function renderWeeklyGrid(schedule) {
    const gridBody = document.getElementById('grid-body');
    if (!gridBody) return;
    gridBody.innerHTML = '';

    // Create time rows from 9 AM to 9 PM
    for (let hour = 9; hour <= 21; hour++) {
        const timeStr = `${hour % 12 || 12} ${hour >= 12 ? 'PM' : 'AM'}`;
        
        // Time Label Cell
        const timeCell = document.createElement('div');
        timeCell.className = 'time-col';
        timeCell.innerText = timeStr;
        gridBody.appendChild(timeCell);

        // Days Cells
        for (let day = 0; day < 7; day++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            
            // Find if any task starts at this hour/day
            // Week starts on Monday (JS date logic)
            const item = schedule.find(it => {
                const itDate = new Date(it.date);
                const itDay = (itDate.getDay() + 6) % 7; // Monday = 0
                const itHour = parseInt(it.start_time.split(':')[0]);
                return itDay === day && itHour === hour;
            });

            if (item) {
                const taskEl = document.createElement('div');
                taskEl.className = 'schedule-item';
                taskEl.style.backgroundColor = item.color || 'var(--primary)';
                taskEl.innerHTML = `
                    <div class="item-subject">${item.subject_name}</div>
                    <div class="item-topic">${item.topic_name}</div>
                `;
                taskEl.onclick = () => openTaskDetails(item);
                cell.appendChild(taskEl);
            }

            gridBody.appendChild(cell);
        }
    }
}

async function generateSchedule() {
    const btn = document.getElementById('btn-generate-schedule');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    btn.disabled = true;

    try {
        await api.post('/schedule/generate', {});
        showToast('New schedule generated!');
        loadSchedule();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function openTaskDetails(item) {
    document.getElementById('task-modal-title').innerText = item.topic_name;
    document.getElementById('task-subj').innerText = item.subject_name;
    document.getElementById('task-topic').innerText = item.topic_name;
    document.getElementById('task-time').innerText = `${item.date} at ${item.start_time}`;
    document.getElementById('task-duration').innerText = item.duration;
    
    toggleTaskModal(true);
}

function toggleTaskModal(show) {
    const modal = document.getElementById('task-modal');
    if (show) modal.classList.add('active');
    else modal.classList.remove('active');
}

function switchView(view) {
    const weekly = document.getElementById('weekly-view');
    const daily = document.getElementById('daily-view');
    const subject = document.getElementById('subject-view');
    
    [weekly, daily, subject].forEach(el => el.style.display = 'none');
    document.querySelectorAll('.view-toggles button').forEach(b => b.classList.remove('active'));

    if (view === 'weekly') {
        weekly.style.display = 'block';
        document.querySelector('[onclick="switchView(\'weekly\')"]').classList.add('active');
    } else if (view === 'daily') {
        daily.style.display = 'block';
        document.querySelector('[onclick="switchView(\'daily\')"]').classList.add('active');
    } else {
        subject.style.display = 'block';
        document.querySelector('[onclick="switchView(\'subject\')"]').classList.add('active');
    }
}

function renderDailyView(schedule) {
    const container = document.getElementById('daily-view');
    if (!container) return;
    container.innerHTML = '';

    // Group by date
    const grouped = {};
    schedule.forEach(item => {
        if (!grouped[item.date]) grouped[item.date] = [];
        grouped[item.date].push(item);
    });

    const sortedDates = Object.keys(grouped).sort();

    sortedDates.forEach(date => {
        const dateObj = new Date(date);
        const dateStr = dateObj.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
        
        const daySection = document.createElement('div');
        daySection.className = 'card';
        daySection.style.marginBottom = '20px';
        daySection.innerHTML = `
            <h3 style="margin-bottom: 16px; border-bottom: 2px solid var(--gray-100); padding-bottom: 8px;">${dateStr}</h3>
            <div class="daily-tasks flex flex-column gap-sm">
                ${grouped[date].sort((a,b) => a.start_time.localeCompare(b.start_time)).map(item => `
                    <div class="topic-item" style="cursor: pointer; padding: 12px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid ${item.color}" onclick="openTaskDetails(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                        <div class="flex justify-between">
                            <div>
                                <strong style="color: ${item.color}">${item.subject_name}</strong>
                                <div style="font-weight: 500;">${item.topic_name}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: 700; color: var(--gray-700);">${item.start_time.substring(0, 5)} - ${item.end_time ? item.end_time.substring(0, 5) : ''}</div>
                                <div style="font-size: 0.75rem; color: var(--gray-400);">${item.duration} hrs</div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(daySection);
    });
}

function renderSubjectView(schedule) {
    const container = document.getElementById('subject-view');
    if (!container) return;
    container.innerHTML = '';

    // Group by subject
    const grouped = {};
    schedule.forEach(item => {
        if (!grouped[item.subject_id]) grouped[item.subject_id] = { name: item.subject_name, color: item.color, items: [] };
        grouped[item.subject_id].items.push(item);
    });

    Object.values(grouped).forEach(subject => {
        const subjSection = document.createElement('div');
        subjSection.className = 'card';
        subjSection.style.marginBottom = '20px';
        subjSection.style.borderTop = `4px solid ${subject.color}`;
        
        subjSection.innerHTML = `
            <h3 style="margin-bottom: 16px;">${subject.name}</h3>
            <div class="subject-tasks flex flex-column gap-sm">
                ${subject.items.sort((a,b) => a.date.localeCompare(b.date) || a.start_time.localeCompare(b.start_time)).map(item => `
                    <div class="topic-item" style="cursor: pointer; padding: 12px; background: var(--gray-50); border-radius: 8px;" onclick="openTaskDetails(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                        <div class="flex justify-between align-center">
                            <div>
                                <div style="font-weight: 600;">${item.topic_name}</div>
                                <div style="font-size: 0.8rem; color: var(--gray-500);">${new Date(item.date).toLocaleDateString()}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: 600; color: var(--primary);">${item.start_time.substring(0, 5)}</div>
                                <div style="font-size: 0.75rem; color: var(--gray-400);">${item.duration} hrs</div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(subjSection);
    });
}
