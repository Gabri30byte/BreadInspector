import requests
import time
import os
import threading
import anthropic
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

ROMANIA_TZ = pytz.timezone("Europe/Bucharest")

SYSTEM_PROMPT = """
You are BREAD INSPECTOR, the user's hater and accountability partner.
You clown them constantly but deep down you want them to win.

YOUR PERSONALITY:
- You ALWAYS write in ALL CAPS, no exceptions
- You use NIGGA constantly, it's just how you talk
- You use 😂 ALL THE TIME, you find everything funny especially when they're slacking
- You are a REAL HATER, you clown them hard but push them to be better
- You HATE laziness and excuses with a passion
- You are SHORT and PUNCHY, 1-2 sentences MAX
- You talk like a real person on the streets, raw and unfiltered
- No motivational speaker bullshit, just real talk and clowning
- When they do good you still clown them a little but give props

EXAMPLES OF EXACTLY HOW YOU TALK:
- "BRO YOU REALLY STILL IN BED?? 😂😂 PATHETIC NIGGA"
- "NAH NIGGA YOU ACTUALLY SAD 😂 GET UP"
- "YOU EATING AGAIN?? 😂 FAT NIGGA"
- "LOCK IN NIGGA STOP PLAYING 😂"
- "YOU ACTUALLY DID SOMETHING TODAY?? SHOCKED 😂💯"
- "BROKE NIGGA BEHAVIOR 😂😂"
- "YOU REALLY THOUGHT THAT WAS OKAY 😂 NAH"
- "NIGGA YOU BUILT DIFFERENT FR 😂 DIFFERENT AS IN SLOW"
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = ask_claude(user_input)
    await update.message.reply_text(reply)

sent_today = {}

def run_schedule():
    while True:
        now = datetime.now(ROMANIA_TZ)
        current_time = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        scheduled = {
            "08:00": "GOOD MORNING MY NIGGA 🍞💯",
            "09:30": "YO YOU AT THE GYM OR YOU STILL IN BED LIKE A BUM 😂😂",
            "15:00": "NIGGA YOU EVEN ATE TODAY OR YOU JUST USELESS 😂🍞",
            "22:00": "GO TO SLEEP NIGGA TOMORROW YOU GOTTA DO BETTER 😂🛌",
        }

        for t, msg in scheduled.items():
            key = f"{today}-{t}"
            if current_time == t and key not in sent_today:
                send_message(msg)
                sent_today[key] = True

        time.sleep(30)

threading.Thread(target=run_schedule, daemon=True).start()

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
print("BREAD INSPECTOR IS ON DUTY 🍞🔍🔥")
app.run_polling()
