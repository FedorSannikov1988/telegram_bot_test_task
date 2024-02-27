"""
Assembly of all application components and variables
(I mean environment variables) necessary for its launch/operation.
"""
from aiogram.fsm.storage.memory import MemoryStorage
from answers import path_for_users_answers, \
                    path_for_button_names, \
                    load_answer_for_user, \
                    path_for_urls
from aiogram.enums import ParseMode
from aiogram import Dispatcher, \
                    Router, \
                    Bot, \
                    F
from config import TOKEN_BOT
from loguru import logger


bot = Bot(token=TOKEN_BOT, parse_mode=ParseMode.HTML)

dp = Dispatcher(storage=MemoryStorage())

router_for_main_menu = Router()

router_for_main_menu.message.filter(F.chat.type == "private")

logger.add('logs/logs.json',
           level='DEBUG',
           format='{time} {level} {message}',
           rotation='10 MB',
           compression='zip',
           serialize=True)

all_urls: dict = load_answer_for_user(path_for_file=
                                      path_for_urls)
button_names: dict = load_answer_for_user(path_for_file=
                                          path_for_button_names)
all_answer_for_user: dict = load_answer_for_user(path_for_file=
                                                 path_for_users_answers)
