
import json

import pytest

from hotel_client.connection import HotelConnection


def test_book_room_immediately_checks_in_guest():
    with HotelConnection() as hotel:
        result = hotel.BookRoom(101, "Иван Петров")

        assert bool(result) is True

        stats = json.loads(hotel.GetHotelStatistics())
        assert stats["occupiedRooms"] >= 1
        assert stats["checkedInBookings"] >= 1


def test_book_room_rejects_occupied_room():
    with HotelConnection() as hotel:
        assert bool(hotel.BookRoom(101, "Ivan Petrov")) is True

        result = hotel.BookRoom(101, "Maria Ivanova")

        assert bool(result) is False


def test_book_room_rejects_unknown_room():
    with HotelConnection() as hotel:
        result = hotel.BookRoom(999999, "Ivan Petrov")

        assert bool(result) is False


def test_cancel_booking_does_not_cancel_checked_in_guest():
    with HotelConnection() as hotel:
        assert bool(hotel.BookRoom(101, "Ivan Petrov")) is True

        result = hotel.CancelBooking(101)

        assert bool(result) is False

        stats = json.loads(hotel.GetHotelStatistics())
        assert stats["occupiedRooms"] >= 1
        assert stats["checkedInBookings"] >= 1


def test_cancel_booking_cancels_confirmed_reservation():
    with HotelConnection() as hotel:
        booking_id = hotel.CreateBooking(
            102,
            "Maria Ivanova",
            "2030-06-10",
            "2030-06-15",
        )

        assert booking_id > 0

        result = hotel.CancelBooking(102)

        assert bool(result) is True

        booking = json.loads(hotel.GetBookingInfo(booking_id))
        assert booking["status"] == "Cancelled"


def test_cancel_booking_returns_false_when_no_reservation_exists():
    with HotelConnection() as hotel:
        result = hotel.CancelBooking(999999)

        assert bool(result) is False
