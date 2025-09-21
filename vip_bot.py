import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ---------- تنظیمات ----------
BOT_TOKEN = "8311865694:AAHrQDLSJcFKOztBj8X2PtMafk7U7AML0Uo"
CHANNEL_ID = "@neuranacademy"
ADMINS = [7374971382]  # آیدی عددی خودت
USERS_FILE = "users.json"
# ------------------------------

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === ذخیره کاربرها ===
def save_user(user_id: int):
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

def get_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# === کیبورد منوی اصلی ===
def main_menu_kb(user_id=None):
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
            InlineKeyboardButton(text="☎️ پشتیبانی ربات", url="https://t.me/aiireza_1383"),
        ],
        [
            InlineKeyboardButton(text="💰 ورود به صرافی", callback_data="exchange_menu")
        ]
    ])

    if user_id in ADMINS:
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text="📢 ارسال پیام همگانی", callback_data="broadcast")]
        )

    return kb

# === کیبورد منوی صرافی ===
def exchange_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="صرافی XT", url="https://www.xtfarsi.net/en/accounts/register?ref=1133")],
        [InlineKeyboardButton(text="صرافی OURBIT", url="https://www.ourbit.com/register?inviteCode=S3ZCNR")],
        [InlineKeyboardButton(text="صرافی BITUNIX", url="https://www.bitunix.com/register?vipCode=hajamin")],
        [InlineKeyboardButton(text="صرافی TOOBIT", url="https://www.toobit.com/t/lpOdP4")],
        [InlineKeyboardButton(text="⬅️ بازگشت", callback_data="back_to_main")]
    ])
    return kb

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    save_user(message.from_user.id)
    text = f"سلام {message.from_user.first_name or ''} 👋\nبه ربات VIP خوش آمدی!"
    await message.answer(text, reply_markup=main_menu_kb(message.from_user.id))

@dp.callback_query(lambda c: c.data == "exchange_menu")
async def cb_exchange_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("یکی از صرافی‌های زیر را انتخاب کنید:", reply_markup=exchange_menu_kb())

@dp.callback_query(lambda c: c.data == "back_to_main")
async def cb_back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("به منوی اصلی بازگشتید:", reply_markup=main_menu_kb(callback.from_user.id))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
