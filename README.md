Umamusume Event Text Extractor

This Python script captures a portion of the screen from the "Umamusume" game window on steam, extracts text using OCR (Tesseract), compares it against known event names, and prints the associated options.

---

## Features

- Automatically finds and focuses the "Umamusume" window.
- Captures a fixed region of the screen and extracts text using Tesseract OCR.
- Matches extracted text against pre-defined event data.
- Displays matching options in a clean, readable format.

---

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and properly configured)
- The following Python libraries:
  - `pygetwindow`
  - `pyautogui`
  - `pywin32`
  - `pytesseract`

---

## Installation Guide

### 1. Install Python

Download and install Python from the [official website](https://www.python.org/downloads/).

Make sure to check the box that says: Add Python to PATH

You can verify the installation by running:

```
python --version
```

### 2. Install Tesseract OCR
Download Tesseract for Windows from UB Mannheim, install it.
You can also download the newest version by go to https://github.com/tesseract-ocr/tesseract/releases and get the newest tesseract-ocr-w64-setup-x.x.x.xxxxx.exe file
Make sure the file exist at C:\Program Files\Tesseract-OCR\tesseract.exe
(If you want to install it in other place, please replace that line in the UmaMusumeHelper.py file

### 3. Install Python libraries
Open a terminal or command prompt and run:

```
pip install pygetwindow pyautogui pywin32 pytesseract
```

### 4. Download this script
Either clone this repo or click on Code > Download ZIP on top of this github page

## How to Run
Once everything is installed and set up:
Make sure the "Umamusume" game is running and the event window is visible.

Open a cmd/Powershell at the location of the downloaded scripts with the command:

```
python UmaMusumeHelper.py
```

Keep the cmd open, you should see logs start coming up now.

Every 5 seconds, the script will capture and OCR the target region and try to return the value base on the data in the 3 data files

## Notes
This script assumes the game runs in 1920x1080 windowed mode.