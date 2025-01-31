from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    INITIAL_TEST = State()        # Состояние начального тестирования
    SKILL_SELECTION = State()     # Выбор навыка для развития
    INTENSITY_SELECTION = State()  # Новое состояние
    MAIN_MENU = State()           # Главное меню (состояние по умолчанию)
