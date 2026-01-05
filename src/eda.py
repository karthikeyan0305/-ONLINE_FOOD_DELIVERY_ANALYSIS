import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(df):

    # Distribution of order values and delivery time

    sns.histplot(df['order_value'], bins=30, kde=True)
    plt.title("Order Value Distribution")
    plt.show()

    # Distance vs delivery delay relationship
    sns.scatterplot(x='distance_km', y='delivery_time_min', data=df)
    plt.title("Distance vs Delivery Time")
    plt.show()

    # City-wise and cuisine-wise order analysis

    df['city'].value_counts().head(10).plot(kind='bar')
    plt.title("Top 10 cities by Orders")
    plt.show()

    print("EDA completed")
    

