import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# دریافت توکن ربات از Railway
API_TOKEN = os.getenv("8311865694:AAHrQDLSJcFKOztBj8X2PtMafk7U7AML0Uo")

# لاگ
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ===== مقادیر قابل تغییر =====
ADMIN_GROUP_ID = -1003086390705  # آیدی گروه خصوصی ادمین‌ها (با -100 شروع میشه)
VIP_CHANNEL_LINK = "https://t.me/NEURANAcademy"  # لینک کانال VIP

EXCHANGE_LINKS = {
    "XT": "https://www.xtfarsi.net/en/accounts/register?ref=1133",
    "OURBIT": "https://www.ourbit.com/register?inviteCode=S3ZCNR",
    "BITUNIX": "https://www.bitunix.com/register?vipCode=hajamin",
    "TOOBIT": "https://www.toobit.com/t/lpOdP4"
}
# ==============================

# دکمه‌های اصلی
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("⚡️ عضویت در Neuran academy 💰", callback_data="join_academy"))
    keyboard.row(
        InlineKeyboardButton("💳 دریافت اشتراک", callback_data="get_sub"),
        InlineKeyboardButton("🚀 دریافت بونس ویژه", callback_data="get_bonus")
    )
    keyboard.row(
        InlineKeyboardButton("👤 مشخصات حساب", callback_data="account_info"),
        InlineKeyboardButton("📞 پشتیبانی", url="https://t.me/AIireza_1383")
    )
    return keyboard

# استارت
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("سلام 👋 به ربات خوش اومدی!", reply_markup=main_menu())

# دکمه دریافت اشتراک
@dp.callback_query_handler(lambda c: c.data == "get_sub")
async def process_subscription(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("XT", callback_data="exchange_X1"),
        InlineKeyboardButton("TOOBIT", callback_data="exchange_X2"),
        InlineKeyboardButton("BITUNIX", callback_data="exchange_X3"),
        InlineKeyboardButton("OURBIT ", callback_data="exchange_X4"),
    )
    await callback.message.edit_text("یکی از صرافی‌ها رو انتخاب کن:", reply_markup=kb)

# وقتی صرافی انتخاب شد
@dp.callback_query_handler(lambda c: c.data.startswith("exchange"))
async def process_exchange(callback: types.CallbackQuery):
    exchange_name = callback.data.split("_")[1]
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("از قبل حساب دارم", callback_data=f"have_acc_{exchange_name}"),
        InlineKeyboardButton("حساب ندارم (ساخت حساب)", callback_data=f"new_acc_{exchange_name}")
    )
    await callback.message.edit_text(f"✅ شما صرافی {exchange_name} را انتخاب کردید.\nلطفا یکی از گزینه‌ها را انتخاب کنید:", reply_markup=kb)

# اگر کاربر حساب داشته باشه
@dp.callback_query_handler(lambda c: c.data.startswith("have_acc"))
async def ask_uid(callback: types.CallbackQuery):
    exchange_name = callback.data.split("_")[-1]
    await callback.message.answer(
        f"لطفا UID صرافی {exchange_name} خود را وارد کنید تا ادمین تایید کند."
    )

# اگر کاربر حساب نداشته باشه
@dp.callback_query_handler(lambda c: c.data.startswith("new_acc"))
async def new_account(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    for name, link in EXCHANGE_LINKS.items():
        kb.add(InlineKeyboardButton(name, url=link))
    await callback.message.edit_text("یکی از صرافی‌های زیر را برای ثبت‌نام انتخاب کنید:", reply_markup=kb)

# وقتی کاربر UID بفرسته
@dp.message_handler(lambda m: m.text.isdigit())
async def get_uid(message: types.Message):
    uid = message.text
    user = message.from_user
    username = f"@{user.username}" if user.username else f"{user.full_name}"
    await bot.send_message(
        ADMIN_GROUP_ID,
        f"🔔 کاربر جدید UID فرستاد:\n👤 آیدی: {username}\n🆔 UID: {uid}\n\nادمین لطفا تایید کنید."
    )
    await message.answer("✅ UID شما برای بررسی به ادمین ارسال شد.")

# وقتی ادمین ریپلای کنه و بنویسه تایید
@dp.message_handler(lambda m: m.reply_to_message and m.text.lower() == "تایید")
async def approve_user(message: types.Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        if "UID" in text and "آیدی" in text:
            username_line = [line for line in text.splitlines() if "آیدی:" in line][0]
            username = username_line.split("@")[-1]
            if username:
                await bot.send_message(
                    message.chat.id,
                    f"✅ کاربر @{username} تایید شد."
                )
                try:
                    await bot.send_message(
                        f"@{username}",
                        f"🎉 تبریک! حساب شما توسط ادمین تایید شد.\nاکنون می‌توانید به کانال VIP بپیوندید 🚀",
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton("📢 ورود به کانال VIP", url=VIP_CHANNEL_LINK)
                        )
                    )
                except:
                    pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
