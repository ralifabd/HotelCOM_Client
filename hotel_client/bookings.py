"""Операции с бронированиями и проживанием."""
import json


def _parse_json(value):
    if isinstance(value, (dict, list)):
        return value
    return json.loads(value)


def create_booking(hotel, room_id: int, guest_name: str, check_in: str, check_out: str) -> int:
    """Создаёт бронирование и возвращает его ID"""
    return int(hotel.CreateBooking(room_id, guest_name, check_in, check_out))


def get_booking_info(hotel, booking_id: int) -> dict:
    """Возвращает сведения о бронировании."""
    return _parse_json(hotel.GetBookingInfo(booking_id))


def update_booking(hotel, booking_id: int, new_check_in: str, new_check_out: str) -> bool:
    """Изменяет даты бронирования."""
    return bool(hotel.UpdateBooking(booking_id, new_check_in, new_check_out))


def calculate_booking_price(hotel, booking_id: int) -> float:
    """Рассчитывает стоимость бронирования."""
    return float(hotel.CalculateBookingPrice(booking_id))


def apply_discount(hotel, booking_id: int, discount: float) -> bool:
    """Применяет скидку в процентах."""
    return bool(hotel.ApplyDiscount(booking_id, discount))


def book_room(hotel, room_id: int, guest_name: str) -> bool:
    """MVP: немедленно заселяет гостя в номер."""
    return bool(hotel.BookRoom(room_id, guest_name))


def cancel_booking(hotel, room_id: int) -> bool:
    """Отменяет подтверждённое бронирование по ID номера.
    В текущем COM-контракте метод принимает room_id, а не booking_id.
    """
    return bool(hotel.CancelBooking(room_id))


def check_in(hotel, booking_id: int) -> bool:
    """Заселяет гостя по ID подтверждённого бронирования."""
    return bool(hotel.CheckIn(booking_id))


def check_out(hotel, booking_id: int) -> bool:
    """Выселяет гостя по ID бронирования."""
    return bool(hotel.CheckOut(booking_id))
