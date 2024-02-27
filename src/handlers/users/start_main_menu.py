"""
The module is responsible for getting the main menu.
"""
from keyboards import main_keyboard, main_keyboard_for_manager
from aiogram.utils.markdown import hbold
from loader import router_for_main_menu
from aiogram.filters import Command
from config import ID_MANAGER
from aiogram import types, F


@router_for_main_menu.message(Command("start"))
@router_for_main_menu.message(F.text == "Старт")
async def start_main_menu(message: types.Message):

    user_id = message.from_user.id

    if ID_MANAGER != user_id:

        text: str = f'Здраствуйте, ' \
                    f'{hbold(message.from_user.first_name)}! '\
                    f'{hbold("Этот бот создает накладную для доставки груза.")}'
        await message.answer(text=text,
                             reply_markup=main_keyboard)
    else:
        await message.answer(text="Здраствуйте. Консультант.",
                             reply_markup=main_keyboard_for_manager)
