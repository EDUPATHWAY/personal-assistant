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
import pywhatkit as kit
from googlesearch import search
from bs4 import BeautifulSoup
import pygetwindow as gw

# Initialize pyttsx3 for text-to-speech
try:
    engine = pyttsx3.init()
    is_tts_working = True  # If pyttsx3 is working, we use it
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    is_tts_working = False  # If pyttsx3 fails, use gTTS

# Global variables
language = 'en'
user_name = "User"
is_sleeping = False
is_youtube_playing = False  # Track if YouTube is playing

# Get a greeting based on the time of day
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

# Speak text using pyttsx3 or gTTS (if pyttsx3 fails)
def speak(text):
    if is_tts_working:
        engine.say(text)
        engine.runAndWait()
    else:
        try:
            tts = gTTS(text=text, lang=language)
            tts.save("output.mp3")
            os.system("start output.mp3" if os.name == 'nt' else "mpg321 output.mp3")
        except Exception as e:
            print(f"Error speaking: {e}")

# Listen for user command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
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

# Execute commands based on user input
def execute_command(command):
    global user_name
    global is_sleeping
    global is_youtube_playing

    if is_sleeping:
        return  # Don't execute commands if the assistant is sleeping

    # Wake-up command
    if "hey pixel" in command:
        if is_sleeping:
            speak("Hello! I am awake now!")
            is_sleeping = False
        else:
            speak("I am already awake and listening.")
        return

    # Personalized greeting
    if "how are you" in command:
        speak(f"I am doing great, {user_name}! How can I assist you today?")
    
    # Command to search and read about a topic
    elif "i want to know about" in command:
        speak("What do you want to know?")
        topic = listen_command()
        if topic:
            search_and_read_about(topic)
        else:
            speak("I couldn't catch that. Please tell me what you want to know.")

    # Play YouTube video
    elif "play youtube" in command or "open youtube" in command:
        speak("What video would you like to watch?")
        video_name = listen_command()
        if video_name:
            kit.playonyt(video_name)
            is_youtube_playing = True
        else:
            speak("Sorry, I couldn't catch the video name.")

    # Turn off YouTube (close the browser tab)
    elif "turn off youtube" in command and is_youtube_playing:
        speak("Turning off YouTube.")
        # Attempt to close the YouTube tab
        try:
            windows = gw.getWindowsWithTitle('YouTube')
            if windows:
                window = windows[0]  # Get the first YouTube window
                window.close()
                is_youtube_playing = False
                speak("YouTube has been turned off.")
            else:
                speak("I couldn't find an open YouTube tab.")
        except Exception as e:
            print(f"Error closing YouTube: {e}")
            speak("Sorry, I couldn't turn off YouTube.")
    
    # Tell a joke
    elif "tell me a joke" in command:
        joke = get_joke()
        speak(joke)

    # Get system information
    elif "battery" in command:
        system_info = get_system_info()
        speak(f"Here is the system information: {system_info}")

    # Shutdown or restart commands
    elif "shutdown" in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "log off" in command:
        log_off_system()

    # Volume control
    elif "increase volume" in command or "decrease volume" in command or "mute volume" in command:
        control_volume(command)

    # Exit command
    elif "exit" in command or "quit" in command:
        speak(f"Goodbye, {user_name}!")
        exit()

    # Sleeping mode
    elif "thanks for helping" in command:
        speak("You're welcome! I am now going to sleep.")
        is_sleeping = True

# Function to search and read about a topic on Google
def search_and_read_about(topic):
    speak(f"Searching about {topic} on Google.")
    
    # Perform Google search
    query = topic
    try:
        search_results = list(search(query, num_results=5))  # Convert the generator to a list
        if search_results:
            result_url = search_results[0]
            speak(f"I found something on Google: {result_url}")

            try:
                response = requests.get(result_url)
                response.raise_for_status()  # Check if the request was successful
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the title of the page
                title = soup.title.string if soup.title else "No title available"
                speak(f"Here's what I found: {title}")

                # Read the first paragraph or summary
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = paragraphs[0].text
                    speak(f"Here's a summary: {content}")
                else:
                    speak("Sorry, I couldn't find any relevant content.")
                    
                speak("Would you like to know more about this topic?")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from the web: {e}")
                speak("Sorry, I couldn't retrieve information from the web.")
        else:
            speak("Sorry, I couldn't find anything on Google.")
    except Exception as e:
        print(f"Error searching Google: {e}")
        speak("Sorry, I couldn't perform the search.")

# Function to get a random joke
def get_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why don't some couples go to the gym? Because some relationships don't work out.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    return random.choice(jokes)

# Function to get system information (battery, CPU, memory, etc.)
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

# System control functions (shutdown, restart, log off)
def shutdown_system():
    speak("Shutting down your system.")
    os.system("shutdown /s /t 1" if os.name == 'nt' else "shutdown now")

def restart_system():
    speak("Restarting your system.")
    os.system("shutdown /r /t 1" if os.name == 'nt' else "reboot")

def log_off_system():
    speak("Logging off.")
    os.system("shutdown /l" if os.name == 'nt' else "gnome-session-quit --logout")

# Control volume (increase, decrease, mute)
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

# Start the assistant
def start_assistant():
    global user_name
    speak("Hello, What is your name?")

    # Wait for a valid user name (retry if None is returned)
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

# Main function to start the assistant
def main():
    start_assistant()

if __name__ == "__main__":
    main()
