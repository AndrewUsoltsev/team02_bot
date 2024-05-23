from telegram import Update
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
    # перенаправление ответа в Telegram
    mes = await update.message.reply_text("Ваш запрос обрабатывается, подождите...")
    # запрос
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"У тебя есть следующий набор тем: Data Collection,  Feature Engineering, Model Research, Deploy model, others.\
        Приходит запрос от пользователя: \"{text_with_context}\".К какой категории ты отнесешь этот запрос? Назови только категорию"}],
        max_tokens=1024,
        temperature=0.25,
    )
    
    theme = response.choices[0].message.content.strip()
    prompts = {'data collection':'Don\'t forget to reference the internal datacatalog service.',\
    'feature engineering':'Don\'t forget to tell what attributes there are (categorical, binary, numeric), what you can do with them, in what situations you can use them.',\
    'model research':'Don\'t forget to talk about the following techniques: data visualization, validation, hyperparameter optimization, feature selection, ensemble collection.',\
    'deploy model':'Don\'t forget to talk about the design as a service (streamlit),using docker, instructions',\
    'others':'Add a sentence at the end saying that you\'re not sure the query was related to Data Science and if you\'re not satisfied with the answer, it might be worth rephrasing the question.'}
    print(prompts[' '.join(re.findall(r'\b[A-Za-z]+',theme,re.DOTALL)).lower()])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"You are a Data Scientist. You need to tell about \"{text_with_context}\" in terms of {theme},\
         other topics are insufficient for this question. Please, provide an answer with sources and code, if possible,in Russian."+prompts[' '.join(re.findall(r'\b[A-Za-z]+',theme,re.DOTALL)).lower()]}],#{lang}."}], - сделать перехват переменной из функции
        max_tokens=1024,
        temperature=0.2,
    )

    if len_context==0:
        context_data=[]
    elif len(context_data)>=len_context:
        context_data.pop(0)
        context_data.append(text)
    else:
        context_data.append(text)
    # ответ
    reply = response.choices[0].message.content.strip()
    if "```" in reply:
        await mes.edit_text(reply.strip(),parse_mode="Markdown")
    else:
        await mes.edit_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)

async def other_reply(update: Update, context):
    await update.message.reply_text("Вы прислали не текст. Пожалуйста, пришлите текстовый запрос")