from services.ai.extractor import extract_features
from services.tnved_search import search_candidates

features = extract_features(
    "Игровой ноутбук ASUS ROG Strix G16"
)

rows = search_candidates(features)

for row in rows:

    print(
        row["score"],
        row["code"],
        row["description"],
    )