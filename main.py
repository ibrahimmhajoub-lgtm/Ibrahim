import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# إعداد التسجيل لمتابعة الـ Logs على Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# جلب المفاتيح من متغيرات البيئة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# إعداد عميل Gemini
ai_client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البدء /start"""
    await update.message.reply_text("أهلاً بك! أنا بوت ذكاء اصطناعي مدعوم بـ Gemini. أرسل لي أي سؤال وسأجيبك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية القادمة من المستخدم"""
    user_text = update.message.text
    
    # إرسال إشارة جاري الكتابة للمستخدم
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # استدعاء نموذج Gemini 2.5 Flash
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"خطأ أثناء الاستجابة: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        logging.error("برجاء التأكد من ضبط TELEGRAM_TOKEN و GEMINI_API_KEY في متغيرات البيئة!")
        exit(1)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logging.info("البوت يعمل الآن...")
    app.run_polling()
