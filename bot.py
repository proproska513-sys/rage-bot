import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SLASH = chr(47)
BOT_TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
U_NAME = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
DIRECT_URL = f"https:{SLASH}{SLASH}t.me{SLASH}{U_NAME}"
BASE_API = f"https:{SLASH}{SLASH}api.telegram.org{SLASH}bot{BOT_TOKEN}{SLASH}"
NFT_CDN = f"https:{SLASH}{SLASH}://fragment.com{SLASH}gift{SLASH}"

TON_PRICE_UAH = 90
UAH_PER_USDT = 45.5
CRYPTO_PAY_TOKEN = ""

# Каталог подарков: название -> (цена в грн, точное имя картинки на Fragment)
NFT_CATALOG = {
    "Plush Pepe #104": (4500, "plushpepe-104.medium.jpg"),
    "Durov's Cap #88": (3200, "durovscap-88.medium.jpg"),
    "Precious Peach #412": (1850, "preciouspeach-412.medium.jpg"),
    "Vintage Cigar #219": (950, "vintagecigar-219.medium.jpg")
}

STATE = {}
ORDERS = {}

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, *args):
        pass

def start_web():
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), PingHandler).serve_forever()

def api(m, d):
    try:
        return requests.post(BASE_API + m, json=d, timeout=25).json()
    except Exception:
        time.sleep(2)
        return None

def crypto_api(m, d):
    if not CRYPTO_PAY_TOKEN:
        return None
    try:
        return requests.post(f"https:{SLASH}{SLASH}pay.crypt.bot{SLASH}api{SLASH}{m}", json=d, headers={"Crypto-Pay-API-Token": CRYPTO_PAY_TOKEN}, timeout=20).json()
    except Exception:
        return None

MAIN_KB = {"keyboard": [[{"text": "⭐️ ТГ Звёзды ⭐️", "style": "primary"}, {"text": "👑 Telegram Premium 👑", "style": "success"}], [{"text": "💎 Купить TON 💎", "style": "primary"}, {"text": "🖼 NFT Маркет 🖼", "style": "success"}], [{"text": "🆘 Поддержка 🆘", "style": "danger"}]], "resize_keyboard": True}
BACK_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
STARS_KB = {"keyboard": [[{"text": "⚡️ 50 Stars — 45 грн ✨", "style": "primary"}, {"text": "⚡️ 100 Stars — 85 грн ✨", "style": "primary"}], [{"text": "🔥 250 Stars — 220 грн ⭐️", "style": "success"}, {"text": "🔥 500 Stars — 410 грн ⭐️", "style": "success"}], [{"text": "👑 1000 Stars — 800 грн 💎", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
PREM_KB = {"keyboard": [[{"text": "💎 3 МЕСЯЦА — 630 ГРН ✨", "style": "primary"}, {"text": "👑 6 МЕСЯЦЕВ — 850 ГРН 🔥", "style": "success"}], [{"text": "👑 1 ГОД — 1520 ГРН 🔥", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
TON_KB = {"keyboard": [[{"text": "💎 1 TON — 90 грн", "style": "primary"}, {"text": "💎 2 TON — 180 грн", "style": "primary"}], [{"text": "🔥 5 TON — 450 грн", "style": "success"}, {"text": "👑 10 TON — 900 грн", "style": "success"}], [{"text": "✍️ Ввести своё количество TON", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
NFT_KB = {"keyboard": [[{"text": "📂 Каталог NFT в наличии", "style": "success"}], [{"text": "🔗 Прислать ссылку на свой NFT", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
MAIN_TEXT = f"⚡️ <b>RAGE STORE // DIGITAL MARKET</b>\nШоп цифровых активов с автовыдачей 24/7.\n\n⭐️ <b>Stars</b> • 👑 <b>Premium</b> • 💎 <b>TON</b> • 🖼 <b>NFT</b>\n🆘 Админ: @{U_NAME}\n⬇️ <i>Выбери раздел в меню внизу</i> ⬇️"

def send(cid, text, kb):
    api("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML", "reply_markup": kb})

def send_photo(cid, photo_url, caption, kb):
    res = api("sendPhoto", {"chat_id": cid, "photo": photo_url, "caption": caption, "parse_mode": "HTML", "reply_markup": kb})
    if not res or not res.get("ok"):
        send(cid, caption, kb)

def pay_kb(oid=None, url=None):
    rows = [[{"text": "⚡️ ОПЛАТИТЬ АВТОМАТОМ (CRYPTOBOT)", "url": url, "style": "success"}], [{"text": "🔄 ПРОВЕРИТЬ ОПЛАТУ", "callback_data": f"chk:{oid}", "style": "primary"}]] if url and oid else []
    rows.extend([[{"text": f"✅ ОПЛАТИЛ НА КАРТУ / ЧЕК (@{U_NAME})", "url": DIRECT_URL, "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "callback_data": "to_main", "style": "danger"}]])
    return {"inline_keyboard": rows}

def create_order(cid, title, price, target):
    oid = f"{cid}_{int(time.time())}"
    res = crypto_api("createInvoice", {"asset": "USDT", "amount": str(round(price / UAH_PER_USDT, 2)), "description": f"{title} -> {target}"})
    inv = res.get("result", {}) if res and res.get("ok") else {}
    ORDERS.update({oid: {"cid": cid, "title": title, "price": price, "target": target, "inv_id": inv.get("invoice_id"), "done": False}})
    send(cid, f"💳 <b>ЗАКАЗ // RAGE STORE</b>\n📦 Товар: <b>{title}</b>\n🎯 Получатель: <code>{target}</code>\n💰 К оплате: <b>{price} грн</b>\n\nКарта (UAH): <code>4874 0700 2382 7379</code>\nПосле оплаты нажми кнопку ниже 👇", pay_kb(oid, inv.get("bot_invoice_url")))

def send_nft_catalog(cid):
    for name, info in NFT_CATALOG.items():
        price, img_file = info
        kb = {"inline_keyboard": [[{"text": f"🛒 Купить {name} — {price} грн", "callback_data": f"buy_nft:{name}", "style": "success"}]]}
        send_photo(cid, NFT_CDN + img_file, f"🖼 <b>{name}</b>\n💰 Цена: <b>{price} грн</b>\n⚡️ Моментальная передача на @username", kb)
    send(cid, "⬆️ Выбери нужный подарок выше или нажми <b>«🔗 Прислать ссылку на свой NFT»</b> 👇", NFT_KB)

def handle(upd):
    if "callback_query" in upd:
        cb = upd.get("callback_query", {})
        cid = cb.get("message", {}).get("chat", {}).get("id")
        data = cb.get("data", "")
        api("answerCallbackQuery", {"callback_query_id": cb.get("id")})
        if data == "to_main":
            STATE.pop(cid, None)
            send(cid, MAIN_TEXT, MAIN_KB)
        elif data.startswith("buy_nft:"):
            _, name = data.split(":", 1)
            info = NFT_CATALOG.get(name, (1000, ""))
            STATE.update({cid: {"step": "user", "title": f"NFT: {name}", "price": info}})
            send(cid, f"🖼 Выбран <b>{name}</b>. Введи свой <b>@username</b>:", BACK_KB)
        elif data.startswith("chk:"):
            _, oid = data.split(":", 1)
            o = ORDERS.get(oid)
            res = crypto_api("getInvoices", {"invoice_ids": str(o.get("inv_id"))}) if o else None
            items = res.get("result", {}).get("items", []) if res and res.get("ok") else []
            if o and next(iter(items), {}).get("status") == "paid":
                o.update({"done": True})
                send(cid, f"🎉 <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n📦 <b>{o.get('title')}</b> -> <code>{o.get('target')}</code>", MAIN_KB)
            else:
                send(cid, "⏳ Оплата ещё не поступила.", pay_kb(oid, None))
        return

    msg = upd.get("message")
    if not msg:
        return
    cid = msg.get("chat", {}).get("id")
    text = msg.get("text", "").strip()
    if text.startswith("/start") or "главное меню" in text:
        STATE.pop(cid, None)
        send(cid, MAIN_TEXT, MAIN_KB)
    elif cid in STATE:
        st = STATE.get(cid, {})
        step = st.get("step")
        if step == "user":
            STATE.pop(cid, None)
            create_order(cid, st.get("title"), st.get("price"), text)
        elif step == "ton":
            try:
                q = float(text.replace(",", "."))
                p = round(q * TON_PRICE_UAH)
                STATE.update({cid: {"step": "user", "title": f"{q} TON", "price": p}})
                send(cid, f"💎 {q} TON = <b>{p} грн</b>. Введи адрес TON-кошелька:", BACK_KB)
            except Exception:
                send(cid, "⚠️ Введи число, например: <code>2.5</code>", BACK_KB)
        elif step == "nft_link":
            STATE.update({cid: {"step": "nft_price", "link": text}})
            slug = text.rstrip(SLASH).split(SLASH)[-1].lower()
            if "nft" in text:
                send_photo(cid, f"{NFT_CDN}{slug}.medium.jpg", "💰 Введи цену этого NFT в грн:", BACK_KB)
            else:
                send(cid, "💰 Введи цену этого NFT в грн:", BACK_KB)
        elif step == "nft_price":
            d = "".join(c for c in text if c.isdigit())
            STATE.update({cid: {"step": "user", "title": f"NFT ({st.get('link')})", "price": int(d) if d else 1000}})
            send(cid, "👤 Введи свой <b>@username</b> для получения NFT:", BACK_KB)
    elif "Звёзды" in text:
        send(cid, "⭐️ Выбери пакет звёзд:", STARS_KB)
    elif "Premium" in text:
        send(cid, "👑 Выбери срок подписки:", PREM_KB)
    elif "Купить TON" in text:
        send(cid, f"💎 Курс: <b>1 TON = {TON_PRICE_UAH} грн</b>. Выбери пакет:", TON_KB)
    elif "Ввести своё количество TON" in text:
        STATE.update({cid: {"step": "ton"}})
        send(cid, "✍️ Введи нужное количество TON:", BACK_KB)
    elif "NFT Маркет" in text:
        send(cid, "🖼 Выбери NFT из каталога или пришли ссылку:", NFT_KB)
    elif "Каталог NFT" in text:
        send_nft_catalog(cid)
    elif "Прислать ссылку на свой NFT" in text:
        STATE.update({cid: {"step": "nft_link"}})
        send(cid, "🔗 Пришли ссылку на нужный NFT:", BACK_KB)
    elif "Поддержка" in text:
        send(cid, f"🆘 Поддержка @{U_NAME} (9:00–22:30)", {"inline_keyboard": [[{"text": f"🆘 НАПИСАТЬ (@{U_NAME})", "url": DIRECT_URL, "style": "danger"}]]})
    elif "—" in text:
        l, r = text.split("—", 1)
        p = int("".join(c for c in r if c.isdigit()))
        STATE.update({cid: {"step": "user", "title": l.strip(), "price": p}})
        ask = "адрес TON-кошелька" if "TON" in text else "<b>@username</b> получателя"
        send(cid, f"✅ Выбрано: <b>{l.strip()}</b> ({p} грн)\nВведи {ask}:", BACK_KB)

def main():
    threading.Thread(target=start_web, daemon=True).start()
