from hotel_client.connection import HotelConnection
from hotel_client.bookings import create_booking, apply_discount
from hotel_client.rooms import get_room_info


def test_create_booking_rejects_invalid_dates():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            107,
            "Invalid Date Guest",
            "2030-06-20",
            "2030-06-10",
        )

        assert booking_id == 0


def test_create_booking_rejects_unknown_room():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            999999,
            "Unknown Room Guest",
            "2030-06-10",
            "2030-06-15",
        )

        assert booking_id == 0


def test_apply_discount_rejects_invalid_percentage():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            107,
            "Discount Test Guest",
            "2030-11-10",
            "2030-11-12",
        )

        assert booking_id > 0
        assert apply_discount(hotel, booking_id, 150.0) is False


def test_get_room_info_for_unknown_room():
    with HotelConnection() as hotel:
        try:
            result = get_room_info(hotel, 999999)
        except Exception:
            return

        assert not result