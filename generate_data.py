import yfinance as yf
import json
import math
from datetime import datetime

# =========================
# 監視する銘柄
# =========================

symbols = [
    "NVDA",
    "MSFT",
    "AMZN",
    "AAPL",
    "GOOGL",
    "META",
    "TSLA"
]


# =========================
# RSI計算
# =========================

def calculate_rsi(prices, period=14):

    delta = prices.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


# =========================
# 株価分析
# =========================

stocks = []


for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)

        # 約3か月分のデータ取得
        hist = ticker.history(period="3mo")

        # 欠損した株価データを除外
        close = hist["Close"].dropna()

        if len(close) < 60:
            continue

        # 最新株価
        latest_price = float(close.iloc[-1])
        previous_price = float(close.iloc[-2])

        change_percent = (
            (latest_price - previous_price)
            / previous_price
            * 100
        )

        # 5日騰落率
        price_5d_ago = float(close.iloc[-6])

        change_5d = (
            (latest_price - price_5d_ago)
            / price_5d_ago
            * 100
        )

        # 移動平均
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        # RSI
        rsi_series = calculate_rsi(close)
        rsi = rsi_series.iloc[-1]

        # スコアリング


        # =========================
        # スコアリング
        # =========================

        score = 0

        reasons = []


        # 株価が20日移動平均より上

        if latest_price > ma20:

            score += 20

            reasons.append(
                "株価が20日移動平均線より上"
            )


        # 20日移動平均が50日移動平均より上

        if ma20 > ma50:

            score += 20

            reasons.append(
                "中期トレンドが上向き"
            )


        # 5日間で上昇

        if change_5d > 0:

            score += 15

            reasons.append(
                "直近5日間で上昇"
            )


        # RSI

        if 50 <= rsi <= 70:

            score += 20

            reasons.append(
                "RSIが適正な上昇ゾーン"
            )


        # 当日上昇

        if change_percent > 0:

            score += 10

            reasons.append(
                "直近取引日で上昇"
            )


        # 強い上昇

        if change_percent > 2:

            score += 15

            reasons.append(
                "強い上昇モメンタム"
            )


        # =========================
        # 判定
        # =========================

        if score >= 70:

            rating = "BUY候補"

        elif score >= 50:

            rating = "WATCH"

        else:

            rating = "HOLD"


        # =========================
        # データ保存
        # =========================

        stocks.append({

            "symbol": symbol,

            "price": round(
                latest_price,
                2
            ),

            "change_percent": round(
                change_percent,
                2
            ),

            "change_5d": round(
                change_5d,
                2
            ),

            "ma20": round(
                float(ma20),
                2
            ),

            "ma50": round(
                float(ma50),
                2
            ),

            "rsi": round(
                float(rsi),
                1
            ),

            "score": score,

            "rating": rating,

            "reasons": reasons

        })


        print(
            f"{symbol} "
            f"score={score} "
            f"rating={rating}"
        )


    except Exception as e:

        print(
            f"Error fetching {symbol}: {e}"
        )


# =========================
# 市場環境
# =========================

buy_candidates = len(
    [
        stock
        for stock in stocks
        if stock["rating"] == "BUY候補"
    ]
)


if buy_candidates >= 3:

    market = "BULLISH"

elif buy_candidates >= 1:

    market = "NEUTRAL"

else:

    market = "BEARISH"


# =========================
# JSON作成
# =========================

data = {

    "updated_at": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),

    "market": market,

    "stocks": stocks

}


# =========================
# JSONファイル保存
# =========================

with open(
    "data.json",
    "w"
) as f:

    json.dump(
    data,
    f,
    indent=2,
    ensure_ascii=False,
    allow_nan=False
)


print("Stock data updated successfully")
