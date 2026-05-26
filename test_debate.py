from debate_engine import start_debate, chat

# ---CHANGE THESE TO TEST DIFF MODES---
MOVIE = "one piece"
MODE = "villain"
USER_SIDE = "Spandam is the most evil character ever and his actions are unjustifiable."
# --------------

#start the debate
start_debate(MODE, MOVIE, USER_SIDE)

print("IMDBait is ready! Type ur arguments and press ENTER.\n Type 'enough! I can't defeat you Daddy' to end the debate.\n")

#keep debate on until user says enough
while True:
    user_input = input("You: ")

    if user_input.lower() == "enough! I can't defeat you Daddy":
        print("\nIMDBait: Hah, I knew you'd say that! Now suck my Fat one, in the end, I reign supreme! come bac again to get your ass whooped\n")
        break
    if user_input.strip() == "":
        continue
    response = chat(user_input)
    print(f"\nIMDBait: {response}\n")