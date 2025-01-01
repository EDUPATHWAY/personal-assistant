import pyttsx3
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import speech_recognition as sr

# Initialize pyttsx3 for text-to-speech
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

# Function to search for a topic on Google and read the first result
def search_and_read_topic(topic):
    speak(f"Searching for {topic}...")
    # Perform Google search (limit to 3 results to speed things up)
    search_results = search(topic, num=3)  # Limit to top 3 search results
    
    # Convert search_results from generator to a list
    search_results = list(search_results)

    if search_results:
        # Get the first result URL
        first_result_url = search_results[0]
        print(f"First result: {first_result_url}")
        speak(f"Fetching information from {first_result_url}")

        try:
            # Make a request to fetch the page content
            response = requests.get(first_result_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title of the page
            title = soup.title.string if soup.title else "No title available"
            speak(f"Title of the page: {title}")

            # Extract paragraphs (main content) from the page
            paragraphs = soup.find_all('p')
            content = ""
            for para in paragraphs[:3]:  # Limit to the first 3 paragraphs to speed up
                content += para.get_text() + "\n"
            
            if content:
                print("Content from the first search result:")
                print(content)
                speak("Here's what I found: " + content)
            else:
                speak("Sorry, I couldn't extract content from the page.")
        except Exception as e:
            print(f"Error fetching or parsing the webpage: {e}")
            speak("Sorry, there was an error while fetching the information.")
    else:
        speak("Sorry, I couldn't find any results on Google.")

# Main function to run the program
def main():
    print("Hello! I can search for a topic and read the results to you.")
    
    while True:
        speak("What do you want to know?")
        topic = listen_command()

        # If no valid topic was captured, ask again
        if not topic:
            speak("Sorry, I didn't catch that. Please repeat your topic.")
            continue

        # If the user wants to stop
        if 'found all things' in topic.lower():
            speak("You said you found all things. Goodbye!")
            break

        # Perform search and read the result aloud
        search_and_read_topic(topic)

        # Ask the user if they want to search again
        speak("Do you want to search for another topic, or say 'I found all things' to stop?")
        command = listen_command()

        if command and 'found all things' in command.lower():
            speak("You said you found all things. Goodbye!")
            break
        else:
            print("Let's continue!")

if __name__ == "__main__":
    main()
