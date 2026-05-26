from groq import Groq
from dotenv import load_dotenv
from prompts import get_system_prompt
import os

#load api key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#a list to store the convo history
conversation_history = []

def start_debate(mode, movie, user_side=None):
    """ 
    Called once at the start of the deabte session.
    Sets up the system prompt and clears any prev history.
    """
    global conversation_history

    #clear history for every new debate
    conversation_history = []

    #Get the right system prompt based on movie and mode
    system_prompt = get_system_prompt(mode, movie, user_side)

    #Add system prompt at the top of the history - this is the AI's secret briefing
    conversation_history.append({
        "role": "system",
        "content": system_prompt
    })

    print(f"\n Starting {mode.upper()} debate about '{movie}'...\n")

def chat(user_message):
        """
        called every time the user sends a message.
        adds user msg to history,gets AI response, and saves it.
        """
        global conversation_history

        #add user's message to history
        conversation_history.append({
            "role": "user",
            "content": user_message
        
        })

        #send complete history to groq api and get a response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )

        #Extract the AI's response text
        ai_message = response.choices[0].message.content

        #Add AI's response to history so it remembers it nxt time
        conversation_history.append({
            "role": "assistant",
            "content": ai_message
        })

        return ai_message