#1: Import necessary classes(CasinoGame.py) and packages
import os
import time
from colorama import Fore, Style
from termcolor import colored
from CasinoGame import Games, Player, Blackjack, Roulette, Slotmachine

#2: Clear the terminal screen

os.system('cls' if os.name == 'nt' else 'clear')

#3: Welcome message and game logo

print("Welcome to Casino Royale!")
print("===========================")
print()

print(Fore.RED + """
 _____           _              ______                  _      
/  __ \         (_)             | ___ \                | |     
| /  \/ __ _ ___ _ _ __   ___   | |_/ /___  _   _  __ _| | ___ 
| |    / _` / __| | '_ \ / _ \  |    // _ \| | | |/ _` | |/ _ |
| \__/\ (_| \__ \ | | | | (_) | | |\ \ (_) | |_| | (_| | |  __/
 \____/\__,_|___/_|_| |_|\___/  \_| \_\___/ \__, |\__,_|_|\___|
                                             __/ |             
                                            |___/ 
""" + Style.RESET_ALL)

#4: Main game loop

while True:
    # Get user input
    choice = input("Enter \"play\" to start the game or \"quit\" to exit: ")

    # Process user input
    if choice.lower() == "play":
        # Start playing the game; add available games, add "Bank" as opposing player (Blackjack)
        print("Good luck!")
        games = Games("Casino Royale")
        bank = Player("Bank", 1000000, "low")
        games.add_game("Blackjack", Blackjack, bank)
        games.add_game("Roulette", Roulette)
        games.add_game("Slotmachine", Slotmachine)
        # Ask for player data
        player_name = input("What's your name? ")
        player_wealth = float(input("How many $$$ do you bring to the tables? "))
        while int(player_wealth) <= 0:
            player_wealth = input("You can\'t play any of our games without a sufficent balance. How much money do you bring to the tables? ")
        player_risk = input("What\'s your risk aversity? Choose between \"low\" (risk 1% of your balance per bet), \"medium\" (risk 2% of your balance per bet) or \"high\"(risk 3% of your balance per bet): ")
        while player_risk not in ["low", "medium", "high"]:
            player_risk = input("What's your risk aversity? Choose between \"low\", \"medium\" or \"high\": ")
        # Create player object
        player1 = Player(player_name, player_wealth, player_risk)
        print(player1)
        # Show available games, ask for preferred game
        print(games)
        games.print_available_games()
        while True:
            game_choice = input("Which game would you like to play? ").lower()
            if game_choice in [game.lower() for game in games.get_available_games()]:
                games.play_game(game_choice.capitalize(), player1)
                if player1.wealth <= 0: # In case player runs out of money the game quits automatically
                    print("You've run out of money! The casino security escorts you to the exit...")
                    print("Thanks for playing. Goodbye!")
                    exit()
                play_again = input("Do you want to play another game? (yes/no): ")
                if play_again.lower() == "no":
                    break
                elif play_again.lower() == "yes":
                    games.print_available_games()
                    continue
            else:
                print("Invalid choice. Please try again.")
    elif choice.lower() == "quit":
        # Exit the game
        print("Thanks for playing. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")##