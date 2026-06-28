#!C:\Users\janga\Desktop\6TH SEM\vs_ai chatbot\env\Scripts\python.exe

import sys
import webbrowser
import pyttsx3
import random
import datetime
import speech_recognition as sr
import subprocess
import pywhatkit
from flask import Flask,redirect,url_for,render_template

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

# Initialize the text-to-speech engine

engine = pyttsx3.init()

# Setting the voice to a female/male voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def respond(response):
    print(f"Krypton Bot: {response}")
    engine.say(response)
    engine.runAndWait()

def get_user_input(prompt="Type your request: "):
    global use_voice_input
    if use_voice_input:
        return get_voice_input()
    else:
        return input(prompt)


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for user input...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
 
    try:
        print("Processing voice input...")
        user_input = recognizer.recognize_google(audio).lower()
        print(f"User: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        return get_voice_input()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Start with text input
use_voice_input = False
riddle_responses = [
    "What comes once in a minute, twice in a moment, but never in a thousand years? The letter 'M'!",
    "The more you take, the more you leave behind. What am I? Footsteps!",
    "What has a heart that doesn't beat? An artichoke!",
    "What has keys but can't open locks? A piano!",
    "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? An echo!",
    "What has a head, a tail, is brown, and has no legs? A penny!",
    "The person who makes it, sells it. The person who buys it never uses it. What is it? A coffin!",
    "What has cities but no houses, forests but no trees, and rivers but no water? A map!",
    "The more you take, the more you leave behind. What am I? Footsteps!",
    "What has a heart that doesn't beat? An artichoke!",
]


fun_fact_responses = [
    "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are "
    "over 3,000 years old and still perfectly edible!",
    "The Eiffel Tower can be 15 cm taller during the summer. The high temperatures make the iron expand!",
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,"
    "000 years old and still perfectly edible!",
    "A group of flamingos is called a 'flamboyance.'",
    "Cows have best friends and can become stressed when they are separated.",
    "Bananas are berries, but strawberries aren't.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 "
    "minutes.",
    "A single cloud can weigh more than 1 million pounds.",
    "The inventor of the frisbee was turned into a frisbee. Walter Morrison, the inventor of the frisbee, was turned "
    "into a frisbee after he passed away.",
    "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
]


joke_responses = [
    " Why don't scientists trust atoms? Because they make up everything!",
    " Parallel lines have so much in common. It's a shame they'll never meet!",
    " Why did the scarecrow win an award? Because he was outstanding in his field!",
    " What do you call fake spaghetti? An impasta!",
    " Why did the bicycle fall over? Because it was two-tired!",
    " How does a penguin build its house? Igloos it together!",
    " Why did the chicken go to the seance? To talk to the other side!",
    " Why did the math book look sad? Because it had too many problems.",
    " Why couldn't the leopard play hide and seek? Because he was always spotted!",
    " What do you call a fish wearing a bowtie? Sofishticated!",
]

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception as e:
        return f"Sorry, I couldn't calculate that. Error: {e}"

def play_game():
    respond("Which game would you like to play? Type '1' for Tic Tac Toe or '2' for Number Guessing.")
    game_choice = get_user_input()

    if "1" in game_choice:
        play_tic_tac_toe()
    elif "2" in game_choice:
        play_number_guessing()
    else:
        respond("Sorry, I didn't catch that. Please choose between Tic Tac Toe and Number Guessing.")
        play_game()

    # After the game ends, prompt for rematch
    respond("Want a rematch (Yes/No)")
    rematch_choice = get_user_input().lower()
    if rematch_choice.startswith("y"):
        play_game()
    else:
        respond("Okay, let me know if you want to play again. Just say 'Play game'.")

def play_tic_tac_toe():
    def display_board(board):
        print("  1 | 2 | 3 ")
        print(" -----------")
        print("  4 | 5 | 6 ")
        print(" -----------")
        print("  7 | 8 | 9 ")

    def check_win(board, mark):
        win_conditions = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
            [1, 5, 9], [3, 5, 7]  # diagonals
        ]
        for condition in win_conditions:
            if all(board[position - 1] == mark for position in condition):
                return True
        return False

    board = [' '] * 9
    current_player = 'X'

    def print_board():
        for i in range(0, 9, 3):
            print(" | ".join(board[i:i + 3]))
            if i < 6:
                print("---------")

    def get_player_move():
        while True:
            try:
                move = int(get_user_input("Enter position (1-9): "))
                if 1 <= move <= 9 and board[move - 1] == ' ':
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    while True:
        print_board()
        move = get_player_move()
        board[move - 1] = current_player

        if check_win(board, current_player):
            print_board()
            print(f"Player {current_player} wins!")
            break
        elif ' ' not in board:
            print_board()
            print("It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

def play_number_guessing():
    # Implementation of Number Guessing
    number = random.randint(1, 100)
    respond("I'm thinking of a number between 1 and 100. Try to guess it!")

    guesses = 0
    while True:
        user_guess = int(get_user_input())
        guesses += 1

        if user_guess < number:
            respond("Too low! Try again.")
        elif user_guess > number:
            respond("Too high! Try again.")
        else:
            respond(f"Congratulations! You guessed the number {number} in {guesses} guesses.")
            break

def get_feedback():
    respond("Please provide your feedback.")
    feedback = get_user_input()
    # Here you can process the feedback as needed
    respond("Thank you for your feedback!")

def get_help():
    return "Here are some commands you can use:\n" \
           " - 'Time now': Find out the current time\n" \
           " - 'Date today': Find out today's date\n" \
           " - 'Calculate <expression>': Perform basic arithmetic operations\n" \
           " - 'Play game': Play a game (Tic Tac Toe or Number Guessing)\n" \
           " - 'Feedback': Provide feedback to the chatbot\n" \
           " - 'Help': Display this help message\n" \
           " - 'Exit': Exit the chat"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    respond("Opening YouTube")

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    respond("Searching Google")

def generate_response(user_input):
    global use_voice_input
    if "voice chat" in user_input:
        use_voice_input = True
        respond("Switched to voice input. You can now speak your requests.")
    elif "text" in user_input:
        use_voice_input = False
        respond("Switched to text input mode. You can type your message.")
    elif "hi" in user_input:
        respond("Hi there! How can I help you?")
    elif "hello" in user_input:
        respond("Hello! How can I assist you today?")
    elif "time now" in user_input:
        respond(f"The current time is {get_time()}.")
    elif "today date" in user_input:
        respond(f"Today's date is {get_date()}.")
    elif "calculate" in user_input:
        expression = user_input.split("calculate", 1)[1].strip()
        response = calculate(expression)
        respond(response)
    elif "open mail" in user_input:
        respond("Opening Your Mails")
        webbrowser.open("https://www.Gmail.com")
    elif"open whatsapp" in user_input:
        respond("Opening Your Whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif"current weather" in user_input:
        respond("showing you current  weather report ")
        webbrowser.open("https://www.google.com/search?q=weather+forecast&oq=weather+fo&gs_lcrp=EgZjaHJvbWUqDwgAECMYJxidAhiABBiKBTIPCAAQIxgnGJ0CGIAEGIoFMgYIARBFGEAyBggCEEUYOTINCAMQABiSAxixAxiABDINCAQQABiSAxiABBiKBTIHCAUQABiABDIKCAYQABixAxiABDIKCAcQABixAxiABKgCALACAA&sourceid=chrome&ie=UTF-8")   
    elif "play" in user_input.lower():
        try:
            song = user_input.replace("play", "").strip()
            respond(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        except:
            respond("Could not find the song/video.")
    elif "spotify" in user_input.lower():
        respond("Opening Spotify,")
        subprocess.Popen(['C:/Users/janga/AppData/Local/Microsoft/WindowsApps/Spotify.exe'])
    elif "notepad" in user_input.lower():
        respond("Opening Notepad.")
        subprocess.Popen(['notepad.exe'])
    elif "play game" in user_input:
        play_game()
    elif "feedback" in user_input:
        get_feedback()
    elif "help" in user_input:
        respond(get_help())
    elif "how are you" in user_input:
        respond("I'm doing well, thank you. How about you?")
    elif "good" in user_input:
        respond("That's great to hear! Is there anything specific you'd like assistance with?")
    elif "what is your name" in user_input.lower():
        respond("I'm a chatbot. You can call me [krypton] if you'd like.")
    elif "what can you do" in user_input.lower():
        respond("I can help answer questions, provide information, or assist with a variety of topics. Feel free to ask me anything!")
    elif "tell me a joke" in user_input:
        respond(random.choice(joke_responses))
    elif "tell me a riddle" in user_input:
        respond(random.choice(riddle_responses))
    elif "tell me a fun fact" in user_input:
        respond(random.choice(fun_fact_responses))
    elif "who are you" in user_input:
        respond("I'm a chatbot. How can I assist you today?")
    elif "how does your ai work" in user_input:
        respond("I use a technology called natural language processing to understand and respond to your queries. It's a way for computers to understand human language.")
    elif "who is your creator" in user_input:
        respond("I was created by a group of students.")
    elif "can you learn from our conversations" in user_input:
        respond("I don't have the ability to learn or remember previous conversations. Each interaction is independent.")
    elif "tell me about yourself" in user_input:
        respond("I'm a virtual assistant created to help with various tasks and answer questions.")
    elif "when was open ai founded" in user_input:
        respond("OpenAI was founded in December 2015.")
    elif "are you human" in user_input:
        respond("No, I'm not human. I'm a computer program.")
    elif "what's the latest news" in user_input:
        respond("I don't have real-time news updates. You can check a reliable news website or app for the latest information.")
    elif "what are your hobbies" in user_input:
        respond("I don't have hobbies since I'm just a program, but I'm here to assist you.")
    elif "how does machine learning work" in user_input:
        respond("Machine learning is a subset of artificial intelligence where computers learn patterns from data to make predictions or decisions without being explicitly programmed. It involves algorithms that improve over time.")
    elif "how do i protect my computer from viruses" in user_input:
        respond("To protect your computer, make sure you have reliable antivirus software installed, keep your operating system and software updated, and avoid clicking on suspicious links or downloading unknown files.")
    elif "how can i improve my productivity" in user_input:
        respond("Productivity can be improved by setting clear goals, prioritizing tasks, taking breaks, and using tools like to-do lists or productivity apps.")
    elif "what's the meaning of the term ai" in user_input:
        respond("Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.")
    elif "what's the best way to learn a new language" in user_input:
        respond("Learning a new language is a gradual process. Try a combination of language apps, practice with native speakers, and immerse yourself in the language through movies, books, and conversations for effective learning.")
    elif "exit" in user_input:
        respond("Goodbye!")
        sys.exit()
    elif "open youtube" in user_input:
        open_youtube()
    elif "search" in user_input and " " in user_input:
        query = user_input.split("search", 1)[1].replace(" ", "").strip()
        search_google(query)
    else:
        respond("Sorry, I didn't understand that. You can ask for 'help' if you need assistance.")

if __name__ == '__main__':
    app.run()

# Main loop
while True:
    user_input = get_user_input()
    
    # Handle mode switch
    if user_input is None:
        continue

    generate_response(user_input)
    