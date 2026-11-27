import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

S = chr(47)
TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
ADM = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
URL = f"https:{S}{S}t.me{S}{ADM}"
API = f"https:{S}{S}api.telegram.org{S}bot{TOKEN}{S}"
TON_UAH, USDT_UAH, CPAY = 90, 45.5, ""

# --- БАЗА АНИМИРОВАННЫХ ПРЕМИУМ-ЭМОДЗИ ---
E_BOLT = "5368324170671202286"
E_STAR = "5447644880824181073"
E_CROWN = "5372981976804366741"
E_GEM = "5465665476971471368"
E_FIRE = "5424972470023104089"
E_GIFT = "5373032425667498601"
E_BEAR = "5370838923828209944"
E_CARD = "5373141891321699086"
E_CHECK = "5373001317042101552"
E_SOS = "5373174941095051646"

def pe(eid, fb):
    return f'<tg-emoji emoji-id="{eid}">{fb}</tg-emoji>'

def btn(text, style, eid):
    return {"text": text, "style": style, "icon_custom_emoji_id": eid}

BEARS = {
    "🧸 Плюшевый мишка (15⭐)": (20, "🧸"),
    "🐻 Бурый мишка (15⭐)": (20, "🐻"),
    "🐼 Панда-мишка (25⭐)": (30, "🐼"),
    "🐨 Коала-мишка (50⭐)": (55, "🐨"),
    "🧸 Toy Bear NFT (Коллекц.)": (1450, "🧸")
}

GIFTS = {
    "💝 Сердце в коробке (15⭐)": (20, "💝"),
    "🌹 Красная роза (25⭐)": (30, "🌹"),
    "🎁 Подарок с бантом (25⭐)": (30, "🎁"),
    "🍾 Шампанское (50⭐)": (55, "🍾"),
    "🎂 Праздничный торт (50⭐)": (55, "🎂"),
    "💐 Букет цветов (50⭐)": (55, "💐"),
    "🚀 Ракета (50⭐)": (55, "🚀"),
    "🏆 Кубок чемпиона (100⭐)": (105, "🏆"),
    "💍 Кольцо с камнем (100⭐)": (105, "💍"),
    "💎 Бриллиант (100⭐)": (105, "💎")
}

NFTS = {
    "🐸 Plush Pepe NFT": (4500, "🐸"),
    "🧢 Durov's Cap NFT": (3200, "🧢"),
    "🍑 Precious Peach NFT": (1850, "🍑"),
    "🚬 Vintage Cigar NFT": (950, "🚬"),
    "📅 Homemade Cake NFT": (420, "🎂"),
    "🍭 Lol Pop NFT": (350, "🍭"),
    "🍬 Candy Cane NFT": (380, "🍬"),
    "🎃 Scared Cat NFT": (1200, "🎃"),
    "🔮 Crystal Ball NFT": (890, "🔮"),
    "🎩 Top Hat NFT": (750, "🎩"),
    "⌚️ Swiss Watch NFT": (1600, "⌚️"),
    "💍 Diamond Ring NFT": (1100, "💍"),
    "🍸 Berry Box NFT": (640, "🍸"),
    "🧿 Evil Eye NFT": (520, "🧿"),
    "🍷 Spiced Wine NFT": (490, "🍷")
}

ST, ORD = {}, {}

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *a): pass

def post(m, d):
    try: return requests.post(API + m, json=d, timeout=25).json()
    except Exception: time.sleep(2); return None

def cpay(m, d):
    if not CPAY: return None
    try: return requests.post(f"https:{S}{S}pay.crypt.bot{S}api{S}{m}", json=d, headers={"Crypto-Pay-API-Token": CPAY}, timeout=20).json()
    except Exception: return None

M_KB = {"keyboard": [[btn("ТГ Звёзды", "primary", E_STAR), btn("Telegram Premium", "success", E_CROWN)], [btn("Купить TON", "primary", E_GEM), btn("Мишки", "success", E_BEAR)], [btn("Подарки", "primary", E_GIFT), btn("NFT-подарки", "success", E_FIRE)], [btn("Поддержка", "danger", E_SOS)]], "resize_keyboard": True}
B_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
S_KB = {"keyboard": [[btn("50 Stars — 45 грн", "primary", E_STAR), btn("100 Stars — 85 грн", "primary", E_STAR)], [btn("250 Stars — 220 грн", "success", E_FIRE), btn("500 Stars — 410 грн", "success", E_FIRE)], [btn("1000 Stars — 800 грн", "success", E_CROWN)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
P_KB = {"keyboard": [[btn("3 МЕСЯЦА — 630 ГРН", "primary", E_GEM), btn("6 МЕСЯЦЕВ — 850 ГРН", "success", E_CROWN)], [btn("1 ГОД — 1520 ГРН", "success", E_FIRE)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
T_KB = {"keyboard": [[btn("1 TON — 90 грн", "primary", E_GEM), btn("2 TON — 180 грн", "primary", E_GEM)], [btn("5 TON — 450 грн", "success", E_FIRE), btn("10 TON — 900 грн", "success", E_CROWN)], [btn("Своё количество TON", "primary", E_BOLT)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}

TXT = (
    f"{pe(E_BOLT, '⚡️')} <b>RAGE STORE // DIGITAL MARKET</b>\n"
    f"Шоп цифровых активов с автовыдачей 24/7.\n\n"
    f"{pe(E_STAR, '⭐️')} <b>Telegram Stars</b> — моментально по @username\n"
    f"{pe(E_CROWN, '👑')} <b>Telegram Premium</b> — 3 / 6 / 12 месяцев\n"
    f"{pe(E_GEM, '💎')} <b>TON</b> — покупка любого количества\n"
    f"{pe(E_BEAR, '🧸')} <b>Мишки / Подарки / NFT</b> — отдельные каталоги\n\n"
    f"{pe(E_SOS, '🆘')} Админ: @{ADM}\n⬇️ <i>Выбери нужный раздел в меню внизу</i> ⬇️"
)

def send(c, t, k=None):
    post("sendMessage", {"chat_id": c, "text": t, "parse_mode": "HTML", **({"reply_markup": k} if k else {})})

def gift_sticker(c, emoji_char):
    post("sendMessage", {"chat_id": c, "text": emoji_char})

def order(c, title, price, target):
    oid = f"{c}_{int(time.time())}"
    r = cpay("createInvoice", {"asset": "USDT", "amount": str(round(price / USDT_UAH, 2)), "description": f"{title} -> {target}"})
    inv = r.get("result", {}) if r and r.get("ok") else {}
    ORD.update({oid: {"c": c, "t": title, "p": price, "u": target, "id": inv.get("invoice_id")}})
    rows = [[{"text": "ОПЛАТИТЬ АВТОМАТОМ (CRYPTOBOT)", "url": inv.get("bot_invoice_url"), "style": "success", "icon_custom_emoji_id": E_BOLT}], [{"text": "ПРОВЕРИТЬ ОПЛАТУ", "callback_data": f"chk:{oid}", "style": "primary", "icon_custom_emoji_id": E_CHECK}]] if inv.get("bot_invoice_url") else []
    rows.extend([[{"text": f"ОПЛАТИЛ НА КАРТУ / ЧЕК (@{ADM})", "url": URL, "style": "success", "icon_custom_emoji_id": E_CHECK}], [{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}]])
    send(c, f"{pe(E_CARD, '💳')} <b>ЗАКАЗ // RAGE STORE</b>\n{pe(E_GIFT, '📦')} <b>{title}</b>\n🎯 <code>{target}</code>\n{pe(E_GEM, '💰')} <b>{price} грн</b>\n\nКарта (UAH): <code>4874 0700 2382 7379</code>\nПосле оплаты нажми кнопку ниже 👇", {"inline_keyboard": rows})

def cat_kb(d, p, eid, extra_nft=False):
    rows = [[{"text": f"{k} — {next(iter(v))} грн", "callback_data": f"{p}:{k}", "style": "success", "icon_custom_emoji_id": eid}] for k, v in d.items()]
    if extra_nft:
        rows.append([{"text": "Прислать ссылку на свой NFT", "callback_data": "link_nft", "style": "primary", "icon_custom_emoji_id": E_BOLT}])
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}])
    return {"inline_keyboard": rows}

def handle(u):
    if "callback_query" in u:
        cb = u.get("callback_query", {}); c = cb.get("message", {}).get("chat", {}).get("id"); d = cb.get("data", "")
        post("answerCallbackQuery", {"callback_query_id": cb.get("id")})
        if d == "main":
            ST.pop(c, None); send(c, TXT, M_KB)
        elif d == "link_nft":
            ST.update({c: {"s": "nl"}}); send(c, f"{pe(E_BOLT, '🔗')} Пришли ссылку на нужный NFT:", B_KB)
        elif d.startswith("b:") or d.startswith("g:") or d.startswith("n:"):
            p, k = d.split(":", 1)
            src = BEARS if p == "b" else (GIFTS if p == "g" else NFTS)
            price, emo = src.get(k, (50, "🎁"))
            gift_sticker(c, emo)
            ST.update({c: {"s": "u", "t": k, "p": price}})
            send(c, f"{pe(E_STAR, '✨')} Выбрано: <b>{k}</b> (<b>{price} грн</b>)\nВведи <b>@username</b> получателя:", B_KB)
        elif d.startswith("chk:"):
            _, oid = d.split(":", 1); o = ORD.get(oid)
            r = cpay("getInvoices", {"invoice_ids": str(o.get("id"))}) if o else None
            it = r.get("result", {}).get("items", []) if r and r.get("ok") else []
            if o and next(iter(it), {}).get("status") == "paid":
                gift_sticker(c, "🎉"); send(c, f"{pe(E_CHECK, '🎉')} <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n📦 <b>{o.get('t')}</b> -> <code>{o.get('u')}</code>", M_KB)
            else:
                send(c, "⏳ Оплата ещё не поступила.")
        return

    m = u.get("message")
    if not m: return
    c = m.get("chat", {}).get("id"); tx = m.get("text", "").strip()
    if tx.startswith("/start") or "главное меню" in tx:
        ST.pop(c, None); send(c, TXT, M_KB)
    elif c in ST:
        s = ST.get(c, {}); stp = s.get("s")
        if stp == "u":
            ST.pop(c, None); order(c, s.get("t"), s.get("p"), tx)
        elif stp == "ton":
            try:
                q = float(tx.replace(",", ".")); p = round(q * TON_UAH)
                ST.update({c: {"s": "u", "t": f"{q} TON", "p": p}})
                send(c, f"{pe(E_GEM, '💎')} {q} TON = <b>{p} грн</b>. Введи адрес TON-кошелька:", B_KB)
            except Exception:
                send(c, "⚠️ Введи число, например: <code>2.5</code>", B_KB)
        elif stp == "nl":
            ST.update({c: {"s": "np", "l": tx}}); send(c, f"{pe(E_GEM, '💰')} Введи цену этого NFT в грн:", B_KB)
        elif stp == "np":
            d = "".join(x for x in tx if x.isdigit())
            ST.update({c: {"s": "u", "t": f"NFT ({s.get('l')})", "p": int(d) if d else 1000}})
            send(c, "👤 Введи свой <b>@username</b> для получения NFT:", B_KB)
    elif "Звёзды" in tx:
        send(c, f"{pe(E_STAR, '⭐️')} <b>TELEGRAM STARS</b>\nВыбери пакет звёзд:", S_KB)
    elif "Premium" in tx:
        send(c, f"{pe(E_CROWN, '👑')} <b>TELEGRAM PREMIUM</b>\nВыбери срок подписки:", P_KB)
    elif "Купить TON" in tx:
        send(c, f"{pe(E_GEM, '💎')} <b>КУПИТЬ TON</b>\nАктуальный курс: <b>1 TON = {TON_UAH} грн</b>", T_KB)
    elif "Своё количество TON" in tx:
        ST.update({c: {"s": "ton"}}); send(c, f"{pe(E_BOLT, '✍️')} Введи нужное количество TON:", B_KB)
    elif "Мишки" in tx:
        send(c, f"{pe(E_BEAR, '🧸')} <b>КАТАЛОГ МИШЕК</b>\nНажми на мишку, чтобы посмотреть стикер и оформить:", cat_kb(BEARS, "b", E_BEAR))
    elif "NFT-подарки" in tx:
        send(c, f"{pe(E_FIRE, '🖼')} <b>КАТАЛОГ КОЛЛЕКЦИОННЫХ NFT</b>\nНажми на NFT или пришли ссылку на свой:", cat_kb(NFTS, "n", E_FIRE, True))
    elif "Подарки" in tx:
