import speech_recognition as sr
import pyttsx3
import webbrowser
import openai 


openai.api_key ="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"

def say(text):
    engine = pyttsx3.init()  # Initialize the TTS engine
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6  # Adjust the pause threshold
        audio = r.listen(source)  # Listen for audio input
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  # Recognize speech
            print(f"user said: {query}")
            return query  # Return the recognized query
        except Exception as e:
            return "Some error occurred. Sorry from Jarvis."  # Handle errors
def get_openai_response(query):
    try:
        response =openai.completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "sorry, i couldn't process that request."
        
if __name__ == '__main__':
    print('Pycharm')
    
    say("Jarvis A.I.")
    while True:
        print("Listening....")
        query = takecommand()
        sites =[["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.com"],
                ["google","https://www.google.com"]]
        for site in sites:       
            if f"Open {site[0]} " .lower() in query.lower():
               say(f"opening {site[0]} sir...")
               webbrowser.open(site[1])
if "using artificial intelligent".lower() in query .lower():
    ai(prompt=query)