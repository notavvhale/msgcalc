# customs.py
# Расчет таможенных платежей по ПП РФ №1638 от 23.10.2025

# Сетка таможенных сборов (базовые нормативы)
FEE_SCHEDULE_2026 = [
    (200_000, 2_500),
    (500_000, 5_500),
    (1_000_000, 9_500),
    (2_000_000, 16_000),
    (5_000_000, 28_000),
    (10_000_000, 45_000),
    (float('inf'), 75_000)
]

# Справочник ТН ВЭД (упрощенный)
TNVED_DB = {
    "Промышленное оборудование": {"code": "8479", "duty": 0.0, "vat": 20.0},
    "Станки и механизмы": {"code": "8462", "duty": 5.0, "vat": 20.0},
    "Изделия из пластика": {"code": "3926", "duty": 6.5, "vat": 20.0},
    "Мебель и части мебели": {"code": "9403", "duty": 10.0, "vat": 20.0},
    "Одежда текстильная": {"code": "6201", "duty": 15.0, "vat": 20.0},
    "Обувь": {"code": "6403", "duty": 10.0, "vat": 20.0},
    "Электроника бытовая": {"code": "8516", "duty": 5.0, "vat": 20.0},
    "Автозапчасти": {"code": "8708", "duty": 5.0, "vat": 20.0},
}

def get_k_cb(key_rate=21.0):
    """Коэффициент K_CB в зависимости от ключевой ставки"""
    if key_rate < 8:
        return 0.85
    elif 8 <= key_rate <= 12:
        return 1.0
    elif 12 < key_rate <= 18:
        return 1.2
    else:
        return 1.35

def calculate_customs_fee(t_val_rub, key_rate=21.0):
    """Расчет таможенного сбора"""
    k_cb = get_k_cb(key_rate)
    for limit, base_rate in FEE_SCHEDULE_2026:
        if t_val_rub <= limit:
            return round(base_rate * k_cb, 2)

def calculate_customs_total(invoice_usd, freight_usd, rate_rub, product_category):
    """Полный расчет таможенных платежей"""
    t_val = (invoice_usd + freight_usd) * rate_rub
    product = TNVED_DB.get(product_category, TNVED_DB["Мебель и части мебели"])

    duty = t_val * (product["duty"] / 100)
    vat = (t_val + duty) * (product["vat"] / 100)
    fee = calculate_customs_fee(t_val)

    return {
        "t_val": round(t_val, 2),
        "duty": round(duty, 2),
        "vat": round(vat, 2),
        "fee": round(fee, 2),
        "total": round(duty + vat + fee, 2)
    }