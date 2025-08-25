#!/bin/zsh

SERVER="http://127.0.0.1:8000"

while true; do
  clear
  echo "=============================="
  echo "   Kairoswarm Demo Launcher   "
  echo "=============================="
  echo "1) Mouse Move"
  echo "2) Mouse Click"
  echo "3) Scroll Down"
  echo "4) Type Text"
  echo "5) Press Enter"
  echo "6) Screenshot (saves to ~/Desktop/screen.png)"
  echo "7) Full Sequence Demo"
  echo "q) Quit"
  echo "=============================="
  vared -p "Choose an option: " -c choice

  case $choice in
    1)
      curl -s -X POST "$SERVER/mouse/move" \
        -H "Content-Type: application/json" \
        -d '{"x": 400, "y": 300}'
      ;;
    2)
      curl -s -X POST "$SERVER/mouse/click" \
        -H "Content-Type: application/json" \
        -d '{"button": "left"}'
      ;;
    3)
      curl -s -X POST "$SERVER/mouse/scroll" \
        -H "Content-Type: application/json" \
        -d '{"amount": -500}'
      ;;
    4)
      curl -s -X POST "$SERVER/keyboard/type" \
        -H "Content-Type: application/json" \
        -d '"Hello from Kairoswarm on Mac!"'
      ;;
    5)
      curl -s -X POST "$SERVER/keyboard/press" \
        -H "Content-Type: application/json" \
        -d '{"key": "enter"}'
      ;;
    6)
      curl -s -X GET "$SERVER/screenshot" --output ~/Desktop/screen.png
      echo "Screenshot saved to Desktop!"
      ;;
    7)
      curl -s -X POST "$SERVER/sequence/run" \
        -H "Content-Type: application/json" \
        -d '{
          "steps": [
            {"action": "mouse_move", "x": 300, "y": 300},
            {"action": "pause", "duration": 1},
            {"action": "mouse_click", "button": "left"},
            {"action": "keyboard_type", "text": "Max is working on Mac!"},
            {"action": "keyboard_press", "key": "enter"}
          ]
        }'
      ;;
    q)
      echo "Exiting Kairoswarm Demo. Bye!"
      exit 0
      ;;
    *)
      echo "Invalid choice"
      ;;
  esac

  echo ""
  read "?Press Enter to continue..."
done

