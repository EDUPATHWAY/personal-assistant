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
import pyautogui
import subprocess
from time import sleep
import pywhatkit as kit
from googlesearch import search
from bs4 import BeautifulSoup
import platform
import cpuinfo
import socket
import openai  # Import OpenAI library

# Initialize pyttsx3 for text-to-speech
try:
    engine = pyttsx3.init()
    is_tts_working = True  # If pyttsx3 is working, we use it
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    is_tts_working = False  # If pyttsx3 fails, use gTTS

# Global variables
language = 'In-en'
user_name = "User"
is_sleeping = False  # Initially, the assistant is awake
openai.api_key = "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"  # Replace with your OpenAI API Key

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

# Function to interact with OpenAI API for advanced responses
def get_openai_response(query):
    try:
        # Requesting OpenAI's GPT model to answer the query
        response = openai.Completion.create(
            moderl="get-3.5-turbo",
            engine="text-davinci-003",  # Or use a different model if needed
            prompt=query,
            max_tokens=150  # Max number of tokens (words) in the response
        )
        answer = response.choices[0].text.strip()  # Extract the text answer from the response
        return answer
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't get a response from OpenAI."

# Shutdown, restart, and sleep commands handling
def execute_shutdown():
    try:
        os.system("shutdown /s /f /t 1")  # Command for Windows shutdown
    except Exception as e:
        print(f"Error executing shutdown: {e}")
        speak("There was an error while shutting down.")

def execute_restart():
    try:
        os.system("shutdown /r /f /t 1")  # Command for Windows restart
    except Exception as e:
        print(f"Error executing restart: {e}")
        speak("There was an error while restarting.")

def execute_sleep():
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Command for Windows sleep
    except Exception as e:
        print(f"Error executing sleep mode: {e}")
        speak("There was an error while going to sleep.")

# Execute commands based on user input
def execute_command(command):
    global is_sleeping  # Declare global variable is_sleeping

    if is_sleeping:
        print("Assistant is sleeping. Not responding to commands.")
        return  # Don't execute commands if the assistant is sleeping

    # Personalized greeting
    if "how are you" in command:
        speak(f"I am doing great, {user_name}! How can I assist you today?")

    # Command to ask OpenAI a question
    elif "ask openai" in command or "what is" in command:
        speak("Let me ask OpenAI for you.")
        question = command.replace("ask openai", "").strip()  # Get the question after the phrase
        if question:
            response = get_openai_response(question)
            speak(response)  # Speak out OpenAI's response
        else:
            speak("Sorry, I didn't catch the question. Please try again.")

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
        else:
            speak("Sorry, I couldn't catch the video name.")

    # Stop YouTube video
    elif "turn off youtube" in command:
        speak("Turning off YouTube.")
        os.system("taskkill /f /im chrome.exe")  # This works if you are using Chrome; adjust for other browsers

    # Get system information
    elif "tell me about my laptop" in command or "system info" in command:
        speak_system_info()

    # Shutdown or restart commands
    elif "shutdown" in command:
        speak("Shutting down the system.")
        execute_shutdown()  # Use the new function to handle shutdown

    elif "restart" in command:
        speak("Restarting the system.")
        execute_restart()  # Use the new function to handle restart

    elif "sleep" in command or "go to sleep" in command:
        speak("Putting the system to sleep.")
        execute_sleep()  # Use the new function to handle sleep mode

    # Volume control
    elif "increase volume" in command or "decrease volume" in command or "mute volume" in command:
        control_volume(command)

    # Weather
    #elif "weather" in command or "what is the weather" in command:
     #   speak("Fetching the weather for you.")
      #  get_weather()
        

    # Exit command
    elif "exit" in command or "quit" in command:
         speak(f"Goodbye, {user_name}!")
         exit()

    # Sleeping mode
    elif "thanks for helping" in command:
        speak("You're welcome! I am now going to sleep.")
        is_sleeping = True

    # Wake-up command
    elif "hello pixel" in command:
        speak("I am ready to help. What do you want to do for you?")
        is_sleeping = False

    # "Bye" command to go to sleep
    elif "bye" in command:
        speak("I am going to sleep now. Goodbye!")
        is_sleeping = True

# Function to search and read about a topic on Google
def search_and_read_about(topic):
    speak(f"Searching about {topic} on Google.")
    
    # Perform Google search
    query = topic
    search_results = list(search(query, num_results=5))  # Convert the generator to a list
    
    if search_results:
        result_url = search_results[0]
        speak(f"I found something on Google: {result_url}")

        try:
            response = requests.get(result_url)
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
        except Exception as e:
            print(f"Error fetching data from the web: {e}")
            speak("Sorry, I couldn't retrieve information from the web.")
    else:
        speak("Sorry, I couldn't find anything on Google.")

# Function to get system information (battery, CPU, memory, etc.)
def get_system_info():
    # Battery Information
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "N/A"
    
    # CPU Information
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_info = cpuinfo.get_cpu_info()
    cpu_model = cpu_info.get('model', 'N/A')
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores
    cpu_threads = psutil.cpu_count(logical=True)  # Logical cores

    # Memory Information
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    total_memory = memory.total / (1024 ** 3)  # Convert to GB

    # Disk Information
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    total_disk = disk.total / (1024 ** 3)  # Convert to GB

    # Operating System Information
    os_info = platform.uname()
    os_name = os_info.system
    os_version = os_info.version
    os_release = os_info.release

    # Network Information
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    system_info = f"""
    Operating System: {os_name} {os_version} {os_release}
    CPU: {cpu_model}
    CPU Cores: {cpu_cores} (Logical: {cpu_threads})
    CPU Usage: {cpu_usage}%
    Memory: {total_memory:.2f} GB (Used: {memory_usage}%)
    Disk Space: {total_disk:.2f} GB (Used: {disk_usage}%)
    Battery: {battery_percent}% (If available)
    Hostname: {hostname}
    IP Address: {ip_address}
    """
    return system_info

# Function to speak the system information
def speak_system_info():
    system_info = get_system_info()
    speak(system_info)

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
webbrowser.open('https://www.example.com')
# Main function to start the assistant
def main():
    start_assistant()

if __name__ == "__main__":
    main()
