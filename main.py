import time
import io
import pyautogui
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Kairoswarm Control",
    description="Local control server for Kairoswarm agents",
)

# ---------- MODELS ----------
class MouseMove(BaseModel):
    x: int
    y: int

class MouseClick(BaseModel):
    button: str = "left"  # "left", "right", or "middle"

class KeyPress(BaseModel):
    key: str  # e.g. "a", "enter", "ctrl"

# ---------- ROUTES ----------

@app.get("/")
def root():
    return {"status": "Kairoswarm Control running locally"}

@app.post("/mouse/move")
def mouse_move(cmd: MouseMove):
    pyautogui.moveTo(cmd.x, cmd.y, duration=0.3)
    return {"moved_to": (cmd.x, cmd.y)}

class MouseDrag(BaseModel):
    x: int
    y: int
    duration: float = 0.5
    button: str = "left"  # Ensure it's one of: left, middle, right

@app.post("/mouse/drag")
def mouse_drag(cmd: MouseDrag):
    if cmd.button not in ("left", "middle", "right"):
        return {"error": "Invalid button. Must be 'left', 'middle', or 'right'."}
    
    pyautogui.mouseDown(button=cmd.button)
    pyautogui.moveTo(cmd.x, cmd.y, duration=cmd.duration)
    pyautogui.mouseUp(button=cmd.button)
    return {
        "dragged_to": (cmd.x, cmd.y),
        "duration": cmd.duration,
        "button": cmd.button
    }

@app.post("/mouse/click")
def mouse_click(cmd: MouseClick):
    pyautogui.click(button=cmd.button)
    return {"clicked": cmd.button}

@app.post("/keyboard/press")
def keyboard_press(cmd: KeyPress):
    pyautogui.press(cmd.key)
    return {"pressed": cmd.key}

@app.get("/screenshot")
def screenshot():
    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Save it to an in-memory buffer
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)

    # Stream directly without writing to disk
    return StreamingResponse(buf, media_type="image/png")

# ---------- NEW ROUTES ----------
class ScrollRequest(BaseModel):
    amount: int

@app.post("/mouse/scroll")
def mouse_scroll(req: ScrollRequest):
    pyautogui.scroll(req.amount)
    return {"scrolled": req.amount}

@app.post("/keyboard/type")
def keyboard_type(text: str = Body(...)):
    """Type a string of text."""
    pyautogui.typewrite(text)
    return {"typed": text}



class HotkeyRequest(BaseModel):
    keys: List[str]

@app.post("/keyboard/hotkey")
def keyboard_hotkey(cmd: HotkeyRequest):
    """Press a combination of keys, e.g. ctrl+c."""
    pyautogui.hotkey(*cmd.keys)
    return {"hotkey": cmd.keys}

