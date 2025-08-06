import pygetwindow as gw
import pyautogui
import time
import win32gui
import win32con
import pytesseract
import difflib

from SupportCardsData import supportCardData
from UmaData import umaData
from EventsData import eventData

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

data = supportCardData + umaData + eventData

def find_best_match(extracted_text, data_list):
    names = [item["name"] for item in data_list]
    matches = difflib.get_close_matches(extracted_text.strip(), names, n=1, cutoff=0.6)
    if matches:
        matched_name = matches[0]
        for item in data_list:
            if item["name"] == matched_name:
                return item
    return None

def find_window_exact(title):
    for w in gw.getAllWindows():
        if w.title == title:
            return w
    return None

# Initial window grab/setup (only once)
win = find_window_exact("Umamusume")
if not win:
    raise Exception("Window with exact title 'Umamusume' not found.")

if win.isMinimized:
    win.restore()

hwnd = win._hWnd
win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
win32gui.SetForegroundWindow(hwnd)

# Main loop
while True:
    left, top = win.topleft
    width, height = win.width, win.height

    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    textLeft = 272
    textUpper = 263
    textRight = 696
    textLower = 303

    textArea = screenshot.crop((textLeft, textUpper, textRight, textLower))
    # textArea.save('screenshot.png');

    text = pytesseract.image_to_string(textArea, lang='eng').strip()
    print(f"\nExtracted text: {text}")

    match = find_best_match(text, data)
    if match:
        print("=" * 40)
        print(f"📘 Match found: {match['name']}")
        print("-" * 40)
        for key in sorted(match["options"].keys()):
            print(f"{key.capitalize()}:")
            lines = [line.strip() for line in match["options"][key].split(',')]
            for line in lines:
                print(f"  - {line}")
            print("-" * 40)
        print("=" * 40)
    else:
        print("❌ No close match found.")

    time.sleep(5)
