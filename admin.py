from aiogram import Dispatcher, types
from sqlite_db import sql_read, sql_read_tokens, get_voice_messages_stat, get_elis_stat
from admin_kb import button_case_admin
from create_bot import bot, my_status

idd = None

# Get Moderator Id 
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def moderator_command(message: types.Message):
    global idd
    idd = message.from_user.id
    #my_status.logger.warning("moderator_command: is Ok!")
    await bot.send_message(message.from_user.id, 'What do you want Sir?', reply_markup=button_case_admin)
    await message.delete()

async def cm_elis_stat(message : types.Message):
    global idd
    if message.from_user.id == idd:
        res = get_elis_stat()
        bbuf = 'Elis stat: [User], [Role], [Messages], [Tokes]\n'
        count = 0
        for i in res:
            count += 1
            bbuf += f'{str(count)}. {i[0]}, {i[1]}, {i[2]}, {i[3]}\n'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=button_case_admin)

async def cm_tokens_used(message : types.Message):
    global idd
    if message.from_user.id == idd:
        res = sql_read_tokens()
        text=f"Расход токенов при вводе сообщения в бот: {res[0]}\n"
        text += f"Токенов расходуется на ответ API OpenAI при выводе сообщения в бот: {res[1]}\n"
        text += f"Всего токенов израсходовано на запрос и на ответ (суммарно в задании к боту): {res[2]}\n"
        await bot.send_message(message.from_user.id, text, reply_markup=button_case_admin)

async def cm_chats(message : types.Message):
    global idd
    if message.from_user.id == idd:
        bbuf = 'Chats in connection: ' + str(len(my_status.group_messages)) + '.\n'
        bbuf += 'Messages in chats\n'
        for i in my_status.count_messages.keys():
            chat = await bot.get_chat(int(i))
            my_status.logger.warning(f"cm_chats: chat: {i}. type: {chat['type']}. title: {chat['title']}")
            print(f"cm_chats: chat: {i}. type: {chat['type']}. title: {chat['title']}")
            if chat['type'] == 'group':
                bbuf += chat['title'] + ': ' + str(my_status.count_messages[i]) + ';\n'
            elif chat['type'] == 'supergroup':
                bbuf += chat['title'] + ': ' + str(my_status.count_messages[i]) + ';\n'
            elif chat['type'] == 'private':
                bbuf += chat['username'] + ': ' + str(my_status.count_messages[i]) + ';\n'
            else:
                bbuf += 'not found...'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=button_case_admin)

async def cm_voice_records(message : types.Message):
    global idd
    if message.from_user.id == idd:
        res = get_voice_messages_stat()
        bbuf = 'Voice messages stat: [User], [Messages], [Words]\n'
        count = 0
        for i in res:
            count += 1
            bbuf += f'{str(count)}. {i[0]}, {i[1]}, {i[2]}\n'
        await bot.send_message(message.from_user.id, bbuf, reply_markup=button_case_admin)

# Handlers Registration
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(moderator_command, commands=['moderator', 'moder'], is_chat_admin=True)
    dp.register_message_handler(cm_tokens_used, commands=['tokens_used'])
    dp.register_message_handler(cm_chats, commands=['chats'])
    dp.register_message_handler(cm_voice_records, commands=['voice_records'])
    dp.register_message_handler(cm_elis_stat, commands=['elis_stat'])
    