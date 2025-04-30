def evaluate_summary(summary: str, reference: str) -> float:
    """
    Return a pseudo-accuracy score by comparing lengths
    (replace with ROUGE/BERTScore for production).
    """
    ratio = len(summary) / (len(reference) + 1)
    return min(ratio, 1.0)
