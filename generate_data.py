import json

data = {
    "market": "BULLISH",
    "stocks": [
        {
            "symbol": "NVDA",
            "score": 88,
            "rating": "BUY候補"
        },
        {
            "symbol": "MSFT",
            "score": 82,
            "rating": "BUY候補"
        },
        {
            "symbol": "AMZN",
            "score": 78,
            "rating": "BUY候補"
        }
    ]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("data.json を生成しました")
