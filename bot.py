# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import init_db, save_link, get_links
import asyncio
import os

bot = Bot(token=os.getenv(8150760033:AAFJDQ67L9h0nrTCtPOzPHf0kK1NI75bL-E))
dp = Dispatcher()

# Инициализация БД при старте
async def on_startup():
    await init_db()

# Клавиатура
def get_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить ссылку ➕")
    builder.button(text="Показать ссылки 🔍")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "📚 Бот для сохранения ссылок\n\n"
        "Отправьте ссылку или используйте кнопки:",
        reply_markup=get_keyboard()
    )

# Добавление ссылки
@dp.message(lambda msg: msg.text and msg.text.startswith(('http://', 'https://')))
async def add_link(message: types.Message):
    await save_link(message.text)
    await message.answer("✅ Ссылка сохранена!")

# Показать все ссылки
@dp.message(lambda msg: msg.text == "Показать ссылки 🔍")
async def show_links(message: types.Message):
    links = await get_links()
    if not links:
        await message.answer("📭 Ссылок пока нет")
        return
    
    response = "📜 Последние ссылки:\n\n" + "\n".join([f"{i+1}. {link.url}" for i, link in enumerate(links)])
    await message.answer(response)

# Запуск бота
async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())