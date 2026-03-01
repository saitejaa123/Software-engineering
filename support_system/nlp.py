import re
from collections import Counter
from typing import Dict, Iterable, Tuple

SEVERITY_KEYWORDS: Dict[str, set] = {
    "critical": {"outage", "breach", "urgent", "cannot login", "payment failed", "service down"},
    "high": {"error", "failed", "not working", "blocked", "escalate"},
    "medium": {"slow", "issue", "problem", "delay", "degraded"},
    "low": {"question", "clarify", "request", "feature", "inquiry"},
}

CATEGORY_KEYWORDS: Dict[str, set] = {
    "billing": {"invoice", "refund", "payment", "charge", "subscription", "billing"},
    "authentication": {"login", "password", "otp", "signin", "access", "2fa"},
    "technical": {"bug", "error", "crash", "api", "integration", "timeout"},
    "shipping": {"delivery", "shipment", "tracking", "courier", "package"},
    "general": set(),
}

SEVERITY_PRIORITY = ("critical", "high", "medium", "low")
SEVERITY_SCORE = {"critical": 100, "high": 70, "medium": 40, "low": 10}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _keyword_hits(clean_text: str, words: Iterable[str]) -> int:
    hits = 0
    for word in words:
        pattern = rf"\b{re.escape(word)}\b"
        if re.search(pattern, clean_text):
            hits += 1
    return hits


def predict_severity(text: str) -> str:
    clean = normalize_text(text)
    scores: Counter = Counter()

    for severity, words in SEVERITY_KEYWORDS.items():
        scores[severity] = _keyword_hits(clean, words)

    if sum(scores.values()) == 0:
        return "medium"

    best_score = max(scores.values())
    candidates = [sev for sev, score in scores.items() if score == best_score]
    for sev in SEVERITY_PRIORITY:
        if sev in candidates:
            return sev
    return "medium"


def predict_category(text: str) -> str:
    clean = normalize_text(text)
    scores: Counter = Counter()
    for category, words in CATEGORY_KEYWORDS.items():
        if category == "general":
            continue
        scores[category] = _keyword_hits(clean, words)

    if sum(scores.values()) == 0:
        return "general"

    return max(scores.items(), key=lambda item: item[1])[0]


def compute_priority(severity: str, sentiment_hint: str = "neutral") -> float:
    base = SEVERITY_SCORE.get(severity, 40)
    sentiment_bonus = {"negative": 8, "neutral": 0, "positive": -5}.get(sentiment_hint, 0)
    return float(max(1, base + sentiment_bonus))


def predict_ticket_labels(text: str, sentiment_hint: str = "neutral") -> Tuple[str, str, float]:
    severity = predict_severity(text)
    category = predict_category(text)
    return severity, category, compute_priority(severity, sentiment_hint)
