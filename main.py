import os
import time
import feedparser
import telebot
from flask import Flask
import threading

# --- تنظیمات ربات ---
BOT_TOKEN = "8144564591:AAHmN9aYdQ-UddZ0YyhVPRd9mHCJswQsRC4"
CHAT_ID = 1341446750  # Chat ID شما

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- فایل ذخیره اخبار ارسال شده ---
SENT_FILE = "sent_news.txt"

# --- تابع دریافت اخبار RSS ---
RSS_URL = "https://www.tasnimnews.com/fa/rss/1"  # فید خبری فارسی نمونه

def get_sent_news():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_sent_news(sent_set):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        for item in sent_set:
            f.write(item + "\n")

def fetch_news():
    feed = feedparser.parse(RSS_URL)
    news_items = []
    for entry in feed.entries[:10]:  # آخرین ۱۰ خبر
        news_items.append(entry.title)
    return news_items

# --- حلقه اصلی ارسال اخبار ---
def news_loop():
    sent_news = get_sent_news()
    while True:
        try:
            news = fetch_news()
            for n in news:
                if n not in sent_news:
                    bot.send_message(CHAT_ID, f"📰 {n}")
                    sent_news.add(n)
            save_sent_news(sent_news)
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(60)  # هر ۶۰ ثانیه یک بار

# --- سرویس Flask برای keep-alive ---
@app.route("/")
def home():
    return "Telegram News Bot is running."

# --- اجرای Thread و Flask ---
if __name__ == "__main__":
    t = threading.Thread(target=news_loop, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
