import json

from services.ai.client import ask
from services.ai.promt import EXTRACT_FEATURES_PROMPT
from services.ai.models import ProductFeatures
from services.ai.parser import parse_json

def extract_features(product: str) -> ProductFeatures:

    prompt = EXTRACT_FEATURES_PROMPT.format(
        product=product,
    )

    response = ask(prompt)
    print("========== AI RESPONSE ==========")
    print(response)
    print("=================================")


    try:
        data = parse_json(response)

    except ValueError as e:
        print("========== AI JSON ERROR ==========")
        print(e)
        print("===================================")

        return ProductFeatures(
            product_type="",
            purpose="",
            features=[],
            exclude=[],
        )

    return ProductFeatures(
        product_type=data["product_type"],
        purpose=data["purpose"],
        features=data["features"],
        exclude=data["exclude"],
    )