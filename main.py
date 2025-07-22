import yfinance as yf
import time
import requests
from datetime import datetime

# Настройки Telegram
TOKEN = "8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs"
CHAT_ID = "5556108366"

# Валютные пары
PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/CHF": "USDCHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "USDCAD=X"
}

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def analyze(name, data):
    if data.empty or len(data) < 3:
        return None

    last = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]
    change = last - prev
    direction = "📈 Buy" if change > 0 else "📉 Sell"
    conf = min(round(abs(change)/last * 1000, 2), 95)

    if conf < 60:
        return None

    return (
        f"🔔 {name}\n"
        f"{direction} @ {round(last,5)}\n"
        f"Уверенность: {conf}%\n"
        f"⏱ Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

def check_all():
    for name, sym in PAIRS.items():
        try:
            df = yf.Ticker(sym).history(period="1d", interval="1m")
            sig = analyze(name, df)
            if sig:
                send_signal(sig)
            else:
                send_signal(f"ℹ️ {name}: нет сигнала — уверенность <60%")
        except Exception as e:
            send_signal(f"❌ Ошибка {name}: {e}")

if __name__ == "__main__":
    send_signal("🤖 Бот запущен, анализ рынка...")
    while True:
        check_all()
        time.sleep(300)
