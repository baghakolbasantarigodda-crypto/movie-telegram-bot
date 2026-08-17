import os
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ.get("BOT_TOKEN")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome!\n\nMovie ya Web Series ka naam bhejiye 🔎"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()

    await update.message.reply_text(
        f"🔎 Searching for: {name}\n\n"
        "⏳ Search system abhi kaam kar raha hai..."
    )

threading.Thread(target=run_server, daemon=False).start()

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, search)
)

print("Telegram bot starting...")
app.run_polling()
