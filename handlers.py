from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import keyboards as kb
from fsms import UserStates
from access_checker import AccessChecker
from gpt import GPTHandler

router = Router()

# Создаем экземпляр проверки доступа
access_filter = AccessChecker()
gpt_handler = GPTHandler()  # Создаем экземпляр обработчика GPT

@router.message(CommandStart(), access_filter)
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.INITIAL_TEST)
    await message.answer(
        "Добро пожаловать! Давайте начнем с оценки вашего текущего уровня.",
        reply_markup=kb.test_kb
    )

@router.message(UserStates.INITIAL_TEST, F.text.in_(["Пройти тестирование", "Тестирование было выполнено ранее"]))
async def handle_test_choice(message: Message, state: FSMContext):
    if message.text == "Тестирование было выполнено ранее":
        await state.set_state(UserStates.MAIN_MENU)
        await message.answer(
            "Добро пожаловать в главное меню!",
            reply_markup=kb.main_menu_kb
        )
    else:  # Пройти тестирование
        await state.set_state(UserStates.SKILL_SELECTION)
        await message.answer(
            "Пожалуйста, укажите навык, который вы хотите развивать:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[kb.back_button]],
                resize_keyboard=True
            )
        )

@router.message(UserStates.SKILL_SELECTION, F.text != "Назад")
async def handle_skill_input(message: Message, state: FSMContext):
    skill = message.text
    await state.update_data(selected_skill=skill)
    
    await message.answer(
        "Выберите интенсивность напоминаний:",
        reply_markup=kb.intensity_kb
    )
    await state.set_state(UserStates.INTENSITY_SELECTION)

@router.message(UserStates.INTENSITY_SELECTION, F.text.in_(["Каждый день", "Свой режим"]))
async def handle_intensity(message: Message, state: FSMContext):
    user_data = await state.get_data()
    skill = user_data.get('selected_skill')
    intensity = message.text
    
    # Получаем план развития от GPT
    development_plan = await gpt_handler.generate_development_plan(skill, intensity)
    
    # Сохраняем данные
    await state.update_data(
        intensity=intensity,
        development_plan=development_plan
    )
    
    await state.set_state(UserStates.MAIN_MENU)
    await message.answer(
        f"Ваш план развития навыка '{skill}' готов!\n\n{development_plan}",
        reply_markup=kb.main_menu_kb
    )

@router.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == UserStates.SKILL_SELECTION:
        await state.set_state(UserStates.INITIAL_TEST)
        await message.answer("Вернемся к началу.", reply_markup=kb.test_kb)
    else:
        await state.set_state(UserStates.MAIN_MENU)
        await message.answer("Главное меню:", reply_markup=kb.main_menu_kb)

# Обработчики кнопок главного меню
@router.message(UserStates.MAIN_MENU, F.text == "Упражнения")
async def handle_exercises(message: Message):
    await message.answer("Раздел упражнений")

@router.message(UserStates.MAIN_MENU, F.text == "Сценарии")
async def handle_scenarios(message: Message):
    await message.answer("Раздел сценариев")

@router.message(UserStates.MAIN_MENU, F.text == "Рекомендации")
async def handle_recommendations(message: Message):
    await message.answer("Раздел рекомендаций")

@router.message(UserStates.MAIN_MENU, F.text == "Прогресс")
async def handle_progress(message: Message):
    await message.answer("Ваш прогресс")

@router.message(UserStates.MAIN_MENU, F.text == "Настройки уведомлений")
async def handle_notifications(message: Message):
    await message.answer("Настройки уведомлений")

@router.message(Command('help'), access_filter)
async def cmd_help(message: Message):
    await message.answer('Супер бот',
                         reply_markup=kb.restart)