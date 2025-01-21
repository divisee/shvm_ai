
# handlers/users_handler.py
import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboard_users import main_keyboard, cancel_keyboard
from utils.vllm_requests import send_request_to_vllm

router = Router()

user_tasks = {}

# Определение состояний
class RequestStates(StatesGroup):
    waiting_for_question = State()

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message):
    username = message.from_user.username
    first_name = message.from_user.first_name
    display_name = first_name if first_name else username if username else "тебя"

    await message.answer(
        text=(
            f"Добро пожаловать, <b>{display_name}</b>!\n"
            "✨ Если ты чувствуешь, что твоя душа запуталась похлеще, чем мантия в заклинании «Левикорпус», "
            "то ты попал по адресу! Нажми на кнопку, чтобы задать свой вопрос мудрецу."
        ),
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )

# Обработчик кнопки "Запрос к Мудрецу"
# @router.message(F.text == "Запрос к Мудрецу")
@router.callback_query(F.data == "Запрос к Мудрецу")
async def handle_request (callback_query: CallbackQuery, state: FSMContext): #(message: Message, state: FSMContext):
  
    await state.set_state(RequestStates.waiting_for_question)
    await callback_query.message.answer(f"Поделитесь своим вопросом.", reply_markup=cancel_keyboard()) 
    await callback_query.answer()

@router.callback_query(F.data == "Отменить")
async def handle_cancel(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await state.clear()
    await callback_query.message.delete()
    await callback_query.answer()

    if user_id in user_tasks:
        del user_tasks[user_id]

    user_tasks[user_id] = True

    if user_tasks[user_id]:
        await asyncio.sleep(20)
        await callback_query.message.answer_sticker(sticker="CAACAgIAAxkBAAIB3WeH1IytpjEIzihGOYVfHMShJnXCAAJRXQACrnnwSx4pXBauflLrNgQ")
        await callback_query.message.answer("Кажется, ты забыл поговорить с Мудрецом.", reply_markup=main_keyboard())
        del user_tasks[user_id]

# Обработчик текста после кнопки "Запрос к Мудрецу"
@router.message( RequestStates.waiting_for_question)
async def process_question(message: Message, state: FSMContext):
    user_question = message.text

    sent_message = await message.reply("💬")

    try:
        response = await send_request_to_vllm(user_question)
        await sent_message.edit_text(response, reply_markup=main_keyboard())
    except Exception as e:
        await sent_message.edit_text("Произошла ошибка при обработке вашего запроса. Попробуйте позже.", reply_markup=main_keyboard())

    await state.clear()


# Обработчик любого сообщения пользователя
@router.message()
async def handle_any_message(message: Message):
    user_id = message.from_user.id
    # await message.answer(f"{message.sticker.file_id}")

    # Если у пользователя была отложенная задача, отменяем ее
    if user_id in user_tasks:
        try:
            del user_tasks[user_id]  # Удаляем пару key:value полностью
        except:
            pass