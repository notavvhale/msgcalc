# formulas.py
# Модуль с формулами расчета стоимости доставки

# Константы (объемные коэффициенты)
K_RAIL = 500      # кг/м³ для Ж/Д
K_AIR = 167       # кг/м³ для Авиа (IATA)
K_SEA = 1000      # кг/м³ для Моря (W/M)
K_LDM = 1850      # кг/LDM для Авто
TRUCK_WIDTH = 2.4 # м, ширина еврофуры

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