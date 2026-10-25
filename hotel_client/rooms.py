"""Операции с гостиничными номерами."""

import json

def _parse_json(value):
    """Преобразует JSON-строку от COM-сервера в Python-объект."""
    if isinstance(value, (dict, list)):
        return value
    return json.loads(value)


def check_room(hotel, room_id: int) -> bool:
    """Проверяет, доступен ли номер сейчас."""
    return bool(hotel.CheckRoom(room_id))


def get_room_info(hotel, room_id: int) -> dict:
    """Возвращает информацию о номере."""
    return _parse_json(hotel.GetRoomInfo(room_id))


def get_rooms_by_type(hotel, room_type: str) -> list:
    """Возвращает номера указанного типа."""
    return _parse_json(hotel.GetRoomsByType(room_type))


def find_available_rooms(hotel, check_in: str, check_out: str, room_type: str = "",) -> list:
    """Ищет номера, доступные в указанный период."""
    return _parse_json(
        hotel.FindAvailableRooms(check_in, check_out, room_type)
    )


def set_room_status(hotel, room_id: int, status: str) -> bool:
    """Изменяет статус номера."""
    return bool(hotel.SetRoomStatus(room_id, status))


def add_room(hotel, room_data: dict) -> bool:
    """Добавляет номер по словарю с его параметрами."""
    room_json = json.dumps(room_data, ensure_ascii=False)
    return bool(hotel.AddRoom(room_json))


def update_room(hotel, room_id: int, room_data: dict) -> bool:
    """Обновляет параметры номера."""
    room_json = json.dumps(room_data, ensure_ascii=False)
    return bool(hotel.UpdateRoom(room_id, room_json))


def remove_room(hotel, room_id: int) -> bool:
    """Удаляет номер, если сервер разрешает удаление."""
    return bool(hotel.RemoveRoom(room_id))