import openai

# Your OpenAI API key
openai.api_key = 'your-api-key-here'

def test_openai():
    try:
        # A simple request to OpenAI's model (e.g., GPT-3)
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can change to another model if necessary
            prompt="Hello, OpenAI!",
            max_tokens=5
        )
        
        # Check if the response is successful
        if response:
            print("OpenAI is working!")
            print("Response:", response.choices[0].text.strip())
        else:
            print("Error: No response received.")
    
    except Exception as e:
        print("An error occurred:", e)

# Call the test function
test_openai()
