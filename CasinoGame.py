#FirstLine
import random

class Games:
    
    def __init__(self, name, entry_fee):
        self.name = name
        self.entry_fee = entry_fee
        self.games = {}
    
    def __repr__(self):
        return "There are currently {games} different games to choose from.".format(games = len(self.games))
    
    def add_game(self, game_name, game_class):
        self.games[game_name] = game_class

    def get_available_games(self):
        return list(self.games.keys())
    
    def play_game(self, game_name, player):
        if game_name in self.games:
            game = self.games[game_name]
            game.play(player)
        else:
            print("Sorry, that game is not available.")


class Player:
    
    def __init__(self, name, wealth, risk_aversity, is_broke = False):
        self.name = name
        self.wealth = wealth
        self.risk_aversity = risk_aversity
        self.is_broke = is_broke
        self.hand = []
    
    def __repr__(self):
        status_broke = ""
        if self.is_broke:
            status_broke = "is broke."
        else:
            status_broke = "is not broke."
        return "Player {name} has {wealth} in his pocket remaining and {status} His risk aversity is: {risk_aversity}.".format(name=self.name, wealth=self.wealth, status=status_broke, risk_aversity=self.risk_aversity)
    
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
    
    def deal_card(self, player):
        card = self.deck.pop()
        player.add_card(card)
        print(f"{player.name} drew a {card}")

    def player_choice(self, player):
        choice = input(f"{player.name}, do you want to draw another card? (yes/no) ")
        return choice.lower() == "yes"
       
    def play(self, player, bank):
        bet_amount = player.bet()
        while self.player_choice(player) and player.calculate_hand() < 21:
            self.deal_card(player)
            print(f"{player.name}'s hand: {player.hand}, total: {player.calculate_hand()}")

        while bank.calculate_hand() < 17:
            self.deal_card(bank)
            print(f"Bank's hand: {bank.hand}, total: {bank.calculate_hand()}")

        self.payout(player, bank, bet_amount)
        self.reset(player, bank)

    def reset(self, player, bank):
        player.hand = []
        bank.hand = []
        self.deck = [i for i in range(1, 12)] * 4
        random.shuffle(self.deck)

    
    print("testtesttest")
    print("testestesttest")


    print("another text right there")

    