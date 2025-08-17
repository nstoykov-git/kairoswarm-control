from fastapi import FastAPI
from pydantic import BaseModel
import pyautogui
import base64
from io import BytesIO

app = FastAPI(title="Kairoswarm Control Server")

# -------------------------------
# Mouse Actions
# -------------------------------

class MouseMoveRequest(BaseModel):
    x: int
    y: int

@app.post("/mouse/move")
def move_mouse(req: MouseMoveRequest):
    pyautogui.moveTo(req.x, req.y)
    return {"status": "ok", "x": req.x, "y": req.y}


class MouseClickRequest(BaseModel):
    button: str = "left"  # left, right, middle

@app.post("/mouse/click")
def click_mouse(req: MouseClickRequest):
    pyautogui.click(button=req.button)
    return {"status": "ok", "button": req.button}


class MouseDragRequest(BaseModel):
    x: int
    y: int
    duration: float = 0.5

@app.post("/mouse/drag")
def drag_mouse(req: MouseDragRequest):
    pyautogui.dragTo(req.x, req.y, duration=req.duration)
    return {"status": "ok", "x": req.x, "y": req.y}


# -------------------------------
# Keyboard Actions
# -------------------------------

class TypeTextRequest(BaseModel):
    text: str

@app.post("/keyboard/type")
def type_text(req: TypeTextRequest):
    pyautogui.typewrite(req.text)
    return {"status": "ok", "text": req.text}


class KeyPressRequest(BaseModel):
    key: str

@app.post("/keyboard/press")
def press_key(req: KeyPressRequest):
    pyautogui.press(req.key)
    return {"status": "ok", "key": req.key}


class HotkeyRequest(BaseModel):
    keys: list[str]

@app.post("/keyboard/hotkey")
def hotkey(req: HotkeyRequest):
    pyautogui.hotkey(*req.keys)
    return {"status": "ok", "keys": req.keys}


# -------------------------------
# Screen Actions
# -------------------------------

@app.get("/screenshot")
def screenshot():
    screenshot = pyautogui.screenshot()
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return {"status": "ok", "image_base64": img_str}


class LocateImageRequest(BaseModel):
    image_base64: str

@app.post("/locate")
def locate_image(req: LocateImageRequest):
    # Save incoming image to temp file
    try:
        img_bytes = base64.b64decode(req.image_base64)
        with open("temp_target.png", "wb") as f:
            f.write(img_bytes)

        location = pyautogui.locateOnScreen("temp_target.png", confidence=0.8)
        if location:
            return {"status": "ok", "location": location._asdict()}
        else:
            return {"status": "not_found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
