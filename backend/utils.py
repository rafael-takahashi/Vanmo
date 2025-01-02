def valida_coordendas(latitude: float, longitude: float) -> bool:
    latitude, longitude = abs(latitude), abs(longitude)
    validacao_lat = (0 <= latitude <= 90)
    validacao_long = (0 <= longitude <= 180)

    return validacao_lat and validacao_long