# Smart Study Planner

An AI-powered personal study assistant for students to automatically generate optimized study timetables, manage deadlines, and track progress.

## Features
- **Intelligent Scheduling:** Rule-based priority algorithm to distribute topics.
- **Adaptive Rescheduling:** Detects missed tasks and recalibrates your plan.
- **Visual Analytics:** Chart.js powered insights into study habits.
- **Subject & Syllabus Management:** Group topics by subject with difficulty levels.
- **Dashboard:** At-a-glance view of today's tasks and upcoming deadlines.

## Tech Stack
- **Frontend:** HTML5, Vanilla CSS3, Vanilla JS (ES6+)
- **Backend:** Python Flask
- **Database:** MySQL
- **Auth:** JWT (JSON Web Tokens)

## Getting Started

### 1. Prerequisites
- Python 3.8+
- MySQL Server

### 2. Database Setup
1. Open your MySQL client.
2. Run the script in `backend/database/schema.sql`.

### 3. Backend Setup
1. Navigate to the `backend` folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env` file (if needed) or edit `config.py`.

### 4. Run the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure
- `frontend/`: All client-side code (HTML, CSS, JS).
- `backend/`: Flask server, API routes, and logic.
- `backend/services/`: Core algorithms for scheduling.
- `backend/database/`: SQL schema and initialization scripts.
