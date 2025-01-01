import speech_recognition as sr
import pyttsx3
import wikipedia

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up the rate and volume of speech
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Function for speaking text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for listening to the user's voice command
def listen():
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, the speech service is down.")
        return ""

# Function to search Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Here are some options: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Wikipedia is taking too long to respond."
    except wikipedia.exceptions.RedirectError:
        return "The page you're looking for has been redirected."
    except Exception as e:
        return f"Sorry, I couldn't find any information. Error: {str(e)}"

# Main assistant function
def assistant():
    speak("Hello, I am your assistant. How can I help you today?")
    
    while True:
        command = listen()
        
        if 'stop' in command or 'exit' in command:
            speak("Goodbye!")
            break
        
        elif 'search' in command:
            speak("What would you like to search for?")
            query = listen()
            if query:
                response = search_wikipedia(query)
                speak(response)
        
        elif 'hello' in command:
            speak("Hello! How can I assist you?")
        
        elif 'how are you' in command:
            speak("I am just a program, but I'm doing great! Thank you for asking.")
        
        else:
            speak("Sorry, I didn't catch that. Can you repeat?")
        
if __name__ == "__main__":
    assistant()
