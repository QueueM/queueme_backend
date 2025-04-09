# ai_features/forecasting.py

import pandas as pd
from prophet import Prophet
from django.utils import timezone
from shopServiceApp.models import ServiceBookingDetailsModel

def _run_prophet(df: pd.DataFrame, periods: int):
    """
    Internal helper: fit Prophet on df (with columns ds, y) and forecast `periods` into the future.
    Returns a list of dicts with keys ds, yhat, yhat_lower, yhat_upper.
    """
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    return result.to_dict(orient='records')

def forecast_bookings(periods: int = 30):
    """
    Forecast future booking counts using Prophet across all services.
    """
    # Pull all booking dates
    qs = ServiceBookingDetailsModel.objects.all().values('booking_date')
    df = pd.DataFrame(list(qs))
    if df.empty:
        return []

    # Prepare for Prophet
    df['ds'] = pd.to_datetime(df['booking_date'])
    df = df[['ds']]
    df['y'] = 1
    daily = df.groupby('ds', as_index=False).agg({'y': 'sum'})

    return _run_prophet(daily, periods)

def calculate_for_service(service, periods: int = 30):
    """
    Forecast future bookings for a specific service.
    """
    qs = ServiceBookingDetailsModel.objects.filter(service=service).values('booking_date')
    df = pd.DataFrame(list(qs))
    if df.empty:
        return []

    df['ds'] = pd.to_datetime(df['booking_date'])
    df = df[['ds']]
    df['y'] = 1
    daily = df.groupby('ds', as_index=False).agg({'y': 'sum'})

    return _run_prophet(daily, periods)

def calculate_for_category(category, periods: int = 30):
    """
    Forecast future bookings aggregated across all services in a category.
    """
    qs = ServiceBookingDetailsModel.objects.filter(service__category=category).values('booking_date')
    df = pd.DataFrame(list(qs))
    if df.empty:
        return []

    df['ds'] = pd.to_datetime(df['booking_date'])
    df = df[['ds']]
    df['y'] = 1
    daily = df.groupby('ds', as_index=False).agg({'y': 'sum'})

    return _run_prophet(daily, periods)
