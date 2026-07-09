---
name: verify
description: Build/launch/drive recipe for verifying changes to the Bubble-Plan task map (index.html) in a headless remote session.
---

# Verifying Bubble-Plan

Single-page React app in `index.html` (JSX compiled in-browser by Babel). No build step. State lives in localStorage key `taskmap.state.v2`.

## Gotcha: CDN scripts are blocked in the remote sandbox

`unpkg.com`, `cdn.tailwindcss.com`, `fonts.googleapis.com` are denied by the egress proxy (403), and Playwright's proxy option force-routes even localhost through it (405). Don't fight the proxy — vendor the deps:

1. `npm install react@18.3.1 react-dom@18.3.1 @babel/standalone@7.24.7 tailwindcss@3.4.14` (registry.npmjs.org is allowed directly) and copy the UMD files from `node_modules`.
2. Build CSS: `npx tailwindcss -c <config with darkMode:"class", content:[copy of index.html]> -i 'base/components/utilities' -o tw.css` — Tailwind's scanner picks class names out of the JSX fine.
3. Copy `index.html` to a scratch dir; replace the four CDN `<script>` tags with the local files (`tw.css` as a `<link>`), drop the fonts/gsi tags. The leftover inline `tailwind.config = ...` throws a harmless pageerror.
4. Serve the scratch dir with `python3 -m http.server`, launch Playwright with **no proxy option** and the pre-installed `/opt/pw-browsers/chromium`.

## Driving it

- Wait for the `+ New Task` header button, then ~1.5s for the viewport to center itself.
- Read state with `JSON.parse(localStorage.getItem('taskmap.state.v2'))` — positions, `zoneId`, `dueDate`, `subtasks` are all there; assert on it instead of pixel-hunting.
- Screen→canvas: `zoom = mapGridRect.width / 22000`; `canvasX = (screenX - rect.left) / zoom`. A task's zone-membership point is `(x + priorityWidth/2, y + 90)`.
- Hotkeys (n/t/z/l/a) are ignored while focus is in any input — blur (`document.activeElement.blur()`) before pressing them after typing.
- `server.py` serves the repo dir and exposes GET/PUT `/state` backed by the tracked `state.json` — the browser app never calls it, but don't PUT to it during tests or you'll dirty the repo.
