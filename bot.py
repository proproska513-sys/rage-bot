import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

SLASH = chr(47)
BOT_TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
U_NAME = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
DIRECT_URL = f"https:{SLASH}{SLASH}t.me{SLASH}{U_NAME}"
BASE_API = f"https:{SLASH}{SLASH}api.telegram.org{SLASH}bot{BOT_TOKEN}{SLASH}"

TON_PRICE_UAH = 90
UAH_PER_USDT = 45.5
CRYPTO_PAY_TOKEN = ""

NFT_CATALOG = {
    "Plush Pepe #104": 4500,
    "Durov's Cap #88": 3200,
    "Precious Peach #412": 1850,
    "Vintage Cigar #219": 950
}

STATE = {}
ORDERS = {}

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RAGE STORE ONLINE 24/7")
    def log_message(self, format, *args):
        pass

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

def api(method, data):
    try:
        return requests.post(BASE_API + method, json=data, timeout=25).json()
    except Exception:
        time.sleep(2)
        return None

def crypto_api(method, data):
    if not CRYPTO_PAY_TOKEN:
        return None
    url = f"https:{SLASH}{SLASH}pay.crypt.bot{SLASH}api{SLASH}{method}"
    try:
        return requests.post(url, json=data, headers={"Crypto-Pay-API-Token": CRYPTO_PAY_TOKEN}, timeout=20).json()
    except Exception:
        return None

MAIN_KB = {
    "keyboard": [
        [{"text": "⭐️ ТГ Звёзды ⭐️", "style": "primary"}, {"text": "👑 Telegram Premium 👑", "style": "success"}],
        [{"text": "💎 Купить TON 💎", "style": "primary"}, {"text": "🖼 NFT Маркет 🖼", "style": "success"}],
        [{"text": "🆘 Поддержка 🆘", "style": "danger"}]
    ],
    "resize_keyboard": True
}

BACK_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}

STARS_KB = {
    "keyboard": [
        [{"text": "⚡️ 50 Stars — 45 грн ✨", "style": "primary"}, {"text": "⚡️ 100 Stars — 85 грн ✨", "style": "primary"}],
        [{"text": "🔥 250 Stars — 220 грн ⭐️", "style": "success"}, {"text": "🔥 500 Stars — 410 грн ⭐️", "style": "success"}],
        [{"text": "👑 1000 Stars — 800 грн 💎", "style": "success"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

PREM_KB = {
    "keyboard": [
        [{"text": "💎 3 МЕСЯЦА — 630 ГРН ✨", "style": "primary"}, {"text": "👑 6 МЕСЯЦЕВ — 850 ГРН 🔥", "style": "success"}],
        [{"text": "👑 1 ГОД — 1520 ГРН 🔥", "style": "success"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

TON_KB = {
    "keyboard": [
        [{"text": "💎 1 TON — 90 грн", "style": "primary"}, {"text": "💎 2 TON — 180 грн", "style": "primary"}],
        [{"text": "🔥 5 TON — 450 грн", "style": "success"}, {"text": "👑 10 TON — 900 грн", "style": "success"}],
        [{"text": "✍️ Ввести своё количество TON", "style": "primary"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

NFT_KB = {
    "keyboard": [
        [{"text": "📂 Каталог NFT в наличии", "style": "success"}],
        [{"text": "🔗 Прислать ссылку на свой NFT", "style": "primary"}],
        [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]
    ],
    "resize_keyboard": True
}

def nft_catalog_inline():
    rows = [[{"text": f"🖼 {k} — {v} грн", "callback_data": f"buy_nft:{k}", "style": "success"}] for k, v in NFT_CATALOG.items()]
    rows.append([{"text": "🔗 Прислать ссылку на другой NFT", "callback_data": "custom_nft", "style": "primary"}])
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "to_main", "style": "danger"}])
    return {"inline_keyboard": rows}

def pay_inline(order_id=None, pay_url=None):
    rows = []
    if pay_url and order_id:
        rows.append([{"text": "⚡️ ОПЛАТИТЬ АВТОМАТОМ (CRYPTOBOT) ⚡️", "url": pay_url, "style": "success"}])
        rows.append([{"text": "🔄 ПРОВЕРИТЬ ОПЛАТУ И ПОЛУЧИТЬ", "callback_data": f"chk:{order_id}", "style": "primary"}])
    rows.append([{"text": "✅ ОПЛАТИЛ НА КАРТУ / СКИНУТЬ ЧЕК (@" + U_NAME + ")", "url": DIRECT_URL, "style": "success"}])
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "to_main", "style": "danger"}])
    return {"inline_keyboard": rows}

MAIN_TEXT = (
    "⚡️ <b>RAGE STORE // DIGITAL MARKET</b>\n"
    "Твой быстрый шоп цифровых активов в Telegram с автовыдачей 24/7.\n\n"
    "⭐️ <b>Telegram Stars</b> — моментально по @username\n"
    "👑 <b>Telegram Premium</b> — 3 / 6 / 12 месяцев\n"
    "💎 <b>TON</b> — покупка любого количества за грн\n"
    "🖼 <b>NFT</b> — каталог подарков и покупка по ссылке\n\n"
    "🆘 Администратор: @" + U_NAME + "\n"
    "⬇️ <i>Выбери нужный раздел в меню внизу</i> ⬇️"
)

def send(cid, text, kb):
    api("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML", "reply_markup": kb})

def create_order(cid, title, price_uah, target):
    oid = f"{cid}_{int(time.time())}"
    pay_url = None
    inv_id = None
    if CRYPTO_PAY_TOKEN:
        usdt_amount = round(price_uah / UAH_PER_USDT, 2)
        res = crypto_api("createInvoice", {"asset": "USDT", "amount": str(usdt_amount), "description": f"{title} -> {target}"})
        if res and res.get("ok"):
            inv_data = res.get("result", {})
            inv_id = inv_data.get("invoice_id")
            pay_url = inv_data.get("bot_invoice_url")
    ORDERS[oid] = {"cid": cid, "title": title, "price": price_uah, "target": target, "inv_id": inv_id, "done": False}
    text = f"💳 <b>ОФОРМЛЕНИЕ ЗАКАЗА // RAGE STORE</b>\n📦 Товар: <b>{title}</b>\n🎯 Получатель: <code>{target}</code>\n💰 К оплате: <b>{price_uah} грн</b>\n\nПереведи <b>{price_uah} грн</b> на карту:\n<code>4874 0700 2382 7379</code>\nи отправь чек @" + U_NAME + " по кнопке ниже 👇"
    send(cid, text, pay_inline(oid, pay_url))

def auto_deliver(order):
    order["done"] = True
    c_id = order.get("cid")
    o_title = order.get("title")
    o_target = order.get("target")
    send(c_id, f"🎉 <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n📦 Товар: <b>{o_title}</b>\n🎯 Получатель: <code>{o_target}</code>\n\nСпасибо за покупку в <b>RAGE STORE</b>! ⚡️", MAIN_KB)

def parse_pack(text):
    left, right = text.split("—", 1)
    price = int("".join(c for c in right if c.isdigit()))
    return left.strip(), price

def handle_cb(cb):
    msg_obj = cb.get("message", {})
    chat_obj = msg_obj.get("chat", {})
    cid = chat_obj.get("id")
    data = cb.get("data", "")
    api("answerCallbackQuery", {"callback_query_id": cb.get("id")})
    if data == "to_main":
        STATE.pop(cid, None)
        send(cid, MAIN_TEXT, MAIN_KB)
    elif data.startswith("buy_nft:"):
        _, nft_name = data.split(":", 1)
        price = NFT_CATALOG.get(nft_name, 1000)
        STATE[cid] = {"step": "nft_user", "title": f"NFT: {nft_name}", "price": price}
        send(cid, f"🖼 Выбран <b>{nft_name}</b> ({price} грн).\n\nВведи свой <b>@username</b>, куда отправить NFT:", BACK_KB)
    elif data == "custom_nft":
        STATE[cid] = {"step": "nft_link"}
        send(cid, "🔗 <b>Пришли ссылку на нужный NFT</b> (Getgems / Fragment / Telegram):", BACK_KB)
    elif data.startswith("chk:"):
        _, oid = data.split(":", 1)
        order = ORDERS.get(oid)
        if not order:
            send(cid, "⚠️ Заказ не найден.", MAIN_KB)
        elif order.get("done"):
            send(cid, "✅ Заказ уже выдан!", MAIN_KB)
        else:
            res = crypto_api("getInvoices", {"invoice_ids": str(order.get("inv_id"))})
            items = res.get("result", {}).get("items", []) if res and res.get("ok") else []
            first_item = next(iter(items), {})
            if first_item.get("status") == "paid":
                auto_deliver(order)
            else:
                send(cid, "⏳ Оплата ещё не поступила. Попробуй через минуту.", pay_inline(oid, None))

def handle_state(cid, text):
    st = STATE.get(cid, {})
    step = st.get("step")
    if step in ("target_user", "nft_user"):
        STATE.pop(cid, None)
        create_order(cid, st.get("title"), st.get("price"), text)
    elif step == "ton_amount":
        try:
            qty = float(text.replace(",", "."))
            if qty < 0.5:
                send(cid, "⚠️ Минимум — от <b>0.5 TON</b>. Введи число ещё раз:", BACK_KB)
                return
            price_uah = round(qty * TON_PRICE_UAH)
            STATE[cid] = {"step": "target_user", "title": f"{qty} TON", "price": price_uah}
            send(cid, f"💎 Количество: <b>{qty} TON</b>\n💰 Стоимость: <b>{price_uah} грн</b>\n\nТеперь введи свой <b>адрес TON-кошелька</b>:", BACK_KB)
        except ValueError:
            send(cid, "⚠️ Введи количество цифрой, например: <code>2.5</code>", BACK_KB)
    elif step == "nft_link":
        STATE[cid] = {"step": "nft_custom_price", "link": text}
        send(cid, "💰 Введи стоимость этого NFT в <b>грн</b>:", BACK_KB)
    elif step == "nft_custom_price":
        digits = "".join(c for c in text if c.isdigit())
        price_uah = int(digits) if digits else 1000
        nft_url = st.get("link", "")
        STATE[cid] = {"step": "nft_user", "title": f"NFT по ссылке ({nft_url})", "price": price_uah}
        send(cid, "👤 Введи свой <b>@username</b>, куда передать NFT после оплаты:", BACK_KB)

def handle_menu(cid, text):
    if "Звёзды" in text:
        send(cid, "⭐️ <b>TELEGRAM STARS</b>\nВыбери нужный пакет звёзд внизу 👇", STARS_KB)
    elif "Premium" in text:
        send(cid, "👑 <b>TELEGRAM PREMIUM</b>\nВыбери срок подписки внизу 👇", PREM_KB)
    elif "Купить TON" in text:
        send(cid, f"💎 <b>RAGE STORE // ПОКУПКА TON</b>\nКурс: <b>1 TON = {TON_PRICE_UAH} грн</b>\n\nВыбери пакет или нажми <b>«Ввести своё количество TON»</b> 👇", TON_KB)
    elif "Ввести своё количество TON" in text:
