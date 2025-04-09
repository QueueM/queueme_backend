import pandas as pd
from sklearn.cluster import KMeans
from shopServiceApp.models import ServiceBookingDetailsModel

def segment_users(n_clusters=3):
    """
    Segments users into clusters based on how many bookings they've made.
    Adjusts the number of clusters automatically.
    """
    qs = ServiceBookingDetailsModel.objects.values('user_id')
    df = pd.DataFrame(list(qs))
    if df.empty:
        raise ValueError("No booking data available for segmentation.")
    
    booking_counts = df.groupby('user_id').size().reset_index(name='booking_count')
    usable_clusters = min(n_clusters, len(booking_counts))
    if usable_clusters < 1:
        raise ValueError("Not enough user data for clustering.")
    
    model = KMeans(n_clusters=usable_clusters, random_state=42)
    booking_counts['cluster'] = model.fit_predict(booking_counts[['booking_count']])
    return booking_counts.to_dict(orient='records')

def calculate_for_shop(instance):
    """
    Returns personalization data for the given shop instance.
    This is a stub implementation—replace it with your actual logic.
    """
    shop_name = getattr(instance, 'name', 'Shop')
    return {
        "welcome_message": f"Welcome back, {shop_name}!",
        "suggested_layout": "modern"
    }
