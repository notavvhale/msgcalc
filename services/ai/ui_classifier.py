from services.ai.extractor import extract_features
from services.ai.selector import select_best
from services.tnved import get_by_code
from services.tnved_search import search_candidates


def classify_product(product: str):

    product = product.strip()

    if not product:
        return None

    features = extract_features(product)

    candidates = search_candidates(features)

    if not candidates:
        return None

    result = select_best(product, candidates)

    if not result:
        return None

    info = get_by_code(result["code"])

    if not info:
        return None

    info["confidence"] = result.get("confidence", 0)
    info["reason"] = result.get("reason", "")

    # первые пять найденных вариантов
    info["alternatives"] = candidates[:5]

    return info