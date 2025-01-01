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

# Global variable for storing the user’s name
user_name = "User"
is_sleeping = False  # Variable to track sleep mode status

# Function to get the appropriate greeting based on the time of day
def get_greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    elif 18 <= hour < 22:
        return "Good Evening"
    else:
        return "Good Night"

# Speak function using pyttsx3 or gTTS as a fallback
def speak(text):
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

# Function to execute commands
def execute_command(command):
    global user_name
    global is_sleeping

    # If the assistant is in sleep mode, don't execute any commands
    if is_sleeping:
        return

    # Weather update command (you need an API key for this)
    if "weather" in command:
        speak("Please wait, getting the weather information.")
        get_weather()
    
    # Personalized greeting
    elif "how are you" in command:
        speak(f"I am doing great, {user_name}! How can I assist you today?")

    # Play YouTube video
    elif "play youtube" in command:
        speak("What video would you like to watch?")
        video_name = listen_command()
        kit.playonyt(video_name)

    # Telling jokes
    elif "tell me a joke" in command:
        joke = get_joke()
        speak(joke)

    # Battery status
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
        speak(f"Goodbye, {user_name}!")
        exit()

    # If you say "thanks for helping", go into sleep mode
    elif "thanks for helping" in command:
        speak("You're welcome! I am now going to sleep.")
        is_sleeping = True

    # If you say "hello t2", wake up the assistant
    elif "hello t2" in command:
        speak("Hello, I am awake now!")
        is_sleeping = False

# Function to get weather information
def get_weather():
    # You need to get your own API key from OpenWeatherMap
    api_key = "your_api_key"
    city = "New York"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        main = data["main"]
        temp = main["temp"]
        weather = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {weather}.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

# Function to get a random joke
def get_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why don't some couples go to the gym? Because some relationships don't work out.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    return random.choice(jokes)

# Function to get system information
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

# Start the assistant and provide greeting
def start_assistant():
    global user_name
    speak("Hello, What is your name?")

    # Wait for a valid user name (retries if None is returned)
    while True:
        user_name = listen_command()
        if user_name:  # Only proceed if a valid name is received
            break
        else:
            speak("I didn't catch that. Could you please repeat your name?")
    
    # Check if the user said "Prince" or any other name
    if "prince" in user_name.lower():
        greeting = f"Hello boss, nice to meet you! {get_greeting()}"
    else:
        greeting = f"Hello sir, I guess you are my boss's friend. Nice to meet you! {get_greeting()}"

    speak(greeting)
    speak(f"What can I do for you today, {user_name}?")

    # Start listening for commands
    while True:
        command = listen_command()
        if command:
            execute_command(command)
        time.sleep(1)  # Added sleep to prevent excessive CPU usage

# Start the assistant
def main():
    # Start the assistant
    start_assistant()

if __name__ == "__main__":
    main()
