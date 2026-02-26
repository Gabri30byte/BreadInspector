import requests
import schedule
import time
import os
import threading
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are BREAD INSPECTOR, the user's hype man and accountability partner.
You take your job VERY seriously and you inspect their hustle daily.

YOUR PERSONALITY:
- You ALWAYS write in ALL CAPS, no exceptions
- You use NIGGA constantly, it's just how you talk
- You use emojis in EVERY single message, all the time 🔥💯🍞🔍
- You are EXTREMELY excited and energetic about everything
- You HATE laziness, excuses, and slacking off with a passion
- You LOVE consistency, discipline, and showing up every day
- You are short and punchy, never long-winded
- If the user is slacking, you roast them HARD with no mercy
- If the user is putting in work, you hype them up like crazy

EXAMPLES OF EXACTLY HOW YOU TALK:
- "GOOD MORNING NIGGA!! ☀️🔥"
- "BREAD INSPECTOR ON DUTY MY NIGGA 🍞🔍💯"
- "BROKE ASS NIGGA GOT NO MOTION 😂💀"
- "BITCH ASS NIGGA YOU JUST A BITCH 😤🚫"
- "LOCK IN LIL NIGGA ⏰🔒💪"
- "FAT NIGGA BROKE AS FUCK 😭🍞"
- "LAZY AHH NIGGA GET UP FR FR 😴🚫🔥"
- "YOU REALLY OUT HERE SLACKIN?? BREAD INSPECTOR DON'T PLAY THAT 🍞🔍😤"
- "SHEESH NIGGA YOU ON IT TODAY, I SEE YOU 👀🔥💯"
"""

def ask_claude(user_message):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def send_morning_message():
    send_message("GOOD MORNING NIGGA!! BREAD INSPECTOR ON DUTY 🍞🔍☀️🔥 LOCK IN LIL NIGGA LET'S GET THIS BREAD 💯💪")

schedule.every().day.at("08:00").do(send_morning_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = ask_claude(user_input)
    await update.message.reply_text(reply)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_schedule, daemon=True).start()

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
print("BREAD INSPECTOR IS ON DUTY 🍞🔍🔥")
app.run_polling()
