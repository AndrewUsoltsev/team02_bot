from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config.openai_client import client
import re

context_data = []
len_context = 0
#может стоит обнулять контекст, если меняется тематика?

async def chatgpt_reply(update: Update, context):
    global context_data
    # текст входящего сообщения
    text = update.message.text
    text_with_context = ' '.join(i for i in context_data if context_data) + text
    #print(text_with_context)
    #print('-------------')
    # перенаправление ответа в Telegram
    mes = await update.message.reply_text("Ваш запрос обрабатывается, подождите...")
    # запрос
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"У тебя есть следующий набор тем: Data Collection,  Feature Engineering, Model Research, Deploy model, others.\
        Приходит запрос от пользователя: \"{text_with_context}\".К какой категории ты отнесешь этот запрос? Назови только категорию"}],
        max_tokens=1024,
        temperature=0.1,
    )
    
    theme = response.choices[0].message.content.strip()
    prompts = {'data collection':'Don\'t forget to reference the internal datacatalog service.',\
    'feature engineering':'Don\'t forget to tell what attributes there are (categorical, binary, numeric), what you can do with them, in what situations you can use them.',\
    'model research':'Don\'t forget to talk about the following techniques: data visualization, validation, hyperparameter optimization, feature selection, ensemble collection.',\
    'deploy model':'Don\'t forget to talk about the design as a service (streamlit),using docker, instructions',\
    'others':'Add a sentence at the end saying that you\'re not sure the query was related to Data Science and if you\'re not satisfied with the answer, it might be worth rephrasing the question.'}
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"You are a Data Scientist. Think step by step before answering. You need to tell about \"{text_with_context}\" in terms of {theme},\
         other topics are insufficient for this question. Please, provide an answer with sources and code, if possible,in Russian."+prompts[' '.join(re.findall(r'\b[A-Za-z]+',theme,re.DOTALL)).lower()]
         +"When you provide code, you must use this format: <pre language=\"lang\">code</pre>, where code is the code itself and lang is a programming language name.\
          Use the <code>variable</code> construction if you need to use some variable from the code in general text or replace `variable` construction with <code>variable</code>."}],#{lang}."}], - сделать перехват переменной из функции
        max_tokens=1024,
        temperature=0.1,
    )
    print(f"You are a Data Scientist. Think step by step before answering. You need to tell about \"{text_with_context}\" in terms of {theme},\
         other topics are insufficient for this question. Please, provide an answer with sources and code, if possible,in Russian."+prompts[' '.join(re.findall(r'\b[A-Za-z]+',theme,re.DOTALL)).lower()]
         +"When you provide code, you must use this format: <pre language=\"lang\">code</pre>, where code is the code itself and lang is a programming language name.\
          Use the <code>variable</code> construction if you need to use some variable from the code in general text or replace `variable` construction with <code>variable</code>.")
    if len_context==0:
        context_data=[]
    elif len(context_data)>=len_context:
        context_data.pop(0)
        context_data.append(text)
    else:
        context_data.append(text)
    # ответ
    reply = response.choices[0].message.content.strip()

    if "<pre" in reply or "<code>" in reply:
        keyboard = [[InlineKeyboardButton("Нажми меня", callback_data='press')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await mes.edit_text(reply.strip(),parse_mode="HTML",reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton("Нажми меня", callback_data='press')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await mes.edit_text(reply.strip(),reply_markup=reply_markup)    
    
    #print("user:", text)
    #print("assistant:", reply)

async def code_button(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Здесь будет ответ по кнопке")
    #await query.edit_message_reply_markup(reply_markup=None)
    #print(f'The query is {query.data}')
    #if query.data=='press':
    #    await update.effective_chat.send_message("Вы нажали на кнопку!")

async def other_reply(update: Update, context):
    await update.message.reply_text("Вы прислали не текст. Пожалуйста, пришлите текстовый запрос")