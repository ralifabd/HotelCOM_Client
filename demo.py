import json
import sys
import traceback

from hotel_client.connection import HotelConnection

def parse_json(value):
    """Преобразует JSON-ответ COM-сервера в Python-объект."""
    if isinstance(value, (dict, list)):
        return value

    if isinstance(value, (tuple, list)) and len(value) == 1:
        value = value[0]

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    if isinstance(value, str):
        return json.loads(value)

    raise ValueError(f"Неожиданный формат ответа сервера: {value!r}")


def print_result(title, result):
    print(f"\n{title}")
    print("-" * 55)

    if isinstance(result, (dict, list)):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)


def read_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Введите целое число.")


def read_float(prompt):
    while True:
        value = input(prompt).strip().replace(",", ".")
        try:
            return float(value)
        except ValueError:
            print("Введите число, например 10 или 10.5.")


def read_date(prompt):
    """Принимает дату в формате YYYY-MM-DD."""
    from datetime import date

    while True:
        value = input(prompt).strip()
        try:
            date.fromisoformat(value)
            if len(value) != 10:
                raise ValueError
            return value
        except ValueError:
            print("Неверная дата. Пример правильного формата: 2030-06-10")


def read_json_object(prompt):
    while True:
        value = input(prompt).strip()
        try:
            result = json.loads(value)
            if not isinstance(result, dict):
                raise ValueError("Нужен JSON-объект.")
            return json.dumps(result, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError) as error:
            print(f"Некорректный JSON: {error}")


def pause():
    input("\nНажмите Enter, чтобы вернуться в меню...")


def show_menu():
    print(
        """
=======================================================
       СИСТЕМА БРОНИРОВАНИЯ НОМЕРОВ В ГОСТИНИЦЕ
             Python + C++ ATL/COM
=======================================================
  1.  Проверить подключение к серверу
  2.  Получить информацию о номере
  3.  Получить список номеров по типу
  4.  Найти свободные номера по датам
  5.  Изменить статус номера
  6.  Создать бронирование
  7.  Получить информацию о бронировании
  8.  Изменить даты бронирования
  9.  Рассчитать стоимость бронирования
 10.  Применить скидку
 11.  Отменить бронирование по ID номера
 12.  Заселить гостя по ID бронирования
 13.  Выселить гостя по ID бронирования
 14.  Немедленно заселить гостя (BookRoom, MVP)
 15.  Добавить номер
 16.  Изменить данные номера
 17.  Удалить номер
 18.  Показать статистику гостиницы
  0.  Выход
=======================================================
"""
    )


def run_action(hotel, choice):
    if choice == 1:
        stats = parse_json(hotel.GetHotelStatistics())
        print("Подключение к COM-серверу работает.")
        print_result("Статистика сервера", stats)

    elif choice == 2:
        room_id = read_int("Введите ID номера (например, 101): ")
        result = parse_json(hotel.GetRoomInfo(room_id))
        print_result("Информация о номере", result)

    elif choice == 3:
        room_type = input("Тип номера (например, Standart, Deluxe): ").strip()
        result = parse_json(hotel.GetRoomsByType(room_type))
        print_result("Номера выбранного типа", result)

    elif choice == 4:
        check_in = read_date("Дата заезда (YYYY-MM-DD): ")
        check_out = read_date("Дата выезда (YYYY-MM-DD): ")

        if check_in >= check_out:
            print("Дата выезда должна быть позже даты заезда.")
            return

        room_type = input("Тип номера (Enter — любой тип): ").strip()

        result = parse_json(
            hotel.FindAvailableRooms(check_in, check_out, room_type)
        )
        print_result("Результат поиска", result)

    elif choice == 5:
        room_id = read_int("ID номера: ")
        print("Допустимые статусы: Available, Occupied, Cleaning,")
        print("                    Maintenance, OutOfService")
        status = input("Новый статус: ").strip()

        result = bool(hotel.SetRoomStatus(room_id, status))
        print("Статус изменён." if result else "Статус не изменён.")

    elif choice == 6:
        room_id = read_int("ID номера: ")
        guest = input("Имя гостя: ").strip()
        check_in = read_date("Дата заезда (YYYY-MM-DD): ")
        check_out = read_date("Дата выезда (YYYY-MM-DD): ")

        if not guest:
            print("Имя гостя не может быть пустым.")
            return

        if check_in >= check_out:
            print("Дата выезда должна быть позже даты заезда.")
            return

        booking_id = int(
            hotel.CreateBooking(room_id, guest, check_in, check_out)
        )

        if booking_id > 0:
            print(f"Бронирование успешно создано. ID: {booking_id}")
        else:
            print("Бронирование не создано. Проверьте номер, даты и его доступность.")

    elif choice == 7:
        booking_id = read_int("ID бронирования: ")
        result = parse_json(hotel.GetBookingInfo(booking_id))
        print_result("Информация о бронировании", result)

    elif choice == 8:
        booking_id = read_int("ID бронирования: ")
        check_in = read_date("Новая дата заезда (YYYY-MM-DD): ")
        check_out = read_date("Новая дата выезда (YYYY-MM-DD): ")

        if check_in >= check_out:
            print("Дата выезда должна быть позже даты заезда.")
            return

        result = bool(
            hotel.UpdateBooking(booking_id, check_in, check_out)
        )
        print(
            "Даты бронирования изменены."
            if result
            else "Не удалось изменить даты."
        )

    elif choice == 9:
        booking_id = read_int("ID бронирования: ")
        price = float(hotel.CalculateBookingPrice(booking_id))
        print(f"Стоимость бронирования: {price:.2f}")

    elif choice == 10:
        booking_id = read_int("ID бронирования: ")
        discount = read_float("Скидка в процентах (0–100): ")

        result = bool(hotel.ApplyDiscount(booking_id, discount))
        print(
            "Скидка применена."
            if result
            else "Не удалось применить скидку. Проверьте ID, статус и размер скидки."
        )

    elif choice == 11:
        room_id = read_int("ID номера для отмены бронирования: ")
        print(
            "Внимание: серверный метод CancelBooking принимает ID номера, а не ID бронирования."
        )

        result = bool(hotel.CancelBooking(room_id))
        print(
            "Подтверждённое бронирование отменено."
            if result
            else "Подтверждённое бронирование для этого номера не найдено или отмена невозможна."
        )

    elif choice == 12:
        booking_id = read_int("ID подтверждённого бронирования: ")
        result = bool(hotel.CheckIn(booking_id))
        print(
            "Гость заселён."
            if result
            else "Не удалось заселить гостя. Проверьте статус бронирования и номера."
        )

    elif choice == 13:
        booking_id = read_int("ID бронирования для выселения: ")
        result = bool(hotel.CheckOut(booking_id))
        print(
            "Гость выселен. Номер переведён в статус Cleaning."
            if result
            else "Не удалось выселить гостя. Проверьте ID и статус бронирования."
        )

    elif choice == 14:
        room_id = read_int("ID свободного номера: ")
        guest = input("Имя гостя: ").strip()

        if not guest:
            print("Имя гостя не может быть пустым.")
            return

        result = bool(hotel.BookRoom(room_id, guest))
        print(
            "Гость немедленно заселён."
            if result
            else "Не удалось заселить гостя. Возможно, номер занят."
        )

    elif choice == 15:
        print(
            "Введите JSON с полями, поддерживаемыми AddRoom "
            "в вашем C++ сервере."
        )
        room_json = read_json_object("JSON нового номера: ")
        result = bool(hotel.AddRoom(room_json))
        print("Номер добавлен." if result else "Не удалось добавить номер.")

    elif choice == 16:
        room_id = read_int("ID номера для изменения: ")
        print(
            "Введите JSON с полями, поддерживаемыми UpdateRoom "
            "в вашем C++ сервере."
        )
        room_json = read_json_object("JSON с новыми данными: ")
        result = bool(hotel.UpdateRoom(room_id, room_json))
        print(
            "Данные номера обновлены."
            if result
            else "Не удалось обновить номер."
        )

    elif choice == 17:
        room_id = read_int("ID номера для удаления: ")
        confirm = input(
            f"Удалить номер {room_id}? Введите ДА для подтверждения: "
        ).strip().upper()

        if confirm != "ДА":
            print("Удаление отменено.")
            return

        result = bool(hotel.RemoveRoom(room_id))
        print("Номер удалён." if result else "Не удалось удалить номер.")

    elif choice == 18:
        result = parse_json(hotel.GetHotelStatistics())
        print_result("Статистика гостиницы", result)

    else:
        print("Неизвестный пункт меню.")


def main():
    print("Запуск Python-клиента гостиничной системы...")

    try:
        with HotelConnection() as hotel:
            print("COM-подключение установлено.")

            while True:
                show_menu()
                choice = input("Выберите действие: ").strip()

                if choice == "0":
                    print("Работа программы завершена.")
                    break

                try:
                    run_action(hotel, int(choice))
                except ValueError as error:
                    print(f"\nОшибка данных: {error}")
                except Exception as error:
                    print("\nОперация завершилась ошибкой.")
                    print(f"Тип: {type(error).__name__}")
                    print(f"Описание: {error}")

                pause()

    except Exception as error:
        print("\nНе удалось подключиться к COM-серверу.")
        print(f"Тип: {type(error).__name__}")
        print(f"Описание: {error}")
        print(
            "\nПроверьте регистрацию HotelServer.dll, разрядность Python "
            "и успешность сборки проекта."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
