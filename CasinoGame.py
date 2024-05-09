#FirstLine
import random

class Games:
    
    def __init__(self, name):
        self.name = name
        self.games = {}
    
    def __repr__(self):
        return "There are currently {games} different games to choose from.".format(games = len(self.games))
    
    def add_game(self, game_name, game_class, *args):
        self.games[game_name] = (game_class, args)

    def get_available_games(self):
        return list(self.games.keys())
    
    def play_game(self, game_name, player):
        if game_name in self.games:
            game_class, args = self.games[game_name]
            game = game_class()
            game.play(player, *args)
        else:
            print("Sorry, that game is not available.")


class Player:
    
    def __init__(self, name, wealth, risk_aversity, is_broke = False):
        self.name = name
        self.wealth = wealth
        self.risk_aversity = risk_aversity
        self.is_broke = is_broke
        self.hand = []
        self.bet_type = ""
        self.chosen_number = None
        self.chosen_numbers = []
    
    def __repr__(self):
        status_broke = ""
        if self.is_broke:
            status_broke = "is broke."
        else:
            status_broke = "not (yet) broke."
        return "Your name is {name}, you have {wealth}$ in your pocket remaining and therefore considered {status}. Your risk aversity is: {risk_aversity}.".format(name=self.name, wealth=self.wealth, status=status_broke, risk_aversity=self.risk_aversity)
    
    def add_card(self, card):
        self.hand.append(card)

    def calculate_hand(self):
        ace_count = self.hand.count(11)
        total = sum(self.hand)
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
        return total
    
    def bet(self):
        if self.risk_aversity == "low":
            bet_amount = self.wealth * 0.01
        elif self.risk_aversity == "medium":
            bet_amount = self.wealth * 0.05
        elif self.risk_aversity == "high":
            bet_amount = self.wealth * 0.1
        self.wealth -= bet_amount
        return bet_amount

class Blackjack:
    def __init__(self):
        self.deck = [i for i in range(1, 12)] * 4
        random.shuffle(self.deck)

    def __repr__(self):
        return "Welcome to Blackjack!"
    
    def payout(self, player, bank, bet_amount):
        player_total = player.calculate_hand()
        bank_total = bank.calculate_hand()
        initial_wealth = player.wealth + bet_amount

        if player_total > 21 or (bank_total <= 21 and bank_total > player_total):
            print(f"{player.name} loses the bet.")
        elif player_total == 21:
            print(f"{player.name} got a Blackjack!")
            player.wealth += bet_amount * 2.5  # Return the bet amount and the winnings at 3:2 ratio
        elif bank_total > 21 or player_total > bank_total:
            print(f"{player.name} wins the bet.")
            player.wealth += bet_amount * 2  # Return the bet amount and the winnings
        else:  # It's a tie
            print("It's a tie.")
            player.wealth += bet_amount  # Return the bet amount

        winnings = player.wealth - initial_wealth
        if winnings > 0:
            print(f"{player.name} won {format(winnings, '.2f')}$ in this round.")
        elif winnings < 0:
            print(f"{player.name} lost {format(-winnings, '.2f')}$ in this round.")
        else:
            print(f"{player.name} didn't win or lose money in this round.")
        print(f"{player.name}'s current balance is {format(player.wealth, '.2f')}$.")
    
    def deal_card(self, player):
        card = self.deck.pop() 
        player.hand.append(card)
        card_str = f"######\n# {card:02d} #\n######\n######\n######"
        return card_str

    def print_hand(self, player):
        hand_str = ", ".join([str(card) if card != 11 or sum(player.hand) <= 21 else f"{card}(1)" for card in player.hand])
        print(f"{player.name}'s hand: [{hand_str}], total: {player.calculate_hand()}")

    def print_rules(self):
        print("Here are the rules:")
        print("1. You are competing against the bank. The goal is to get as close to 21 as possible without going over.")
        print("2. You start with two cards and can choose to draw more.")
        print("3. The bank will draw cards until it has at least 17.")
        print("4. If you go over 21, or if the bank gets closer to 21 than you without going over, you lose.")
        print("5. If you get 21 exactly (Blackjack!), or if the bank goes over 21, you win.")
        print("6. If neither you nor the bank gets 21, the one closest to 21 wins.")
        print("7. REMEMBER: An Ace can be treated as either the value of 1 or 11!")

    def player_choice(self, player):
        choice = input(f"{player.name}, do you want to draw another card? (yes/no) ")
        return choice.lower() == "yes"
       
    def play(self, player, bank):
        self.print_rules()
        while True:
            start_game = input("Do you want to start the game and draw two cards? (yes/no): ")
            if start_game.lower() == "yes":
                # Deal initial cards
                self.deal_card(player)
                self.deal_card(player)
                self.deal_card(bank)
                self.deal_card(bank)

                # Print player's and bank's cards
                print(f"{player.name} drew the following cards:")
                for i in range(5):  # Assuming each card has 5 lines
                    for card in player.hand:
                        if i == 2:  # The line with the card number
                            print(f"# {card:02d} #  ", end='')
                        else:
                            print("######  ", end='')
                    print()
                print("\n")  # Print a large space
                print("Bank drew the following cards:")
                for i in range(5):  # Assuming each card has 5 lines
                    for card in bank.hand:
                        if i == 2:  # The line with the card number
                            print(f"# {card:02d} #  ", end='')
                        else:
                            print("######  ", end='')
                    print()

                bet_amount = player.bet()
                outcome = None # Variable to keep track of the game's outcome
                while self.player_choice(player):
                    self.deal_card(player)
                    self.print_hand(player)
                    for i in range(5):  # Assuming each card has 5 lines
                        for card in player.hand:
                            if i == 2:  # The line with the card number
                                print(f"# {card:02d} #  ", end='')
                            else:
                                print("######  ", end='')
                        print()
                    if player.calculate_hand() > 21:
                        print(f"{player.name} is overbought!")
                        outcome = 'overbought'
                        break
                    elif player.calculate_hand() == 21:
                        print(f"{player.name} has a Blackjack!")
                        outcome = 'blackjack'
                        break
                    elif bank.calculate_hand() >= 17 and player.calculate_hand() > bank.calculate_hand():
                        print(f"{player.name} wins!")
                        outcome = 'win'
                        break
            
                if outcome is None:
                    while bank.calculate_hand() < 17:
                        self.deal_card(bank)
                        print(f"Bank's hand: {bank.hand}, total: {bank.calculate_hand()}")
                        for i in range(5):  # Assuming each card has 5 lines
                            for card in bank.hand:
                                if i == 2:  # The line with the card number
                                    print(f"# {card:02d} #  ", end='')
                                else:
                                    print("######  ", end='')
                            print()

                self.payout(player, bank, bet_amount)
                self.reset(player, bank)

                play_again = input("Do you want to play another round of Blackjack? (yes/no): ")
                if play_again.lower() != "yes":
                    break
            elif start_game.lower() == "no":
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def reset(self, player, bank):
        player.hand = []
        bank.hand = []
        self.deck = [i for i in range(1, 12)] * 4
        random.shuffle(self.deck)

class Roulette:

    def __init__(self):
        self.roulette_options = {
    0: "green",
    1: "red",
    2: "black",
    3: "red",
    4: "black",
    5: "red",
    6: "black",
    7: "red",
    8: "black",
    9: "red",
    10: "black",
    11: "black",
    12: "red",
    13: "black",
    14: "red",
    15: "black",
    16: "red",
    17: "black",
    18: "red",
    19: "red",
    20: "black",
    21: "red",
    22: "black",
    23: "red",
    24: "black",
    25: "red",
    26: "black",
    27: "red",
    28: "black",
    29: "black",
    30: "red",
    31: "black",
    32: "red",
    33: "black",
    34: "red",
    35: "black",
    36: "red"
}
        self.betting_grid = [
    ["3", "6", "9", "12", "15", "18", "21", "24", "27", "30", "33", "36"],
    ["2", "5", "8", "11", "14", "17", "20", "23", "26", "29", "32", "35"],
    ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
    ["0", "00"]
]
        self.bet_types = {
    "Straight Up": "Bet on a single number.",
    "Split Bet": "Bet on two adjacent numbers by placing chips on the line between them.",
    "Street Bet": "Bet on three numbers in a row (a 'street') by placing chips on the edge of the row.",
    "Corner Bet": "Bet on a group of four numbers that form a square by placing chips at the corner where the four numbers meet.",
    "Line Bet": "Bet on six numbers by placing chips on the edge of two adjacent rows.",
    "Dozens Bet": "Bet on a group of twelve numbers (1-12, 13-24, or 25-36).",
    "Column Bet": "Bet on a vertical column of twelve numbers.",
    "Even/Odd": "Bet on whether the ball will land on an even or odd number.",
    "Red/Black": "Bet on whether the ball will land on a red or black number.",
    "Low/High": "Bet on whether the ball will land on a low (1-18) or high (19-36) number."
}


    def __repr__(self):
        return "Welcome to Roulette!"
    
    def spin_wheel(self):
        self.winning_number = random.randint(0, 36)

    def choose_bet_type(self):
        bet_type = input("Please enter your bet type: ")
        if bet_type in self.bet_types:
            if bet_type == "Straight":
                self.straight_bet()
            elif bet_type == "Split":
                self.split_bet()
            elif bet_type == "Street":
                self.street_bet()
            elif bet_type == "Corner":
                self.corner_bet()
            elif bet_type == "Six Line":
                self.six_line_bet()
            elif bet_type == "Column":
                self.column_bet()
            elif bet_type == "Dozen":
                self.dozen_bet()
            elif bet_type == "Red/Black":
                self.red_black_bet()
            elif bet_type == "Even/Odd":
                self.even_odd_bet()
            elif bet_type == "Low/High":
                self.low_high_bet()
            return bet_type
        else:
            print("Invalid bet type")
            return self.choose_bet_type()
    
    def show_bet_types(self):
        self.all_bet_types = []
        for key in self.bet_types.keys():
            self.all_bet_types.append(self.bet_types[key])
        return "These are all the possible bet types you can choose from: " + ", ".join(self.all_bet_types)
    
    def explain_bet_type(self, bet_type):
        if bet_type in self.bet_types:
            return self.bet_types[bet_type]
        else:
            return "Invalid bet type"

    def straight_up_type(self, bet_type, player):
        if bet_type == "Straight Up":
            while True:
                chosen_number = input("Enter a number to bet on: ")
                if chosen_number in self.roulette.options:
                    player.chosen_number = chosen_number  # Set the chosen_number attribute of the player
                    return chosen_number
                else:
                    print("Invalid number. Please enter a number between 0 and 36.")

    def split_bet_type(self, bet_type, player):
        if bet_type == "Split Bet":
            while True:
                chosen_numbers = input("Enter two adjacent numbers to bet on, separated by a space: ").split()
                if len(chosen_numbers) != 2:
                    print("Invalid input. Please enter two numbers in the range of 0-36.")
                    continue
                # Convert chosen_numbers to integers
                chosen_numbers = [int(num) for num in chosen_numbers]
                 # Check if the numbers are in the roulette options
                if min(chosen_numbers) < 0 or max(chosen_numbers) > 36:
                    print("Invalid numbers. Please enter numbers between 0 and 36.")
                    continue
                # Check if the difference between the two numbers is 1 (for horizontal adjacency)
                # or 3 (for vertical adjacency in the betting grid)
                if abs(chosen_numbers[0] - chosen_numbers[1]) in [1, 3]:
                    player.chosen_numbers = chosen_numbers
                    return chosen_numbers
                else:
                    print("Invalid numbers. Please enter two adjacent numbers from the roulette options.")

    def street_bet_type(self, bet_type, player):
        if bet_type == "Street Bet":
            while True:
                chose_numbers = input("Enter three numbers in a row (a street), separated by a space: ").split()
                if len(chose_numbers) != 3:
                    print("Invalid input. Please enter three numbers in the range of 0-36.")
                    continue
                # Convert chosen_numbers to integers
                chosen_numbers = [int(num) for num in chosen_numbers]
                 # Check if the numbers are in the roulette options
                if min(chosen_numbers) < 0 or max(chosen_numbers) > 36:
                    print("Invalid numbers. Please enter numbers between 0 and 36.")
                    continue
                # Check if the numbers form a street
                if chosen_numbers[1] - chosen_numbers[0] == 1 and chosen_numbers[2] - chosen_numbers[1] == 1:
                    player.chosen_numbers = chosen_numbers
                    return chosen_numbers
                else:
                    print("Invalid numbers. Please enter three numbers in a row.")

    def corner_bet_type(self, bet_type, player):
        if bet_type == "Corner Bet":
            while True:
                chosen_numbers = input("Enter four numbers forming a square (a corner), separated by a space: ").split()
                if len(chosen_numbers) != 4:
                    print("Invalid input. Please enter four numbers.")
                    continue
                # Convert chosen_numbers to integers
                chosen_numbers = [int(num) for num in chosen_numbers]
                # Check if the numbers are in the roulette options
                if min(chosen_numbers) < 0 or max(chosen_numbers) > 36:
                    print("Invalid numbers. Please enter numbers between 0 and 36.")
                    continue
                # Check if the numbers form a corner
                chosen_numbers.sort()
                if (chosen_numbers[1] - chosen_numbers[0] == 1 and chosen_numbers[2] - chosen_numbers[1] == 2 and
                    chosen_numbers[3] - chosen_numbers[2] == 1):
                    player.chosen_numbers = chosen_numbers
                    return chosen_numbers
                else:
                    print("Invalid numbers. Please enter four numbers forming a square. To get an impression of a square look at a typical roulette grid.")

    def line_bet_type(self, player, bet_type):
        if bet_type == "Line Bet":
            while True:
                chosen_numbers = input("Enter six numbers by placing chips on the edge of two adjacent rows, separated by a space: ").split()
                if len(chosen_numbers) != 6:
                    print("Invalid input. Please enter six numbers.")
                    continue
                # Convert chosen_numbers to integers
                chosen_numbers = [int(num) for num in chosen_numbers]
                # Check if the numbers are in the roulette options
                if min(chosen_numbers) < 0 or max(chosen_numbers) > 36:
                    print("Invalid numbers. Please enter numbers between 0 and 36.")
                    continue
                # Check if the numbers are six in a row
                chosen_numbers.sort()
                if (chosen_numbers[5] - chosen_numbers[4] == 1 and chosen_numbers[4] - chosen_numbers[3] == 1 and chosen_numbers[3] - chosen_numbers[2] == 1 and
                    chosen_numbers[2] - chosen_numbers[1] == 1 and chosen_numbers[1] - chosen_numbers[0]== 1):
                    player.chosen_numbers = chosen_numbers
                    return chosen_numbers
                else:
                    print("Invalid numbers. Please enter six numbers forming a row.")
    
    def dozens_bet_type(self, player, bet_type):
        if bet_type == "Dozens Bet":
            while True:
                chosen_number = input("Enter a number from 1 to 3 representing a group of twelve numbers. 1 for the group 1-12, 2 for the group 13-24, 3 for the group 25-36.")
                if int(chosen_number) != 1 and int(chosen_number) != 2 and int(chosen_number) != 3:
                    print("Invalid input. Please enter the number 1, 2 or 3 representing a group of twelve numbers.(1: 1-12, 2: 13-24, 3: 25-36)")
                    continue
                # Map the chosen number to the corresponding group of twelve numbers
                dozens = {
                    1: list(range(1, 13)),
                    2: list(range(13, 25)),
                    3: list(range(25, 37))
                }
                player.chosen_numbers = dozens[int(chosen_number)]
                return player.chosen_numbers
    
    def column_bet_type(self, player, bet_type):
        if bet_type == "Column Bet":
            while True:
                chosen_number = input("Enter a number from 1 to 3 representing a column of twelve numbers according to the typical roulette grid. 1 for the column 3, 6, 9, 12...; 2 for the column 2, 5, 8, 11...; 3 for the column 1, 4, 7, 10... .")
                if int(chosen_number) != 1 and int(chosen_number) != 2 and int(chosen_number) != 3:
                    print("Invalid input. Please enter the number 1, 2, or 3 representing a column of twelve numbers according to the typical roulette grid. 1 for the column 3, 6, 9, 12...; 2 for the column 2, 5, 8, 11...; 3 for the column 1, 4, 7, 10... .")
                    continue
                # Map the chosen number to the corresponding group of twelve numbers in a single column
                columns = {
                    1: list(range(3, 37, 3)),
                    2: list(range(2, 36, 3)),
                    3: list(range(1, 35, 3))
                }
                player.chosen_numbers = columns[int(chosen_number)]
                return player.chosen_numbers
            
    def even_odd_bet_type(self, player, bet_type):
        if bet_type == "Even/Odd":
            while True:
                chosen_string = input("What is your preferred range of numbers? Type \"even\" to select all even numbers, type \"odd\" to select all odd numbers.")
                if chosen_string.lower() != "even" and chosen_string.lower() != "odd":
                    print("Invalid input. Please enter \"even\" or \"odd\" according to your preferred range of numbers.")
                    continue
                even_odd_dict = {
                    "even": list(range(2, 37,  2)),
                    "odd": list(range(1, 36, 2))
                }
                player.chosen_numbers = even_odd_dict[chosen_string]
                return player.chosen_numbers
    
    def red_black_bet_type(self, player, bet_type):
        if bet_type == "Red/Black":
            while True:
                chosen_string = input("What is your preferred colour to bet on? Type \"red\" to select all red numbers, type \"black\" to select all black numbers.")
                if chosen_string.lower() != "red" and chosen_string.lower() != "black":
                    print("Invalid input. Please enter \"red\" to choose all red numbers, enter \"black\" to choose all black numbers.")
                    continue
                player.chosen_numbers = []  # Initialize as an empty list
                if chosen_string.lower() == "red":
                    for key, value in self.roulette_options.items():
                        if value == "red":
                            player.chosen_numbers.append(key)
                if chosen_string.lower() == "black":
                    for key, value in self.roulette_options.items():
                        if value == "black":
                            player.chosen_numbers.append(key)
                return player.chosen_numbers
    
    def low_high_bet_type(self, player, bet_type):
        if bet_type == "Low/High":
            while True:
                chosen_string = input("What is your preferred range to bet on? Type \"low\" to select all the numbers between 1 and 18, type \"high\" to select all the numbers between 19 and 36.")
                if chosen_string.lower() != "low" and chosen_string.lower() != "high":
                    print("Invalid input. Please enter \"low\" to select all the numbers between 1 and 18 or enter \"high\" to select all the numbers between 19 and 36.")
                    continue
                player.chosen_numbers = [] # Initialize as an empty list
                if chosen_string.lower() == "low":
                    player.chosen_numbers.extend(range(1, 19))
                elif chosen_string.lower() == "high":
                    player.chosen_numbers.extend(range(19, 37))
                return player.chosen_numbers
    
    def payout(self, player, bet_amount, bet_type):
        if bet_type == "Straight":
            payout_ratio = 36
        elif bet_type == "Split":
            payout_ratio = 18
        elif bet_type == "Street":
            payout_ratio = 12
        elif bet_type == "Corner":
            payout_ratio = 9
        elif bet_type == "Six Line":
            payout_ratio = 6
        elif bet_type == "Column":
            payout_ratio = 3
        elif bet_type == "Dozen":
            payout_ratio = 3
        elif bet_type == "Red/Black":
            payout_ratio = 2
        elif bet_type == "Even/Odd":
            payout_ratio = 2
        elif bet_type == "Low/High":
            payout_ratio = 2
        else:
            print("Invalid bet type.")
            return

        if self.winning_number in player.chosen_numbers:
            print(f"{player.name} wins the bet.")
            player.wealth += bet_amount * payout_ratio
        else:
            print(f"{player.name} loses the bet.")
            player.wealth -= bet_amount
    
    def play(self, player):
        bet_amount = player.bet()
        bet_type = self.choose_bet_type()
        self.spin_wheel()

        # Print the winning number with a frame around it
        print(f"╔══════╗")
        print(f"║  {self.winning_number:02d} ║")
        print(f"╚══════╝")

        self.payout(player, bet_amount, bet_type)



class SlotMachine:

    def __init__(self):

        self.slot_grid = [
            [],
            [],
            []
        ]

    def __repr__(self):
        return "Welcome to the Slot Machine!"
    
    def pulling_the_lever(self):
        for i in range(3):
            self.slot_grid[i] = [random.randint(0, 9) for _ in range(3)]
        return self.slot_grid

    def ask_bet_amount(self, player):
        while True:
            print(f"You can bet up to {player.balance}")
            bet_amount = input("Enter your bet amount: ")
            if bet_amount.isdigit() and 0 < int(bet_amount) <= player.balance:
                return int(bet_amount)
            else:
                print("Invalid input. Please enter a positive number up to your current balance.")

    def display_slot_grid(self):
        for row in self.slot_grid:
            print("+---+---+---+")
            print("|", end="")
            for num in row:
                print(f" {num} |", end="")
            print()
        print("+---+---+---+")

    def pulling_the_lever(self, player, bet_amount):
        for i in range(3):
            self.slot_grid[i] = [random.randint(0, 9) for _ in range(3)]
        self.display_slot_grid()
        if self.payout(player, bet_amount):
            print("Congratulations, you won!")
        return self.slot_grid
    
    def payout(self, player, bet_amount):
        # Check for horizontal wins
        for row in self.slot_grid:
            if len(set(row)) == 1:
                player.balance += bet_amount * 10
                return True

        # Check for diagonal wins
        if self.slot_grid[0][0] == self.slot_grid[1][1] == self.slot_grid[2][2] or \
           self.slot_grid[0][2] == self.slot_grid[1][1] == self.slot_grid[2][0]:
            player.balance += bet_amount * 10
            return True

        return False
    
    def game_loop(self, player):
        bet_amount = self.ask_bet_amount(player)
        while True:
            self.pulling_the_lever(player, bet_amount)
            print("1. Spin again")
            print("2. Change bet amount")
            command = input("Enter a command by typing \"1\" or \"2\": ")
            if command == "2":
                bet_amount = self.ask_bet_amount(player)
            elif command == "1":
                continue


