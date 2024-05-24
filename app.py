from telegram.ext import MessageHandler, CommandHandler,CallbackQueryHandler,filters
from config.telegram_bot import application 
from handlers.message_handlers import chatgpt_reply,other_reply,code_button
from handlers.command_handlers import start_reply,setlang_reply,language_choice,tech_reply
from handlers.audio_handlers import audio_reply

# Регистрация обработчика текстовых сообщений
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply)
application.add_handler(message_handler)

# Регистрация обработчика аудио сообщений
audio_handler = MessageHandler(filters.VOICE, audio_reply)
application.add_handler(audio_handler)

other_content_handler = MessageHandler(~filters.TEXT, other_reply)
application.add_handler(other_content_handler)

# Регистрация обработчика команд
start_command_handler = CommandHandler("start", start_reply)
application.add_handler(start_command_handler)

tech_command_handler = CommandHandler("tech", tech_reply)
application.add_handler(tech_command_handler)

setlang_command_handler = CommandHandler("setlang", setlang_reply)
application.add_handler(setlang_command_handler)

application.add_handler(CallbackQueryHandler(code_button,pattern='press'))
application.add_handler(CallbackQueryHandler(language_choice))

# Запуск бота
application.run_polling()