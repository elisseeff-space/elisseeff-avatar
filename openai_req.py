#import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json, string
from sqlite_db import elisseeff_avatar_log_insert, sql_start
from create_bot import bot, my_status
from detect_intent_texts import detect_intent_texts

file = open('/home/pavel/cfg/config.json', 'r')
config = json.load(file)

#openai.api_key = config['openai']

# storage = MemoryStorage()

def update(chat_id, group_messages, role, content, count_messages) -> bool:
    
    messages_int=[
    #{"role": "system", "content": "Technology, Medicine and Science consultant"},
    {"role": "system", "content": "Ты консультант по разным жизненным ситуациям. Тебя зовут Элис."},
    {"role": "user", "content": "Мы хотим узнать много нового и интересного."},
    {"role": "assistant", "content": "День добрый! Что бы вы хотели узнать?"}]

    # Check if the chat ID is already in the dictionary
    if chat_id not in group_messages:
        group_messages[chat_id] = messages_int
    else:
        group_messages[chat_id].append({"role": role, "content": content})

    if chat_id not in count_messages:
        count_messages[chat_id] = 0
    else: 
        count_messages[chat_id] += 1

    if(len(group_messages[chat_id])) > 11:
        group_messages[chat_id].pop(3)
    
    #elis_openai_log_insert(my_status.dbase, message.date, str(message.from_user.id), str(message.from_user.username), 'chat_user', str(message.text))

    return True

"""
def call_openai(chat_id) :
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = my_status.group_messages[chat_id]
        )
    return response
"""

async def send(message : types.Message):
    
    with open('/home/pavel/cfg/words.json', 'r', encoding='utf-8') as ffile:
        data = json.load(ffile)

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(i['word'] for i in data)) != set():
        await message.reply('Маты запрещены!')
        await message.delete()
    else :
        # Get the chat ID and user ID
        chat_id = str(message.chat.id)
        #chat_id = message.chat.id
        bot_info = await message.bot.get_me()
        
#        if f'@{bot_info.username}' in message.text:
        #await bot.send_chat_action(message.chat.id, 'typing')
        update(chat_id, my_status.group_messages, "user", message.text, my_status.count_messages)
        elisseeff_avatar_log_insert(message.date, str(message.from_user.id), 
                    str(message.from_user.username), chat_id, 'user', str(message.text), 'query', 0, 0, 0)
        
        response = detect_intent_texts(my_status.project_id, message.text, 'en-US')
        res_txt = response.query_result.fulfillment_text
        update(chat_id, my_status.group_messages, "assistant", response.query_result.fulfillment_text, my_status.count_messages)
        elisseeff_avatar_log_insert(message.date, str(message.from_user.id), 
                    str(message.from_user.username), chat_id, 'assistant', res_txt, 
                    response.query_result.intent.display_name, response.query_result.intent_detection_confidence, 0, 0)
        await message.answer(res_txt)

if __name__ == '__main__':
    print('Hello!')
    #dbase = sql_start(logger)
    #cur = dbase.cursor()

