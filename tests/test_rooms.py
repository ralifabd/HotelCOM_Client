import json

from hotel_client.connection import HotelConnection
from hotel_client.rooms import (
    check_room, get_room_info,get_rooms_by_type, find_available_rooms,
)


def test_check_room_returns_boolean():
    with HotelConnection() as hotel:
        result = check_room(hotel, 101)
        assert isinstance(result, bool)


def test_get_room_info_returns_dictionary():
    with HotelConnection() as hotel:
        room = get_room_info(hotel, 101)

        assert isinstance(room, dict)
        assert room["roomId"] == 101


def test_get_rooms_by_type_returns_list():
    with HotelConnection() as hotel:
        rooms = get_rooms_by_type(hotel, "Standard")

        assert isinstance(rooms, list)
        assert all(room["type"] == "Standard" for room in rooms)


def test_find_available_rooms_returns_list():
    with HotelConnection() as hotel:
        rooms = find_available_rooms(
            hotel,
            "2030-06-10",
            "2030-06-15",
            "Standard",
        )

        assert isinstance(rooms, list)
