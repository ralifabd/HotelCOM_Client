
from hotel_client.connection import HotelConnection


def test_com_server_connection():
    with HotelConnection() as hotel:
        assert hotel is not None


def test_check_room_method_is_available():
    with HotelConnection() as hotel:
        result = hotel.CheckRoom(101)
        assert result is not None
