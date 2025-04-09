import pandas as pd
from surprise import SVD, Dataset, Reader
from shopServiceApp.models import ServiceBookingDetailsModel, ShopServiceDetailsModel

def train_recommendation_model():
    """
    Train a collaborative filtering model using booking data.
    Since ServiceBookingDetailsModel does not have a 'rating' field,
    we compute a synthetic rating as: final_amount / price.
    If no data exists, return None.
    """
    qs = ServiceBookingDetailsModel.objects.all().values('user_id', 'service_id', 'price', 'final_amount')
    df = pd.DataFrame(list(qs))
    if df.empty:
        # No booking data: return None instead of raising an error.
        return None
    
    # Compute synthetic rating; avoid division by zero.
    df['rating'] = df.apply(lambda row: row['final_amount'] / row['price'] if row['price'] else 0, axis=1)
    
    # Adjust rating scale to 0-1; modify if needed.
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df[['user_id', 'service_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    return algo

def get_recommendations_for_user(user_id, algo, top_n=5):
    """
    Predict ratings for all services and return the top N recommendations.
    """
    all_service_ids = list(ShopServiceDetailsModel.objects.all().values_list('id', flat=True))
    predictions = []
    for service_id in all_service_ids:
        pred = algo.predict(user_id, service_id)
        predictions.append((service_id, pred.est))
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:top_n]

def get_marketing_offers(user_id, recommendations):
    """
    Generate personalized marketing offers based on recommendations.
    """
    offers = []
    for service_id, predicted_rating in recommendations:
        offer = {
            "service_id": service_id,
            "offer": f"Get 10% off on service {service_id} exclusively for you!",
            "predicted_rating": predicted_rating
        }
        offers.append(offer)
    return offers

def calculate_for_shop(instance):
    """
    Calculates recommendations for a given shop instance.
    Expects the instance to have a 'user_id' attribute; if not, falls back to instance.pk.
    If there is no booking data, returns an empty list.
    """
    user_id = getattr(instance, 'user_id', None)
    if user_id is None:
        user_id = getattr(instance, 'pk', None)
    if user_id is None:
        raise ValueError("Instance does not have a valid user identifier.")
    
    algo = train_recommendation_model()
    if not algo:
        return []  # Return an empty list when no booking data is available.
    
    recommendations = get_recommendations_for_user(user_id, algo, top_n=5)
    offers = get_marketing_offers(user_id, recommendations)
    return offers
