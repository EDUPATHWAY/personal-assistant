import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification
import time

# Initialize the speech engine with error handling
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing pyttsx3: {e}")
    exit()  # Exit if pyttsx3 is not working

# Set properties (Optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I could not understand that. Please repeat.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech service. Please check your internet connection.")
            return None
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
            return None

# Weather function
def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        speak(f"The weather in {city} is currently {weather_desc} with a temperature of {temp} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather data.")

# Send email function
def send_email(subject, body, to_email):
    from_email = "your_email@gmail.com"  # Replace with your Gmail address
    password = "your_email_password"    # Replace with your Gmail password or App password

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Start TLS for security
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            speak(f"Email sent to {to_email}")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

# Set reminder function
def set_reminder(time_in_minutes, reminder_message):
    time.sleep(time_in_minutes * 60)
    notification.notify(
        title="Reminder",
        message=reminder_message,
        timeout=10  # The notification will show for 10 seconds
    )
    speak(f"Reminder: {reminder_message}")

# Execute command function
def execute_command(command):
    if "open youtube" in command:
        speak("Opening YouTube now.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google now.")
        webbrowser.open("https://www.google.com")
    elif "weather in" in command:
        city = command.replace("weather in", "").strip()
        get_weather(city)
    elif "send email" in command:
        speak("What is the subject of the email?")
        subject = listen_command()
        speak("What should I write in the email body?")
        body = listen_command()
        speak("Who is the recipient? Please provide the email address.")
        recipient = listen_command()
        send_email(subject, body, recipient)
    elif "set a reminder" in command:
        speak("In how many minutes would you like to be reminded?")
        minutes = int(listen_command())
        speak("What is the reminder message?")
        message = listen_command()
        set_reminder(minutes, message)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        search_google(query)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

# Main function
def run_assistant():
    speak("Hello, how can I assist you today?")
    
    while True:
        command = listen_command()
        if command:
            execute_command(command)

# Start the assistant
run_assistant()
