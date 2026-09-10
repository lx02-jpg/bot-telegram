import telebot
import time
import requests
from requests.adapters import HTTPAdapter                                        from urllib3.util.retry import Retry
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
                                                                                 TOKEN = "8886956439:AAEUJWuQSj_YvTw1_H7GVjGEnQXoQRH6jKs"                         FILE_LINKS = "links.txt"
                                                                                 # Konfigurasi Session agar tahan banting dari koneksi putus                      session = requests.Session()                                                     retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))                                                                                                       # Inject session ke TeleBot                                                      telebot.apihelper.CUSTOM_REQUEST_SENDER = None                                   bot = telebot.TeleBot(TOKEN)                                                     
def read_links():                                                                    try:
        with open(FILE_LINKS, 'r', encoding='utf-8') as file:                                return [line.strip() for line in file if line.strip()]                   except FileNotFoundError:
        return None                                                                                                                                               @bot.message_handler(commands=['links'])
def send_menu_links(message):
    lines = read_links()

    if lines is None:                                                                    bot.reply_to(message, "❌ File `links.txt` tidak ditemukan.")
        return
                                                                                     if not lines:
        bot.reply_to(message, "⚠️ Belum ada link yang tersimpan di file `links.txt`.")                                                                                     return

    markup = InlineKeyboardMarkup()                                              
    for index, line in enumerate(lines):
        if "|" in line:                                                                      judul, _ = line.split("|", 1)
            teks_tombol = judul.strip()                                                  else:
            teks_tombol = f"Link Kategori {index + 1}"

        tombol = InlineKeyboardButton(text=teks_tombol, callback_data=f"getlink_{index}")
        markup.add(tombol)

    bot.send_message(
        message.chat.id,
        "📂 **Silakan pilih kategori link yang ingin Anda ambil:**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("getlink_"))
def handle_button_click(call):
    try:
        bot.answer_callback_query(call.id, "Memuat link...")
    except Exception:
        pass

    lines = read_links()
    if not lines:
        bot.send_message(call.message.chat.id, "❌ File kosong atau tidak ditemukan!")
        return

    try:
        index_dipilih = int(call.data.split("_")[1])
        line_dipilih = lines[index_dipilih]

        if "|" in line_dipilih:
            _, url = line_dipilih.split("|", 1)
            link_tujuan = url.strip()
        else:
            link_tujuan = line_dipilih

        teks_balasan = f"PhisbyTransaksi - Url ({link_tujuan})"
        bot.send_message(call.message.chat.id, teks_balasan, disable_web_page_preview=True)

    except IndexError:
        bot.send_message(call.message.chat.id, "❌ Link sudah tidak tersedia.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Terjadi error: {str(e)}")

if __name__ == "__main__":
    print("=== BOT LINKS DIAKTIFKAN ===")

    while True:
        try:
            bot.delete_webhook(drop_pending_updates=True)
            # Menggunakan polling standar tanpa threading berlebih agar tidak crash di Termux
            bot.polling(non_stop=True, interval=2, timeout=20)
        except Exception as e:
            time.sleep(3)