import json

from hotel_client.connection import HotelConnection
from hotel_client.bookings import (
    create_booking,
    get_booking_info,
    update_booking,
    calculate_booking_price,
    apply_discount,
    book_room,
    cancel_booking,
    check_in,
    check_out,
)


def test_create_booking_returns_id():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            102,
            "Абдуллин Ралиф",
            "2030-06-10",
            "2030-06-15",
        )

        assert booking_id > 0

        booking = get_booking_info(hotel, booking_id)
        assert booking["guestName"] == "Абдуллин Ралиф"


def test_update_booking_dates():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            103,
            "Абдуллин Ралиф2",
            "2030-07-10",
            "2030-07-15",
        )

        assert booking_id > 0

        result = update_booking(
            hotel,
            booking_id,
            "2030-07-11",
            "2030-07-16",
        )
        assert result is True


def test_calculate_booking_price():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            104,
            "Price Guest",
            "2030-08-10",
            "2030-08-12",
        )

        assert booking_id > 0
        price = calculate_booking_price(hotel, booking_id)
        assert price >= 0


def test_apply_discount():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            105,
            "Discount Guest",
            "2030-09-10",
            "2030-09-12",
        )

        assert booking_id > 0
        assert apply_discount(hotel, booking_id, 10.0) is True


def test_book_room_mvp():
    with HotelConnection() as hotel:
        result = book_room(hotel, 101, "MVP Guest")
        assert result is True


def test_cancel_booking_rejects_unknown_room():
    with HotelConnection() as hotel:
        assert cancel_booking(hotel, 999999) is False


def test_check_in_and_check_out():
    with HotelConnection() as hotel:
        booking_id = create_booking(
            hotel,
            106,
            "Stay Guest",
            "2030-10-10",
            "2030-10-12",
        )

        assert booking_id > 0
        assert check_in(hotel, booking_id) is True
        assert check_out(hotel, booking_id) is True