from loader import router_for_main_menu, bot
from aiogram.filters import Command
from config import ID_MANAGER
from aiogram import types, F


BUFFER: dict = {ID_MANAGER: None}


@router_for_main_menu.message(Command("call_manager"))
@router_for_main_menu.message(F.text == "Позвать консультанта")
async def call_manager(message: types.Message):

    if BUFFER[ID_MANAGER] is None:

        name_user: str = message.from_user.first_name
        BUFFER[ID_MANAGER] = message.from_user.id

        args_for_send_message = {
            'chat_id': ID_MANAGER,
            'text': f"Пользователь {name_user} "
                    f"просит провести консультацию",
        }
        await bot.send_message(**args_for_send_message)

    elif BUFFER[ID_MANAGER] == message.from_user.id:

        name_user: str = message.from_user.first_name

        args_for_send_message = {
            'chat_id': ID_MANAGER,
            'text': f"Пользователь {name_user} "
                    f"просит обратиь на себя внимание",
        }
        await bot.send_message(**args_for_send_message)

    else:

        text: str = f"Консультант занят. " \
                    f"Пожалуйста подождите."
        await message.answer(text=text)


@router_for_main_menu.message()
async def dialogue(message: types.Message):

    user_id = message.from_user.id

    if BUFFER[ID_MANAGER] and BUFFER[ID_MANAGER] != 'resting':

        if user_id == ID_MANAGER:

            text: str = message.text

            if text == 'в ожидании':
                BUFFER[ID_MANAGER] = None
            elif text == 'отдыхаю':
                BUFFER[ID_MANAGER] = 'resting'
            else:
                answer_manager: str = "Консультант: " + text
                await bot.send_message(chat_id=BUFFER[ID_MANAGER], text=answer_manager)

        elif BUFFER[ID_MANAGER] == user_id:

            name_user: str = message.from_user.first_name
            answer_user: str = f"{name_user}: " + message.text

            args_for_send_message = {
                    'text': answer_user,
                    'chat_id': ID_MANAGER
            }

            await bot.send_message(**args_for_send_message)

    elif BUFFER[ID_MANAGER] and BUFFER[ID_MANAGER] == 'resting':

        if user_id == ID_MANAGER:

            if message.text == 'в ожидании':
                BUFFER[ID_MANAGER] = None

        else:

            text: str = f"Консультант занят. " \
                        f"Пожалуйста подождите."
            await message.answer(text=text)

    elif BUFFER[ID_MANAGER] is None and user_id == ID_MANAGER:

        text: str = f"Консультант не может заговорить первым. " \
                    f"К нему должны сначала обратиться."
        await message.answer(text=text)

    else:

        text: str = f"Сначало нужно позвать " \
                    f"консультанта прежде чем писать " \
                    f"здесь или нажать любую другую кнопку."
        await bot.send_message(chat_id=user_id, text=text)
