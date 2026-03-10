// Weather form
document.getElementById("assistant-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const res = await fetch("/assistant", { method: "POST", body: form });
  const data = await res.json();
  document.getElementById("response").innerText = data.reply || "No response";
});

// Quotes
document.getElementById("quote-refresh")?.addEventListener("click", async () => {
  try {
    const res = await fetch("/quote");
    const q = await res.json();
    document.getElementById("quote-text").textContent = q.quote || "Keep going.";
    document.getElementById("quote-author").textContent = q.author ? `— ${q.author}` : "";
  } catch (err) {
    document.getElementById("quote-text").textContent = "Couldn't fetch a quote.";
    document.getElementById("quote-author").textContent = "";
  }
});
// Load a quote on page load
document.getElementById("quote-refresh").click();
// Jokes
document.getElementById("joke-refresh")?.addEventListener("click", async () => {
  try {
    const res = await fetch("/joke");
    const j = await res.json();
    document.getElementById("joke-setup").textContent = j.setup || "No joke right now.";
    // Small delay for comedic timing (optional)
    setTimeout(() => {
      document.getElementById("joke-punchline").textContent = j.punchline || "";
    }, 500);
  } catch (err) {
    document.getElementById("joke-setup").textContent = "Couldn't fetch a joke.";
    document.getElementById("joke-punchline").textContent = "";
  }
});
// Load a joke on page load (optional)
document.getElementById("joke-refresh")?.click();
// News
document.getElementById("news-refresh")?.addEventListener("click", async () => {
  try {
    const res = await fetch("/news");
    const n = await res.json();
    const list = document.getElementById("news-list");
    list.innerHTML = ""; // Clear old items
    
    if (n.headlines && n.headlines.length > 0) {
      n.headlines.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.title} — ${item.source}`;
        list.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "No news available right now.";
      list.appendChild(li);
    }
  } catch (err) {
    const list = document.getElementById("news-list");
    list.innerHTML = "<li>Couldn't fetch news.</li>";
  }
});
// Load news on page load
document.getElementById("news-refresh")?.click();
// Dictionary
document.getElementById("dict-search")?.addEventListener("click", async () => {
  const word = document.getElementById("dict-input").value.trim();
  if (!word) return;
  
  try {
    const res = await fetch(`/dictionary?word=${word}`);
    const d = await res.json();
    document.getElementById("dict-meaning").textContent = d.meaning || "No definition found.";
    document.getElementById("dict-example").textContent = d.example || "";
  } catch (err) {
    document.getElementById("dict-meaning").textContent = "Error fetching definition.";
    document.getElementById("dict-example").textContent = "";
  }
});
// To-Do List
const API_URL = "https://69419c70686bc3ca816790ec.mockapi.io/tasks";

async function loadTasks() {
  const res = await fetch(API_URL);
  const tasks = await res.json();
  const list = document.getElementById("todo-list");
  list.innerHTML = "";

  tasks.forEach(t => {
    const li = document.createElement("li");
    li.textContent = t.task;
    if (t.done) li.style.textDecoration = "line-through";

    // Toggle done
    li.addEventListener("click", async () => {
      await fetch(`${API_URL}/${t.id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({done: !t.done})
      });
      loadTasks();
    });

    // Delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "❌";
    delBtn.style.marginLeft = "10px";
    delBtn.addEventListener("click", async () => {
      await fetch(`${API_URL}/${t.id}`, { method: "DELETE" });
      loadTasks();
    });

    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

document.getElementById("todo-add")?.addEventListener("click", async () => {
  const task = document.getElementById("todo-input").value.trim();
  if (!task) return;
  await fetch(API_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({task, done: false})
  });
  document.getElementById("todo-input").value = "";
  loadTasks();
});

// Load tasks on page load
loadTasks();

// mood music player
const playlists = {
  chill: "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",   // Chill Hits
  sad: "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",     // Sad Songs
  happy: "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",   // Happy Vibes
  emotional: "https://open.spotify.com/embed/playlist/37i9dQZF1DX3YSRoSdA634", // Emotional Songs
  dance: "https://open.spotify.com/embed/playlist/37i9dQZF1DX0BcQWzuB7ZO",   // Dance Hits
  vibe: "https://open.spotify.com/embed/playlist/37i9dQZF1DX889U0CL85jj",    // Good Vibes
  focus: "https://open.spotify.com/embed/playlist/37i9dQZF1DX3PFzdbtx1Us",   // Focus / Study
  energetic: "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7cM", // Energetic Mix
  romantic: "https://open.spotify.com/embed/playlist/37i9dQZF1DWXbttAJcbphx", // Love Songs
  lofi: "https://open.spotify.com/embed/playlist/37i9dQZF1DXd9rSDyQguIk",    // Lofi Beats
  retro: "https://open.spotify.com/embed/playlist/37i9dQZF1DX4UtSsGT1Sbe",   // Retro Classics
  bollywood: "https://open.spotify.com/embed/playlist/37i9dQZF1DWXVJK4aT7pmk", // Bollywood Hits
  telugu: "https://open.spotify.com/embed/playlist/37i9dQZF1DWYJ5kmTbkZiz",  // Telugu Songs
  workout: "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7cM", // Workout Mix
  calm: "https://open.spotify.com/embed/playlist/37i9dQZF1DWUvH8E2BvRXK",    // Calm & Relax
  party: "https://open.spotify.com/embed/playlist/37i9dQZF1DXaXB8fQg7xif"    // Party Hits
};
document.getElementById("mood-select").addEventListener("change", function() {
  const mood = this.value;
  const player = document.getElementById("music-player");
  player.innerHTML = `
    <iframe style="border-radius:12px" 
      src="${playlists[mood]}" 
      width="100%" height="380" frameborder="0" allowfullscreen="" 
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
      loading="lazy">
    </iframe>`;
});

function renderPlayer(src) {
  const player = document.getElementById("music-player");
  // YouTube embed iframe (works without API keys)
  player.innerHTML = `
    <iframe
      width="100%"
      height="360"
      src="${src}"
      title="Mood music"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen>
    </iframe>
  `;
}

// Default mood on load
document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("mood-select");
  renderPlayer(playlists.chill);
  select.addEventListener("change", (e) => {
    const mood = e.target.value;
    renderPlayer(playlists[mood]);
  });
});
// Dark/Light mode toggle
const toggleBtn = document.getElementById("theme-toggle");

// Apply saved preference on page load
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
  document.body.classList.add("dark-mode");
} else {
  document.body.classList.remove("dark-mode");
}

toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  // Save preference
  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
});

// Load saved preference
window.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }
});
// Calendar feature
document.getElementById('calendar-add').onclick = () => {
  const date = document.getElementById('calendar-date').value;
  const event = document.getElementById('calendar-event').value.trim();
  if (!date || !event) return;

  const list = document.getElementById('calendar-list');
  const li = document.createElement('li');
  li.textContent = `${date}: ${event}`;

  // Delete button
  const delBtn = document.createElement('button');
  delBtn.textContent = "❌";
  delBtn.style.marginLeft = "10px";
  delBtn.onclick = () => {
    li.remove();
    // Remove from localStorage
    let events = JSON.parse(localStorage.getItem('calendarEvents') || '[]');
    events = events.filter(e => !(e.date === date && e.event === event));
    localStorage.setItem('calendarEvents', JSON.stringify(events));
  };

  li.appendChild(delBtn);
  list.appendChild(li);

  // Save to localStorage
  const events = JSON.parse(localStorage.getItem('calendarEvents') || '[]');
  events.push({ date, event });
  localStorage.setItem('calendarEvents', JSON.stringify(events));

  document.getElementById('calendar-event').value = '';
};

// Load saved events on page load
window.addEventListener('DOMContentLoaded', () => {
  const list = document.getElementById('calendar-list');
  const events = JSON.parse(localStorage.getItem('calendarEvents') || '[]');
  events.forEach(e => {
    const li = document.createElement('li');
    li.textContent = `${e.date}: ${e.event}`;

    // Delete button for loaded events
    const delBtn = document.createElement('button');
    delBtn.textContent = "❌";
    delBtn.style.marginLeft = "10px";
    delBtn.onclick = () => {
      li.remove();
      let updated = events.filter(ev => !(ev.date === e.date && ev.event === e.event));
      localStorage.setItem('calendarEvents', JSON.stringify(updated));
    };

    li.appendChild(delBtn);
    list.appendChild(li);
  });
});
// Load all habits and build the grid
async function loadHabits() {
  const res = await fetch("/habits");
  const data = await res.json();
  const habits = data.habits || [];

  if (habits.length === 0) {
    document.getElementById("habit-table").innerHTML = "<p>No habits yet. Add one above!</p>";
    return;
  }

  let table = "<table><tr><th>Habit</th>";
  for (let d = 1; d <= 30; d++) {
    table += `<th>${d}</th>`;
  }
  table += "</tr>";

  for (let habit of habits) {
    table += `<tr>
                <td>
                  ${habit.habit}
                  <button class="delete-btn" data-habit="${habit.id}">🗑️</button>
                </td>`;

    const logRes = await fetch(`/habit_logs/${habit.id}`);
    const logData = await logRes.json();
    const logs = logData.logs || {};

    for (let d = 1; d <= 30; d++) {
      let status = logs[d] || "missed";
      table += `<td data-habit="${habit.id}" data-day="${d}" class="${status}">
                  ${status === "done" ? "✅" : "❌"}
                </td>`;
    }
    table += "</tr>";
  }

  table += "</table>";
  document.getElementById("habit-table").innerHTML = table;

  // Toggle habit status on cell click
  document.querySelectorAll("#habit-table td[data-habit]").forEach(cell => {
    cell.addEventListener("click", async () => {
      const habitId = cell.getAttribute("data-habit");
      const day = cell.getAttribute("data-day");
      const newStatus = cell.classList.contains("done") ? "missed" : "done";

      await fetch("/habit_logs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          habit_id: parseInt(habitId),
          day: parseInt(day),
          status: newStatus
        })
      });

      loadHabits(); // reload table to reflect change
    });
  });

  // Attach delete button listeners
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const habitId = btn.getAttribute("data-habit");
      if (!confirm("Are you sure you want to delete this habit?")) return;

      await fetch(`/habits/${habitId}`, { method: "DELETE" });
      loadHabits(); // refresh the grid
    });
  });
}

// Add new habit
document.getElementById("habit-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const habitName = document.getElementById("habit-name").value.trim();
  if (!habitName) return;

  await fetch("/habits", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ habit: habitName })
  });

  document.getElementById("habit-name").value = "";
  loadHabits();
});

// Initial load
document.addEventListener("DOMContentLoaded", loadHabits);
// Notes feature
document.getElementById("note-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const content = document.getElementById("note-input").value;

  const res = await fetch("/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content })
  });

  document.getElementById("note-input").value = "";
  loadNotes();
});

async function loadNotes() {
  const res = await fetch("/notes");
  const data = await res.json();
  const list = document.getElementById("notes-list");
  list.innerHTML = "";
  data.notes.forEach(note => {
    const li = document.createElement("li");
    li.textContent = note.content;
    const delBtn = document.createElement("button");
    delBtn.textContent = "❌";
    delBtn.onclick = async () => {
      await fetch(`/notes/${note.id}`, { method: "DELETE" });
      loadNotes();
    };
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

loadNotes();
const sections = document.querySelectorAll('.section');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
});

