import numpy as np

def clean_data(df):

    # standarize clum name
    df.columns = df.columns.str.lower().str.strip()

    # missing value
    df['delivery_time_min'].fillna(df['delivery_time_min'].median(), inplace=True)

    df['delivery_rating'].fillna(df['delivery_rating'].mean(),inplace=True)

    df['payment_mode'].fillna(df['payment_mode'].mode()[0],inplace=True)

    df.loc[df['delivery_rating'] > 5, 'delivery_rating'] = 5
    df.loc[df['profit_margin'] < 0, 'profit_margin'] = 0

     # 🔹 Outlier capping (order_value)
    q1 = df['order_value'].quantile(0.25)
    q3 = df['order_value'].quantile(0.75)
    iqr = q3 - q1
    upper_limit = q3 + 1.5 * iqr

    df['order_value'] = np.where(
        df['order_value'] > upper_limit,
        upper_limit,
        df['order_value']
    )

    print(" Data Cleaning Completed")
    return df

