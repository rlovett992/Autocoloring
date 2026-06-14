# Autocoloring

A lightweight Python automation script that scans the screen for a specific color and moves the mouse across matching areas in real time.

The reason for this project was I was curious if I could make a script to automate, as lame as it sounds, a coloring game.
The color it searches for is easily altered by changing the RGB code to match the target color.
While not perfect it works quite well for something built in about a week

This project was built as a small personal experiment in:
- screen capture
- color detection
- automation with Python
- precision tuning for interactive environments (like games)

---

## Features

- Detects specific colored pixels on screen
- Treats visual grid boxes as single targets
- Moves cursor across detected areas (no clicking)
- Adjustable speed and precision
- Continuous scanning loop for dynamic changes
- ESC key kill switch for safety

---

## How It Works

1. Takes a screenshot of the screen  
2. Scans it in a grid pattern  
3. Checks each grid cell for a target color  
4. Moves the mouse to matching locations  
5. Repeats continuously as new pixels appear
6. If no new pixels appear, move to a random white pixel and right-click to make new green boxes appear  

The script is tuned to:
- avoid skipping boxes
- compensate for imperfect alignment
- balance speed vs reliability

The limiting factor for reliability is the TOUCH_DELAY variable. If you slow it down, it will hit more, or even all, of the green boxes on the first pass.

---

## Requirements

Install dependencies:

```bash
pip install pyautogui pillow keyboard
