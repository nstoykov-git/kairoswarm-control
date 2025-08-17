import os
import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pyautogui


app = FastAPI(title="Kairoswarm Control", description="Local control server for Kairoswarm agents")

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


@app.post("/mouse/click")
def mouse_click(cmd: MouseClick):
    pyautogui.click(button=cmd.button)
    return {"clicked": cmd.button}


@app.post("/keyboard/press")
def keyboard_press(cmd: KeyPress):
    pyautogui.press(cmd.key)
    return {"pressed": cmd.key}


from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pyautogui
import io

app = FastAPI()

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
