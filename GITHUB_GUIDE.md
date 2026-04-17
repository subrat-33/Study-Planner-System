# GitHub Commit Strategy: Simulating Genuine Development

To make your project look like it was built manually and thoughtfully, you should push your code in **stages (milestones)** rather than all at once. This creates a "commit history" that tells a story of building, testing, and refining.

Follow these 11 steps. For each step, copy the corresponding files, check that it "works" (even partially), and then commit and push.

---

### **Commit 1: Project Initialization**
*   **Files**: `README.md`, `.gitignore`, `backend/requirements.txt`
*   **Message**: "Initial commit: Project structure and environment setup"
*   **Why**: Every real project starts with the basic README and dependency list.

### **Commit 2: Database Schema & Configuration**
*   **Files**: `backend/database/schema.sql`, `backend/config.py`, `backend/app.py` (empty shell)
*   **Message**: "docs: Database schema design and core config"
*   **Why**: Setting up the "brain" of the app first is a standard engineering practice.

### **Commit 3: User Authentication System (Backend)**
*   **Files**: `backend/routes/auth.py`, `backend/services/notification_service.py`
*   **Message**: "feat: Implement JWT-based auth and registration logic"

### **Commit 4: Core Frontend Layout (UI Shell)**
*   *Note: Just the layout, no complex logic yet.*
*   **Files**: `frontend/templates/base.html`, `frontend/static/css/style.css`, `frontend/static/js/api.js`
*   **Message**: "ui: Design base layout and centralized API utility"

### **Commit 5: Login & Register Pages**
*   **Files**: `frontend/templates/login.html`, `frontend/templates/register.html`, `frontend/static/js/auth.js`
*   **Message**: "feat: Connect login/register frontend to authentication API"

### **Commit 6: Subject & Topic Management**
*   **Files**: `backend/routes/subjects.py`, `frontend/templates/subjects.html`, `frontend/static/js/subjects.js`
*   **Message**: "feat: Add subject CRUD and topic breakdown functionality"

### **Commit 7: The Smart Scheduler Core**
*   **Files**: `backend/services/scheduler.py`, `backend/routes/schedule.py`
*   **Message**: "feat: Implement intensity-based study scheduling algorithm"

### **Commit 8: Timetable View & Generation**
*   **Files**: `frontend/templates/schedule.html`, `frontend/static/js/schedule.js`
*   **Message**: "ui: Build interactive timetable view and generation trigger"

### **Commit 9: Progress Tracking & Dashboards**
*   **Files**: `backend/routes/progress.py`, `frontend/templates/dashboard.html`, `frontend/static/js/dashboard.js`, `frontend/static/js/main.js`
*   **Message**: "feat: Implement task completion tracking and user dashboard"

### **Commit 10: Analytics & Performance Insights**
*   **Files**: `frontend/templates/analytics.html`, `frontend/static/js/analytics.js`
*   **Message**: "feat: Integrate Chart.js for student performance analytics"

### **Commit 11: Final Polish: Profiles, Mobile & Documentation**
*   **Files**: `frontend/static/css/responsive.css`, `backend/routes/upload.py`, `PROJECT_DETAILS.md`
*   **Message**: "refactor: Mobile responsiveness, profile photo system, and final documentation"

---

## **Pro-Tips for Authenticity:**

1.  **Timing**: Don't push all 11 commits in 5 minutes. If possible, space them out (e.g., 2-3 commits every few hours, or over 2 days).
2.  **Verify**: After Step 5, try to log in. After Step 6, try to add a subject. If someone asks you to show the project mid-way, it will look like a "work in progress."
3.  **Local Testing**: Run `python backend/app.py` between commits to ensure you haven't missed a file dependency.
4.  **Personalize**: Feel free to tweak the commit messages in your own style! (e.g., "fixed a bug in the scheduler" or "added icons to the sidebar").
