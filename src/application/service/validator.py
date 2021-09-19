import emoji
import re

PATTERN = '[/]'  # '[/!]' añadir todos los simbolos no soportados
VALID_COMMANDS = ['comenzar', 'dieta', 'ayuda']


def is_emoji(user_input):
    return emoji.get_emoji_regexp().search(user_input)


def is_not_valid_command(user_input):
    first_character = user_input[0]
    if bool(re.search(PATTERN, first_character)):
        command = user_input[1:]
        return command not in VALID_COMMANDS

    return False


def is_emoji_or_is_not_valid_command(user_input):
    return is_emoji(user_input) or is_not_valid_command(user_input)
