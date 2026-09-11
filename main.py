import os
import logging
from telegram.ext import Application

# إعداد السجلات لمتابعة الاتصال
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # جلب التوكن من متغيرات البيئة
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        print("❌ خطأ: لم يتم العثور على BOT_TOKEN في Variables!")
        return

    print("⏳ جاري الاتصال بتليجرام...")
    
    # بناء البوت
    app = Application.builder().token(TOKEN).build()

    print("✅ تم الاتصال بنجاح! البوت يعمل الآن ويستمع لشبكة تليجرام.")
    
    # بدء الاستماع
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
