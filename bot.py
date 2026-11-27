import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

S = chr(47)
TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
ADM = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
URL = f"https:{S}{S}t.me{S}{ADM}"
API = f"https:{S}{S}api.telegram.org{S}bot{TOKEN}{S}"
TON_UAH, USDT_UAH, CPAY = 90, 45.5, ""

E_BOLT, E_STAR, E_CROWN, E_GEM, E_FIRE, E_GIFT, E_BEAR, E_SOS = "5368324170671202286", "5447644880824181073", "5372981976804366741", "5465665476971471368", "5424972470023104089", "5373032425667498601", "5370838923828209944", "5373174941095051646"
def pe(i, f): return f'<tg-emoji emoji-id="{i}">{f}</tg-emoji>'
def bt(t, st, i): return {"text": t, "style": st, "icon_custom_emoji_id": i}

BEARS = {"🧸 Плюшевый мишка (15⭐)": (20, "🧸"), "🐻 Бурый мишка (15⭐)": (20, "🐻"), "🐼 Панда-мишка (25⭐)": (30, "🐼"), "🐨 Коала-мишка (50⭐)": (55, "🐨"), "🧸 Toy Bear NFT": (1450, "🧸")}
GIFTS = {"💝 Сердце (15⭐)": (20, "💝"), "🌹 Роза (25⭐)": (30, "🌹"), "🎁 Коробка (25⭐)": (30, "🎁"), "🍾 Шампанское (50⭐)": (55, "🍾"), "🎂 Торт (50⭐)": (55, "🎂"), "💐 Букет (50⭐)": (55, "💐"), "🚀 Ракета (50⭐)": (55, "🚀"), "🏆 Кубок (100⭐)": (105, "🏆"), "💍 Кольцо (100⭐)": (105, "💍"), "💎 Бриллиант (100⭐)": (105, "💎")}
NFTS = {"🐸 Plush Pepe NFT": (4500, "🐸"), "🧢 Durov's Cap": (3200, "🧢"), "🍑 Precious Peach": (1850, "🍑"), "🚬 Vintage Cigar": (950, "🚬"), "📅 Homemade Cake": (420, "🎂"), "🍭 Lol Pop NFT": (350, "🍭"), "🍬 Candy Cane": (380, "🍬"), "🎃 Scared Cat": (1200, "🎃"), "🔮 Crystal Ball": (890, "🔮"), "🎩 Top Hat": (750, "🎩"), "⌚️ Swiss Watch": (1600, "⌚️"), "💍 Diamond Ring": (1100, "💍"), "🍸 Berry Box": (640, "🍸"), "🧿 Evil Eye": (520, "🧿"), "🍷 Spiced Wine": (490, "🍷")}
ST, ORD = {}, {}

class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *a): pass

def post(m, d):
    try: return requests.post(API + m, json=d, timeout=25).json()
    except Exception: time.sleep(2); return None

def cpay(m, d):
    if not CPAY: return None
    try: return requests.post(f"https:{S}{S}pay.crypt.bot{S}api{S}{m}", json=d, headers={"Crypto-Pay-API-Token": CPAY}, timeout=20).json()
    except Exception: return None

M_KB = {"keyboard": [[bt("ТГ Звёзды", "primary", E_STAR), bt("Telegram Premium", "success", E_CROWN)], [bt("Купить TON", "primary", E_GEM), bt("Мишки", "success", E_BEAR)], [bt("Подарки", "primary", E_GIFT), bt("NFT-подарки", "success", E_FIRE)], [bt("Поддержка", "danger", E_SOS)]], "resize_keyboard": True}
B_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
S_KB = {"keyboard": [[bt("50 Stars — 45 грн", "primary", E_STAR), bt("100 Stars — 85 грн", "primary", E_STAR)], [bt("250 Stars — 220 грн", "success", E_FIRE), bt("500 Stars — 410 грн", "success", E_FIRE)], [bt("1000 Stars — 800 грн", "success", E_CROWN)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
P_KB = {"keyboard": [[bt("3 МЕСЯЦА — 630 ГРН", "primary", E_GEM), bt("6 МЕСЯЦЕВ — 850 ГРН", "success", E_CROWN)], [bt("1 ГОД — 1520 ГРН", "success", E_FIRE)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
T_KB = {"keyboard": [[bt("1 TON — 90 грн", "primary", E_GEM), bt("2 TON — 180 грн", "primary", E_GEM)], [bt("5 TON — 450 грн", "success", E_FIRE), bt("10 TON — 900 грн", "success", E_CROWN)], [bt("Своё количество TON", "primary", E_BOLT)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
TXT = f"{pe(E_BOLT, '⚡️')} <b>RAGE STORE // DIGITAL MARKET</b>\nШоп цифровых активов с автовыдачей 24/7.\n\n{pe(E_STAR, '⭐️')} <b>Telegram Stars</b> • {pe(E_CROWN, '👑')} <b>Premium</b>\n{pe(E_GEM, '💎')} <b>TON</b> • {pe(E_BEAR, '🧸')} <b>Мишки / Подарки / NFT</b>\n\n🆘 Админ: @{ADM}\n⬇️ <i>Выбери нужный раздел в меню внизу</i> ⬇️"

def send(c, t, k=None): post("sendMessage", {"chat_id": c, "text": t, "parse_mode": "HTML", **({"reply_markup": k} if k else {})})
def stk(c, e): post("sendMessage", {"chat_id": c, "text": e})

def order(c, title, price, target):
    oid = f"{c}_{int(time.time())}"
    r = cpay("createInvoice", {"asset": "USDT", "amount": str(round(price / USDT_UAH, 2)), "description": f"{title} -> {target}"})
    inv = r.get("result", {}) if r and r.get("ok") else {}
    ORD.update({oid: {"c": c, "t": title, "p": price, "u": target, "id": inv.get("invoice_id")}})
    rows = [[{"text": "⚡️ ОПЛАТИТЬ АВТОМАТОМ (CRYPTOBOT)", "url": inv.get("bot_invoice_url"), "style": "success"}], [{"text": "🔄 ПРОВЕРИТЬ ОПЛАТУ", "callback_data": f"chk:{oid}", "style": "primary"}]] if inv.get("bot_invoice_url") else []
    rows.extend([[{"text": f"✅ ОПЛАТИЛ НА КАРТУ / ЧЕК (@{ADM})", "url": URL, "style": "success"}], [{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}]])
    send(c, f"💳 <b>ЗАКАЗ // RAGE STORE</b>\n📦 <b>{title}</b>\n🎯 <code>{target}</code>\n💰 <b>{price} грн</b>\n\nКарта (UAH): <code>4874 0700 2382 7379</code>\nПосле оплаты нажми кнопку ниже 👇", {"inline_keyboard": rows})

def cat(d, p, nft=False):
    rows = [[{"text": f"{k} — {next(iter(v))} грн", "callback_data": f"{p}:{k}", "style": "success"}] for k, v in d.items()]
    if nft: rows.append([{"text": "🔗 Прислать ссылку на свой NFT", "callback_data": "link_nft", "style": "primary"}])
    rows.append([{"text": "⬅️ В главное меню 🏠", "callback_data": "main", "style": "danger"}])
    return {"inline_keyboard": rows}

def handle(u):
    if "callback_query" in u:
        cb = u.get("callback_query", {}); c = cb.get("message", {}).get("chat", {}).get("id"); d = cb.get("data", "")
        post("answerCallbackQuery", {"callback_query_id": cb.get("id")})
        if d == "main": ST.pop(c, None); send(c, TXT, M_KB)
        elif d == "link_nft": ST.update({c: {"s": "nl"}}); send(c, "🔗 Пришли ссылку на нужный NFT:", B_KB)
        elif d.startswith("b:") or d.startswith("g:") or d.startswith("n:"):
            p, k = d.split(":", 1); src = BEARS if p == "b" else (GIFTS if p == "g" else NFTS)
            price, emo = src.get(k, (50, "🎁")); stk(c, emo)
            ST.update({c: {"s": "u", "t": k, "p": price}}); send(c, f"✨ Выбрано: <b>{k}</b> (<b>{price} грн</b>)\nВведи <b>@username</b> получателя:", B_KB)
        elif d.startswith("chk:"):
            _, oid = d.split(":", 1); o = ORD.get(oid)
            r = cpay("getInvoices", {"invoice_ids": str(o.get("id"))}) if o else None
            it = r.get("result", {}).get("items", []) if r and r.get("ok") else []
            if o and next(iter(it), {}).get("status") == "paid": stk(c, "🎉"); send(c, f"🎉 <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n📦 <b>{o.get('t')}</b> -> <code>{o.get('u')}</code>", M_KB)
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
    elif "Звёзды" in tx: send(c, f"{pe(E_STAR, '⭐️')} <b>TELEGRAM STARS</b>\nВыбери пакет звёзд:", S_KB)
    elif "Premium" in tx: send(c, f"{pe(E_CROWN, '👑')} <b>TELEGRAM PREMIUM</b>\nВыбери срок подписки:", P_KB)
    elif "Купить TON" in tx: send(c, f"{pe(E_GEM, '💎')} <b>КУПИТЬ TON</b>\nКурс: <b>1 TON = {TON_UAH} грн</b>", T_KB)
    elif "Своё количество TON" in tx: ST.update({c: {"s": "ton"}}); send(c, "✍️ Введи нужное количество TON:", B_KB)
    elif tx == "Мишки": send(c, f"{pe(E_BEAR, '🧸')} <b>КАТАЛОГ МИШЕК</b>\nНажми на мишку:", cat(BEARS, "b"))
    elif tx == "Подарки": send(c, f"{pe(E_GIFT, '🎁')} <b>КАТАЛОГ ПОДАРКОВ</b>\nНажми на подарок:", cat(GIFTS, "g"))
    elif tx == "NFT-подарки": send(c, f"{pe(E_FIRE, '🖼')} <b>КАТАЛОГ NFT-ПОДАРКОВ</b>\nНажми на NFT или пришли ссылку:", cat(NFTS, "n", True))
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

