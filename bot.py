import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

S = chr(47)
TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
ADM = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
URL = f"https:{S}{S}t.me{S}{ADM}"
API = f"https:{S}{S}api.telegram.org{S}bot{TOKEN}{S}"
TON_UAH, USDT_UAH, CPAY = 90, 45.5, ""

BASIC = {"🧸 Мишка (15⭐)": 20, "💝 Сердце (15⭐)": 20, "🌹 Роза (25⭐)": 30, "🎁 Коробка (25⭐)": 30, "🍾 Шампанское (50⭐)": 55, "🎂 Торт (50⭐)": 55, "💐 Букет (50⭐)": 55, "🚀 Ракета (50⭐)": 55, "🏆 Кубок (100⭐)": 105, "💍 Кольцо (100⭐)": 105, "💎 Бриллиант (100⭐)": 105}
NFTS = {"🧸 Toy Bear NFT": 1450, "🐸 Plush Pepe NFT": 4500, "🧢 Durov's Cap": 3200, "🍑 Precious Peach": 1850, "🚬 Vintage Cigar": 950, "📅 Homemade Cake": 420, "🍭 Lol Pop NFT": 350, "🍬 Candy Cane": 380, "🎃 Scared Cat": 1200, "🔮 Crystal Ball": 890, "🎩 Top Hat": 750, "⌚️ Swiss Watch": 1600, "💍 Diamond Ring": 1100, "🍸 Berry Box": 640, "🧿 Evil Eye": 520, "🍷 Spiced Wine": 490}
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

M_KB = {"keyboard": [[{"text": "⭐️ ТГ Звёзды ⭐️", "style": "primary"}, {"text": "👑 Telegram Premium 👑", "style": "success"}], [{"text": "💎 Купить TON 💎", "style": "primary"}, {"text": "🎁 Подарки и NFT 🧸", "style": "success"}], [{"text": "🆘 Поддержка 🆘", "style": "danger"}]], "resize_keyboard": True}
B_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
S_KB = {"keyboard": [[{"text": "⚡️ 50 Stars — 45 грн ✨", "style": "primary"}, {"text": "⚡️ 100 Stars — 85 грн ✨", "style": "primary"}], [{"text": "🔥 250 Stars — 220 грн ⭐️", "style": "success"}, {"text": "🔥 500 Stars — 410 грн ⭐️", "style": "success"}], [{"text": "👑 1000 Stars — 800 грн 💎", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
P_KB = {"keyboard": [[{"text": "💎 3 МЕСЯЦА — 630 ГРН ✨", "style": "primary"}, {"text": "👑 6 МЕСЯЦЕВ — 850 ГРН 🔥", "style": "success"}], [{"text": "👑 1 ГОД — 1520 ГРН 🔥", "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
T_KB = {"keyboard": [[{"text": "💎 1 TON — 90 грн", "style": "primary"}, {"text": "💎 2 TON — 180 грн", "style": "primary"}], [{"text": "🔥 5 TON — 450 грн", "style": "success"}, {"text": "👑 10 TON — 900 грн", "style": "success"}], [{"text": "✍️ Своё количество TON", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
N_KB = {"keyboard": [[{"text": "🧸 Все мишки и подарки", "style": "primary"}], [{"text": "🖼 Каталог NFT-подарков", "style": "success"}], [{"text": "🔗 Ссылка на свой NFT", "style": "primary"}], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
TXT = f"⚡️ <b>RAGE STORE // DIGITAL MARKET</b>\nШоп цифровых активов с автовыдачей 24/7.\n\n⭐️ <b>Stars</b> • 👑 <b>Premium</b> • 💎 <b>TON</b> • 🧸 <b>Мишки и NFT</b>\n🆘 Админ: @{ADM}\n⬇️ <i>Выбери раздел в меню внизу</i> ⬇️"

def send(c, t, k=None): post("sendMessage", {"chat_id": c, "text": t, "parse_mode": "HTML", **({"reply_markup": k} if k else {})})
def anim(c, e): post("sendMessage", {"chat_id": c, "text": e})

def order(c, title, price, target):
    oid = f"{c}_{int(time.time())}"
    r = cpay("createInvoice", {"asset": "USDT", "amount": str(round(price / USDT_UAH, 2)), "description": f"{title} -> {target}"})
    inv = r.get("result", {}) if r and r.get("ok") else {}
    ORD.update({oid: {"c": c, "t": title, "p": price, "u": target, "id": inv.get("invoice_id")}})
    rows = [[{"text": "⚡️ ОПЛАТИТЬ АВТОМАТОМ (CRYPTOBOT)", "url": inv.get("bot_invoice_url"), "style": "success"}], [{"text": "🔄 ПРОВЕРИТЬ ОПЛАТУ", "callback_data": f"chk:{oid}", "style": "primary"}]] if inv.get("bot_invoice_url") else []
    rows.extend([[{"text": f"✅ ОПЛАТИЛ НА КАРТУ / ЧЕК (@{ADM})", "url": URL, "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}]])
    send(c, f"💳 <b>ЗАКАЗ // RAGE STORE</b>\n📦 <b>{title}</b>\n🎯 <code>{target}</code>\n💰 <b>{price} грн</b>\n\nКарта (UAH): <code>4874 0700 2382 7379</code>\nПосле оплаты нажми кнопку ниже 👇", {"inline_keyboard": rows})

def g_kb(d, p):
    rows = [[{"text": f"{k} — {v} грн", "callback_data": f"{p}:{k}", "style": "success"}] for k, v in d.items()]
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}])
    return {"inline_keyboard": rows}

def handle(u):
    if "callback_query" in u:
        cb = u.get("callback_query", {}); c = cb.get("message", {}).get("chat", {}).get("id"); d = cb.get("data", "")
        post("answerCallbackQuery", {"callback_query_id": cb.get("id")})
        if d == "main": ST.pop(c, None); send(c, TXT, M_KB)
        elif d.startswith("gb:") or d.startswith("gn:"):
            p, k = d.split(":", 1); src = BASIC if p == "gb" else NFTS
            anim(c, "🧸" if p == "gb" else "🎁"); ST.update({c: {"s": "u", "t": k, "p": src.get(k, 50)}})
            send(c, f"🎁 Выбрано: <b>{k}</b> ({src.get(k, 50)} грн)\nВведи <b>@username</b> получателя:", B_KB)
        elif d.startswith("chk:"):
            _, oid = d.split(":", 1); o = ORD.get(oid)
            r = cpay("getInvoices", {"invoice_ids": str(o.get("id"))}) if o else None
            it = r.get("result", {}).get("items", []) if r and r.get("ok") else []
            if o and next(iter(it), {}).get("status") == "paid": anim(c, "🎉"); send(c, f"🎉 <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n📦 <b>{o.get('t')}</b> -> <code>{o.get('u')}</code>", M_KB)
            else: send(c, "⏳ Оплата ещё не поступила.")
        return

    m = u.get("message")
    if not m: return
    c = m.get("chat", {}).get("id"); tx = m.get("text", "").strip()
    if tx.startswith("/start") or "главное меню" in tx: ST.pop(c, None); send(c, TXT, M_KB)
    elif c in ST:
        s = ST.get(c, {}); stp = s.get("s")
        if stp == "u": ST.pop(c, None); order(c, s.get("t"), s.get("p"), tx)
        elif stp == "ton":
            try: q = float(tx.replace(",", ".")); p = round(q * TON_UAH); ST.update({c: {"s": "u", "t": f"{q} TON", "p": p}}); send(c, f"💎 {q} TON = <b>{p} грн</b>. Введи TON-кошелёк:", B_KB)
            except Exception: send(c, "⚠️ Введи число, например: <code>2.5</code>", B_KB)
        elif stp == "nl": ST.update({c: {"s": "np", "l": tx}}); send(c, "💰 Введи цену этого NFT в грн:", B_KB)
        elif stp == "np": d = "".join(x for x in tx if x.isdigit()); ST.update({c: {"s": "u", "t": f"NFT ({s.get('l')})", "p": int(d) if d else 1000}}); send(c, "👤 Введи свой <b>@username</b>:", B_KB)
    elif "Звёзды" in tx: anim(c, "⭐️"); send(c, "⭐️ Выбери пакет звёзд:", S_KB)
    elif "Premium" in tx: anim(c, "👑"); send(c, "👑 Выбери срок подписки:", P_KB)
    elif "Купить TON" in tx: anim(c, "💎"); send(c, f"💎 Курс: <b>1 TON = {TON_UAH} грн</b>:", T_KB)
    elif "Своё количество TON" in tx: ST.update({c: {"s": "ton"}}); send(c, "✍️ Введи количество TON:", B_KB)
    elif "Подарки и NFT" in tx: anim(c, "🧸"); send(c, "🎁 <b>ВСЕ МИШКИ, ПОДАРКИ И NFT</b>:", N_KB)
    elif "Все мишки" in tx: anim(c, "🧸"); send(c, "🧸 <b>ВСЕ МИШКИ И ПОДАРКИ (15–100⭐)</b>:", g_kb(BASIC, "gb"))
    elif "Каталог NFT" in tx: anim(c, "🎁"); send(c, "🖼 <b>КОЛЛЕКЦИОННЫЕ NFT-ПОДАРКИ</b>:", g_kb(NFTS, "gn"))
    elif "Ссылка на свой NFT" in tx: ST.update({c: {"s": "nl"}}); send(c, "🔗 Пришли ссылку на NFT:", B_KB)
    elif "Поддержка" in tx: send(c, f"🆘 Поддержка @{ADM} (9:00–22:30)", {"inline_keyboard": [[{"text": f"🆘 НАПИСАТЬ (@{ADM})", "url": URL, "style": "danger"}]]})
    elif "—" in tx:
        l, r = tx.split("—", 1); p = int("".join(x for x in r if x.isdigit())); ST.update({c: {"s": "u", "t": l.strip(), "p": p}})
        send(c, f"✅ Выбрано: <b>{l.strip()}</b> ({p} грн)\nВведи {'адрес TON-кошелька' if 'TON' in tx else '<b>@username</b> получателя'}:", B_KB)

def main():
    threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), H).serve_forever(), daemon=True).start()
    post("deleteWebhook", {"drop_pending_updates": True}); print("RAGE STORE 24/7 ONLINE!", flush=True); off = 0
    while True:
        r = post("getUpdates", {"offset": off, "timeout": 20})
        if r and r.get("ok"):
            for u in r.get("result", []): off = u.get("update_id", 0) + 1; handle(u)

if __name__ == "__main__": main()
# END
