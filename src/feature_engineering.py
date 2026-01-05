import numpy as np
import pandas as pd

def feature_engineering(df):

    # 🔹 Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # 🔹 Create day_type correctly (FIXED)
    df['day_type'] = np.where(
        df['order_date'].dt.weekday >= 5,
        "Weekend",
        "Weekday"
    )

    # 🔹 Convert order_time to datetime
    df['order_time'] = pd.to_datetime(df['order_time'])

    # 🔹 Extract hour
    df['order_hour'] = df['order_time'].dt.hour

    # 🔹 Peak / Non-Peak
    df['peak_hour'] = np.where(
        df['order_hour'].between(12, 14) |
        df['order_hour'].between(19, 22),
        "Peak",
        "Non-Peak"
    )

    # 🔹 Delivery performance
    df['delivery_performance'] = np.where(
        df['delivery_time_min'] <= 30,
        "On-Time",
        "Delayed"
    )

    print("Feature Engineering Completed")
    return df
