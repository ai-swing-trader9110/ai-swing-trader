import yfinance as yf
import json
from datetime import datetime

# 監視銘柄
symbols = ["NVDA", "MSFT", "AMZN"]

stocks = []

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)

        # 直近5日間の株価データ取得
        hist = ticker.history(period="5d")

        if len(hist) < 2:
            continue

        latest_price = float(hist["Close"].iloc[-1])
        previous_price = float(hist["Close"].iloc[-2])

        change = latest_price - previous_price
        change_percent = (change / previous_price) * 100

        # 仮のスコア
        score = 50

        if change_percent > 3:
            score = 90
        elif change_percent > 1:
            score = 80
        elif change_percent > 0:
            score = 70
        elif change_percent > -2:
            score = 60
        else:
            score = 50

        rating = "BUY候補" if score >= 70 else "WATCH"

        stocks.append({
            "symbol": symbol,
            "price": round(latest_price, 2),
            "previousClose": round(previous_price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
            "score": score,
            "rating": rating
        })

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# スコア順に並び替え
stocks.sort(key=lambda x: x["score"], reverse=True)

data = {
    "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "marketTrend": "BULLISH",
    "stocks": stocks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Stock data updated successfully")
