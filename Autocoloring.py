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

OUTLINE_COLOR = (62, 64, 69)  # #3E4045
OUTLINE_TOLERANCE = 5
MIN_OUTLINE_HITS = 1

START_DELAY = 5

BOX_SIZE = 10
GRID_X_OFFSET = 39
GRID_Y_OFFSET = 57

MOVE_DURATION = 0
TOUCH_DELAY = 0.004
LOOP_DELAY = 0.08

RIGHT_CLICK_DELAY = 0.25

AIM_X_RATIO = 0.35
AIM_Y_RATIO = 0.35

RIGHT_CLICK_X_RATIO = 0.50
RIGHT_CLICK_Y_RATIO = 0.50

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


def box_has_white(pixels, width, height, x, y):
    sample_points = [
        (x + BOX_SIZE // 2, y + BOX_SIZE // 2),
        (x + 4, y + 4),
        (x + BOX_SIZE - 5, y + 4),
        (x + 4, y + BOX_SIZE - 5),
        (x + BOX_SIZE - 5, y + BOX_SIZE - 5),
    ]

    white_hits = 0

    for sx, sy in sample_points:
        if 0 <= sx < width and 0 <= sy < height:
            if color_close(pixels[sx, sy], WHITE_COLOR, WHITE_TOLERANCE):
                white_hits += 1

    return white_hits >= 1


def box_has_outline(pixels, width, height, x, y):
    outline_hits = 0

    check_points = []

    # Check slightly outside and inside the box border
    for offset in [-2, -1, 0, 1, 2]:
        # top / bottom areas
        check_points.extend([
            (x + BOX_SIZE // 2, y + offset),
            (x + BOX_SIZE // 2, y + BOX_SIZE - 1 + offset),
        ])

        # left / right areas
        check_points.extend([
            (x + offset, y + BOX_SIZE // 2),
            (x + BOX_SIZE - 1 + offset, y + BOX_SIZE // 2),
        ])

    # Also check corners nearby
    corner_points = [
        (x - 1, y - 1),
        (x + BOX_SIZE, y - 1),
        (x - 1, y + BOX_SIZE),
        (x + BOX_SIZE, y + BOX_SIZE),
    ]

    check_points.extend(corner_points)

    for sx, sy in check_points:
        if 0 <= sx < width and 0 <= sy < height:
            if color_close(
                pixels[sx, sy],
                OUTLINE_COLOR,
                OUTLINE_TOLERANCE
            ):
                outline_hits += 1

    return outline_hits >= 1


def find_random_white_box():
    screenshot = pyautogui.screenshot()
    img = screenshot.convert("RGB")

    width, height = img.size
    pixels = img.load()

    white_boxes = []

    for y in range(GRID_Y_OFFSET, height, BOX_SIZE):
        for x in range(GRID_X_OFFSET, width, BOX_SIZE):

            if keyboard.is_pressed("esc"):
                raise SystemExit

            if (
                box_has_white(pixels, width, height, x, y)
                and box_has_outline(pixels, width, height, x, y)
            ):
                white_boxes.append((x, y))

    if not white_boxes:
        return None

    return random.choice(white_boxes)


def right_click_box(x, y):
    cx = x + int(BOX_SIZE * RIGHT_CLICK_X_RATIO)
    cy = y + int(BOX_SIZE * RIGHT_CLICK_Y_RATIO)

    pyautogui.moveTo(cx, cy, duration=0)
    time.sleep(0.03)

    pyautogui.rightClick()

    time.sleep(RIGHT_CLICK_DELAY)


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
        print("No green boxes found. Looking for outlined white box...")

        white_target = find_random_white_box()

        if white_target is not None:
            print(f"Right-clicking outlined white box at {white_target}.")
            right_click_box(*white_target)
        else:
            print("No outlined white boxes found.")

    print(f"Touched {touched} green boxes.")

    time.sleep(LOOP_DELAY)
    round_num += 1
