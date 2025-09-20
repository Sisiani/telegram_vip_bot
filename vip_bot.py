import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

# ---------- تنظیمات ----------
BOT_TOKEN = "8311865694:AAHrQDLSJcFKOztBj8X2PtMafk7U7AML0Uo"
CHANNEL_ID = "@neuranacademy"
# ------------------------------

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔵 عضویت در کانال VIP", callback_data="check_sub"),
            InlineKeyboardButton(text="🎁 دریافت بونوس", callback_data="bonus"),
        ],
        [
            InlineKeyboardButton(text="📩 دریافت اشتراک", callback_data="get_sub"),
            InlineKeyboardButton(text="🧾 مشخصات حساب", callback_data="account"),
        ],
        [
            InlineKeyboardButton(text="☎️ پشتیبانی ربات", url="https://t.me/e11_s33"),
        ]
    ])
    return kb

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = f"سلام {message.from_user.first_name or ''} 👋\nبه ربات VIP خوش آمدی!"
    await message.answer(text, reply_markup=main_menu_kb())

async def user_is_member(user_id: int) -> bool:
    try:
        mem = await bot.get_chat_member(CHANNEL_ID, user_id)
        return mem.status in ("creator", "administrator", "member")
    except Exception as e:
        logging.error(f"Error checking membership: {e}")
        return False

@dp.callback_query(lambda c: c.data == "check_sub")
async def cb_check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ok = await user_is_member(user_id)
    if ok:
        await callback.message.answer("✅ شما عضو کانال هستید و دسترسی دارید.\n🔐 محتوای VIP اینجاست.")
    else:
        join_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 ورود به کانال", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
            [InlineKeyboardButton(text="📥 من عضو شدم، بررسی مجدد", callback_data="check_sub")]
        ])
        await callback.message.answer(
            "⛔ شما هنوز عضو کانال نیستید.\nلطفاً عضو شوید و دوباره امتحان کنید.",
            reply_markup=join_kb
        )

@dp.callback_query(lambda c: c.data == "get_sub")
async def cb_get_sub(callback: types.CallbackQuery):
    await callback.message.answer("برای خرید اشتراک اینجا لینک پرداخت قرار می‌گیرد.")

@dp.callback_query(lambda c: c.data == "bonus")
async def cb_bonus(callback: types.CallbackQuery):
    await callback.message.answer("🎁 بونوس شما: کد هدیه BONUS123")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

