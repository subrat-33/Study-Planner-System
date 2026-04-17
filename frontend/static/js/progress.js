// Progress Tracker Logic

document.addEventListener('DOMContentLoaded', () => {
    loadProgressData();
});

async function loadProgressData() {
    const container = document.getElementById('progress-list-container');
    
    try {
        const subjects = await api.get('/subjects');
        
        if (subjects.length === 0) {
            container.innerHTML = `
                <div class="card" style="text-align: center; padding: 60px;">
                    <i class="fas fa-book-reader" style="font-size: 3rem; color: var(--gray-300); margin-bottom: 20px;"></i>
                    <h3>No subjects added yet</h3>
                    <p style="color: var(--gray-500); margin-bottom: 24px;">Add some subjects to start tracking your progress.</p>
                    <a href="/subjects" class="btn btn-primary">Go to Subjects</a>
                </div>
            `;
            return;
        }

        container.innerHTML = '';
        let totalTopics = 0;
        let completedTopics = 0;

        for (const subject of subjects) {
            const topics = await api.get(`/subjects/${subject.id}/topics`);
            
            const subjTotal = topics.length;
            const subjCompleted = topics.filter(t => t.status === 'Completed').length;
            
            totalTopics += subjTotal;
            completedTopics += subjCompleted;

            const section = document.createElement('div');
            section.className = 'card progress-card';
            section.style.borderLeftColor = subject.color || 'var(--primary)';
            
            const progressPct = subjTotal > 0 ? Math.round((subjCompleted / subjTotal) * 100) : 0;

            section.innerHTML = `
                <div class="flex justify-between align-center" style="margin-bottom: 16px;">
                    <div>
                        <h2 style="margin: 0;">${subject.name}</h2>
                        <p style="font-size: 0.875rem; color: var(--gray-500);">${subjCompleted} of ${subjTotal} topics completed</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-weight: 800; color: var(--primary); font-size: 1.25rem;">${progressPct}%</span>
                    </div>
                </div>
                
                <div class="progress-container" style="height: 10px; margin-bottom: 24px;">
                    <div class="progress-bar" style="width: ${progressPct}%"></div>
                </div>

                <div class="topics-list flex flex-column gap-sm">
                    ${topics.length > 0 ? 
                        topics.map(topic => `
                            <div class="topic-item ${topic.status === 'Completed' ? 'completed' : ''}">
                                <div class="flex align-center gap-md">
                                    <input type="checkbox" class="completion-checkbox" 
                                           ${topic.status === 'Completed' ? 'checked' : ''} 
                                           onchange="handleTopicToggle(${topic.id}, this.checked)">
                                    <div>
                                        <div style="font-weight: 500;">${topic.name}</div>
                                        <div style="font-size: 0.75rem; color: var(--gray-500);">${topic.estimated_hours} hrs • ${topic.priority} Priority</div>
                                    </div>
                                </div>
                                <span class="status-badge ${topic.status === 'Completed' ? 'status-completed' : 'status-pending'}">
                                    ${topic.status}
                                </span>
                            </div>
                        `).join('') 
                        : '<p style="color: var(--gray-400); font-style: italic;">No topics added for this subject.</p>'
                    }
                </div>
            `;
            container.appendChild(section);
        }

        // Update overall stats
        document.getElementById('total-topics-count').innerText = totalTopics;
        document.getElementById('completed-topics-count').innerText = completedTopics;
        document.getElementById('remaining-topics-count').innerText = totalTopics - completedTopics;
        const overallPct = totalTopics > 0 ? Math.round((completedTopics / totalTopics) * 100) : 0;
        document.getElementById('overall-percentage').innerText = `${overallPct}%`;

    } catch (error) {
        console.error('Failed to load progress:', error);
        showToast('Error loading progress data', 'error');
    }
}

async function handleTopicToggle(topicId, isChecked) {
    const status = isChecked ? 'Completed' : 'Pending';
    
    try {
        await api.put(`/progress/${topicId}`, { status });
        showToast(`Topic marked as ${status}`);
        // Refresh after a short delay to show updated stats
        setTimeout(loadProgressData, 500);
    } catch (error) {
        showToast('Failed to update progress', 'error');
        // Revert checkbox if failed
        loadProgressData();
    }
}
