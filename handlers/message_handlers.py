from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InputMediaVideo
from config.openai_client import client
import re

context_data = []
len_context = 3
#может стоит обнулять контекст, если меняется тематика?

def get_answer(text, context="",t=0.5):
    system_prompts = [
        "You are a very useful assistant for Data Scientist.",
        "Ты очень педантично используешь термины и с досточно большой специфичностью выбираешь и используешь их. Расписываешь всё структурировано и по пунктам.\
                      тебе могут задавать некорректные вопросы, связанные с несуществующими определениями, нужно их отклонять и предложить альтернативные темы. Желательно предоставлять примеры, где это возможно",
        "Для всех методов крайне рекомендуется упоминать подводные камни по их использованию. А также необходимо писать и плюсы и минусы заданного подхода.",
        "Если у данного метода есть альтернативы, нужно выписать их по пунктам и предоставить сравнение с ними. Рекомендуется взять 3 альтернативы, если они имеются.\
        Крайне рекомендуется дополнительно описать специфичные альтернативы и в каких случаях можно их использовать.\
        Все сравнения описывать по пунктам.\
        Описать в чем превосходство текущего метода и в чем его недостатки в сравнении с другими методами.",
        "When you provide code, you must use this format: <pre language=\"lang\">code</pre>, where code is the code itself and lang is a programming language name.\
          Use the <code>variable</code> construction if you need to use some variable from the code in general text or replace `variable` construction with <code>variable</code>."
    ]
    system_messages = [{"role":"system", "content": prompt} for prompt in system_prompts]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = system_messages +
            [{"role": "user", "content": context}, ### объединить, если нет контекста
            {"role": "user", "content": text}],
        max_tokens=1024,
        temperature=t,
    )
    print(response.choices[0].message.content.strip())
    print('-'*10)
    return response.choices[0].message.content.strip()


async def chatgpt_reply(update: Update, context):
    global context_data
    # текст входящего сообщения
    text = update.message.text
    text_with_context = ' '.join(i for i in context_data if context_data) + text
    #print(text_with_context)
    #print('-------------')
    # перенаправление ответа в Telegram
    mes = await update.message.reply_text("Ваш запрос обрабатывается, пожалуйста, подождите...")
    # запрос
    #response = client.chat.completions.create(
    #    model="gpt-3.5-turbo",
    #    messages=[{"role": "user", "content": f"У тебя есть следующий набор тем: Data Collection,  Feature Engineering, Model Research, Deploy model, others.\
    #    Приходит запрос от пользователя: \"{text_with_context}\".К какой категории ты отнесешь этот запрос? Назови только категорию"}],
    #    max_tokens=1024,
    #    temperature=0.1,
    #)
    
    #theme = response.choices[0].message.content.strip()
    #prompts = {'data collection':'Don\'t forget to reference the internal datacatalog service.',\
    #'feature engineering':'Don\'t forget to tell what attributes there are (categorical, binary, numeric), what you can do with them, in what situations you can use them.',\
    #'model research':'Don\'t forget to talk about the following techniques: data visualization, validation, hyperparameter optimization, feature selection, ensemble collection.',\
    #'deploy model':'Don\'t forget to talk about the design as a service (streamlit),using docker, instructions',\
    #'others':'Add a sentence at the end saying that you\'re not sure the query was related to Data Science and if you\'re not satisfied with the answer, it might be worth rephrasing the question.'}
    reply =  get_answer(text, context=text_with_context, t=0.2)
    
    if len_context==0:
        context_data=[]
    elif len(context_data)>=len_context:
        context_data.pop(0)
        context_data.append(text+' - '+reply)
    else:
        context_data.append(text+' - '+reply)
    # ответ
    #reply = response.choices[0].message.content.strip()

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
    #print("user:", text)
    #print("assistant:", reply)

async def code_button(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Здесь мог бы быть пример кода в контексте вопроса")
    #await query.edit_message_reply_markup(reply_markup=None)
    #print(f'The query is {query.data}')
    #if query.data=='press':
    #    await update.effective_chat.send_message("Вы нажали на кнопку!")

async def other_reply(update: Update, context):
    video = InputMediaVideo(open('/root/bot/team02_bot/content/Huh Cat Meme Template.mp4', 'rb'), caption='Вы расстроили котика... Пришлите текст или голосовое, пожалуйста')
    await update.message.reply_media_group([video])
    #await update.message.reply_text("Вы прислали не текст. Пожалуйста, пришлите текстовый запрос")