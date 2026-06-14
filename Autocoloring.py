import pyautogui
from PIL import Image
import time
import keyboard
import random

# ---------- SETTINGS ----------

TARGET_COLOR = (181, 255, 181)
TOLERANCE = 5

WHITE_COLOR = (255, 255, 255)
WHITE_TOLERANCE = 5
RIGHT_DELAY = 0.25

START_DELAY = 5

BOX_SIZE = 10
GRID_X_OFFSET = 39
GRID_Y_OFFSET = 57

MOVE_DURATION = 0
TOUCH_DELAY = 0.004

LOOP_DELAY = 0.08

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
            if color_close(
                pixels[sx, sy],
                TARGET_COLOR,
                TOLERANCE
            ):
                return True

    return False


def find_random_white_box():
    screenshot = pyautogui.screenshot()
    img = screenshot.convert("RGB")

    width, height = img.size
    pixels = img.load()

    white_boxes = []

    for y in range(GRID_Y_OFFSET, height, BOX_SIZE):
        for x in range(GRID_X_OFFSET, width, BOX_SIZE):

            sample_x = x + BOX_SIZE // 2
            sample_y = y + BOX_SIZE // 2

            if sample_x >= width or sample_y >= height:
                continue

            if color_close(
                pixels[sample_x, sample_y],
                WHITE_COLOR,
                WHITE_TOLERANCE
            ):
                white_boxes.append((x, y))

    if not white_boxes:
        return None

    return random.choice(white_boxes)


def right_click_box(x, y):
    cx = x + int(BOX_SIZE * AIM_X_RATIO)
    cy = y + int(BOX_SIZE * AIM_Y_RATIO)

    pyautogui.moveTo(cx, cy, duration=0)
    pyautogui.rightClick()

    time.sleep(RIGHT_DELAY)


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

    if touched == 0:
        white_target = find_random_white_box()

        if white_target is not None:
            print("No green boxes found. Right-clicking a random white box.")
            right_click_box(*white_target)

    print(f"Touched {touched} green boxes.")

    time.sleep(LOOP_DELAY)
    round_num += 1
