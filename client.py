#from sqlite_db import use_log_add_command
import logging
from pathlib import Path
from aiogram import Dispatcher, types
from aiogram.types import ContentType, File, Message, ReplyKeyboardRemove
from create_bot import bot, my_status
from client_kb import kb_client
#from recognize_yandex_stt import transcribe_file
from datetime import datetime
from openai_req import send, update#, call_openai
from sqlite_db import get_help_text #elis_openai_log_insert

async def command_start(message : types.Message):

    text_for_out = get_help_text()
    try:
        await bot.send_message(message.chat.id, text_for_out, reply_markup=kb_client)
        #await message.delete()
    except:
        await message.answer('Something wrong with me... \nhttps://t.me/Elis_OpenAI_bot', reply_markup=kb_client)

"""
async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


async def voice_message_handler(message: Message): # types.Message):
    # Set prefix for send correct query to OpenAI
    my_status.set_open_ai_prefix(str(message.chat.id),'~~~')
    # Get the file ID of the voice message
    voice = await message.voice.get_file()
    path = "/home/pavel/github/elis_openai_plus/voices"

    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    
    file_name = path + f"/{voice.file_id}.ogg"
    start_time = datetime.now()
    str_buf = f"Recognition starts at: {start_time.strftime('%H:%M:%S')}."
    await message.answer(str_buf)
    await bot.send_chat_action(message.chat.id, 'typing')
    alternative = transcribe_file(file_name)
    end_time = datetime.now()
    runtime = end_time - start_time
    str_buf = f"Recognition ready in: {runtime.seconds} seconds. Elis starts some corrections."
    start_time = end_time
    await message.answer(str_buf)

    chat_id = str(message.chat.id)
    #chat_id = message.chat.id
    str_buf = str(my_status.get_open_ai_prefix(chat_id)) + str(alternative.text)
    update(chat_id, my_status.group_messages, "user", str_buf, my_status.count_messages)
    elis_openai_log_insert(message.date, str(message.from_user.id), 
                        str(message.from_user.username), chat_id, 'user', str_buf, 0, 0, 0)
    await bot.send_chat_action(message.chat.id, 'typing')
    chat_response = call_openai(chat_id)
    update(chat_id, my_status.group_messages, "assistant", chat_response['choices'][0]['message']['content'], my_status.count_messages)
    elis_openai_log_insert(message.date, str(message.from_user.id), 
                        str(message.from_user.username), chat_id, 'assistant', chat_response['choices'][0]['message']['content'], 
                        int(chat_response['usage']['prompt_tokens']), int(chat_response['usage']['completion_tokens']), int(chat_response['usage']['total_tokens']))
    end_time = datetime.now()
    runtime = end_time - start_time
    str_buf = f"Elis ready in: {runtime.seconds} seconds."
    await message.answer(str_buf)

    use_log_add_command(message.from_user.username, message.from_user.id, alternative.text, len(alternative.words), my_status.get_open_ai_prefix(chat_id), float(alternative.confidence))
    await message.answer(chat_response['choices'][0]['message']['content'])

async def affect_command(message : types.Message):
    my_status.set_open_ai_prefix(str(message.chat.id),'Исправь текст в ласковом тоне:')
    #await bot.send_message(message.from_user.id, 'English Language of Voice Messages.')
    await message.answer('Коррекция текста в ласковом тоне, чтобы было приятно читать.')

async def medical_command(message : types.Message):
    my_status.set_open_ai_prefix(str(message.chat.id),'Исправь текст строго в медицинской терминологии:')
    #await bot.send_message(message.from_user.id, 'France Language of Voice Messages.')
    await message.answer('Коррекция текста по медицинской терминологии.')

async def dialog_command(message : types.Message):
    my_status.set_open_ai_prefix(str(message.chat.id),'')
    #await bot.send_message(message.from_user.id, 'France Language of Voice Messages.')
    await message.answer('Прямой диалог c ChatGPT.')
"""
async def correction_command(message : types.Message):
    my_status.set_open_ai_prefix(str(message.chat.id),'Исправь текст:')
    #await bot.send_message(message.from_user.id, 'Russian Language of Voice Messages.')
    await message.answer('Коррекция текста. Исправление ошибок распознавания')

def register_handlers_client(dp : Dispatcher):

    # Voice recognition handlers
    #dp.register_message_handler(voice_message_handler, content_types=[
    #types.ContentType.VOICE,
    #types.ContentType.AUDIO,
    #types.ContentType.DOCUMENT
    #])
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(correction_command, commands=['corr', 'correction'])
    #dp.register_message_handler(affect_command, commands=['aff', 'affect'])
    #dp.register_message_handler(medical_command, commands=['med', 'medical'])
    #dp.register_message_handler(dialog_command, commands=['dialog'])
    #dp.register_message_handler(language_auto_command, commands=['auto'])

    dp.register_message_handler(send)
    dp.register_edited_message_handler(send)