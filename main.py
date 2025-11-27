import os
import time
import telebot

# --- تنظیمات ربات ---
BOT_TOKEN = os.environ.get("8144564591:AAHmN9aYdQ-UddZ0YyhVPRd9mHCJswQsRC4")
CHAT_ID = os.environ.get("1341446750")  # عدد chat_id شما

bot = telebot.TeleBot(BOT_TOKEN)

# --- تابع دریافت اخبار نمونه ---
def get_news():
    # جایگزین با API واقعی توییتر یا RSS کنید
    return ["خبر نمونه ۱", "خبر نمونه ۲", "خبر نمونه ۳"]

# --- متغیر ذخیره خبرهای ارسال شده ---
last_sent = set()

# --- حلقه اصلی Polling ---
while True:
    try:
        news = get_news()
        for n in news:
            if n not in last_sent:
                bot.send_message(CHAT_ID, n)
                last_sent.add(n)
    except Exception as e:
        print("Error:", e)
    time.sleep(60)