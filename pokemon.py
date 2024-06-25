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

def stats(pokemon):
    return f"Nom : {pokemon['name'].capitalize()}\nHP : {pokemon['stats'][0]['base_stat']}\n"

#---------------------- Main ------------------------------
print(encadrer("Bienvenue Dans Le Jeu De Combat De Pokemon"))

joueur1 = input("Quel est votre nom ? ")
joueur2 = input("Quel est le nom de votre adversaire ? ")

print("Le jeu commence\n")

        # Choix du Pokémon pour le joueur 1
while True:
    choix = input(f"{joueur1}, choisissez votre Pokémon : ").lower()
    pokemonJoueur1 = infoPokemon(choix)
    if pokemonJoueur1:
        print(f"{joueur1} a choisi {choix.capitalize()} !\n")
        print(encadrer(stats(pokemonJoueur1)))
        break
    else:
        print(f"{joueur1}, votre Pokémon n'existe pas !")
        print("Ressayez à nouveau.\n")

        # Choix du Pokémon pour le joueur 2
while True:
    choix = input(f"{joueur2}, choisissez votre Pokémon : ").lower()
    pokemonJoueur2 = infoPokemon(choix)
    if pokemonJoueur2:
        print(f"{joueur2} a choisi {choix.capitalize()} !\n")
        break
    else:
        print(f"{joueur2}, votre Pokémon n'existe pas !")
        print("Ressayez à nouveau.\n")

