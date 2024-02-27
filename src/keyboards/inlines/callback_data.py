"""
Callback for Inline Keyboard .
"""
from aiogram.filters.callback_data import CallbackData


class PaymentMethod(CallbackData, prefix="choosing_payment_method"):
    payment_method: str
