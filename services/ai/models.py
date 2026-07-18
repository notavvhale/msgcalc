from dataclasses import dataclass, field


@dataclass
class ProductFeatures:

    product_type: str | None = None

    purpose: str | None = None

    features: list[str] = field(default_factory=list)

    exclude: list[str] = field(default_factory=list)