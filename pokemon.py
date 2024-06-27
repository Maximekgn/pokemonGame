import requests
import os

#---------------------- Functions --------------------------

def enclose(text):
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    border = '+' + '-' * (max_len + 2) + '+'
    enclosure = [border]
    for line in lines:
        enclosure.append('| ' + line.ljust(max_len) + ' |')
    enclosure.append(border)
    return '\n'.join(enclosure)

def clear():
    # Détecte le système d'exploitation
    if os.name == 'nt':  # Pour Windows
        os.system('cls')
    else:  # Pour Mac et Linux (os.name est 'posix')
        os.system('clear')
    print(enclose("Pokemon Game"))

def getData(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return 0

def getMovePower(move_url):
    try:
        response = requests.get(move_url)
        response.raise_for_status()
        move_data = response.json()
        power = move_data.get('power', None)
        return power
    except requests.exceptions.RequestException as e:
        return None

#---------------------- Classes --------------------------

class Pokemon:
    def __init__(self, name):
        data = getData(name)
        self.name = name
        self.hp = data['stats'][0]['base_stat'] * 10
        self.attacks = {}
        for move in data['moves'][:5]:
            power = getMovePower(move['move']['url'])
            if power is not None:
                self.attacks[move['move']['name']] = power

    def display(self):
        print(enclose(f"Pokemon: {self.name}\nHP: {self.hp}\nAttacks: {self.attacks}"))

    def attack(self, other, move):
        if move in self.attacks:
            other.hp -= self.attacks[move]
            return self.attacks[move]
        return 0

#---------------------- Main ------------------------------

print(enclose("Welcome to the Pokemon Fighting Game"))

player1 = input("What is your name? ")
player2 = input("What is your opponent's name? ")
clear()
print("The game starts\n")

            # Choice of the Pokemon for player 1
while True:
    pokemonPlayer1 = input(f"{player1}, choose your Pokemon: ").lower()
    if getData(pokemonPlayer1):
        pokemonPlayer1 = Pokemon(pokemonPlayer1)
        pokemonPlayer1.display()
        break
    else:
        print("That Pokemon does not exist, please try again")

            # Choice of the Pokemon for player 2
while True:
    pokemonPlayer2 = input(f"{player2}, choose your Pokemon: ").lower()
    if getData(pokemonPlayer2):
        pokemonPlayer2 = Pokemon(pokemonPlayer2)
        pokemonPlayer2.display()
        break
    else:
        print("That Pokemon does not exist, please try again")

clear()
            # Start of the game
winner = ""

while pokemonPlayer1.hp > 0 and pokemonPlayer2.hp > 0:
    print(f"{player1.upper()} ATTACKS {player2.upper()}")
    print(f"{pokemonPlayer1.display()} vs {pokemonPlayer2.display()}")
    move = list(pokemonPlayer1.attacks)[int(input(f"{player1}, choose your move (1-5): ")) - 1]
    damage = pokemonPlayer1.attack(pokemonPlayer2, move)
    clear()
    print(f"{player1} inflicts {damage} damage to {player2}'s Pokemon")
    if pokemonPlayer2.hp <= 0:
        winner = player1
        break

    print(f"{player2.upper()} ATTACKS {player1.upper()}")
    print(f"{pokemonPlayer2.display()} vs {pokemonPlayer1.display()}")
    move = list(pokemonPlayer2.attacks)[int(input(f"{player2}, choose your move (1-5): ")) - 1]
    damage = pokemonPlayer2.attack(pokemonPlayer1, move)
    clear()
    print(f"{player2} inflicts {damage} damage to {player1}'s Pokemon")
    if pokemonPlayer1.hp <= 0:
        winner = player2
        break
  
print(f"The winner is {winner}!")
