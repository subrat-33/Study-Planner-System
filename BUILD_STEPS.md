# 🛠️ Smart Study Planner: Step-by-Step Build Guide

Follow this strictly linear path to build the application from scratch. This sequence ensures each piece builds on a working foundation.

---

### Step 1: Project Structure & Initialization
*   **Action**: Create `backend/` and `frontend/` directories.
*   **Action**: Initialize a Git repository (`git init`).
*   **Action**: Create a `.gitignore` to skip `venv`, `__pycache__`, and `.env` files.
*   **Commit Message**: `chore: initial project structure and git setup`

---

### Step 2: Backend Environment
*   **Action**: Inside `backend/`, create a virtual environment: `python -m venv venv`.
*   **Action**: Activate it and install dependencies: `pip install flask flask-cors mysql-connector-python PyJWT bcrypt`.
*   **Action**: Save them: `pip freeze > requirements.txt`.
*   **Commit Message**: `chore: setup python virtualenv and dependencies`

---

### Step 3: Database Foundation
*   **Action**: Open MySQL Workbench/CLI.
*   **Action**: Run the `backend/database/schema.sql` script to create your tables.
*   **Action**: Create a `backend/config.py` file with your DB credentials (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
*   **Commit Message**: `feat: initialize database schema and configuration`

---

### Step 4: The Main Entry Point
*   **Action**: Create `backend/app.py`.
*   **Action**: Setup basic Flask app with `CORS` enabled.
*   **Action**: Add a "health check" route: `@app.route('/')`.
*   **Commit Message**: `feat: setup initial flask entry point`

---

### Step 5: Backend Authentication
*   **Action**: Create `backend/routes/auth.py`.
*   **Action**: Write logic for `/register` (hashing password with `bcrypt`) and `/login` (generating a `JWT` token).
*   **Action**: Register this blueprint in `app.py`.
*   **Commit Message**: `feat: implement JWT-based user authentication logic`

---

### Step 6: Frontend Authentication Pages
*   **Action**: Create `frontend/templates/login.html` and `register.html`.
*   **Action**: Use a simple form layout with `email` and `password` fields.
*   **Commit Message**: `feat: add login and registration templates`

---

### Step 7: Connection Logic (JS Auth)
*   **Action**: Create `frontend/static/js/auth.js`.
*   **Action**: Write the `login()` function that `fetch`es the backend token and saves it to `localStorage`.
*   **Commit Message**: `feat: connect frontend auth to backend API`

---

### Step 8: Subject Management (Backend)
*   **Action**: Create `backend/routes/subjects.py`.
*   **Action**: Implement `GET /subjects` (list) and `POST /subjects` (create).
*   **Action**: Add a `token_required` decorator to protect these routes.
*   **Commit Message**: `feat: implement protected API routes for subject management`

---

### Step 9: Subject Management (Frontend)
*   **Action**: Create `frontend/templates/subjects.html`.
*   **Action**: Build a UI to input subject names, category, and difficulty level.
*   **Commit Message**: `feat: add UI for managing academic subjects`

---

### Step 10: Topic Management (Backend)
*   **Action**: Create `backend/routes/topics.py`.
*   **Action**: Build routes to link multiple "Topics" (chapters) to a specific "Subject".
*   **Commit Message**: `feat: implement backend support for subject topics`

---

### Step 11: The Core Algorithm (The Brain)
*   **Action**: Create `backend/services/scheduler.py`.
*   **Action**: Write the logic to calculate `priority_score` for each topic.
*   **Action**: Implement a function that distributes these topics across available study hours.
*   **Commit Message**: `feat: develop core priority-based scheduling algorithm`

---

### Step 12: Schedule Generation Route
*   **Action**: Create `backend/routes/schedule.py`.
*   **Action**: Add a route that triggers the `scheduler.py` logic and saves the daily sessions into the database.
*   **Commit Message**: `feat: add endpoint to generate and save study plans`

---

### Step 13: Timetable Visualization
*   **Action**: Create `frontend/templates/schedule.html`.
*   **Action**: Use JavaScript to render the fetched study sessions into a clean, grid-based timetable.
*   **Commit Message**: `feat: implement interactive study schedule viewer`

---

### Step 14: Progress Tracking Logic
*   **Action**: Create `backend/routes/progress.py`.
*   **Action**: Implement a route to update a session status (e.g., `completed = true`).
*   **Commit Message**: `feat: implement progress tracking API`

---

### Step 15: Progress UI (Checkboxes)
*   **Action**: Update the schedule UI to include a "Mark as Done" button or checkbox for each session.
*   **Commit Message**: `feat: allow users to mark study topics as completed`

---

### Step 16: The Dashboard (Home)
*   **Action**: Create `frontend/templates/dashboard.html`.
*   **Action**: Aggregate data to show stats like "3 Tasks Done Today" and "Next Subject: Physics at 4 PM".
*   **Commit Message**: `feat: add main dashboard with summary statistics`

---

### Step 17: Data Visualization (Analytics)
*   **Action**: Create `backend/routes/analytics.py`.
*   **Action**: Write a route that returns the count of completed topics per subject.
*   **Commit Message**: `feat: implement analytics backend for progress reporting`

---

### Step 18: Charts Integration
*   **Action**: Create `frontend/templates/analytics.html`.
*   **Action**: Use **Chart.js** to display a Pie chart of your syllabus completion.
*   **Commit Message**: `feat: visualize study progress with Chart.js analytics`

---

### Step 19: Adaptive Logic (Reschedule)
*   **Action**: Create `backend/services/reschedule.py`.
*   **Action**: Write logic to detect "Missed" sessions and move them to tomorrow automatically.
*   **Commit Message**: `feat: implement adaptive rescheduling for missed tasks`

---

### Step 20: Final UI/UX Polish
*   **Action**: Apply the final `style.css` (Indigo theme, custom fonts, glassmorphism).
*   **Action**: Add mobile responsiveness using CSS Media Queries.
*   **Action**: Finalize the `README.md` with setup instructions.
*   **Commit Message**: `style: final UI polish and mobile responsiveness`

