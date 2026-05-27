from debate_engine import start_debate, get_opening_message, chat

# Ask for movie
MOVIE = input("Enter a movie or show: ").strip()

# Ask for mode
print("\nPick a mode:")
print("1. debate")
print("2. villain")
print("3. plothole")
print("4. fantheory")
MODE = input("\nEnter mode name: ").strip().lower()

# Ask for user side only if debate mode
USER_SIDE = None
if MODE == "debate":
    USER_SIDE = input("What's your stance on this movie/show: ").strip()

#start the debate
start_debate(MODE, MOVIE, USER_SIDE)

# AI throws the first punch
opening = get_opening_message()
print(f"IMDBait: {opening}\n")

print("IMDBait is ready! Type ur arguments and press ENTER.\n Type 'enough! I can't defeat you Daddy' to end the debate.\n")

#keep debate on until user says enough
while True:
    user_input = input("You: ")

    if user_input.lower() == "enough! I can't defeat you Daddy":
        print("\nIMDBait: Hah, I knew you'd say that! Now suck my Fat one, in the end, I reign supreme! come back again to get your ass whooped\n")
        break


    response = chat(user_input)
    print(f"\nIMDBait: {response}\n")