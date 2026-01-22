from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
 
bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    username = State()
    mc_nick = State()
    mc_version = State()
    source = State()
    activity = State()
    playstyle = State()
    reason = State()
    about = State()

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("📝 АНКЕТА\n\n1️⃣ Ваше имя / прозвище:")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def q2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("2️⃣ Ваш возраст:")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def q3(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("3️⃣ Ваш юзер (Telegram / Discord):")
    await state.set_state(Form.username)

@dp.message(Form.username)
async def q4(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("4️⃣ Ник в Minecraft:")
    await state.set_state(Form.mc_nick)

@dp.message(Form.mc_nick)
async def q5(message: Message, state: FSMContext):
    await state.update_data(mc_nick=message.text)
    await message.answer("5️⃣ Версия Minecraft:")
    await state.set_state(Form.mc_version)

@dp.message(Form.mc_version)
async def q6(message: Message, state: FSMContext):
    await state.update_data(mc_version=message.text)
    await message.answer("6️⃣ Откуда узнали о нашем хаусе?")
    await state.set_state(Form.source)

@dp.message(Form.source)
async def q7(message: Message, state: FSMContext):
    await state.update_data(source=message.text)
    await message.answer("7️⃣ Будете ли вы активны на сервере и в чате?")
    await state.set_state(Form.activity)

@dp.message(Form.activity)
async def q8(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.answer("8️⃣ Что больше любите делать в хаусе / Minecraft?")
    await state.set_state(Form.playstyle)

@dp.message(Form.playstyle)
async def q9(message: Message, state: FSMContext):
    await state.update_data(playstyle=message.text)
    await message.answer(
        "9️⃣ Если вы раньше были в другом хаусе — почему ушли / выгнали?\n"
        "Если не были — напишите «не был(а)»"
    )
    await state.set_state(Form.reason)

@dp.message(Form.reason)
async def q10(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("🔟 Расскажите немного о себе:")
    await state.set_state(Form.about)

@dp.message(Form.about)
async def finish(message: Message, state: FSMContext):
    data = await state.update_data(about=message.text)

    text = (
        "📋 **НОВАЯ АНКЕТА В ХАУС**\n\n"
        f"1. Имя: {data['name']}\n"
        f"2. Возраст: {data['age']}\n"
        f"3. Юзер: {data['username']}\n"
        f"4. MC ник: {data['mc_nick']}\n"
        f"5. Версия MC: {data['mc_version']}\n"
        f"6. Узнал о хаусе: {data['source']}\n"
        f"7. Активность: {data['activity']}\n"
        f"8. Любит делать: {data['playstyle']}\n"
        f"9. Причина ухода: {data['reason']}\n"
        f"10. О себе: {data['about']}\n\n"
        f"👤 TG: @{message.from_user.username}"
    )

    await bot.send_message(ADMIN_CHAT_ID, text)
    await message.answer("✅ Анкета принята. Ожидайте рассмотрения.")
    await state.clear()

# Фоновая задача для поддержания активности (защита от замедления)
async def keepalive_task():
    """Периодический ping для предотвращения замедления на бесплатных инстансах"""
    while True:
        try:
            await asyncio.sleep(60)  # Ждём 60 секунд
            me = await bot.get_me()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{current_time}] Бот активен: @{me.username}")
        except Exception as e:
            logger.error(f"Ошибка в keepalive_task: {e}")

async def main():
    # Запуск фоновой задачи
    asyncio.create_task(keepalive_task())
    await dp.start_polling(bot)

asyncio.run(main())
