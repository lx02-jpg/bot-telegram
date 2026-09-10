import telebot
import os
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Server dummy agar Render Web Service (Free) tidak mati
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Jalankan server dummy di thread terpisah
Thread(target=run_flask).start()

# Kode Utama Bot
TOKEN = "8886956439:AAEwKEOs6QqFsZK8llRg5o28We0QsIoFVtU"
bot = telebot.TeleBot(TOKEN)
FILE_LINKS = "links.txt"

def read_links():
    try:
        with open(FILE_LINKS, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return None

@bot.message_handler(commands=['links'])
def send_menu_links(message):
    lines = read_links()
    if not lines:
        bot.reply_to(message, "❌ File links.txt kosong atau tidak ditemukan.")
        return

    markup = InlineKeyboardMarkup()
    for index, line in enumerate(lines):
        teks_tombol = line.split("|")[0].strip() if "|" in line else f"Link {index + 1}"
        markup.add(InlineKeyboardButton(text=teks_tombol, callback_data=f"getlink_{index}"))

    bot.send_message(message.chat.id, "📂 **Silakan pilih kategori link:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("getlink_"))
def handle_button_click(call):
    try:
        bot.answer_callback_query(call.id, "Memuat link...")
    except Exception:
        pass

    lines = read_links()
    if lines:
        try:
            idx = int(call.data.split("_")[1])
            line = lines[idx]
            link = line.split("|")[1].strip() if "|" in line else line
            bot.send_message(call.message.chat.id, f"PhisbyTransaksi - Url ({link})", disable_web_page_preview=True)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=== BOT DIAKTIFKAN ===")
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
