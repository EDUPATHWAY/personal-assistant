import requests
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
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

# Function to search for a topic using Google Custom Search API and read the result aloud
def search_and_read_topic(topic):
    speak(f"Searching for {topic}...")
    
    # Your Google Custom Search API credentials
    api_key = 'YOUR_GOOGLE_API_KEY'  # Replace with your actual API key
    cx = 'YOUR_CSE_ID'  # Replace with your actual Custom Search Engine ID (CX)
    
    # Google API request URL
    url = f"https://www.googleapis.com/customsearch/v1?q={topic}&key={api_key}&cx={cx}"
    
    try:
        # Send the GET request to the Google Custom Search API
        response = requests.get(url)
        
        # Check if the response is valid JSON and contains results
        search_results = response.json()
        
        if 'items' in search_results:
            first_result = search_results['items'][0]  # Get the first result
            title = first_result['title']
            link = first_result['link']
            snippet = first_result.get('snippet', 'No description available.')
            
            print(f"Title: {title}")
            print(f"Link: {link}")
            print(f"Snippet: {snippet}")
            
            # Read the result aloud
            speak(f"Title: {title}")
            speak(f"Link: {link}")
            speak(f"Snippet: {snippet}")
        else:
            speak("Sorry, no results found.")
            
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, there was an error while fetching the information.")

# Main function to run the program
def main():
    print("Hello! I can search for a topic and read the results to you.")
    
    while True:
        speak("What do you want to know?")
        topic = listen_command()
        
        if not topic:
            speak("Sorry, I didn't catch that. Please repeat your topic.")
            continue
        
        if 'stop' in topic:
            speak("Goodbye!")
            break
        
        # Perform the search and read the result aloud
        search_and_read_topic(topic)

if __name__ == "__main__":
    main()
