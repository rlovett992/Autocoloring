import pyautogui
from PIL import Image
import time
import keyboard

# ---------- SETTINGS ----------

TARGET_COLOR = (0, 200, 40)
TOLERANCE = 90

START_DELAY = 10

BOX_SIZE = 10
GRID_X_OFFSET = 39
GRID_Y_OFFSET = 57

# A bit slower so the game can keep up
MOVE_DURATION = 0.006
TOUCH_DELAY = 0.003

LOOP_DELAY = 0.08

# Aim more toward the upper-left/middle of each box
# because it was landing near the bottom-right.
AIM_X_RATIO = 0.35
AIM_Y_RATIO = 0.35

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0


def color_close(pixel, target, tolerance):
    r, g, b = pixel[:3]
    tr, tg, tb = target

    return (
        abs(r - tr) <= tolerance and
        abs(g - tg) <= tolerance and
        abs(b - tb) <= tolerance
    )


def box_has_green(pixels, width, height, x, y):
    sample_points = [
        (x + BOX_SIZE // 2, y + BOX_SIZE // 2),
        (x + 2, y + 2),
        (x + BOX_SIZE - 3, y + 2),
        (x + 2, y + BOX_SIZE - 3),
        (x + BOX_SIZE - 3, y + BOX_SIZE - 3),
    ]

    for sx, sy in sample_points:
        if 0 <= sx < width and 0 <= sy < height:
            if color_close(pixels[sx, sy], TARGET_COLOR, TOLERANCE):
                return True

    return False


def scan_and_touch_green_boxes():
    screenshot = pyautogui.screenshot()
    img = screenshot.convert("RGB")

    width, height = img.size
    pixels = img.load()

    touched = 0

    for y in range(GRID_Y_OFFSET, height, BOX_SIZE):
        for x in range(GRID_X_OFFSET, width, BOX_SIZE):
            if keyboard.is_pressed("esc"):
                raise SystemExit

            if box_has_green(pixels, width, height, x, y):
                cx = x + int(BOX_SIZE * AIM_X_RATIO)
                cy = y + int(BOX_SIZE * AIM_Y_RATIO)

                pyautogui.moveTo(cx, cy, duration=MOVE_DURATION)
                time.sleep(TOUCH_DELAY)

                touched += 1

    return touched


print(f"Starting in {START_DELAY} seconds...")
print("Press ESC to stop.")
time.sleep(START_DELAY)

round_num = 1

while True:
    if keyboard.is_pressed("esc"):
        print("Stopped by ESC.")
        break

    print(f"Scan round {round_num}...")

    touched = scan_and_touch_green_boxes()

    print(f"Touched {touched} green boxes.")

    time.sleep(LOOP_DELAY)
    round_num += 1