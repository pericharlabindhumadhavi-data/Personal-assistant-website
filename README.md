# My Personal Assistant Dashboard 🧠

A Flask-based personal assistant web application with login authentication, notes, habits, weather, dictionary, jokes, quotes, music, calendar, and news all in one polished dashboard with video background and dark/light mode toggle.

## Overview
This project is a personal productivity dashboard built with Flask and SQLite.  
It allows users to log in and access multiple assistant tools — including notes, habits, weather, dictionary, jokes, quotes, music, calendar, and news all from a single homepage.  
The dashboard features a video background, modular panels, and a dark/light mode toggle for a modern user experience.

## Features
- 🎥 **Video background login page:** Modern UI with floating login form over video.
- 🔐 **User authentication:** Register, login, logout, and secure session management.
- 🏠 **Dashboard homepage:** Central hub with multiple assistant panels.
- 🌦 **Weather panel:** Enter a location and get current weather information.
- 💡 **Daily quote panel:** Displays motivational quotes with a refresh option.
- 😂 **Joke panel:** Shows a joke with “Tell me another” button.
- 📰 **Latest news panel:** Displays headlines from multiple sources with refresh option.
- 📖 **Dictionary panel:** Search for word meanings and example usage.
- ✅ **To‑Do list panel:** Add and manage personal tasks.
- 🎵 **Mood music panel:** Choose a vibe and play curated YouTube music.
- 📅 **Calendar panel:** Add events to specific dates.
- 📊 **Habit tracker panel:** Create habits and track daily progress.
- 📝 **Notes panel:** Write and save personal notes.
- 🌗 **Dark/Light mode toggle:** Switch between light and dark themes.
- 📁 **Modular project structure:** Templates, static assets, and separate databases.
- 💾 **SQLite databases:** `users.db`, `notes.db`, `habits.db` for persistent storage.
- 🌐 **Flask backend:** Routes for authentication, notes, habits, and dashboard features.

## Tech Stack
- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, JavaScript  
- **UI Enhancements:** Video backgrounds, dark/light mode toggle  
- **Version Control:** Git & GitHub  

## Project Structure

- **app.py** → Main Flask application file  
- **templates/** → HTML templates  
  - index.html  
  - login.html  
  - register.html  
  - dashboard.html  
- **static/** → Static assets (CSS, JS, videos)  
  - css/style.css  
  - js/script.js  
  - loginpage.mp4  
  - homepage.mp4  
- **users.db** → Database for user accounts  
- **notes.db** → Database for notes  
- **habits.db** → Database for habits  
- **requirements.txt** → Python dependencies  
- **.gitignore** → Git ignore rules  

## Project Structure
<pre>
├── app.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── loginpage.mp4
│   └── homepage.mp4
├── users.db
├── notes.db
├── habits.db
├── requirements.txt
└── .gitignore
<pre>

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pericharlabindhumadhavi-data/personal-assistant-website.git
   cd personal-assistant-website
pip install -r requirements.txt
py app.py
http://127.0.0.1:5000
