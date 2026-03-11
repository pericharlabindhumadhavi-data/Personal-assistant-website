# My Personal Assistant Dashboard 🧠

A Flask-based personal assistant web application with login authentication, notes, habits, weather, dictionary, jokes, quotes, music, calendar, and news all in one polished dashboard with video background and dark/light mode toggle.

## Overview
This project is a personal productivity dashboard built with Flask and SQLite.  
It allows users to log in and access multiple assistant tools including notes, habits, weather, dictionary, jokes, quotes, music, calendar, and news all from a single homepage.  
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
- 🎵 **Mood music panel:** Choose a vibe and stream curated Spotify playlists.
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
</pre></pre>

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/pericharlabindhumadhavi-data/personal-assistant-dashboard.git
   ```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
py app.py
```
Open in browser:
http://127.0.0.1:5000


## Usage Guide
- Register a new account or log in with your credentials.
- Access the dashboard with panels for notes, habits, weather, dictionary, jokes, quotes, music, calendar, and news.
- Toggle between dark/light mode for your preferred theme.
- Upload a profile photo or reset to default.


## APIs Used
- **OpenWeather API** → Provides live weather data based on user location.
- **ZenQuotes API** → Supplies motivational quotes for the daily quote panel.
- **NewsAPI** → Fetches latest headlines from multiple sources.
- **Official Joke API** → Delivers random jokes for the joke panel.


## Roadmap
- 🔐 Add secure password hashing (using Werkzeug or bcrypt).
- 📱 Improve mobile responsiveness for dashboard panels.
- ☁️ Deploy to cloud platforms (Heroku, Render, or AWS).
- 📊 Add analytics panel to track user activity and habits.
- 🧠 Integrate AI-powered assistant responses (chat or voice).

