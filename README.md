# Kairoswarm Control Agent

This is the local control agent for **Kairoswarm** — enabling real-time control of your computer via remote agents like Max, Iris, and Marin. It acts as a local relay that securely receives input commands over WebSocket and executes them using `pyautogui`.

> ⚠️ This agent can move your mouse, type on your keyboard, take screenshots, and simulate keypresses. Use only on machines you control and trust.

---

## ✅ Features

- Real-time input control via WebSocket
- Mouse movement, clicks, drags, and scrolls
- Keyboard typing, keypresses, and hotkeys
- Screenshot capture (base64)
- Multi-step sequence execution
- Local testing utilities to build trust

---

## 💪 Installation

### 1. Clone the repo

```bash
git clone https://github.com/nstoykov-git/kairoswarm-control.git
cd kairoswarm-control
```

### 2. Install dependencies

If you're using `conda`:

```bash
conda create -n kairoswarm python=3.10
conda activate kairoswarm
pip install -r requirements.txt
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

## 🧺a Test the Connection (Safe Intro)

To try a **safe, minimal test** and confirm that the agent works, run:

```bash
python test.py
```

This will:

- Connect to the Portal WebSocket server
- Move your mouse to position (600, 400)
- Print a response from your own machine

### 👀 What You Should See

- No typing, clicking, or scrolling — just one visible movement
- Console log like:

```
✅ Connected to Portal server at wss://...
📤 Sent handshake
📤 Sent test command: {'action': 'mouse_move', 'x': 600, 'y': 400}
📥 Got reply: {"moved_to": [600, 400]}
```

---

## 🧹 Run a Full Local Sequence (Optional)

Once you're comfortable, you can try running a full **pre-defined action sequence**.

Open `sequence.json` to inspect the commands:

```json
{
  "steps": [
    {"action": "mouse_move", "x": 200, "y": 200},
    {"action": "pause", "duration": 1},
    {"action": "mouse_click", "button": "left"},
    {"action": "keyboard_type", "text": "Hello from curl!"},
    {"action": "keyboard_press", "key": "enter"},
    {"action": "pause", "duration": 1},
    {"action": "keyboard_hotkey", "keys": ["ctrl", "a"]},
    {"action": "pause", "duration": 1},
    {"action": "mouse_drag", "x": 400, "y": 400, "button": "left"},
    {"action": "pause", "duration": 1},
    {"action": "mouse_scroll", "amount": -500}
  ]
}
```

You can use this as a reference or build your own sequences.

To run a sequence like this, you'll need to send the full command from your LLM or extend `test.py` to load and dispatch `sequence.json`.

---

## 🔒 Permissions (macOS)

On macOS, the agent needs permissions to control input:

1. **System Settings → Privacy & Security → Accessibility**
2. Add **Terminal.app** or the Python binary you're using
3. **(Optional)**: Add permission under **Input Monitoring** and **Screen Recording** for screenshots

If these aren’t granted, the agent may silently fail to control your system.

---

## 📁 File Overview

| File              | Purpose                                                       |
|-------------------|---------------------------------------------------------------|
| `prod_agent.py`   | Main WebSocket-based control agent (run this in production)   |
| `test.py`         | Safe first-time test — only moves the mouse                  |
| `sequence.json`   | Example full action chain — safe to inspect, edit, and reuse |
| `requirements.txt`| Python dependencies (`pyautogui`, `websockets`, etc.)         |
| `README.md`       | You're reading it!                                             |

---

## 🧠 About This Agent

This agent was built to support **Max** and other AI personalities in the **Kairoswarm** system. It runs locally, connects securely to the Kairoswarm Portal, and acts as a bridge between high-level agent reasoning and physical device control.

> “Talk to Max. He moves your mouse.” — a demo you'll never forget.

---

## 🧹 Notes

- The legacy HTTP-based `main.py` has been removed — replaced by the WebSocket-based `prod_agent.py`.
- This agent doesn't exfiltrate any data — it simply listens for commands on your machine and acts accordingly.
- You can inspect and test every command before enabling anything live.

---

## 🧠 Next Steps

- Customize `sequence.json` to simulate your own workflows
- Connect this agent to the Kairoswarm Portal via LLM-based interfaces
- Add logging or keyboard intercepts for advanced tracing/debugging
- Build confidence, then automate more.

---

Let us know if you need help building your first Max-powered workflow. This is just the beginning.
