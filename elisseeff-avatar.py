import logging
from aiogram.utils import executor
from client import register_handlers_client

from create_bot import dp, my_status

register_handlers_client(dp)

my_status.logger = logging.getLogger(__name__)
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    filename="/home/pavel/github/elisseeff-avatar/log/elisseeff_avatar_bot.log",
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def on_startup(_):
    my_status.logger.warning("Elisseeff Avatar Bot logging is ON!")
    my_status.dbase = sql_start()
    res = get_elis_chats_for_initialisation()
    for i in res:
        if i[0] is not None:
            res1 = get_chat_messages(i[0])
            for j in res1:
                update(i[0], my_status.group_messages, j[0], j[1], my_status.count_messages)
                    
# Start the bot
if __name__ == '__main__':
    
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except (KeyboardInterrupt, SystemExit):
        pass