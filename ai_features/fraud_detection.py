import pandas as pd
from sklearn.ensemble import IsolationForest
from shopServiceApp.models import ServiceBookingDetailsModel

def check_booking():
    """
    Detect anomalies in booking/payment data using Isolation Forest.
    Assumes ServiceBookingDetailsModel has 'price' and 'final_amount'.
    """
    qs = ServiceBookingDetailsModel.objects.all().values('id', 'price', 'final_amount')
    df = pd.DataFrame(list(qs))
    if df.empty:
        # Instead of raising an error, return an empty list if no booking data is available.
        return []
    df['ratio'] = df['final_amount'] / df['price']
    iso = IsolationForest(contamination=0.05)
    df['anomaly'] = iso.fit_predict(df[['ratio']])
    anomalies = df[df['anomaly'] == -1]
    return anomalies.to_dict(orient='records')

# Add alias so that "from ai_features.fraud_detection import detect_fraud" works.
detect_fraud = check_booking
