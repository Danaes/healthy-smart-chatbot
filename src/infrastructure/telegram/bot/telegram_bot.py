import logging
from time import sleep

from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.application.service.chat_service import ChatService
from . import credentials


class TelegramBot:
    RESTART_MSG = "Para volver a comenzar es necesario que escribas /comenzar"
    ERROR_MSG = "No tengo registrado el comando que has introducido. Por favor, prueba con /comenzar o /ayuda"
    ERROR_NOT_DIET = "No tengo datos tuyos aún. " + RESTART_MSG

    chat_service = None

    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def start(self, update, context):
        self.chat_service = ChatService()
        self.__reply_message(update, context, 'start', update.message.chat.username)

    def diet(self, update, context):
        if self.chat_service is None:
            self.__reply_error(update, context, self.ERROR_NOT_DIET)
        else:
            self.__reply_message(update, context, 'diet', update.message.chat.username)

    def help(self, update, context):
        self.chat_service = ChatService()
        self.__reply_message(update, context, 'help', update.message.chat.username)

    def reply(self, update, context):
        self.__reply_message(update, context, 'reply', update.message.chat.username)

    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)
        self.__reply_error(update, context, self.ERROR_MSG)

    def __reply_message(self, update, context, key, username):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        msg = self.chat_service.out_coming_message(update, key, username)
        if msg is None:
            msg = self.RESTART_MSG

        if msg.type.name == 'TEXT':
            for idx, question in enumerate(msg.text):
                sleep(3 * (1 - 1 / len(question)))
                context.bot.sendMessage(chat_id=update.message.chat_id, text=question)
                if idx < len(msg) - 1:
                    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)

        elif msg.type.name == 'FILE':
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
            sleep(3 * (1 - 1 / len(msg.text[0])))
            with open(msg.text[0], 'rb') as file:
                context.bot.sendDocument(chat_id=update.message.chat_id, caption='Disfruta de la dieta',
                                         document=file)

    def __reply_error(self, update, context, text):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        sleep(3 * (1 - 1 / len(text)))
        context.bot.sendMessage(chat_id=update.message.chat_id, text=text)

    def main(self):
        updater = Updater(credentials.TOKEN, use_context=True)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("comenzar", self.start))
        dp.add_handler(CommandHandler("dieta", self.diet))
        dp.add_handler(CommandHandler("ayuda", self.help))

        dp.add_handler(MessageHandler(Filters.text, self.reply))
        dp.add_handler(MessageHandler(Filters.document, self.diet))

        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()
        updater.idle()
