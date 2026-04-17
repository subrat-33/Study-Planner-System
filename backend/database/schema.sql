-- Smart Study Planner Database Schema

CREATE DATABASE IF NOT EXISTS study_planner;
USE study_planner;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(100),
  profile_picture_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_settings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL UNIQUE,
  study_hours_per_day DECIMAL(3,1) DEFAULT 3.0,
  study_start_time TIME DEFAULT '09:00:00',
  study_end_time TIME DEFAULT '22:00:00',
  exam_date DATE,
  learning_style ENUM('Visual', 'Reading', 'Practical', 'Mixed') DEFAULT 'Mixed',
  break_duration_minutes INT DEFAULT 15,
  email_notifications BOOLEAN DEFAULT TRUE,
  browser_notifications BOOLEAN DEFAULT TRUE,
  daily_summary BOOLEAN DEFAULT TRUE,
  deadline_alerts BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE subjects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL,
  deadline DATE NOT NULL,
  total_topics INT DEFAULT 0,
  weekly_hours DECIMAL(3,1) NOT NULL,
  description TEXT,
  color VARCHAR(7) DEFAULT '#4F46E5',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX (user_id, deadline)
);

CREATE TABLE topics (
  id INT PRIMARY KEY AUTO_INCREMENT,
  subject_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  estimated_hours DECIMAL(3,1) NOT NULL,
  difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL,
  priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
  status ENUM('Pending', 'In Progress', 'Completed', 'Skipped', 'Revision') DEFAULT 'Pending',
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
  INDEX (subject_id, status)
);

CREATE TABLE schedules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  schedule_json LONGTEXT,
  total_hours_planned DECIMAL(5,1),
  status ENUM('Active', 'Archived', 'Superseded') DEFAULT 'Active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX (user_id, status)
);

CREATE TABLE schedule_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  schedule_id INT NOT NULL,
  user_id INT NOT NULL, -- ADDED THIS LINE
  subject_id INT NOT NULL,
  topic_id INT NOT NULL,
  day_of_week INT NOT NULL,
  schedule_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  duration_hours DECIMAL(3,1),
  status ENUM('Pending', 'Completed', 'Skipped', 'Rescheduled') DEFAULT 'Pending',
  completed_at TIMESTAMP NULL,
  hours_taken DECIMAL(3,1),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- FOREIGN KEYS
  FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- ADDED THIS LINE
  FOREIGN KEY (subject_id) REFERENCES subjects(id),
  FOREIGN KEY (topic_id) REFERENCES topics(id),
  -- INDEXES (Now they will work!)
  INDEX (schedule_date, user_id),
  INDEX (status, user_id)
);


CREATE TABLE progress (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  topic_id INT NOT NULL,
  status ENUM('Pending', 'Completed', 'Skipped', 'Revision') DEFAULT 'Pending',
  completed_at TIMESTAMP NULL,
  hours_taken DECIMAL(3,1),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
  INDEX (user_id, status),
  UNIQUE (user_id, topic_id)
);

CREATE TABLE notifications (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  notification_type ENUM('Task Reminder', 'Daily Summary', 'Missed Task', 'Schedule Adjusted', 'Deadline Alert', 'Exam Countdown') NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX (user_id, is_read, created_at)
);

CREATE TABLE rescheduling_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  old_schedule_id INT,
  new_schedule_id INT,
  topic_id INT,
  old_date DATE,
  new_date DATE,
  old_time TIME,
  new_time TIME,
  reason VARCHAR(200),
  status ENUM('Accepted', 'Rejected', 'Pending') DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (topic_id) REFERENCES topics(id),
  INDEX (user_id, created_at)
);
