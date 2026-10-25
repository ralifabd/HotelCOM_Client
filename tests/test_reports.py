from hotel_client.connection import HotelConnection
from hotel_client.reports import get_hotel_statistics


def test_hotel_statistics_returns_dictionary():
    with HotelConnection() as hotel:
        stats = get_hotel_statistics(hotel)

        assert isinstance(stats, dict)

def test_hotel_statistics_contains_room_counts():
    with HotelConnection() as hotel:
        stats = get_hotel_statistics(hotel)

        assert "totalRooms" in stats
        assert "availableRooms" in stats
        assert "occupiedRooms" in stats


def test_hotel_statistics_contains_booking_counts():
    with HotelConnection() as hotel:
        stats = get_hotel_statistics(hotel)

        assert "confirmedBookings" in stats
        assert "checkedInBookings" in stats