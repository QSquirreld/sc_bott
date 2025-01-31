from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

remove = ReplyKeyboardRemove()

# Кнопка "Назад"
back_button = KeyboardButton(text="Назад")

# Клавиатура для начального тестирования
test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пройти тестирование")],
        [KeyboardButton(text="Тестирование было выполнено ранее")]
    ],
    resize_keyboard=True
)

# Клавиатура главного меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Упражнения"), KeyboardButton(text="Сценарии")],
        [KeyboardButton(text="Рекомендации"), KeyboardButton(text="Прогресс")],
        [KeyboardButton(text="Настройки уведомлений")]
    ],
    resize_keyboard=True
)

# Клавиатура выбора интенсивности
intensity_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каждый день")],
        [KeyboardButton(text="Свой режим")],
        [back_button]
    ],
    resize_keyboard=True
)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Кнопка 1')], [KeyboardButton(text='Кнопка 2')]],
                           resize_keyboard=True, input_field_placeholder='Выберите действие')

restart = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать заново')]],
                              resize_keyboard=True, input_field_placeholder='Выберите действие')

