from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv() #load api key from .env file

#create groq client(our connection to the ai)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def test_groq():
    #send a simple msg to ai and get response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", #the llama 3 model we're using
        messages=[
            {"role": "user", "content": "Say hello and tell me you're ready to debate!"}
        ]
    )
    #extract the text response from the api response object
    print(response.choices[0].message.content)

#rune the test
test_groq()