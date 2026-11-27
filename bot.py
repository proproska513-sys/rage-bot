import os, time, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

S = chr(47)
TOKEN = "9286788881:AAE7Zlt5Gbxk3FGdVHpSMXVFHfARMQRxjL0"
ADM = "".join(["m", "a", "n", "d", "r", "u", "s", "y", "a"])
URL, API = f"https:{S}{S}t.me{S}{ADM}", f"https:{S}{S}api.telegram.org{S}bot{TOKEN}{S}"
TON_UAH, USDT_UAH, CPAY, SPLIT_KEY = 45, 45.6, "", ""

E_BOLT, E_STAR, E_CROWN, E_GEM, E_FIRE, E_GIFT, E_BEAR, E_SOS = "5368324170671202286", "5447644880824181073", "5372981976804366741", "5465665476971471368", "5424972470023104089", "5373032425667498601", "5370838923828209944", "5373174941095051646"
def pe(i, f): return f'<tg-emoji emoji-id="{i}">{f}</tg-emoji>'
def bt(t, st, i): return {"text": t, "style": st, "icon_custom_emoji_id": i}

BEARS = {"🧸 Плюшевый мишка (15⭐)": (12, "🧸"), "🐻 Бурый мишка (15⭐)": (12, "🐻"), "🐼 Панда-мишка (25⭐)": (20, "🐼"), "🐨 Коала-мишка (50⭐)": (39, "🐨"), "🧸 Toy Bear NFT": (470, "🧸")}
GIFTS = {"💝 Сердце (15⭐)": (12, "💝"), "🌹 Роза (25⭐)": (20, "🌹"), "🎁 Коробка (25⭐)": (20, "🎁"), "🍾 Шампанское (50⭐)": (39, "🍾"), "🎂 Торт (50⭐)": (39, "🎂"), "💐 Букет (50⭐)": (39, "💐"), "🚀 Ракета (50⭐)": (39, "🚀"), "🏆 Кубок (100⭐)": (78, "🏆"), "💍 Кольцо (100⭐)": (78, "💍"), "💎 Бриллиант (100⭐)": (78, "💎")}
NFTS = {"🐸 Plush Pepe NFT": [1730, "🐸", "plushpepe"], "🧢 Durov's Cap": [1190, "🧢", "durovscap"], "🍑 Precious Peach": [650, "🍑", "preciouspeach"], "🚬 Vintage Cigar": [360, "🚬", "vintagecigar"], "📅 Homemade Cake": [135, "🎂", "homemadecake"], "🍭 Lol Pop NFT": [120, "🍭", "lolpop"], "🍬 Candy Cane": [125, "🍬", "candycane"], "🎃 Scared Cat": [360, "🎃", "scaredcat"], "🔮 Crystal Ball": [270, "🔮", "crystalball"], "🎩 Top Hat": [225, "🎩", "tophat"], "⌚️ Swiss Watch": [515, "⌚️", "swisswatch"], "💍 Diamond Ring": [335, "💍", "diamondring"], "🍸 Berry Box": [180, "🍸", "berrybox"], "🧿 Evil Eye": [155, "🧿", "evileye"], "🍷 Spiced Wine": [145, "🍷", "spicedwine"]}
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

def frag_ton(slug, col):
    for u in (f"https:{S}{S}fragment.com{S}gift{S}{slug}", f"https:{S}{S}fragment.com{S}gifts{S}{col}?sort=price_asc&filter=sale"):
        try:
            html = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).text
            for p in html.split('icon-ton">'):
                if 'tm-value">' in p:
                    raw = p.split('tm-value">', 1).pop().split("<", 1).pop(0).replace(",", "").strip()
                    if raw.replace(".", "", 1).isdigit() and 0.5 <= float(raw) <= 500: return float(raw)
        except Exception: pass
    return None

def auto_send(o):
    if SPLIT_KEY:
        try:
            t = o.get("t", ""); u = o.get("u", "").lstrip("@"); d = "".join(c for c in t if c.isdigit()); q = int(d) if d else 50
            requests.post(f"https:{S}{S}api.split.tg{S}v1{S}buy{S}{'premium' if 'МЕСЯЦ' in t or 'ГОД' in t else 'stars'}", json={"username": u, "months": q, "quantity": q}, headers={"Authorization": f"Bearer {SPLIT_KEY}"}, timeout=15)
        except Exception: pass
    o.update({"done": True})

M_KB = {"keyboard": [[bt("ТГ Звёзды", "primary", E_STAR), bt("Telegram Premium", "success", E_CROWN)], [bt("Мишки", "success", E_BEAR), bt("Подарки", "primary", E_GIFT)], [bt("NFT-подарки", "success", E_FIRE), bt("Поддержка", "danger", E_SOS)]], "resize_keyboard": True}
B_KB = {"keyboard": [[{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
S_KB = {"keyboard": [[bt("50 Stars — 38 грн", "primary", E_STAR), bt("100 Stars — 76 грн", "primary", E_STAR)], [bt("250 Stars — 190 грн", "success", E_FIRE), bt("500 Stars — 380 грн", "success", E_FIRE)], [bt("1000 Stars — 760 грн", "success", E_CROWN)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
P_KB = {"keyboard": [[bt("3 МЕСЯЦА — 590 ГРН", "primary", E_GEM), bt("6 МЕСЯЦЕВ — 790 ГРН", "success", E_CROWN)], [bt("1 ГОД — 1430 ГРН", "success", E_FIRE)], [{"text": "⬅️ В главное меню 🏠", "style": "danger"}]], "resize_keyboard": True}
TXT = f"{pe(E_BOLT, '⚡️')} <b>RAGE STORE // DIGITAL MARKET</b>\nАвтовыдача 24/7 по ценам Fragment (+20 грн).\n\n{pe(E_STAR, '⭐️')} <b>Telegram Stars</b> • {pe(E_CROWN, '👑')} <b>Premium</b>\n{pe(E_BEAR, '🧸')} <b>Мишки / Подарки / NFT</b>\n\n🆘 Админ: @{ADM}\n⬇️ <i>Выбери нужный раздел в меню внизу</i> ⬇️"

def send(c, t, k=None): post("sendMessage", {"chat_id": c, "text": t, "parse_mode": "HTML", **({"reply_markup": k} if k else {})})
def stk(c, e): post("sendMessage", {"chat_id": c, "text": e})

def order(c, title, price, target):
    oid = f"{c}_{int(time.time())}"
    r = cpay("createInvoice", {"asset": "USDT", "amount": str(round(price / USDT_UAH, 2)), "description": f"{title} -> {target}"})
    inv = r.get("result", {}) if r and r.get("ok") else {}
    ORD.update({oid: {"c": c, "t": title, "p": price, "u": target, "id": inv.get("invoice_id"), "done": False}})
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
            it = list(src.get(k, (12, "🎁"))); price, emo = it.pop(0), it.pop(0); stk(c, emo)
            ST.update({c: {"s": "u", "t": k, "p": price}}); send(c, f"✨ Выбрано: <b>{k}</b> (<b>{price} грн</b>)\nВведи <b>@username</b> получателя:", B_KB)
        elif d.startswith("chk:"):
            _, oid = d.split(":", 1); o = ORD.get(oid)
            if not o or o.get("done"): send(c, "✅ Заказ уже выдан!", M_KB); return
            r = cpay("getInvoices", {"invoice_ids": str(o.get("id"))})
            it = r.get("result", {}).get("items", []) if r and r.get("ok") else []
            if next(iter(it), {}).get("status") == "paid": auto_send(o); stk(c, "🎉"); send(c, f"🎉 <b>ОПЛАТА ПОДТВЕРЖДЕНА! АВТОВЫДАЧА ВЫПОЛНЕНА</b>\n📦 <b>{o.get('t')}</b> -> <code>{o.get('u')}</code>", M_KB)
            else: send(c, "⏳ Оплата ещё не поступила.")
        return

    m = u.get("message")
    if not m: return
    c = m.get("chat", {}).get("id"); tx = m.get("text", "").strip()
    if tx.startswith("/start") or "главное меню" in tx: ST.pop(c, None); send(c, TXT, M_KB)
    elif c in ST:
        s = ST.get(c, {}); stp = s.get("s")
        if stp == "u": ST.pop(c, None); order(c, s.get("t"), s.get("p"), tx)
        elif stp == "nl":
            slug = tx.rstrip(S).split(S).pop().lower(); ton_p = frag_ton(slug, slug.split("-").pop(0)) or 18.2; auto_p = round(ton_p * TON_UAH) + 20
            ST.update({c: {"s": "u", "t": f"NFT ({tx})", "p": auto_p}}); send(c, f"🖼 <b>Fragment: {ton_p} TON</b>\n💰 К оплате (+20 грн): <b>{auto_p} грн</b>\n\n👤 Введи свой <b>@username</b>:", B_KB)
    elif "Звёзды" in tx: send(c, f"{pe(E_STAR, '⭐️')} <b>TELEGRAM STARS</b>\nВыбери пакет звёзд:", S_KB)
    elif "Premium" in tx: send(c, f"{pe(E_CROWN, '👑')} <b>TELEGRAM PREMIUM</b>\nВыбери срок подписки:", P_KB)
    elif tx == "Мишки": send(c, f"{pe(E_BEAR, '🧸')} <b>КАТАЛОГ МИШЕК</b>\nНажми на мишку:", cat(BEARS, "b"))
    elif tx == "Подарки": send(c, f"{pe(E_GIFT, '🎁')} <b>КАТАЛОГ ПОДАРКОВ</b>\nНажми на подарок:", cat(GIFTS, "g"))
    elif tx == "NFT-подарки": send(c, f"{pe(E_FIRE, '🖼')} <b>КАТАЛОГ NFT-ПОДАРКОВ (FRAGMENT +20 ГРН)</b>\nНажми на NFT или пришли ссылку:", cat(NFTS, "n", True))
    elif "Поддержка" in tx: send(c, f"🆘 Поддержка @{ADM} (9:00–22:30)", {"inline_keyboard": [[{"text": f"🆘 НАПИСАТЬ (@{ADM})", "url": URL, "style": "danger"}]]})
    elif "—" in tx:
        l, r = tx.split("—", 1); p = int("".join(x for x in r if x.isdigit())); ST.update({c: {"s": "u", "t": l.strip(), "p": p}})
        send(c, f"✅ Выбрано: <b>{l.strip()}</b> ({p} грн)\nВведи <b>@username</b> получателя:", B_KB)

def sync_frag():
    for it in NFTS.values():
        col = it.copy().pop(); v = frag_ton(col, col)
        if v: it.pop(0); it.insert(0, round(v * TON_UAH) + 20)

threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), H).serve_forever(), daemon=True).start()
