import re

def valida_coordendas(latitude: float, longitude: float) -> bool:
    latitude, longitude = abs(latitude), abs(longitude)
    validacao_lat = (0 <= latitude <= 90)
    validacao_long = (0 <= longitude <= 180)

    return validacao_lat and validacao_long

def valida_placa(placa: str) -> bool:
    # formato ABC-1234
    placa_antiga = r"^[A-Z]{3}-\d{4}$"
    # formato ABC1D23
    placa_mercosul = r"^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$"

    return bool((re.fullmatch(placa_antiga, placa)) or (re.fullmatch(placa_mercosul, placa)))