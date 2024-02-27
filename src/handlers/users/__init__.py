"""
Since there is only one menu, only one router was used.

However, the reaction to each button/command was placed in a
separate module for ease of writing (since some chains of
events turned out to be too long for their adequate perception
in one file).
"""
from .create_an_invoice_for_cargo import router_for_main_menu
from .give_all_commands_bot import router_for_main_menu
from .start_main_menu import router_for_main_menu
from .hide_main_menu import router_for_main_menu
from .give_developer import router_for_main_menu
from .give_manual import router_for_main_menu
from .call_manager import router_for_main_menu

__all__ = ['router_for_main_menu']
