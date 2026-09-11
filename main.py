import os
import random
import string
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- دالات التوليد ---

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "tempmail.org"]
    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"{username}@{random.choice(domains)}"

def generate_message():
    messages = [
        "مرحباً! هذا إشعار تجريبي لاختبار النظام.",
        "تم تسجيل دخولك بنجاح من جهاز جديد.",
        "رمز التحقق الخاص بك هو: " + str(random.randint(100000, 999999)),
        "تذكير: لديك موعد مجدول غداً في تمام الساعة 5 مساءً."
    ]
    return random.choice(messages)

# --- أوامر البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **أهلاً بك في بوت التوليد العشوائي!**\n\n"
        "الأوامر المتاحة:\n"
        "/pass - توليد كلمة مرور قوية\n"
        "/email - توليد بريد إلكتروني وهمي\n"
        "/msg - توليد رسالة تجريبية\n"
        "/all - توليد الحزمة كاملة"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def send_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔑 **كلمة المرور:** `{generate_password()}`", parse_mode="Markdown")

async def send_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📧 **البريد الإلكتروني:** `{generate_email()}`", parse_mode="Markdown")

async def send_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💬 **الرسالة:**\n{generate_message()}")

async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = (
        f"📧 **الإيميل:** `{generate_email()}`\n"
        f"🔑 **كلمة المرور:** `{generate_password()}`\n"
        f"💬 **الرسالة:** {generate_message()}"
    )
    await update.message.reply_text(res, parse_mode="Markdown")

# --- التشغيل الرئيسي ---

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        logger.error("خطأ: لم يتم العثور على متغير BOT_TOKEN!")
        return

    app = Application.builder().token(TOKEN).build()

    # تسجيل الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pass", send_pass))
    app.add_handler(CommandHandler("email", send_email))
    app.add_handler(CommandHandler("msg", send_msg))
    app.add_handler(CommandHandler("all", send_all))

    logger.info("تم تشغيل البوت بنجاح...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
