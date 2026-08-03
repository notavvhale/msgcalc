from services.ai.extractor import extract_features
from services.ai.selector import rank_candidates
from services.tnved import get_by_code
from services.tnved_search import search_candidates


def classify_product(product: str):

    product = product.strip()

    if not product:
        return []

    features = extract_features(product)

    candidates = search_candidates(features)

    if not candidates:
        return []

    # Берём только наиболее подходящие кандидаты из поиска,
    # чтобы не перегружать ИИ большим промптом.
    candidates = candidates[:20]

    ranked = rank_candidates(product, candidates)

    if not ranked:
        return []

    results = []

    for item in ranked:

        info = get_by_code(item["code"])

        if not info:
            continue

        info["confidence"] = item.get("confidence", 0)
        info["reason"] = item.get("reason", "")

        results.append(info)

    return results