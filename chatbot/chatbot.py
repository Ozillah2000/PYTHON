#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CryptoBuddy: A simple rule-based chatbot for crypto advice.
Run in: Google Colab, Jupyter, or any IDE/terminal.
Author: You ✨
"""

from typing import Dict, Any, List, Tuple

# --------------------------
# 1) Bot personality
# --------------------------
BOT_NAME = "CryptoBuddy"
BOT_TONE = "Friendly and professional"  # you can switch to meme-loving if you want 😄

OPENING_LINE = (
    "Hey there! I'm CryptoBuddy 🤖💬 — let's find you a green and growing crypto!"
)

DISCLAIMER = (
    "⚠️ Heads up: Crypto is risky and volatile. This is educational info, not financial advice. "
    "Always do your own research (DYOR)."
)

# --------------------------
# 2) Predefined Crypto Data
# --------------------------
crypto_db: Dict[str, Dict[str, Any]] = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3/10,
        "ticker": "BTC",
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6/10,
        "ticker": "ETH",
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8/10,
        "ticker": "ADA",
    },
}

VALID_TRENDS = {"rising", "stable", "falling"}
VALID_MARKET_CAPS = {"high", "medium", "low"}
VALID_ENERGY = {"low", "medium", "high"}

# --------------------------
# 3) Helper functions (rules)
# --------------------------
def score_profitability(asset: Dict[str, Any]) -> float:
    """Higher is better. Prioritize rising + high market cap."""
    base = 0.0
    trend = asset.get("price_trend", "stable")
    mcap = asset.get("market_cap", "medium")
    # Trend scoring
    if trend == "rising":
        base += 2.0
    elif trend == "stable":
        base += 1.0
    else:  # falling
        base -= 1.0
    # Market cap scoring (liquidity / maturity proxy)
    if mcap == "high":
        base += 1.5
    elif mcap == "medium":
        base += 0.5
    else:
        base -= 0.5
    return base

def score_sustainability(asset: Dict[str, Any]) -> float:
    """Higher is better. Prioritize low energy use and high sustainability_score."""
    base = 0.0
    energy = asset.get("energy_use", "medium")
    score = float(asset.get("sustainability_score", 0))
    # Energy efficiency
    if energy == "low":
        base += 2.0
    elif energy == "medium":
        base += 1.0
    else:
        base -= 0.5
    # Normalized sustainability score (already 0..1)
    base += 3.0 * score
    return base

def rank_assets(db: Dict[str, Dict[str, Any]], scorer) -> List[Tuple[str, float]]:
    ranked = [(name, scorer(info)) for name, info in db.items()]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

def best_profitable(db: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any], float]:
    ranked = rank_assets(db, score_profitability)
    name, score = ranked[0]
    return name, db[name], score

def best_sustainable(db: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any], float]:
    ranked = rank_assets(db, score_sustainability)
    name, score = ranked[0]
    return name, db[name], score

def filter_by_trend(db: Dict[str, Dict[str, Any]], trend: str) -> List[str]:
    trend = trend.lower()
    return [name for name, info in db.items() if info.get("price_trend","").lower() == trend]

def explain_profitability(name: str, info: Dict[str, Any]) -> str:
    reasons = []
    if info.get("price_trend") == "rising":
        reasons.append("price trend is rising")
    elif info.get("price_trend") == "stable":
        reasons.append("price is stable (lower risk than falling)")
    else:
        reasons.append("price is falling (higher risk)")
    if info.get("market_cap") == "high":
        reasons.append("strong (high) market cap indicating liquidity")
    elif info.get("market_cap") == "medium":
        reasons.append("moderate market cap")
    else:
        reasons.append("small market cap (more volatile)")
    return f"{name} looks profitable because its " + " and ".join(reasons) + "."

def explain_sustainability(name: str, info: Dict[str, Any]) -> str:
    energy = info.get("energy_use")
    sus = info.get("sustainability_score")
    return (
        f"{name} looks sustainable due to {energy} energy use "
        f"and a sustainability score of {sus:.1f}/1.0."
    )

# --------------------------
# 4) Intent detection (very simple keyword matching)
# --------------------------
def detect_intent(query: str) -> str:
    q = query.lower().strip()
    if any(k in q for k in ["sustainable", "eco", "green", "environment"]):
        return "sustainable_recommendation"
    if any(k in q for k in ["profit", "profitable", "make money", "gains"]):
        return "profit_recommendation"
    if "trending up" in q or ("trending" in q and "up" in q) or "rising" in q:
        return "list_trending_up"
    if "most sustainable" in q or "top sustainable" in q:
        return "top_sustainable"
    if "help" in q or "what can you do" in q:
        return "help"
    if "data" in q or "show" in q:
        return "show_data"
    return "fallback"

# --------------------------
# 5) Response generation
# --------------------------
def handle_query(query: str) -> str:
    intent = detect_intent(query)
    if intent == "sustainable_recommendation":
        name, info, _ = best_sustainable(crypto_db)
        expl = explain_sustainability(name, info)
        return (
            f"{name} ({info.get('ticker')}) 🌱 — {expl} "
            f"\n{DISCLAIMER}"
        )
    elif intent == "profit_recommendation":
        name, info, _ = best_profitable(crypto_db)
        expl = explain_profitability(name, info)
        return (
            f"{name} ({info.get('ticker')}) 🚀 — {expl} "
            f"\n{DISCLAIMER}"
        )
    elif intent == "list_trending_up":
        ups = filter_by_trend(crypto_db, "rising")
        if ups:
            listed = ", ".join(ups)
            return f"Trending up 📈: {listed}. \n{DISCLAIMER}"
        return "None are trending up at the moment. \n" + DISCLAIMER
    elif intent == "top_sustainable":
        name, info, _ = best_sustainable(crypto_db)
        return f"Most sustainable right now: {name} ({info.get('ticker')}) 🌍. \n{DISCLAIMER}"
    elif intent == "show_data":
        rows = []
        for n, d in crypto_db.items():
            rows.append(
                f"- {n}: trend={d['price_trend']}, mcap={d['market_cap']}, energy={d['energy_use']}, "
                f"sustainability={d['sustainability_score']:.1f}/1.0"
            )
        return "Here’s my dataset:\n" + "\n".join(rows)
    elif intent == "help":
        return (
            f"I can help with:\n"
            f"• Profitability picks (e.g., 'Which coin is most profitable?')\n"
            f"• Sustainability picks (e.g., 'What's the most sustainable coin?')\n"
            f"• Trends (e.g., 'Which crypto is trending up?')\n"
            f"Try me!"
        )
    else:
        return (
            "I didn't quite get that. Try asking about profitability, sustainability, or trends. "
            "For example: 'Which crypto is trending up?'"
        )

# --------------------------
# 6) CLI loop (optional)
# --------------------------
def chat_loop() -> None:
    print(OPENING_LINE)
    print(DISCLAIMER)
    print("Type 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            print(f"{BOT_NAME}: Bye! 👋")
            break
        reply = handle_query(user)
        print(f"{BOT_NAME}: {reply}\n")

if __name__ == "__main__":
    chat_loop()
    # Uncomment to run interactive chat in terminal/IDE
    # chat_loop()
    # Quick demo:
    demo_questions = [
        "Which crypto should I buy for long-term growth?",
        "What's the most sustainable coin?",
        "Which crypto is trending up?",
        "Show me your data",
    ]
    for q in demo_questions:
        print(f"You: {q}")
        print(f"{BOT_NAME}: {handle_query(q)}\n")
