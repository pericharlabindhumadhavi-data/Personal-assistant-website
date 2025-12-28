import requests
import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session handling
 # --- Users DB setup ---
def init_users_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_users_db()

# Landing page at /
@app.route("/")
def landing():
    return render_template("home.html")

# Dashboard at /dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("index.html")
    return redirect(url_for("login"))



# Weather API key (hard-coded)
API_KEY = "c99719ce609ea56a318477d5050fe9e3"

@app.route("/")
def home():
    return render_template("index.html")
# --- Auth routes ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            return render_template("register.html", error="Username and password required")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already exists")
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))   # ✅ add this here

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# --- Weather Assistant ---
@app.route("/assistant", methods=["POST"])
def assistant():
    user_input = request.form.get("query", "").lower()

    if "weather" in user_input:
        city = "hyderabad"
        words = user_input.split()
        if "in" in words:
            idx = words.index("in")
            if idx + 1 < len(words):
                city = words[idx + 1]

        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url).json()

        if not geo_data or isinstance(geo_data, dict):
            return jsonify({"reply": f"City '{city}' not found or API error."})

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather = requests.get(weather_url).json()

        if "main" in weather:
            temp = weather["main"]["temp"]
            desc = weather["weather"][0]["description"]
            return jsonify({"reply": f"The weather in {city.title()} is {temp}°C with {desc}."})
        else:
            return jsonify({"reply": f"Couldn't fetch weather for {city}."})

    return jsonify({"reply": "Try asking: weather in Delhi"})

# --- Quotes route ---
@app.route("/quote", methods=["GET"])
def quote():
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=5)
        data = response.json()
        quote_data = data[0]
        return jsonify({
            "quote": quote_data["q"],
            "author": quote_data["a"]
        })
    except Exception:
        return jsonify({
            "quote": "Couldn't fetch a quote right now.",
            "author": ""
        })

# --- Joke route ---
@app.route("/joke", methods=["GET"])
def joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        res = requests.get(url, timeout=5)
        data = res.json()
        return jsonify({
            "setup": data.get("setup", "Couldn't fetch a joke."),
            "punchline": data.get("punchline", "")
        })
    except Exception:
        return jsonify({
            "setup": "Why did the developer go broke?",
            "punchline": "Because they used up all their cache."
        })

# --- News route ---
@app.route("/news", methods=["GET"])
def news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=113c8ab78e6248a9a7ca439077912b19"
        res = requests.get(url, timeout=5)
        data = res.json()
        articles = data.get("articles", [])
        headlines = []
        for a in articles[:5]:
            headlines.append({
                "title": a["title"],
                "source": a["source"]["name"]
            })
        return jsonify({"headlines": headlines})
    except Exception as e:
        print("Error:", e)
        return jsonify({"headlines": []})

# --- Dictionary route ---
@app.route("/dictionary", methods=["GET"])
def dictionary():
    word = request.args.get("word", "")
    if not word:
        return jsonify({"error": "No word provided"})
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        res = requests.get(url, timeout=5)
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            example = data[0]["meanings"][0]["definitions"][0].get("example", "")
            return jsonify({
                "word": word,
                "meaning": meaning,
                "example": example
            })
        else:
            return jsonify({"word": word, "meaning": "No definition found", "example": ""})
    except Exception as e:
        print("Error:", e)
        return jsonify({"word": word, "meaning": "Couldn't fetch definition", "example": ""})

# --- To-do list route ---
@app.route("/tasks", methods=["GET", "POST", "PUT", "DELETE"])
def todo():
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()

    if request.method == "GET":
        c.execute("SELECT id, task, done FROM tasks")
        rows = c.fetchall()
        conn.close()
        tasks = [{"id": r[0], "task": r[1], "done": bool(r[2])} for r in rows]
        return jsonify({"tasks": tasks})

    if request.method == "POST":
        new_task = request.json.get("task", "")
        if new_task:
            c.execute("INSERT INTO tasks (task) VALUES (?)", (new_task,))
            conn.commit()
        conn.close()
        return jsonify({"status": "added"})

    if request.method == "PUT":
        task_id = request.json.get("id")
        done = request.json.get("done", False)
        c.execute("UPDATE tasks SET done=? WHERE id=?", (int(done), task_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "updated"})

    if request.method == "DELETE":
        task_id = request.json.get("id")
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "deleted"})



# --- Habit Tracker ---
def init_habit_db():
    conn = sqlite3.connect("habits.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            day INTEGER,
            status TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    """)
    conn.commit()
    conn.close()

init_habit_db()
# Handle GET (list habits) and POST (add habit) in one route
@app.route("/habits", methods=["GET", "POST"])
def habits():
    conn = sqlite3.connect("habits.db")
    c = conn.cursor()

    if request.method == "POST":
        habit = request.json.get("habit", "")
        if habit:
            c.execute("INSERT INTO habits (habit) VALUES (?)", (habit,))
            conn.commit()
            conn.close()
            return jsonify({"status": "habit added"})
        conn.close()
        return jsonify({"status": "no habit provided"})

    # GET
    c.execute("SELECT id, habit FROM habits")
    rows = c.fetchall()
    conn.close()
    habits = [{"id": r[0], "habit": r[1]} for r in rows]
    return jsonify({"habits": habits})

# Delete a habit by ID
@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    conn = sqlite3.connect("habits.db")
    c = conn.cursor()
    # Delete logs tied to this habit
    c.execute("DELETE FROM habit_logs WHERE habit_id=?", (habit_id,))
    # Delete the habit itself
    c.execute("DELETE FROM habits WHERE id=?", (habit_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "habit deleted", "habit_id": habit_id})

# Log habit status
@app.route("/habit_logs", methods=["POST"])
def log_habit():
    data = request.get_json(force=True) or {}
    habit_id = data.get("habit_id")
    day = data.get("day")
    status = data.get("status")  # 'done' or 'missed'

    conn = sqlite3.connect("habits.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO habit_logs (habit_id, day, status) VALUES (?, ?, ?)",
              (habit_id, day, status))
    conn.commit()
    conn.close()
    return jsonify({"status": "logged"})

# Get logs for a habit
@app.route("/habit_logs/<int:habit_id>", methods=["GET"])
def get_habit_logs(habit_id):
    conn = sqlite3.connect("habits.db")
    c = conn.cursor()
    c.execute("SELECT day, status FROM habit_logs WHERE habit_id=?", (habit_id,))
    rows = c.fetchall()
    conn.close()
    logs = {r[0]: r[1] for r in rows}
    return jsonify({"habit_id": habit_id, "logs": logs})
# --- Notes DB setup ---
def init_notes_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_notes_db()
# --- Notes Routes ---
@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    if request.method == "POST":
        content = request.json.get("content", "")
        if content:
            c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            conn.commit()
            conn.close()
            return jsonify({"status": "note added"})
        conn.close()
        return jsonify({"status": "no content provided"})

    # GET
    c.execute("SELECT id, content FROM notes")
    rows = c.fetchall()
    conn.close()
    notes = [{"id": r[0], "content": r[1]} for r in rows]
    return jsonify({"notes": notes})

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "note deleted", "note_id": note_id})

if __name__ == "__main__":
    app.run(debug=True)
