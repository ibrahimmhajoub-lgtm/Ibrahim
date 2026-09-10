import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from google import genai

logging.basicConfig(level=logging.INFO)

# جلب المتغيرات من بيئة Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# إعداد عميل Gemini
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# إعداد تطبيق تليجرام
telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("أهلاً بك! أنا جاهز للرد على أي سؤال تررسه فوراً.")

async def handle_message(update: Update, context):
    user_text = update.message.text

    # إظهار مؤشر "جاري الكتابة..." للمستخدم
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # معالجة الرسالة مباشرة وبشكل مستقل دون حفظ السياق
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("حدث خطأ أثناء معالجة رسالتك، يرجى المحاولة لاحقاً.")

# تسجيل الأوامر
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# تطبيق Flask للـ Webhook
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is live and running!", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
async def webhook():
    """استقبال التحديثات المباشرة من تليجرام"""
    update = Update.de_json(data=request.get_json(force=True), bot=telegram_app.bot)
    await telegram_app.initialize()
    await telegram_app.process_update(update)
    await telegram_app.shutdown()
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
