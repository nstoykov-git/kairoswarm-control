import pyautogui, time

print("⏳ Moving mouse in 3 seconds...")
time.sleep(3)
pyautogui.moveTo(300, 300, duration=1)
print("✅ Mouse should now be at (300, 300)")

