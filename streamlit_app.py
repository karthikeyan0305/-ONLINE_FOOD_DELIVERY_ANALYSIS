
import streamlit as st          
import pandas as pd             


# Browser tab title, icon, layout (wide = full screen)
st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    layout="wide"
)

# Dashboard main title
st.title("🍔 Online Food Delivery Analysis Dashboard")


# cache_data -> performance improve (file reload aagadhu)
@st.cache_data
def load_data():
    
    return pd.read_csv("data/processed/cleaned_food_orders.csv")

# Call function and store dataframe
df = load_data()

st.sidebar.header(" Filters")

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
