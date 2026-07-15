# formulas.py
# Модуль с формулами расчета стоимости доставки

# Константы (объемные коэффициенты)
K_RAIL = 500      # кг/м³ для Ж/Д
K_AIR = 167       # кг/м³ для Авиа (IATA)
K_SEA = 1000      # кг/м³ для Моря (W/M)
K_LDM = 1850      # кг/LDM для Авто
TRUCK_WIDTH = 2.4 # м, ширина еврофуры
DOVOZ_BASE = 5000
DOVOZ_ADD_KM = 90
FEE_SCHEDULE = [
    (200000, 1231), (450000, 2462), (1200000, 4924),
    (2700000, 13541), (4200000, 18465), (5500000, 21344),
    (10000000, 49240), (float('inf'), 73860)
]


def calc_volume(l_m, w_m, h_m, qty):
    return round((l_m * w_m * h_m) * qty, 4)

def calc_customs_fee(t_val_rub):
    for limit, fee in FEE_SCHEDULE:
        if t_val_rub <= limit:
            return fee




#########################
def calculate_volume(length_m, width_m, height_m, quantity):
    """Расчет объема груза в м³"""
    return round(length_m * width_m * height_m * quantity, 4)

def calculate_ldm(length_m, width_m, quantity):
    """Расчет погрузочных метров (LDM)"""
    ldm_per_unit = (length_m * width_m) / TRUCK_WIDTH
    # Стандарт для европаллет
    if length_m <= 1.2 and width_m <= 0.8:
        ldm_per_unit = 0.4
    return round(ldm_per_unit * quantity, 2)

def calculate_chargeable_weight(actual_weight_kg, volume_m3, coefficient):
    """Определение оплачиваемой базы"""
    volumetric_weight = volume_m3 * coefficient
    return max(actual_weight_kg, volumetric_weight)

def calculate_cost(chargeable_weight, rate_per_kg, additional_fee=0):
    """Расчет итоговой стоимости"""
    return round(chargeable_weight * rate_per_kg + additional_fee, 2)
def calc_dovoz(km):
    return DOVOZ_BASE if km <= 20 else DOVOZ_BASE + (km - 20) * DOVOZ_ADD_KM
    
def calculate(cargo, tariffs, rates, customs):
    l_m = cargo["length"] / 1000
    w_m = cargo["width"] / 1000
    h_m = cargo["height"] / 1000

    total_weight = cargo["weight_per_unit"] * cargo["qty"]

    volume = calculate_volume(
    l_m,
    w_m,
    h_m,
    cargo["qty"]
    )

    invoice_rub = cargo["invoice_usd"] * rates["USD_RUB"]
    insurance_rub = cargo["invoice_usd"] * rates["USD_RUB"] * 0.001
    dovoz_cost = calc_dovoz(cargo["dovoz_km"])


    # ===========================
    # Прямое ЖД
    # ===========================

    vw_rail = volume * K_RAIL
    cw_rail = max(total_weight, vw_rail)

    cost_rail_usd = max(
        cw_rail * tariffs["rail_usd_kg"],
        volume * tariffs["rail_usd_m3"]
    ) + tariffs["rail_doc_usd"]

    cost_rail_rub = cost_rail_usd * rates["USD_RUB"] + dovoz_cost

    # ===========================
    # Авиа
    # ===========================

    vw_air = volume * K_AIR
    cw_air = max(total_weight, vw_air)

    cost_air_usd = max(
        cw_air * tariffs["air_usd_kg"],
        200
    )

    cost_air_rub = cost_air_usd * rates["USD_RUB"]

    terminal_air = (
        total_weight * tariffs["air_prr_rub_kg"]
        + 1481.92
        + 724.95
        + 1240.74
    )

    cost_air_total_rub = (
        cost_air_rub
        + terminal_air
        + dovoz_cost
    )

    # ===========================
    # Авто
    # ===========================

    ldm_total = calculate_ldm(
        l_m,
        w_m,
        cargo["qty"]
    )

    vw_road = ldm_total * K_LDM

    cw_road = max(total_weight, vw_road)

    cost_road_usd = (
        cw_road * tariffs["road_usd_kg"]
        + tariffs["road_doc_usd"]
    )

    cost_road_rub = (
        cost_road_usd * rates["USD_RUB"]
        + dovoz_cost
    )

    # ===========================
    # Море + ЖД
    # ===========================

    cw_sea_multi = max(
        total_weight,
        volume * K_SEA
    )

    cw_rail_multi = max(
        total_weight,
        volume * K_RAIL
    )

    thc_rub = (
        volume
        * tariffs["thc_sea_usd_m3"]
        * rates["USD_RUB"]
    )

    doc_sea_rub = (
        tariffs["doc_sea_usd"]
        * rates["USD_RUB"]
    )

    f_rail_rub = (
        cw_rail_multi
        * tariffs["r_rail_usd_m3"]
        * rates["USD_RUB"]
    )

    f_sea_rub = (
        cw_sea_multi
        * tariffs["r_sea_usd_kg"]
        * rates["USD_RUB"]
    )

    cost_multi_rub = (
        thc_rub
        + doc_sea_rub
        + f_rail_rub
        + f_sea_rub
        + dovoz_cost
    )

    results = [
        (
            "🚂 Ж/Д прямая (LCL RW)",
            cost_rail_rub,
            25,
            f"{cw_rail:.0f} кг"
        ),
        (
            "✈️ Авиа прямая (AIR)",
            cost_air_total_rub,
            5,
            f"{cw_air:.0f} кг"
        ),
        (
            "🚢 Море+ЖД (LCL SR)",
            cost_multi_rub,
            35,
            f"Море: {cw_sea_multi:.0f} кг / ЖД: {cw_rail_multi:.0f} кг"
        )
    ]
    return {

        "length_m": l_m,
        "width_m": w_m,
        "height_m": h_m,

        "volume": volume,
        "total_weight": total_weight,

        "invoice_rub": invoice_rub,
        "insurance_rub": insurance_rub,
        "dovoz_cost": dovoz_cost,

        "cost_rail_usd": cost_rail_usd,
        "cost_rail_rub": cost_rail_rub,

        "cost_air_total_rub": cost_air_total_rub,

        "cost_road_rub": cost_road_rub,

        "cost_multi_rub": cost_multi_rub,

        "cw_rail": cw_rail,
        "cw_air": cw_air,
        "cw_road": cw_road,
        "cw_sea_multi": cw_sea_multi,
        "cw_rail_multi": cw_rail_multi,

        "results": results
    }