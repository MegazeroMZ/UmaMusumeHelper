import pygetwindow as gw
import pyautogui
import time
import win32gui
import win32con
import pytesseract
import difflib
import re

from SupportCardsData import supportCardData
from UmaData import umaData
from EventsData import eventData

from PIL import Image, ImageEnhance
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# psm 6 can deal with 1-2 lines
config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '

data = supportCardData + umaData + eventData

def clean_text(text):
    # Remove trailing punctuation and multiple spaces
    return re.sub(r'[-–—\s]+$', '', text).strip()

def find_best_match(extracted_text, data_list):
    extracted_text = clean_text(extracted_text)
    names = [clean_text(item["name"]) for item in data_list]
    matches = difflib.get_close_matches(extracted_text, names, n=1, cutoff=0.6)
    if matches:
        matched_name = matches[0]
        for item in data_list:
            if clean_text(item["name"]) == matched_name:
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

    textLeft = 282
    textUpper = 253
    textRight = 696
    textLower = 313

    textArea = screenshot.crop((textLeft, textUpper, textRight, textLower))
    scale_factor = 2
    new_size = (textArea.width * scale_factor, textArea.height * scale_factor)
    textArea = textArea.resize(new_size, Image.LANCZOS)
    text = pytesseract.image_to_string(textArea, lang='eng', config=config).strip()

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
