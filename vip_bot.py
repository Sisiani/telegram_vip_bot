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
            InlineKeyboardButton(text="💰 ورود به صرافی", url="https://google.com")
        ]
    ])

    # دکمه ویژه فقط برای ادمین
    if user_id in ADMINS:
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text="📢 ارسال پیام همگانی", callback_data="broadcast")]
        )

    return kb


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    save_user(message.from_user.id)  # ذخیره کاربر
    text = f"سلام {message.from_user.first_name or ''} 👋\nبه ربات VIP خوش آمدی!"
    await message.answer(text, reply_markup=main_menu_kb(message.from_user.id))


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

# === ارسال پیام همگانی فقط برای ادمین ===
@dp.callback_query(lambda c: c.data == "broadcast")
async def cb_broadcast(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMINS:
        return await callback.message.answer("❌ شما دسترسی ندارید.")
    await callback.message.answer("✍️ پیام خود را ارسال کنید:")

    @dp.message()
    async def get_broadcast(msg: types.Message):
        if msg.from_user.id not in ADMINS:
            return
        users = get_users()
        sent = 0
        for user_id in users:
            try:
                await bot.send_message(user_id, msg.text)
                sent += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await msg.answer(f"✅ پیام برای {sent} نفر ارسال شد.")
        dp.message.handlers.unregister(get_broadcast)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
