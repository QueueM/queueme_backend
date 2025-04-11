import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
from shopServiceApp.models import ServiceBookingDetailsModel

logger = logging.getLogger(__name__)

def check_booking(instance):
    """
    Advanced fraud detection using IsolationForest.

    This function checks if a given booking instance appears anomalous
    based on historical booking data. It does so by:
      - Retrieving all booking records (id, price, final_amount) from ServiceBookingDetailsModel.
      - Converting the data into a pandas DataFrame and cleaning it.
      - Computing a 'ratio' of final_amount/price.
      - Fitting an IsolationForest model to detect anomalies.
      - Checking if the provided instance is flagged as anomalous, either by:
          (a) its id appearing in the anomaly list, or
          (b) its ratio deviating significantly (more than 3 standard deviations)
              from the population mean.

    Args:
        instance: An instance of ServiceBookingDetailsModel to be checked for fraud risk.

    Returns:
        bool: True if the instance is considered anomalous (potential fraud), False otherwise.
    """
    try:
        # Retrieve historical booking data.
        qs = ServiceBookingDetailsModel.objects.all().values('id', 'price', 'final_amount')
        df = pd.DataFrame(list(qs))
        if df.empty:
            logger.warning("No booking data available; defaulting to not anomalous.")
            return False

        # Ensure the fields are numeric and drop any problematic rows.
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['final_amount'] = pd.to_numeric(df['final_amount'], errors='coerce')
        df.dropna(subset=['price', 'final_amount'], inplace=True)
        # Avoid division by zero.
        df = df[df['price'] != 0]
        if df.empty:
            logger.warning("All booking data invalid after cleaning; defaulting to not anomalous.")
            return False

        # Compute the ratio of final_amount to price.
        df['ratio'] = df['final_amount'] / df['price']

        # Fit the IsolationForest model using the ratio.
        iso = IsolationForest(contamination=0.05, random_state=42)
        df['anomaly'] = iso.fit_predict(df[['ratio']])
        anomalies = df[df['anomaly'] == -1]

        # Compute the ratio for the provided instance.
        try:
            instance_price = float(getattr(instance, 'price', None))
            instance_final = float(getattr(instance, 'final_amount', None))
            if not instance_price or instance_price == 0:
                logger.error("Instance price is zero or invalid; cannot compute ratio.")
                return False
            instance_ratio = instance_final / instance_price
        except Exception as e:
            logger.error("Error computing ratio for instance (ID: %s): %s", getattr(instance, 'id', 'N/A'), e)
            return False

        # Advanced check: if the instance ratio deviates significantly from mean.
        ratio_mean = df['ratio'].mean()
        ratio_std = df['ratio'].std()
        if ratio_std > 0 and abs(instance_ratio - ratio_mean) > 3 * ratio_std:
            logger.info("Instance (ID: %s) ratio deviates significantly (instance_ratio: %.3f, mean: %.3f, std: %.3f).",
                        getattr(instance, 'id', 'N/A'), instance_ratio, ratio_mean, ratio_std)
            return True

        # Otherwise, check if the instance ID is among those detected as anomalies.
        if instance.id in anomalies['id'].values:
            logger.info("Instance (ID: %s) is flagged as an anomaly by the model.", instance.id)
            return True

        return False

    except Exception as e:
        logger.exception("Exception in check_booking: %s", e)
        return False

# Create an alias so that this function can be imported as "detect_fraud"
detect_fraud = check_booking
