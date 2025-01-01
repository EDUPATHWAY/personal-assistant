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
from PIL import Image
from tkinter import Tk

# Initialize pyttsx3 for text-to-speech
try:
    engine = pyttsx3.init()
    is_tts_working = True  # If pyttsx3 is working, we use it
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    is_tts_working = False  # If pyttsx3 fails, use gTTS

# Variable to track language preference (English by default)
language = 'en'

# Function to display background image
def show_background_image(image_path):
    root = Tk()
    root.title("Assistant Running")  # Window Title
    img = Image.open(image_path)
    img = img.resize((800, 600))  # Resize to fit your screen (you can adjust dimensions)
    img.show()
    root.withdraw()  # Hide the tkinter main window (only the image will be shown)
    return root

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
    elif "open google" in command:
        speak("Opening Google now.")
        webbrowser.open("https://www.google.com")
    elif "battery" in command:
        system_info = get_system_info()
        speak(f"Here is the system information: {system_info}")
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "news" in command:
        speak("Fetching news for you.")
        # Call your get_news function here
    elif "weather in" in command:
        city = command.replace("weather in", "").strip()
        # Call your get_weather function here
    elif "tell me a joke" in command:
        speak("Here's a joke for you.")
        # Call your tell_joke function here
    elif "tell me a fact" in command:
        speak("Here's a fact for you.")
        # Call your tell_fact function here
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {current_time}.")
    elif "play music" in command:
        speak("Searching for music on YouTube.")
        # Call your play_music function here
    elif "shutdown" in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "log off" in command:
        log_off_system()
    elif "increase volume" in command or "decrease volume" in command or "mute volume" in command:
        control_volume(command)
    elif "open notepad" in command or "open chrome" in command or "open vs code" in command:
        open_application(command)
    elif "close notepad" in command or "close chrome" in command:
        close_application(command)
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

# Application Management Functions
def open_application(command):
    if "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad" if os.name == 'nt' else "gedit")
    elif "open chrome" in command:
        speak("Opening Chrome.")
        webbrowser.open("https://www.google.com/chrome/")
    elif "open vs code" in command:
        speak("Opening Visual Studio Code.")
        os.system("code" if os.name == 'nt' else "code")

def close_application(command):
    if "close notepad" in command:
        speak("Closing Notepad.")
        os.system("taskkill /im notepad.exe" if os.name == 'nt' else "pkill gedit")
    elif "close chrome" in command:
        speak("Closing Chrome.")
        os.system("taskkill /im chrome.exe" if os.name == 'nt' else "pkill chrome")

# Path to your image (change this path to the location where your image is stored)
image_path = "th.jpg"  # Replace with your image path

# Start the assistant and show the background image
def main():
    # Show the background image
    background_window = show_background_image(image_path)

    # Start the assistant
    start_assistant()

if __name__ == "__main__":
    main()
