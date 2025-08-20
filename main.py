import time
import io
import pyautogui
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Kairoswarm Control",
    description="Local control server for Kairoswarm agents",
)

# ---------- GLOBAL SETTINGS ----------
GLOBAL_STEP_DELAY = 0.3  # delay between steps (seconds)


# ---------- MODELS ----------
class MouseMove(BaseModel):
    x: int
    y: int
    duration: float = 0.3


class MouseClick(BaseModel):
    button: str = "left"  # "left", "right", "middle"


class KeyPress(BaseModel):
    key: str  # e.g. "a", "enter", "ctrl"


class MouseDrag(BaseModel):
    x: int
    y: int
    duration: float = 0.5
    button: str = "left"


class ScrollRequest(BaseModel):
    amount: int


class HotkeyRequest(BaseModel):
    keys: List[str]


# ---------- BASIC ROUTES ----------
@app.get("/")
def root():
    return {"status": "Kairoswarm Control running locally"}


@app.post("/mouse/move")
def mouse_move(cmd: MouseMove):
    pyautogui.moveTo(cmd.x, cmd.y, duration=cmd.duration)
    return {"moved_to": (cmd.x, cmd.y)}


@app.post("/mouse/drag")
def mouse_drag(cmd: MouseDrag):
    if cmd.button not in ("left", "middle", "right"):
        return {"error": "Invalid button. Must be 'left', 'middle', or 'right'."}
    pyautogui.mouseDown(button=cmd.button)
    pyautogui.moveTo(cmd.x, cmd.y, duration=cmd.duration)
    pyautogui.mouseUp(button=cmd.button)
    return {"dragged_to": (cmd.x, cmd.y), "duration": cmd.duration, "button": cmd.button}


@app.post("/mouse/click")
def mouse_click(cmd: MouseClick):
    pyautogui.click(button=cmd.button)
    return {"clicked": cmd.button}


@app.post("/keyboard/press")
def keyboard_press(cmd: KeyPress):
    pyautogui.press(cmd.key)
    return {"pressed": cmd.key}


@app.post("/keyboard/type")
def keyboard_type(text: str = Body(...)):
    pyautogui.typewrite(text)
    return {"typed": text}


@app.post("/keyboard/hotkey")
def keyboard_hotkey(cmd: HotkeyRequest):
    pyautogui.hotkey(*cmd.keys)
    return {"hotkey": cmd.keys}


@app.post("/mouse/scroll")
def mouse_scroll(req: ScrollRequest):
    pyautogui.scroll(req.amount)
    return {"scrolled": req.amount}


@app.get("/screenshot")
def screenshot():
    screenshot = pyautogui.screenshot()
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# ---------- SEQUENCE EXECUTION ----------
class Step(BaseModel):
    action: str
    x: Optional[int] = None
    y: Optional[int] = None
    button: str = "left"
    key: Optional[str] = None
    text: Optional[str] = None
    amount: Optional[int] = None
    duration: float = 0.3
    keys: Optional[List[str]] = None


class SequenceRequest(BaseModel):
    steps: List[Step]


def do_pause(seconds: float):
    time.sleep(seconds)
    return {"paused": seconds}


@app.post("/sequence/run")
def run_sequence(req: SequenceRequest):
    results = []
    for step in req.steps:
        if step.action == "mouse_move" and step.x is not None and step.y is not None:
            pyautogui.moveTo(step.x, step.y, duration=step.duration)
            results.append({"moved_to": (step.x, step.y)})

        elif step.action == "mouse_click":
            pyautogui.click(button=step.button)
            results.append({"clicked": step.button})

        elif step.action == "keyboard_press" and step.key:
            pyautogui.press(step.key)
            results.append({"pressed": step.key})

        elif step.action == "keyboard_type" and step.text:
            pyautogui.typewrite(step.text)
            results.append({"typed": step.text})

        elif step.action == "mouse_scroll" and step.amount is not None:
            pyautogui.scroll(step.amount)
            results.append({"scrolled": step.amount})

        elif step.action == "keyboard_hotkey" and step.keys:
            pyautogui.hotkey(*step.keys)
            results.append({"hotkey": step.keys})

        elif step.action == "pause":
            results.append(do_pause(step.duration))

        else:
            results.append({"error": f"Invalid or missing params for action '{step.action}'"})

        # Global delay between steps
        time.sleep(GLOBAL_STEP_DELAY)

    return {"sequence_results": results}
