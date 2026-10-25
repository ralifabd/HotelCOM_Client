
import pythoncom
import pywintypes
import win32com.client


HOTEL_CLSID = "{4f72097e-cf14-45d3-9232-ca002e541fff}"


class HotelConnection:
    """Управляет COM-подключением к гостиничному серверу."""

    def __init__(self):
        self.hotel = None
        self._initialized = False

    def __enter__(self):
        pythoncom.CoInitialize()
        self._initialized = True

        try:
            obj = pythoncom.CoCreateInstance(
                pywintypes.IID(HOTEL_CLSID),
                None,
                pythoncom.CLSCTX_INPROC_SERVER,
                pythoncom.IID_IDispatch,
            )

            self.hotel = win32com.client.Dispatch(obj)
            return self.hotel

        except Exception:
            self.close()
            raise

    def close(self):
        self.hotel = None

        if self._initialized:
            pythoncom.CoUninitialize()
            self._initialized = False

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
