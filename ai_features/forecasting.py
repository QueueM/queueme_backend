# File: ai_features/forecasting.py

def generate_forecast(data: dict) -> list[dict]:
    """
    data: {
      'shop_id': int,
      'horizon': int
    }
    Returns a list of forecast points:
      [
        {'date': 'YYYY-MM-DD', 'value': float},
        ...
      ]
    """
    # TODO: implement your forecasting logic here
    raise NotImplementedError("Implement forecasting logic")


def forecast_bookings() -> dict:
    """
    Forecast bookings for all companies (used in companyApp.signals).
    Returns a JSON-serializable dict to store in CompanyDetailsModel.forecast_data.
    """
    # TODO: implement your company-level bookings forecast here
    return {}


def calculate_for_category(category_id: int, horizon: int) -> list[dict]:
    """
    Forecast bookings breakdown for a specific service category over the given horizon.
    Returns a list of forecasted values per period.
    """
    # TODO: implement category-level forecasting logic here
    return []


def calculate_for_service(service_id: int, horizon: int) -> list[dict]:
    """
    Forecast bookings breakdown for a specific service over the given horizon.
    Returns a list of forecasted values per period.
    """
    # TODO: implement service-level forecasting logic here
    return []

