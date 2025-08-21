import asyncio
import json
import time
import io
import base64

import pyautogui
import websockets


# ---------- CONFIG ----------
CLIENT_ID = "local-test-client"  # later: unique per user
WS_URL = f"wss://nstoykov-git--kairoswarm-serverless-api-fastapi-app.modal.run/control/ws/client/{CLIENT_ID}"


# ---------- HELPERS ----------
async def handle_command(cmd: dict) -> dict:
    """Execute a single command from Modal and return a result dict."""
    action = cmd.get("action")

    if action == "mouse_move":
        x, y = cmd["x"], cmd["y"]
        pyautogui.moveTo(x, y)
        return {"moved_to": [x, y]}

    if action == "mouse_click":
        button = cmd.get("button", "left")
        pyautogui.click(button=button)
        return {"clicked": button}

    if action == "mouse_drag":
        x, y = cmd["x"], cmd["y"]
        button = cmd.get("button", "left")
        pyautogui.mouseDown(button=button)
        pyautogui.moveTo(x, y)
        pyautogui.mouseUp(button=button)
        return {"dragged_to": [x, y], "button": button}

    if action == "mouse_scroll":
        amount = cmd["amount"]
        pyautogui.scroll(amount)
        return {"scrolled": amount}

    if action == "keyboard_type":
        text = cmd["text"]
        pyautogui.typewrite(text)
        return {"typed": text}

    if action == "keyboard_press":
        key = cmd["key"]
        pyautogui.press(key)
        return {"pressed": key}

    if action == "keyboard_hotkey":
        keys = cmd["keys"]
        pyautogui.hotkey(*keys)
        return {"hotkey": keys}

    if action == "screenshot":
        buf = io.BytesIO()
        img = pyautogui.screenshot()
        img.save(buf, format="PNG")
        return {"image_base64": base64.b64encode(buf.getvalue()).decode("utf-8")}

    if action == "sequence_run":
        steps = cmd.get("steps", [])
        results = []
        for step in steps:
            try:
                result = await handle_command(step)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
            time.sleep(0.3)  # small pause between steps
        return {"sequence_results": results}

    if action == "locate":
        image_path = cmd["image"]
        confidence = cmd.get("confidence", 0.8)
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return {
                    "found": True,
                    "box": {
                        "left": location.left,
                        "top": location.top,
                        "width": location.width,
                        "height": location.height,
                    },
                }
            return {"found": False}
        except Exception as e:
            return {"error": f"locate failed: {str(e)}"}

    return {"error": f"Unknown action {action}"}


# ---------- MAIN LOOP ----------
async def run_agent() -> None:
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to Modal at {WS_URL}")
                await ws.send(json.dumps({"status": "ready", "client_id": CLIENT_ID}))

                async for message in ws:
                    try:
                        cmd = json.loads(message)
                        print(f"📥 Received: {cmd}")
                        result = await handle_command(cmd)
                        await ws.send(json.dumps({"result": result, "client_id": CLIENT_ID}))
                    except Exception as e:
                        err = {"error": str(e)}
                        await ws.send(json.dumps(err))
        except Exception as e:
            print(f"❌ Connection failed: {e}, retrying in 3s...")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(run_agent())
