HIGH_RISK_KEYWORDS = ["indemnify", "penalty", "liquidated damages", "termination for convenience"]

def flag_high_risk(text: str) -> list[str]:
    found = [kw for kw in HIGH_RISK_KEYWORDS if kw.lower() in text.lower()]
    return found
