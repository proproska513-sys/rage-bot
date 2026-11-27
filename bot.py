import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

SLASH = chr(47)
BOT_TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
U_NAME = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
DIRECT_URL = f"https:{SLASH}{SLASH}t.me{SLASH}{U_NAME}"

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RAGE STORE IS ONLINE 24/7")
    def log_message(self, format, *args):
        pass

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    server.serve_forever()

def api(method, data):
    url = f"https:{SLASH}{SLASH}api.telegram.org{SLASH}bot{BOT_TOKEN}{SLASH}{method}"
    try:
        return requests.post(url, json=data, timeout=25).json()
    except Exception:
        time.sleep(2)
        return None

MAIN_KB = {
    "keyboard": [
        [{"text": "⭐️ ТГ Звёзды ⭐️", "style": "primary"}, {"text": "👑 Telegram Premium 👑", "style": "success"}],
        [{"text": "💎 Купить TON 💎", "style": "primary"}, {"text": "🖼 NFT Маркет 🖼", "style": "success"}],
        [{"text": "🆘 Поддержка 🆘", "style": "danger"}]
    ],
    "resize_keyboard": True
}

STARS_KB = {
    "keyboard": [
        [{"text": "⚡️ 50 Stars — 45 грн ✨", "style": "primary"}, {"text": "⚡️ 100 Stars — 80 грн ✨", "style": "primary"}],
        [{"text": "🔥 250 Stars — 220 грн ⭐️", "style": "success"}, {"text": "🔥 500 Stars — 410 грн ⭐️", "style": "success"}],
        [{"text": "👑 1000 Stars — 800 грн 💎", "style": "success"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

PREM_KB = {
    "keyboard": [
        [{"text": "💎 1 МЕСЯЦ — 120 ГРН ✨", "style": "primary"}, {"text": "💎 3 МЕСЯЦА — 500 ГРН ✨", "style": "primary"}],
        [{"text": "👑 6 МЕСЯЦЕВ — 700 ГРН 🔥", "style": "success"}, {"text": "👑 1 ГОД — 1100 ГРН 🔥", "style": "success"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

def link_kb(btn_text, style):
    return {"inline_keyboard": [
        [{"text": btn_text, "url": DIRECT_URL, "style": style}],
        [{"text": "⬅️ В главное меню 🏠", "callback_data": "to_main", "style": "danger"}]
    ]}

TON_KB = link_kb("💎 КУПИТЬ TON (@" + U_NAME + ") 💎", "primary")
NFT_KB = link_kb("🖼 КУПИТЬ / ПРОДАТЬ NFT (@" + U_NAME + ") 🖼", "success")
SUP_KB = link_kb("🆘 НАПИСАТЬ В ПОДДЕРЖКУ (@" + U_NAME + ") 🆘", "danger")
PAY_KB = link_kb("✅ Я ОПЛАТИЛ / СКИНУТЬ ЧЕК (@" + U_NAME + ") ✅", "success")

MAIN_TEXT = (
    "⚡️ <b>RAGE STORE // DIGITAL MARKET</b>\n"
    "Твой быстрый шоп цифровых активов в Telegram без переплат и лишнего шума.\n\n"
    "⭐️ <b>Telegram Stars</b> — моментально по @username\n"
    "👑 <b>Telegram Premium</b> — подписка на любой срок\n"
    "💎 <b>TON</b> — покупка и пополнение кошелька за грн\n"
    "🖼 <b>NFT</b> — покупка, продажа и обмен подарков TG\n\n"
    "💳 Оплата напрямую на карту (UAH)\n"
    "🆘 Администратор: @" + U_NAME + "\n\n"
    "⬇️ <i>Выбери нужный раздел в меню внизу</i> ⬇️"
)

PACKAGE_KEYS = ("50 Stars", "100 Stars", "250 Stars", "500 Stars", "1000 Stars", "1 МЕСЯЦ", "3 МЕСЯЦА", "6 МЕСЯЦЕВ", "1 ГОД")

def send(cid, text, kb):
    api("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML", "reply_markup": kb})

def handle(upd):
    if "callback_query" in upd:
        cb = upd["callback_query"]
        api("answerCallbackQuery", {"callback_query_id": cb["id"]})
        if cb.get("data") == "to_main":
            send(cb["message"]["chat"]["id"], MAIN_TEXT, MAIN_KB)
        return

    msg = upd.get("message")
    if not msg:
        return
    cid = msg["chat"]["id"]
    text = msg.get("text", "").strip()

    if text.startswith("/start") or "главное меню" in text:
        send(cid, MAIN_TEXT, MAIN_KB)
    elif "Звёзды" in text:
        send(cid, "⭐️ <b>TELEGRAM STARS</b>\nВыбери пакет звёзд внизу 👇", STARS_KB)
    elif "Premium" in text:
        send(cid, "👑 <b>TELEGRAM PREMIUM</b>\nВыбери срок подписки внизу 👇", PREM_KB)
    elif "Купить TON" in text:
        send(cid, "💎 <b>RAGE STORE // ПОКУПКА TON</b>\nБыстрое пополнение кошелька за грн (UAH) без бирж.\n\n🩸 От 1 TON • Зачисление за 2–5 минут\n🩸 Оплата на карту (UAH)\n\nДля покупки пиши @" + U_NAME + " или жми кнопку ниже 👇", TON_KB)
    elif "NFT Маркет" in text:
        send(cid, "🖼 <b>RAGE STORE // NFT & ПОДАРКИ TG</b>\nПокупка, продажа и обмен коллекционных NFT-подарков.\n\n🩸 Выкуп ваших NFT за грн (UAH) или TON\n🩸 Продажа редких коллекций\n\nДля сделки пиши @" + U_NAME + " по кнопке ниже 👇", NFT_KB)
    elif "Поддержка" in text:
        send(cid, "🆘 <b>ПОДДЕРЖКА RAGE STORE</b>\n⏰ График работы: с 9:00 по 22:30\n\nПо всем вопросам пиши @" + U_NAME + " 👇", SUP_KB)
    elif any(k in text for k in PACKAGE_KEYS):
        send(cid, f"💳 <b>ОПЛАТА ЗАКАЗА // RAGE STORE</b>\nТовар: <b>{text}</b>\n\nКарта для перевода (нажмите, чтобы скопировать):\n<code>4874 0700 2382 7379</code>\n\nПосле оплаты скинь чек + @username администратору @" + U_NAME + " по кнопке ниже 👇", PAY_KB)

def main():
    threading.Thread(target=start_web_server, daemon=True).start()
    api("deleteWebhook", {"drop_pending_updates": True})
    print("RAGE STORE 24/7 ЗАПУЩЕН!", flush=True)
    offset = 0
    while True:
        res = api("getUpdates", {"offset": offset, "timeout": 20})
        if res and res.get("ok"):
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                handle(upd)

if __name__ == "__main__":
    main()
# END




