# entropy — Spatial Task Manager

A visual, map-based task manager. Tasks live as draggable cards on a 2D canvas instead of a list.

## Run it

Everything is in a single file — no install, no build step:

- **Easiest:** double-click `index.html` (needs internet for the React/Tailwind CDNs).
- **Local server:** `python -m http.server 8123` in this folder, then open http://localhost:8123
- **CodeSandbox / v0:** paste the contents of `index.html` into a static HTML sandbox.

## Features

### Map basics
- **Spatial map** — a 2200×1500 scrollable canvas styled as a light, Apple-style whiteboard: off-white background, subtle dot grid, Inter/San Francisco typography, borderless white cards with soft elevation shadows, and glassmorphism panels. A subtle warm glow marks the center of the map — the "hot zone" where important work lives.
- **Add tasks** — title, description, priority (Low / Medium / High / Critical), time estimate, and due date via a modal.
- **Priority visuals** — Critical cards are red and larger; High amber, Medium blue, Low gray and smaller.
- **Drag anywhere** — smooth native pointer-event dragging, clamped to the canvas.
- **Zoom** — scroll wheel zooms in/out around the cursor, from 200% all the way down to 1%. Bottom-right −/+ controls with a click-to-reset percent readout; Ctrl+= / Ctrl+− / Ctrl+0 also work.
- **Pan** — hold **right-click** and drag to move around the map (scrollbars still work too).
- **Google Calendar** — connect with your own Google OAuth Client ID (read-only scope) and import upcoming events as tasks with due dates. Setup steps are shown in the panel.
- **Arrange** — radial priority layout: Critical tasks go to the glowing center of the map, with High, Medium, and Low in expanding rings outward. Zones move too: each zone travels toward or away from the center based on the average priority of the tasks inside it (members ride along), and its header shows that aggregate priority as a badge. Empty zones stay put.
- **Dark mode** — a header toggle switches light/dark; your choice is remembered, and the first visit follows your OS preference.
- **Complete** — completed tasks move off the map into the Done Zone panel (restore, delete, or clear all).

### Connections & grouping
- **Link (dependencies)** — click Link, pick the task that must finish first, then the task that depends on it. A dashed arrow connects them, the downstream task shows a **blocked** badge until the upstream one is completed, and clicking an arrow removes it.
- **Zones (buckets)** — draw named, colored boundary boxes ("Work", "Personal", …). Zones are draggable (member tasks move with them), resizable from the corner handle, renamable inline, and **collapsible** — collapsing hides all tasks inside behind a compact pill with a count. Click the colored dot in a zone's header to cycle through 5 accent colors. Each zone shows a priority badge summarizing the tasks inside it.

### Time & focus
- **Pomodoro timer** — hit "25m" on any card to start a 25-minute session on it. The corner widget shows the countdown with pause/resume, chimes when done, tallies a focus-session count on the task, and survives page refreshes.
- **Time estimates** — the optional "time needed" field rolls up into a total-hours chip in the header: your workload reality check.
- **Focus mode** — dims everything except Critical tasks and the task you're running a Pomodoro on.

### Urgency & analytics
- **Gravity (urgency aging)** — as a due date approaches, cards gain deepening red rings; overdue cards pulse with a red glow and an OVERDUE badge. Tasks due within ~2 days also slowly drift toward the map center so they enter your field of view.
- **Stats panel** — completion velocity (today vs. yesterday), focus sessions today, total mapped hours, overdue count, and a 7-day completion bar chart.

### Persistence
- Everything — tasks, positions, links, zones, timer state, and completion history — is saved to `localStorage` and survives refreshes.

> Note: `localStorage` is per-origin, so tasks saved while using the local server won't appear when opening the file directly (and vice versa). Pick one way of running it and stick with it.
