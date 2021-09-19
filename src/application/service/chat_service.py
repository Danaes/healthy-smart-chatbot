from . import constants, validator
from ...domain.chatbot.speech import Speech
from ...domain.entity.messageRS import MessageType, MessageRS


class ChatService:

    def __init__(self):
        self.speech = Speech()

    def out_coming_message(self, msg, key, username):
        user_input = msg.message.text

        if validator.is_emoji_or_is_not_valid_command(user_input):
            return MessageRS([constants.ERROR_MSG], MessageType.TEXT)

        return self.speech.out_coming_message(user_input, key, username)
