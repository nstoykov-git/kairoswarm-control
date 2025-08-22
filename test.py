import asyncio
import websockets
import json

CLIENT_ID = "local-test-client"
WS_URL = f"wss://nstoykov-git--kairoswarm-serverless-api-fastapi-app.modal.run/control/ws/client/{CLIENT_ID}"

async def main():
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                # 🔑 Proper handshake
                await ws.send(json.dumps({"role": "controller", "client_id": CLIENT_ID}))
                print("✅ Controller handshake sent")

                # Send test command
                cmd = {"action": "mouse_move", "x": 600, "y": 400}
                await ws.send(json.dumps(cmd))
                print("📤 Sent mouse_move")

                # Wait for reply
                reply = await ws.recv()
                print("📥 Got reply:", reply)

                return
        except Exception as e:
            print(f"❌ Connection failed: {e}, retrying in 3s...")
            await asyncio.sleep(3)

asyncio.run(main())
