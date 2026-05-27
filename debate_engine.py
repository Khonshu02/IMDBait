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

def get_opening_message():
      """
      Called once after start_debate() to get the AI's opening statement.
      The AI throws the first punch before the user says anything.
      """
      global conversation_history

      #we send a hidden trigger message to get the opening statement
      #This message won't be shown to the user
      trigger = "Make your opening statemnet now. Set the tone and challenge me."

      conversation_history.append({
            "role":"user",
            "content": trigger
      })

      response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation_history
      )

      opening = response.choices[0].message.content

      #replace the trigger with AI's opening history 
      #later the trigger shouldn't show up as the user msg
      conversation_history[-1] = {
            "role":"user",
            "content": "[debate started]"
        }
      
      #Add AI opening to history
      conversation_history.append({
            "role":"assistant",
            "content": opening
      })

      return opening

def validate_input(user_message):
      """
      Checks if the user's message is valid before sending to API.
      return a tuple: (is valid, error_message)
      """
      #check if message is empty or just whitespace
      if not user_message or user_message.strip() == " ":
            return False, "Say Something retard! I'm not debating with the air."
      
      #check if the message is too short to argue with
      if len(user_message.strip()) < 3:
            return False, "Is that even an argument?! atleast put some efforts in defending you end of the debate!"
      
      #check if the message is too long - trim long messages
      if len(user_message.strip()) > 1000:
            return False, "Easy there now! this is not a court of justice that you bring in an entire case file to discuss, neither is this your discussion group of bunch of losers."
      
      return True, None

def chat(user_message):
        """
        called every time the user sends a message.
        adds user msg to history,gets AI response, and saves it.
        """
        global conversation_history

        #validate and add user's message to history
        is_valid, error = validate_input(user_message)
        if not is_valid:
            return error

        conversation_history.append({
            "role": "user",
            "content": user_message
        
        })

        #send complete history to groq api and get a response
        try:
            response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
            )
            
            #Extract the AI's response text
            ai_message = response.choices[0].message.content
        except Exception as e:
              #remove the user from history if API call Falied
              conversation_history.pop()
              return f"Connection issue. Try again. (Error: {str(e)})"

        #Add AI's response to history so it remembers it nxt time
        conversation_history.append({
            "role": "assistant",
            "content": ai_message
        })

        return ai_message