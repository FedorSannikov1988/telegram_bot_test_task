"""
Main keyboard.
"""
from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton


main_keyboard = \
    ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Помощь"),
                KeyboardButton(text="Инструкция"),
                KeyboardButton(text="Скрыть меню")
            ],
            [
                KeyboardButton(text="Создать накладную"),
                KeyboardButton(text="Позвать консультанта")
            ],
            [
                KeyboardButton(text="Разработчик"),
            ],
        ],
        resize_keyboard=True
    )


main_keyboard_for_manager = \
    ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="в ожидании"),
                KeyboardButton(text="отдыхаю")
            ],
        ],
        resize_keyboard=True
    )
