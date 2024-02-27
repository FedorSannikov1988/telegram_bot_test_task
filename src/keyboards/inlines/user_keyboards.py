"""
All Inline Keyboard for users .
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import PaymentMethod


def get_user_payment_method():

    builder = InlineKeyboardBuilder()

    builder.button(
        text='Наличными',
        callback_data=PaymentMethod(
            payment_method='Наличный расчет')
    )

    builder.button(
        text='Картой',
        callback_data=PaymentMethod(
            payment_method='Безналичный расчет')
    )

    builder.adjust(2)

    return builder.as_markup()
