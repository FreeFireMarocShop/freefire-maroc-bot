import os
import json
import urllib.request
import urllib.parse

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = json.dumps({
            "keyboard": keyboard,
            "resize_keyboard": True
        })

    encoded = urllib.parse.urlencode(data).encode()
    urllib.request.urlopen(API + "sendMessage", encoded)

def main():
    offset = 0
    orders = {}

    while True:
        params = urllib.parse.urlencode({
            "timeout": 30,
            "offset": offset
        })

        with urllib.request.urlopen(API + "getUpdates?" + params) as response:
            updates = json.loads(response.read())

        for update in updates.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                send_message(
                    chat_id,
                    "🔥 مرحبا بك في FreeFire Maroc\n\nاختار الباقة اللي بغيتي:",
                    [
                        ["💎 100 جوهرة", "💎 310 جوهرة"],
                        ["💎 520 جوهرة", "💎 1060 جوهرة"],
                        ["📦 طلباتي"]
                    ]
                )

            elif text.startswith("💎"):
                orders[chat_id] = {"package": text}

                send_message(
                    chat_id,
                    "مزيان ✅\n\nصيفط ليا دابا UID ديال حساب Free Fire ديالك.\n\n⚠️ ما تصيفطش كلمة السر."
                )

            elif text.isdigit() and chat_id in orders:
                orders[chat_id]["uid"] = text

                send_message(
                    chat_id,
                    f"✅ تسجل الطلب ديالك.\n\n"
                    f"الباقة: {orders[chat_id]['package']}\n"
                    f"UID: {text}\n\n"
                    "📌 الطلب باقي فانتظار التأكيد والشحن.",
                    [["🏠 القائمة الرئيسية"]]
                )

            elif text == "🏠 القائمة الرئيسية":
                send_message(
                    chat_id,
                    "اختار الباقة اللي بغيتي:",
                    [
                        ["💎 100 جوهرة", "💎 310 جوهرة"],
                        ["💎 520 جوهرة", "💎 1060 جوهرة"],
                        ["📦 طلباتي"]
                    ]
                )

            elif text == "📦 طلباتي":
                if chat_id in orders:
                    order = orders[chat_id]
                    send_message(
                        chat_id,
                        f"📦 آخر طلب:\n\n"
                        f"الباقة: {order.get('package')}\n"
                        f"UID: {order.get('uid', 'مازال ما دخلتيهش')}"
                    )
                else:
                    send_message(chat_id, "ما عندك حتى طلب حالياً.")

if __name__ == "__main__":
    main()
