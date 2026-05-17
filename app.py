import requests
import sqlite3
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- Upload Folder ----------
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- USERS DATABASE ----------
def init_users_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

init_users_db()

# ---------- HABITS DATABASE ----------
def init_habits_db():
    conn = sqlite3.connect("users.db")
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
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

init_habits_db()

# ---------- LANDING PAGE ----------
@app.route("/")
def landing():
    return render_template("home.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    photo_url = session.get("photo_url", "uploads/default.jpg")

    return render_template(
        "index.html",
        username=session["user"],
        photo_url=photo_url
    )

# ---------- PHOTO UPLOAD ----------
@app.route("/upload_photo", methods=["POST"])
def upload_photo():

    if "photo" not in request.files:
        return redirect(url_for("dashboard"))

    photo = request.files["photo"]

    if photo.filename == "":
        return redirect(url_for("dashboard"))

    filename = secure_filename(photo.filename)

    photo.save(
        os.path.join(app.config["UPLOAD_FOLDER"], filename)
    )

    session["photo_url"] = f"uploads/{filename}"

    return redirect(url_for("dashboard"))

@app.route("/reset_photo")
def reset_photo():

    session["photo_url"] = "uploads/default.jpg"

    return redirect(url_for("dashboard"))

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not email or not password:
            return render_template(
                "register.html",
                error="All fields required"
            )

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:

            c.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (username, email, password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "register.html",
                error="Username or email already exists"
            )

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            """
            SELECT user_id, password_hash
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        row = c.fetchone()

        conn.close()

        if row and row[1] == password:

            session["user"] = username

            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))

# ---------- WEATHER ----------
API_KEY = "c99719ce609ea56a318477d5050fe9e3"

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

            return jsonify({
                "reply": f"City '{city}' not found"
            })

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        weather = requests.get(weather_url).json()

        if "main" in weather:

            temp = weather["main"]["temp"]

            desc = weather["weather"][0]["description"]

            return jsonify({
                "reply": f"The weather in {city.title()} is {temp}°C with {desc}"
            })

    return jsonify({
        "reply": "Try asking: weather in Delhi"
    })

# ---------- QUOTES ----------
@app.route("/quote")
def quote():

    try:

        res = requests.get(
            "https://zenquotes.io/api/random",
            timeout=5
        )

        data = res.json()[0]

        return jsonify({
            "quote": data["q"],
            "author": data["a"]
        })

    except:

        return jsonify({
            "quote": "Couldn't fetch quote",
            "author": ""
        })

# ---------- JOKES ----------
@app.route("/joke")
def joke():

    try:

        res = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=5
        )

        data = res.json()

        return jsonify({
            "setup": data["setup"],
            "punchline": data["punchline"]
        })

    except:

        return jsonify({
            "setup": "Why did the developer go broke?",
            "punchline": "Because they used up all their cache."
        })

# ---------- NEWS ----------
@app.route("/news")
def news():

    try:

        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=113c8ab78e6248a9a7ca439077912b19"

        res = requests.get(url, timeout=5)

        data = res.json()

        articles = data.get("articles", [])

        headlines = []

        for article in articles[:5]:

            headlines.append({
                "title": article["title"],
                "source": article["source"]["name"]
            })

        return jsonify({
            "headlines": headlines
        })

    except:

        return jsonify({
            "headlines": []
        })

# ---------- DICTIONARY ----------
@app.route("/dictionary")
def dictionary():

    word = request.args.get("word", "")

    if not word:

        return jsonify({
            "error": "No word provided"
        })

    try:

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        res = requests.get(url, timeout=5)

        data = res.json()

        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]

        example = data[0]["meanings"][0]["definitions"][0].get(
            "example",
            ""
        )

        return jsonify({
            "word": word,
            "meaning": meaning,
            "example": example
        })

    except:

        return jsonify({
            "word": word,
            "meaning": "No definition found",
            "example": ""
        })

# ---------- TODO ----------
@app.route("/tasks", methods=["GET", "POST", "PUT", "DELETE"])
def tasks():

    conn = sqlite3.connect("todo.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            done INTEGER DEFAULT 0
        )
    """)

    if request.method == "GET":

        c.execute("SELECT id, task, done FROM tasks")

        rows = c.fetchall()

        tasks = []

        for row in rows:

            tasks.append({
                "id": row[0],
                "task": row[1],
                "done": bool(row[2])
            })

        conn.close()

        return jsonify({
            "tasks": tasks
        })

    if request.method == "POST":

        task = request.json.get("task", "")

        if task:

            c.execute(
                "INSERT INTO tasks(task) VALUES(?)",
                (task,)
            )

            conn.commit()

        conn.close()

        return jsonify({
            "status": "added"
        })

    if request.method == "PUT":

        task_id = request.json.get("id")
        done = request.json.get("done")

        c.execute(
            "UPDATE tasks SET done=? WHERE id=?",
            (int(done), task_id)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "updated"
        })

    if request.method == "DELETE":

        task_id = request.json.get("id")

        c.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "deleted"
        })

# ---------- HABIT TRACKER ----------
@app.route("/habits", methods=["GET", "POST"])
def habits():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    if request.method == "GET":

        c.execute("SELECT id, habit FROM habits")

        rows = c.fetchall()

        habits = []

        for row in rows:

            habits.append({
                "id": row[0],
                "habit": row[1]
            })

        conn.close()

        return jsonify({
            "habits": habits
        })

    if request.method == "POST":

        data = request.get_json()

        habit = data.get("habit")

        c.execute(
            "INSERT INTO habits (habit) VALUES (?)",
            (habit,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "added"
        })

# ---------- DELETE HABIT ----------
@app.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM habits WHERE id=?",
        (habit_id,)
    )

    c.execute(
        "DELETE FROM habit_logs WHERE habit_id=?",
        (habit_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "deleted"
    })

# ---------- GET HABIT LOGS ----------
@app.route("/habit_logs/<int:habit_id>", methods=["GET"])
def get_habit_logs(habit_id):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT day, status
        FROM habit_logs
        WHERE habit_id=?
        """,
        (habit_id,)
    )

    rows = c.fetchall()

    logs = {}

    for row in rows:
        logs[str(row[0])] = row[1]

    conn.close()

    return jsonify({
        "logs": logs
    })

# ---------- UPDATE HABIT LOG ----------
@app.route("/habit_logs", methods=["POST"])
def update_habit_log():

    data = request.get_json()

    habit_id = data.get("habit_id")
    day = data.get("day")
    status = data.get("status")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT id
        FROM habit_logs
        WHERE habit_id=? AND day=?
        """,
        (habit_id, day)
    )

    existing = c.fetchone()

    if existing:

        c.execute(
            """
            UPDATE habit_logs
            SET status=?
            WHERE habit_id=? AND day=?
            """,
            (status, habit_id, day)
        )

    else:

        c.execute(
            """
            INSERT INTO habit_logs (habit_id, day, status)
            VALUES (?, ?, ?)
            """,
            (habit_id, day, status)
        )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "updated"
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )