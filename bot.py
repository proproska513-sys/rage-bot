import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SLASH = chr(47)
BOT_TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
U_NAME = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
DIRECT_URL = f"https:{SLASH}{SLASH}t.me{SLASH}{U_NAME}"
BASE_API = f"https:{SLASH}{SLASH}api.telegram.org{SLASH}bot{BOT_TOKEN}{SLASH}"

TON_PRICE_UAH = 90
UAH_PER_USDT = 45.5
CRYPTO_PAY_TOKEN = ""

# --- ВСЕ МИШКИ И СТАНДАРТНЫЕ ПОДАРКИ TELEGRAM (ЦЕНА В ГРН) ---
GIFTS_BASIC = {
    "🧸 Плюшевый мишка (15 ⭐)": 20,
    "💝 Сердце в коробке (15 ⭐)": 20,
    "🌹 Красная роза (25 ⭐)": 30,
    "🎁 Подарочная коробка (25 ⭐)": 30,
    "🍾 Шампанское (50 ⭐)": 55,
    "🎂 Праздничный торт (50 ⭐)": 55,
    "💐 Букет цветов (50 ⭐)": 55,
    "🚀 Ракета (50 ⭐)": 55,
    "🏆 Кубок чемпиона (100 ⭐)": 105,
    "💍 Кольцо с бриллиантом (100 ⭐)": 105,
    "💎 Бриллиант (100 ⭐)": 105
}

# --- КОЛЛЕКЦИОННЫЕ NFT-ПОДАРКИ И МИШКИ (ЦЕНА В ГРН) ---
GIFTS_NFT = {
    "🧸 Toy Bear (Мишка NFT)": 1450,
    "🐸 Plush Pepe (Пепе NFT)": 4500,
    "🧢 Durov's Cap (Кепка Дурова)": 3200,
    "🍑 Precious Peach (Персик)": 1850,
    "🚬 Vintage Cigar (Сигара)": 950,
    "📅 Homemade Cake (Торт NFT)": 420,
    "🍭 Lol Pop (Леденец NFT)": 350,
    "🍬 Candy Cane (Карамель NFT)": 380,
    "🎃 Scared Cat (Кот NFT)": 1200,
    "🔮 Crystal Ball (Шар NFT)": 890,
    "🎩 Top Hat (Цилиндр NFT)": 750,
    "⌚️ Swiss Watch (Часы NFT)": 1600,
    "💍 Diamond Ring (Кольцо NFT)": 1100,
    "🍸 Berry Box (Ягоды NFT)": 640,
    "🧿 Evil Eye (Оберег NFT)": 520,
    "🍷 Spiced Wine (Вино NFT)": 490
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

MAIN_KB = {"keyboard": [[{"text": "⭐️ ТГ Звёзды ⭐️", "style": "primary"}, {"text": "👑 Telegram Premium 👑", "style": "success"}], [{"text": "💎 Купить TON 💎", "style": "primary"}, {"text": "🎁 Подарки и NFT 🧸", "style": "success"}], [{"text": "🆘 Поддержка 🆘", "style": "danger"}]], "resize_keyboard": True}
BACK_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
STARS_KB = {"keyboard": [[{"text": "⚡️ 50 Stars — 45 грн ✨", "style": "primary"}, {"text": "⚡️ 100 Stars — 85 грн ✨", "style": "primary"}], [{"text": "🔥 250 Stars — 220 грн ⭐️", "style": "success"}, {"text": "🔥 500 Stars — 410 грн ⭐️", "style": "success"}], [{"text": "👑 1000 Stars — 800 грн 💎", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
PREM_KB = {"keyboard": [[{"text": "💎 3 МЕСЯЦА — 630 ГРН ✨", "style": "primary"}, {"text": "👑 6 МЕСЯЦЕВ — 850 ГРН 🔥", "style": "success"}], [{"text": "👑 1 ГОД — 1520 ГРН 🔥", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
TON_KB = {"keyboard": [[{"text": "💎 1 TON — 90 грн", "style": "primary"}, {"text": "💎 2 TON — 180 грн", "style": "primary"}], [{"text": "🔥 5 TON — 450 грн", "style": "success"}, {"text": "👑 10 TON — 900 грн", "style": "success"}], [{"text": "✍️ Ввести своё количество TON", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
NFT_KB = {"keyboard": [[{"text": "🧸 Все мишки и подарки (15–100 ⭐)", "style": "primary"}], [{"text": "🖼 Каталог NFT-подарков", "style": "success"}], [{"text": "🔗 Прислать ссылку на свой NFT", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
MAIN_TEXT = f"⚡️ <b>RAGE STORE // DIGITAL MARKET</b>\nШоп цифровых активов с автовыдачей 24/7.\n\n⭐️ <b>Stars</b> • 👑 <b>Premium</b> • 💎 <b>TON</b> • 🧸 <b>Все мишки и NFT</b>\n🆘 Админ: @{U_NAME}\n⬇️ <i>Выбери раздел в меню внизу</i> ⬇️"

def send(cid, text, kb):
    api("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML", "reply_markup": kb})

def send_anim(cid, emoji_char):
    # Отправляет живой анимированный стикер-эмодзи перед каталогом
    api("sendMessage", {"chat_id": cid, "text": emoji_char})

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

def build_gifts_kb(catalog_dict, prefix):
    rows = [[{"text": f"{k} — {v} грн", "callback_data": f"{prefix}:{k}", "style": "success"}] for k, v in catalog_dict.items()]
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "to_main", "style": "danger"}])
    return {"inline_keyboard": rows}

def handle(upd):
    if "callback_query" in upd:
        cb = upd.get("callback_query", {})
        cid = cb.get("message", {}).get("chat", {}).get("id")
        data = cb.get("data", "")
        api("answerCallbackQuery", {"callback_query_id": cb.get("id")})
        if data == "to_main":
            STATE.pop(cid, None)
            send(cid, MAIN_TEXT, MAIN_KB)
        elif data.startswith("gb:"):
            _, name = data.split(":", 1)
            price = GIFTS_BASIC.get(name, 25)
            send_anim(cid, "🧸")
            STATE.update({cid: {"step": "user", "title": name, "price": price}})
            send(cid, f"🎁 Выбран подарок: <b>{name}</b> ({price} грн)\n\nВведи <b>@username</b>, кому отправить подарок:", BACK_KB)
        elif data.startswith("gn:"):
            _, name = data.split(":", 1)
            price = GIFTS_NFT.get(name, 1000)
            send_anim(cid, "🎁")
            STATE.update({cid: {"step": "user", "title": f"NFT: {name}", "price": price}})
            send(cid, f"🖼 Выбран NFT: <b>{name}</b> ({price} грн)\n\nВведи свой <b>@username</b> для получения NFT:", BACK_KB)
        elif data.startswith("chk:"):
            _, oid = data.split(":", 1)
            o = ORDERS.get(oid)
            res = crypto_api("getInvoices", {"invoice_ids": str(o.get("inv_id"))}) if o else None
            items = res.get("result", {}).get("items", []) if res and res.get("ok") else []
            if o and next(iter(items), {}).get("status") == "paid":
                o.update({"done": True})
                send_anim(cid, "🎉")
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
            send(cid, "💰 Введи цену этого NFT в грн:", BACK_KB)
        elif step == "nft_price":
            d = "".join(c for c in text if c.isdigit())
            STATE.update({cid: {"step": "user", "title": f"NFT ({st.get('link')})", "price": int(d) if d else 1000}})
            send(cid, "👤 Введи свой <b>@username</b> для получения NFT:", BACK_KB)
    elif "Звёзды" in text:
        send_anim(cid, "⭐️")
        send(cid, "⭐️ Выбери пакет звёзд:", STARS_KB)
    elif "Premium" in text:
        send_anim(cid, "👑")
        send(cid, "👑 Выбери срок подписки:", PREM_KB)
    elif "Купить TON" in text:
        send_anim(cid, "💎")
        send(cid, f"💎 Курс: <b>1 TON = {TON_PRICE_UAH} грн</b>. Выбери пакет:", TON_KB)
    elif "Ввести своё количество TON" in text:
        STATE.update({cid: {"step": "ton"}})
