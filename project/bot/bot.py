from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
import asyncio

TOKEN = "8072237017:AAHKxLznmEVzKy0YU8HVJbPSnUZg8zDydJU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="📚 Открыть курсы",
                    web_app=WebAppInfo(
                        url="https://classy-figolla-f8e223.netlify.app/"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer("Открыть Mini App:", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
