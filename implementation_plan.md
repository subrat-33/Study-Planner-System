# Implementation Plan - Smart Study Planner

## 1. Project Setup & Infrastructure
- [ ] Create directory structure for `backend/` and `frontend/`
- [ ] Set up Python virtual environment and `requirements.txt`
- [ ] Initialize MySQL database with `schema.sql`
- [ ] Configure environment variables (`.env`)

## 2. Backend Development (Flask)
- [ ] **Infrastructure:**
    - [ ] `app.py` entry point
    - [ ] Configuration management (`config.py`)
    - [ ] Database connection utility
- [ ] **Authentication (JWT):**
    - [ ] Register/Login endpoints
    - [ ] Token verification middleware
    - [ ] Password hashing with bcrypt
- [ ] **Subject & Topic Management:**
    - [ ] CRUD for Subjects
    - [ ] CRUD for Topics
- [ ] **Scheduling Engine:**
    - [ ] Core priority calculation logic
    - [ ] Topic distribution algorithm
    - [ ] Schedule generation and storage
- [ ] **Progress & Analytics:**
    - [ ] Progress update endpoints
    - [ ] Analytics data aggregation
- [ ] **Notifications:**
    - [ ] Notification storage and retrieval

## 3. Frontend Development (HTML/CSS/JS)
- [ ] **Design System:**
    - [ ] `colors.css` - CSS Variables for Indigo theme
    - [ ] `style.css` - Global resets and base typography
    - [ ] `components.css` - Reusable cards, buttons, forms
- [ ] **Layout:**
    - [ ] `base.html` - Navigation, Sidebar, Footer skeleton
- [ ] **Pages:**
    - [ ] Auth: `login.html`, `register.html`
    - [ ] Home: `dashboard.html`
    - [ ] Management: `subjects.html`, `schedule.html`
    - [ ] Tracking: `progress.html`, `analytics.html`
    - [ ] User: `settings.html`, `notifications.html`
- [ ] **Interactivity (Vanilla JS):**
    - [ ] `api.js` - Centralized Fetch wrapper
    - [ ] `auth.js` - JWT handling and redirect logic
    - [ ] `dashboard.js` - Interactive widgets and summaries
    - [ ] `schedule.js` - Timetable grid generation (Weekly/Daily)
    - [ ] `analytics.js` - Chart.js integration

## 4. Core Algorithm Implementation
- [ ] `scheduler.py`:
    - [ ] `priority_score = (difficulty_multiplier * estimated_hours) / days_remaining`
    - [ ] Load balancing across study hours
- [ ] `reschedule.py`:
    - [ ] Detection of missed tasks
    - [ ] Catch-up logic

## 5. Polish & Finalization
- [ ] Mobile responsiveness (`responsive.css`)
- [ ] Input validation (Frontend & Backend)
- [ ] UI feedback (Toasts, Spinners)
- [ ] Documentation (README.md)
