import random


def random_string():
    random_list = [
        "Veuillez essayer d'écrire quelque chose de plus descriptif.",
        "Oh ! Il semble que vous ayez écrit quelque chose que je ne comprends pas encore.",
        "Est-ce que ça vous dérange d'essayer de reformuler votre demande ?",
        "Je suis désolé, je n'ai pas bien compris.",
        "Je ne peux pas répondre à cela pour le moment, veuillez essayer de poser une autre question."
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]