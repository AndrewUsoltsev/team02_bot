import json

from telegram import Update,KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # перенаправление ответа в Telegram
    await update.message.reply_text(f"Приветствую,{' '.join([update['message']['chat']['last_name'],update['message']['chat']['first_name']])}!")
    await update.message.reply_text(f"Я помогу тебе с различными вопросами, связанными с Data Science! Задай свой вопрос в текстовом или голосовом сообщении.")
    await update.message.reply_text(f"И не вздумай прислать что-то в другом формате (actually попробуй хотя бы разок).")

async def tech_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # объект обновления
    update_obj = json.dumps(update.to_dict(), indent=4)

    # ответ
    reply = "*update object*\n\n" + "```json\n" + update_obj + "\n```"

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply, parse_mode="Markdown")

    print("assistant:", reply)


async def setlang_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data='English')],
        [InlineKeyboardButton("Русский", callback_data='Русский')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите язык / Choose language:', reply_markup=reply_markup)
    
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()# впилить глобальную переменную для влияния на промпты?
    print(f'The query is {query.data} in lang func')
    if query.data=='English':
        await query.edit_message_text(text=f"The chosen language is: {query.data}")
    elif query.data=='Русский':
        await query.edit_message_text(text=f"Выбранный язык: {query.data}")