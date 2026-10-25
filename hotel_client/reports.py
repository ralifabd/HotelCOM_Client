import json


def get_hotel_statistics(hotel) -> dict:
    """Возвращает статистику по номерам и бронированиям."""
    result = hotel.GetHotelStatistics()

    if isinstance(result, dict):
        return result

    return json.loads(result)