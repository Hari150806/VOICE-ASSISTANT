# ================== IMPORTS ==================
import os
import datetime
import threading
import queue
import subprocess
import shutil
import webbrowser

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

# ================== LOAD CONFIG ==================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-flash-latest")

# ================== STATE ==================
ACTIVE = threading.Event()

# ================== CHROME PATH ==================
def get_chrome_path():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return shutil.which("chrome")

CHROME_PATH = get_chrome_path()

# ================== TTS ==================
tts_queue = queue.Queue()

def tts_worker():
    engine = pyttsx3.init()
    engine.setProperty("rate", 185)
    for v in engine.getProperty("voices"):
        if "zira" in v.name.lower():
            engine.setProperty("voice", v.id)
            break
    while True:
        text = tts_queue.get()
        try:
            engine.say(text)
            engine.runAndWait()
        finally:
            tts_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    print("Jarvis:", text)
    tts_queue.put(text)

# ================== SYSTEM ==================
def set_volume(level):
    speakers = AudioUtilities.GetSpeakers()
    interface = speakers._ctl.QueryInterface(IAudioEndpointVolume)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

def tell_time():
    return datetime.datetime.now().strftime("%I:%M %p")

# ================== BROWSER ==================
def open_url(url, msg):
    speak(msg)
    if CHROME_PATH:
        subprocess.Popen([CHROME_PATH, url])
    else:
        webbrowser.open(url)

# ================== APPS (ALL YOU ASKED) ==================
APP_OPEN = {
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "notepad": "notepad.exe",
    "spotify": "Spotify.exe",
    "word": "WINWORD.EXE",
    "powerpoint": "POWERPNT.EXE",
    "file manager": "explorer.exe"
}

APP_PATH = {
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "notepad": "notepad",
    "spotify": "spotify",
    "word": "winword",
    "powerpoint": "powerpnt",
    "file manager": "explorer"
}

# ================== OPEN / CLOSE ==================
def open_app(app):
    if app in APP_PATH:
        speak(f"Opening {app}")
        subprocess.Popen(APP_PATH[app], shell=True)
    else:
        speak("Unknown application")

def close_app(app):
    if app in APP_OPEN:
        speak(f"Closing {app}")
        os.system(f"taskkill /f /im {APP_OPEN[app]}")
    else:
        speak("Cannot close that")

# ================== SPEECH ==================
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.6
mic = sr.Microphone()

def recognize(audio):
    try:
        return recognizer.recognize_google(audio, language="en-IN")
    except:
        return None

# ================== COMMAND UTILS ==================
def normalize(cmd):
    return cmd.replace("please", "").strip()

# ================== COMMAND HANDLER ==================
def handle_command(cmd):
    cmd = normalize(cmd)

    if cmd in ["hi", "hello", "hey"]:
        speak("Hello")
        return

    if cmd in ["sleep", "exit", "bye"]:
        speak("Shutting down. Goodbye")
        ACTIVE.clear()
        os._exit(0)

    if cmd == "open google":
        open_url("https://www.google.com", "Opening Google")
        return

    if cmd == "open youtube":
        open_url("https://www.youtube.com", "Opening YouTube")
        return

    if cmd.startswith("search"):
        q = cmd.replace("search", "").strip()
        open_url(f"https://www.google.com/search?q={q}", f"Searching {q}")
        return

    # IMPORTANT: YouTube/Search live INSIDE Chrome
    # FIX: NLP variations like "close search nlp", "close the search", etc.
    if "close" in cmd and "search" in cmd and "stop" in cmd:
        close_app("chrome")
        return

    if "close" in cmd and "youtube" in cmd:
        close_app("chrome")
        return

    if cmd.startswith("open"):
        open_app(cmd.replace("open", "").strip())
        return

    if cmd.startswith("close"):
        close_app(cmd.replace("close", "").strip())
        return

    if "time" in cmd:
        speak(tell_time())
        return

    # AI fallback
    try:
        reply = model.generate_content(cmd)
        speak(reply.text.strip())
    except:
        speak("AI unavailable")

# ================== TEXT MODE ==================
def text_loop():
    while True:
        txt = input("You: ").strip().lower()
        if txt == "jarvis":
            ACTIVE.set()
            speak("I'm listening")
            continue
        if ACTIVE.is_set():
            handle_command(txt)

threading.Thread(target=text_loop, daemon=True).start()

# ================== VOICE LOOP ==================
print("🎤 Jarvis running. Say 'jarvis'")

while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)

    text = recognize(audio)
    if not text:
        continue

    text = text.lower()
    print("You:", text)

    if not ACTIVE.is_set() and "jarvis" in text:
        ACTIVE.set()
        speak("I'm listening")
        continue

    if ACTIVE.is_set():
        handle_command(text)
