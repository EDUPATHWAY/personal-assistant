import pyttsx3
import speech_recognition as sr
import psutil
import webbrowser
import os
import time
import random
import requests
import datetime
from gtts import gTTS
from plyer import notification
import pyautogui
import subprocess
import os
from time import sleep
import pywhatkit as kit  # To play YouTube videos via voice commands

# Initialize pyttsx3 for text-to-speech
try:
    engine = pyttsx3.init()
    is_tts_working = True  # If pyttsx3 is working, we use it
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    is_tts_working = False  # If pyttsx3 fails, use gTTS

# Variable to track language preference (English by default)
language = 'en'

# Function to show a simple "image" in the terminal using ASCII art
def show_terminal_image(image_path):
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(image_path)
        img = img.convert("L")  # Convert image to grayscale
        img = img.resize((50, 50))  # Resize image for terminal display
        np_img = np.array(img)
        for row in np_img:
            print("".join(["@" if pixel < 128 else " " for pixel in row]))
    except Exception as e:
        print("Error showing image:", e)

# Speak function using pyttsx3 or gTTS as a fallback
def speak(text):
    if language == 'hi':  # Hindi Language
        try:
            tts = gTTS(text=text, lang='hi')
            tts.save("output.mp3")
            os.system("start output.mp3" if os.name == 'nt' else "mpg321 output.mp3")
        except Exception as e:
            print(f"Error speaking in Hindi: {e}")
    else:  # Default to English
        if is_tts_working:
            engine.say(text)
            engine.runAndWait()
        else:
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("output.mp3")
                os.system("start output.mp3" if os.name == 'nt' else "mpg321 output.mp3")
            except Exception as e:
                print(f"Error speaking: {e}")

# Listen command function
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjusting for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Network error. Please check your connection.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Function to start listening for commands
def start_assistant():
    active = False
    while True:
        if not active:
            print("Assistant is inactive.")
            command = listen_command()
            if command and "start" in command:
                speak("I am now awake and ready to assist you.")
                active = True
        else:
            print("Assistant is active.")
            command = listen_command()
            if command:
                execute_command(command)
                if "wait" in command:  # Stop listening when "wait" is said
                    speak("Pausing the assistant.")
                    active = False
            time.sleep(1)  # Added sleep to prevent excessive CPU usage

# Function to execute commands
def execute_command(command):
    if "open youtube" in command:
        speak("Opening YouTube now.")
        webbrowser.open("https://www.youtube.com")
    elif "play hindi song" in command:
        speak("Playing Hindi song for you.")
        kit.playonyt("Hindi song")  # Uses pywhatkit to play song from YouTube
    elif "stop youtube" in command:
        speak("Stopping YouTube.")
        # Since there's no direct way to stop YouTube using Python, you can try killing browser processes.
        os.system("taskkill /im chrome.exe" if os.name == 'nt' else "pkill chrome")
    elif "battery" in command:
        system_info = get_system_info()
        speak(f"Here is the system information: {system_info}")
    elif "shutdown" in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "log off" in command:
        log_off_system()
    elif "increase volume" in command or "decrease volume" in command or "mute volume" in command:
        control_volume(command)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

# Get system information function
def get_system_info():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "N/A"
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    try:
        cpu_temperature = psutil.sensors_temperatures()['coretemp'][0].current
    except (KeyError, IndexError):
        cpu_temperature = "N/A"

    return f"Battery: {battery_percent}% | CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | Disk Usage: {disk_usage}% | CPU Temp: {cpu_temperature}°C"

# System Control Functions
def shutdown_system():
    speak("Shutting down your system.")
    os.system("shutdown /s /t 1" if os.name == 'nt' else "shutdown now")

def restart_system():
    speak("Restarting your system.")
    os.system("shutdown /r /t 1" if os.name == 'nt' else "reboot")

def log_off_system():
    speak("Logging off.")
    os.system("shutdown /l" if os.name == 'nt' else "gnome-session-quit --logout")

def control_volume(command):
    if "increase volume" in command:
        pyautogui.press('volumeup')
        speak("Volume increased.")
    elif "decrease volume" in command:
        pyautogui.press('volumedown')
        speak("Volume decreased.")
    elif "mute volume" in command:
        pyautogui.press('volumemute')
        speak("Volume muted.")

# Start the assistant and show the background image
def main():
    # Show the background image in terminal
    show_terminal_image("th.jpg")  # Make sure the image is in your working directory

    # Start the assistant
    start_assistant()

if __name__ == "__main__":
    main()
