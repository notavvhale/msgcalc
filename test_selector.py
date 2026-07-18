from services.ai.extractor import extract_features
from services.tnved_search import search_candidates
from services.ai.selector import select_best

product = "Игровой ноутбук ASUS ROG Strix G16"

features = extract_features(product)

candidates = search_candidates(features)

result = select_best(
    product,
    candidates,
)

print(result)