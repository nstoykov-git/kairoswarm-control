import asyncio
import websockets
import json

PORTAL_ID = "local-test-portal"
WS_URL = "wss://nstoykov-git--kairoswarm-serverless-api-fastapi-app.modal.run/portals/ws"


async def main():
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to Portal server at {WS_URL}")

                # 🔑 Handshake: register as agent
                await ws.send(json.dumps({"portal_id": PORTAL_ID, "role": "agent"}))
                print(f"✅ Handshake sent (portal={PORTAL_ID}, role=agent)")

                # Send test command
                cmd = {"action": "mouse_move", "x": 600, "y": 400}
                await ws.send(json.dumps(cmd))
                print("📤 Sent command:", cmd)

                # Wait for reply from device
                reply = await ws.recv()
                print("📥 Got reply:", reply)

                return

        except Exception as e:
            print(f"❌ Connection failed: {e}, retrying in 3s...")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
