"""
Class in the module for FSM State used when
registering a user/buyer.
"""
from aiogram.fsm.state import StatesGroup, State


class CreateAnInvoiceForCargo(StatesGroup):

    wait_cargo_description = State()
    wait_cargo_weight = State()
    wait_dimensions_cargo = State()
    wait_exact_shipping_address = State()
    wait_exact_receiving_address = State()
