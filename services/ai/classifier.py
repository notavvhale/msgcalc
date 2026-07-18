from services.ai.client import ask
from services.ai.promt import DESCRIPTION_PROMPT


def normalize_product(product: str):

    prompt = DESCRIPTION_PROMPT.format(
        product=product,
    )

    return ask(prompt)