import streamlit as st
import pandas as pd


# Page config
#
st.set_page_config(
    page_title="Online Food Delivery – Analyst Tasks",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Online Food Delivery – Analyst Tasks Dashboard")


# Load cleaned data

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cleaned_food_orders.csv")

df = load_data()

# City filter (multi-select)
city = st.sidebar.multiselect(
    "Select City",
    options=df['city'].unique(),
    default=df['city'].unique()
)

# Cuisine filter
cuisine = st.sidebar.multiselect(
    "Select Cuisine",
    options=df['cuisine_type'].unique(),
    default=df['cuisine_type'].unique()
)

# Order status filter (Delivered / Cancelled)
order_status = st.sidebar.multiselect(
    "Order Status",
    options=df['order_status'].unique(),
    default=df['order_status'].unique()
)


# Applying filters to df

df_filtered = df[
    (df['city'].isin(city)) &
    (df['cuisine_type'].isin(cuisine)) &
    (df['order_status'].isin(order_status))
]



# KPI Calculations


# Total numb of orders
total_orders = df_filtered.shape[0]

# Total reve
total_revenue = df_filtered['order_value'].sum()

# Average order value
avg_order_value = df_filtered['order_value'].mean()

# Average delivery time
avg_delivery_time = df_filtered['delivery_time_min'].mean()

# Cancellation rate (%)
cancellation_rate = (
    df_filtered['order_status']
    .value_counts(normalize=True)
    .get('Cancelled', 0) * 100
)

# Average delivery rating
avg_delivery_rating = df_filtered['delivery_rating'].mean()

# Average profit margin percentage
profit_margin = df_filtered['profit_margin'].mean()


# KPI Display (Cards)

st.subheader("📌 Key Performance Indicators")

# 1st row of KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} mins")

# 2nd row of KPIs
col5, col6, col7 = st.columns(3)
col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}")
col7.metric("Profit Margin %", f"{profit_margin:.2f}%")


# Charts Section

st.divider()
st.subheader(" Business Insights")

# Orders by Day Type (Weekend vs Weekday)
orders_day = df_filtered.groupby('day_type')['order_id'].count()
st.bar_chart(orders_day)

# Revenue by City
revenue_city = (
    df_filtered.groupby('city')['order_value']
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(revenue_city)

# Peak hour demand
peak_orders = df_filtered.groupby('peak_hour')['order_id'].count()
st.bar_chart(peak_orders)

# Payment mode preference
payment_pref = df_filtered['payment_mode'].value_counts()
st.bar_chart(payment_pref)

# View raw filtered data

with st.expander(" View Filtered Data"):
    st.dataframe(df_filtered)

# Sidebar – Analysis Dropdown

st.sidebar.header("📊 Select Analysis")

analysis_option = st.sidebar.selectbox(
    "Choose Analyst Task",
    [
        "Top-Spending Customers",
        "Age Group vs Order Value",
        "Weekend vs Weekday Orders",
        "Monthly Revenue Trend",
        "Discount Impact on Profit",
        "High-Revenue Cities & Cuisines",
        "Avg Delivery Time by City",
        "Distance vs Delivery Delay",
        "Delivery Rating vs Delivery Time",
        "Top-Rated Restaurants",
        "Cancellation Rate by Restaurant",
        "Cuisine-wise Performance",
        "Peak Hour Demand",
        "Payment Mode Preference",
        "Cancellation Reason Analysis"
    ]
)

  
# ANALYST TASKS LOGIC
  

# 1️⃣ Top-Spending Customers
if analysis_option == "Top-Spending Customers":
    st.subheader("💰 Top-Spending Customers")
    data = (
        df.groupby("customer_id")["order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(data)

# 2️⃣ Age Group vs Order Value
elif analysis_option == "Age Group vs Order Value":
    st.subheader("👥 Age Group vs Order Value")
    data = df.groupby("customer_age")["order_value"].mean()
    st.bar_chart(data)

# 3️⃣ Weekend vs Weekday Orders
elif analysis_option == "Weekend vs Weekday Orders":
    st.subheader("📅 Weekend vs Weekday Orders")
    data = df.groupby("day_type")["order_id"].count()
    st.bar_chart(data)

# 4️⃣ Monthly Revenue Trend
elif analysis_option == "Monthly Revenue Trend":
    st.subheader("📈 Monthly Revenue Trend")
    df["month"] = pd.to_datetime(df["order_date"]).dt.to_period("M").astype(str)
    data = df.groupby("month")["order_value"].sum()
    st.line_chart(data)

# 5️⃣ Discount Impact on Profit
elif analysis_option == "Discount Impact on Profit":
    st.subheader("🏷 Discount Impact on Profit")
    data = df.groupby("discount_applied")["profit_margin_pct"].mean()
    st.bar_chart(data)

# 6️⃣ High-Revenue Cities & Cuisines
elif analysis_option == "High-Revenue Cities & Cuisines":
    st.subheader("🏙 High-Revenue Cities")
    city_data = df.groupby("city")["order_value"].sum()
    st.bar_chart(city_data)

    st.subheader("🍽 High-Revenue Cuisines")
    cuisine_data = df.groupby("cuisine_type")["order_value"].sum()
    st.bar_chart(cuisine_data)

# 7️⃣ Avg Delivery Time by City
elif analysis_option == "Avg Delivery Time by City":
    st.subheader("🚴 Avg Delivery Time by City")
    data = df.groupby("city")["delivery_time_min"].mean()
    st.bar_chart(data)

# 8️⃣ Distance vs Delivery Delay
elif analysis_option == "Distance vs Delivery Delay":
    st.subheader("📍 Distance vs Delivery Delay")
    st.scatter_chart(df[["distance_km", "delivery_time_min"]])

# 9️⃣ Delivery Rating vs Delivery Time
elif analysis_option == "Delivery Rating vs Delivery Time":
    st.subheader("⭐ Delivery Rating vs Delivery Performance")
    data = df.groupby("delivery_performance")["delivery_rating"].mean()
    st.bar_chart(data)

# 🔟 Top-Rated Restaurants
elif analysis_option == "Top-Rated Restaurants":
    st.subheader("🏆 Top-Rated Restaurants")
    data = (
        df.groupby("restaurant_name")["restaurant_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(data)

# 1️⃣1️⃣ Cancellation Rate by Restaurant
elif analysis_option == "Cancellation Rate by Restaurant":
    st.subheader("❌ Cancellation Rate by Restaurant")
    data = (
        df.groupby("restaurant_name")["order_status"]
        .apply(lambda x: (x == "Cancelled").mean() * 100)
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(data)

# 1️⃣2️⃣ Cuisine-wise Performance
elif analysis_option == "Cuisine-wise Performance":
    st.subheader("🍴 Cuisine-wise Performance")
    data = df.groupby("cuisine_type")["order_value"].mean()
    st.bar_chart(data)

# 1️⃣3️⃣ Peak Hour Demand
elif analysis_option == "Peak Hour Demand":
    st.subheader("⏰ Peak Hour Demand")
    data = df.groupby("peak_hour")["order_id"].count()
    st.bar_chart(data)

# 1️⃣4️⃣ Payment Mode Preference
elif analysis_option == "Payment Mode Preference":
    st.subheader("💳 Payment Mode Preference")
    data = df["payment_mode"].value_counts()
    st.bar_chart(data)

# 1️⃣5️⃣ Cancellation Reason Analysis
elif analysis_option == "Cancellation Reason Analysis":
    st.subheader("🛑 Cancellation Reason Analysis")
    data = df["cancellation_reason"].value_counts()
    st.bar_chart(data)

  
# Raw data view (optional)
  
with st.expander("📄 View Raw Data"):
    st.dataframe(df)
