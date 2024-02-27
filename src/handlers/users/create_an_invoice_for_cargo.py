from utilities import create_pdf_document, generate_file_name_and_path_for_file
from keyboards import get_user_payment_method, PaymentMethod
from aiogram.types.input_file import FSInputFile
from states import CreateAnInvoiceForCargo
from aiogram.fsm.context import FSMContext
from validation import ValidationReviews
from loader import router_for_main_menu
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram import types, F
from loader import bot
import collections


MINIMUM_LENGTH_CARGO_DESCRIPTION: int = 3
QUESTIONS_FOR_CUSTOMER: dict = \
    {
        "cargo_description": "Описание груза",
        "cargo_weight": "Вес груза",
        "dimensions_cargo": "Габариты груза",
        "exact_shipping_address": "Адрес отправки",
        "exact_receiving_address": "Адрес доставки",
        "payment_method": "Метод оплаты",
    }


@router_for_main_menu.message(Command("create_an_invoice_for_cargo"))
@router_for_main_menu.message(F.text == "Создать накладную")
async def start_create_an_invoice_for_cargo(message: types.Message,
                                            state: FSMContext):

    text: str = f"Введите описание груза"

    await state.set_state(CreateAnInvoiceForCargo.wait_cargo_description)
    await message.answer(text=text)


@router_for_main_menu.message(CreateAnInvoiceForCargo.wait_cargo_description)
async def entering_description_cargo(message: types.Message,
                                     state: FSMContext):

    cargo_description: str = message.text

    if cargo_description != "" and \
        ValidationReviews().validation_long_reviews(
            min_len=MINIMUM_LENGTH_CARGO_DESCRIPTION,
            text=cargo_description):

        await state.update_data({'cargo_description': cargo_description})
        await state.set_state(CreateAnInvoiceForCargo.wait_cargo_weight)

        text: str = "Введите вес груза в киллограммах. " \
                    "Пример: 0.5 или 2"

    else:
        text: str = "Введите описание груза " \
                    "(описание груза не может " \
                    "быть меньше трех символов)."

    await message.answer(text=text)


@router_for_main_menu.message(CreateAnInvoiceForCargo.wait_cargo_weight)
async def entering_cargo_weight(message: types.Message,
                                state: FSMContext):

    cargo_weight: str = message.text

    try:
        cargo_weight: float = float(cargo_weight)

        if cargo_weight > 0:

            await state.update_data({'cargo_weight': cargo_weight})
            await state.set_state(CreateAnInvoiceForCargo.wait_dimensions_cargo)

            text: str = "Введите габариты груза в сантиметрах " \
                        "в следующем формате X*Y*Z. где X, Y, Z " \
                        "- можно ввести как десятичные числа " \
                        "так и целыми." \
                        "Пример: 0.5*0.6*0.7"
        else:

            text: str = "Вес груза должен быть больше нуля."

        await message.answer(text=text)

    except ValueError:

        text: str = "Введите вес груза в киллограммах " \
                    "(введенный ранее текс не может быть " \
                    "интерпритирован как число)"
        await message.answer(text=text)


@router_for_main_menu.message(CreateAnInvoiceForCargo.wait_dimensions_cargo)
async def entering_dimensions_cargo(message: types.Message,
                                    state: FSMContext):

    dimensions_cargo: str = message.text
    counter_element = collections.Counter(dimensions_cargo)
    counter_separator = counter_element.get('*')

    if counter_separator is not None \
            and counter_separator == 2:
        dimensions_cargo: list = dimensions_cargo.split('*')

        try:
            x_y_z_cm = tuple(map(lambda x: float(x), dimensions_cargo))

            if all(num > 0 for num in x_y_z_cm):

                await state.update_data({'dimensions_cargo': x_y_z_cm})
                await state.set_state(CreateAnInvoiceForCargo.wait_exact_shipping_address)

                text: str = "Введите точный адрес отправителя груза:"

            else:
                text: str = "Введите габариты груза в сантиметрах " \
                            "в следующем формате X*Y*Z. " \
                            "Габариты груза должны быть " \
                            "положительными."

            await message.answer(text=text)

        except ValueError:

            text: str = "Введите габариты груза в сантиметрах " \
                        "в следующем формате X*Y*Z." \
                        "Введенный ранее текст не возможно " \
                        "преобразовать в числа."
            await message.answer(text=text)

    else:
        text: str = "Введите габариты груза в сантиметрах " \
                    "в следующем формате X*Y*Z. " \
                    "Введенный ранее текст не соответствует " \
                    "формату."
        await message.answer(text=text)


@router_for_main_menu.message(CreateAnInvoiceForCargo.wait_exact_shipping_address)
async def entering_exact_shipping_address(message: types.Message,
                                          state: FSMContext):

    exact_shipping_address: str = message.text

    if exact_shipping_address != "":
        await state.update_data({'exact_shipping_address': exact_shipping_address})
        await state.set_state(CreateAnInvoiceForCargo.wait_exact_receiving_address)

        text: str = "Введите точный адрес получателя груза:"

        await message.answer(text=text)


@router_for_main_menu.message(CreateAnInvoiceForCargo.wait_exact_receiving_address)
async def entering_exact_receiving_address(message: types.Message,
                                           state: FSMContext):

    exact_receiving_address: str = message.text

    if exact_receiving_address != "":
        await state.update_data({'exact_receiving_address': exact_receiving_address})
        await state.set_state()

        text: str = f"Выберите способ отплаты:"

        await message.answer(text=text,
                             reply_markup=get_user_payment_method())


@router_for_main_menu.callback_query(PaymentMethod.filter())
async def entering_payment_method_and_get_document(callback: CallbackQuery,
                                                   callback_data: PaymentMethod,
                                                   state: FSMContext):

    chat_id = callback.message.chat.id
    user_id = callback.message.from_user.id
    payment_method = callback_data.payment_method

    await state.update_data({'payment_method': payment_method})

    pdf_file_path = \
        generate_file_name_and_path_for_file(user_id=user_id)

    create_pdf_document(data=await state.get_data(),
                        pdf_file_path=pdf_file_path,
                        questions=QUESTIONS_FOR_CUSTOMER)

    args_for_send_document = {
        'chat_id': chat_id,
        'document': FSInputFile(pdf_file_path),
        'caption': "Документ сформирован"
    }
    await bot.send_document(**args_for_send_document)
