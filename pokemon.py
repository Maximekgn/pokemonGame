import requests

#---------------------- Functions --------------------------
def encadrer(texte):
    lignes = texte.split('\n')
    max_len = max(len(ligne) for ligne in lignes)
    bordure = '+' + '-' * (max_len + 2) + '+'
    encadrement = [bordure]
    for ligne in lignes:
        encadrement.append('| ' + ligne.ljust(max_len) + ' |')
    encadrement.append(bordure)
    return '\n'.join(encadrement)

def infoPokemon(nom):
    url = f"https://pokeapi.co/api/v2/pokemon/{nom.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.RequestException:
        return None

def degat(move):
    url = f"https://pokeapi.co/api/v2/move/{move.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['power']
    except requests.exceptions.HTTPError:
        return None

def afficherPokemon(pokemon):
    print(encadrer(f"{pokemon.nom.capitalize()}"))
    print(f"Vie : {pokemon.vie}")
    print("Attaques :")
    for attaque in pokemon.attaques:
        print(f"    {attaque} - Dégât : {degat(attaque)}")


#---------------------- Classes --------------------------
class Pokemon:
    def __init__(self, nom, vie, attaques):
        self.nom = nom
        self.vie = vie
        self.attaques = attaques


#---------------------- Main ------------------------------
print(encadrer("Bienvenue Dans Le Jeu De Combat De Pokemon"))

joueur1 = input("Quel est votre nom ? ")
joueur2 = input("Quel est le nom de votre adversaire ? ")

print("Le jeu commence\n")

        # Choix du Pokémon pour le joueur 1
while True:
    choix = input(f"{joueur1}, choisissez votre Pokémon : ").lower()
    pokemon_json = infoPokemon(choix)
    if pokemon_json:
        pokemonJoueur1 = Pokemon(choix, pokemon_json['stats'][0]['base_stat'] * 10,
                                 [move['move']['name'] for move in pokemon_json['moves'][:6]])
        afficherPokemon(pokemonJoueur1)
        break
    else:
        print(f"{joueur1}, votre Pokémon n'existe pas !")
        print("Ressayez à nouveau.\n")

        # Choix du Pokémon pour le joueur 2

while True:
    choix = input(f"{joueur2}, choisissez votre Pokémon : ").lower()
    pokemon_json = infoPokemon(choix)
    if pokemon_json:
        pokemonJoueur2 = Pokemon(choix, pokemon_json['stats'][0]['base_stat'] * 10,
                                 [move['move']['name'] for move in pokemon_json['moves'][:6]])
        afficherPokemon(pokemonJoueur2)
        break
    else:
        print(f"{joueur2}, votre Pokémon n'existe pas !")
        print("Ressayez à nouveau.\n")


        # Début du jeu

gagnant = ""
while pokemonJoueur1.vie > 0 and pokemonJoueur2.vie > 0:
    attaque = pokemonJoueur1.attaques[int(input(f"{joueur1}, choisissez votre attaque : ")) - 1]
    pokemonJoueur2.vie -= degat(attaque)
    print(f"{joueur2} a perdu {degat(attaque)} points de vie")
    print(f"{joueur2} a {pokemonJoueur2.vie} points de vie restants")

    if pokemonJoueur2.vie <= 0:
        gagnant = joueur1
        break

    attaque = pokemonJoueur2.attaques[int(input(f"{joueur2}, choisissez votre attaque : ")) - 1]
    pokemonJoueur1.vie -= degat(attaque)
    print(f"{joueur1} a perdu {degat(attaque)} points de vie")
    print(f"{joueur1} a {pokemonJoueur1.vie} points de vie restants")

    if pokemonJoueur1.vie <= 0:
        gagnant = joueur2
        break

print(f"Le gagnant est {gagnant} !")



