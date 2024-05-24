from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.message_handlers import get_answer
from config.openai_client import client, generate_response, generate_transcription
from io import BytesIO

async def audio_reply(update: Update, context):
    if update.message.voice is None:
        return
    mes = await update.message.reply_text("Ваш аудиозапрос обрабатывается, пожалуйста, подождите...")
    # входящее аудио сообщение
    audio_file = await context.bot.get_file(update.message.voice.file_id)

    # конвертация аудио в формат .ogg
    audio_bytes = BytesIO(await audio_file.download_as_bytearray())
    
    # запрос транскрипции аудио
    transcription = generate_transcription(audio_bytes)
    
    # openai ответ
    reply = get_answer(transcription)
    
    # перенаправление ответа в Telegram
    if "<pre" in reply or "<code>" in reply:
        keyboard = [[InlineKeyboardButton("Нажми меня", callback_data='press')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await mes.edit_text(reply.strip(),parse_mode="HTML",reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton("Нажми меня", callback_data='press')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await mes.edit_text(reply.strip(),parse_mode="Markdown",reply_markup=reply_markup)    
        except:
            await mes.edit_text(reply.strip(),reply_markup=reply_markup)
    
    print("user:", audio_file.file_path)
    print("transcription:", transcription)
    print("assistant:", reply)