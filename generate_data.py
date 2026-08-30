import yfinance as yf
import json
from datetime import datetime

# 監視する銘柄
symbols = [
    "NVDA",
    "MSFT",
    "AMZN"
]

stocks = []

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)

        # 過去5日間の株価データを取得
        hist = ticker.history(period="5d")

        if len(hist) < 2:
            continue

        latest_price = round(float(hist["Close"].iloc[-1]), 2)
        previous_price = float(hist["Close"].iloc[-2])

        # 前日比(%)
        change_percent = round(
            (latest_price - previous_price)
            / previous_price
            * 100,
            2
        )

        # 簡易スコア
        score = 50

        if change_percent > 0:
            score += 15

        if change_percent > 2:
            score += 10

        # スコア上限
        score = min(score, 100)

        # 評価
        if score >= 75:
            rating = "BUY候補"
        elif score >= 60:
            rating = "WATCH"
        else:
            rating = "HOLD"

        stocks.append({
            "symbol": symbol,
            "price": latest_price,
            "change_percent": change_percent,
            "score": score,
            "rating": rating
        })

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# 市場環境（簡易判定）
market = "BULLISH"

data = {
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "market": market,
    "stocks": stocks
}

# JSONファイルへ保存
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Stock data updated successfully")
