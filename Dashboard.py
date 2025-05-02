import streamlit as st
st.title("Data E-Commerce")

# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.graph_objects as go

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("C:/Users/sandi/Downloads/orders_gabungan_df.csv")
customers_df=pd.read_csv("C:/Users/sandi/Downloads/customers_dataset.csv")
sellers_df=pd.read_csv("C:/Users/sandi/Downloads/sellers_df.csv")
geolocation_df=pd.read_csv("C:/Users/sandi/Downloads/geolocation_df.csv")

# Pilih tipe pembayaran secara manual
payment_type_selected = 'credit_card'  # Ganti dengan tipe pembayaran yang kamu inginkan, misalnya 'credit_card'

# Filter data berdasarkan tipe pembayaran yang dipilih
filtered_df = df[df['payment_type'] == payment_type_selected]

# 1. Distribusi Jumlah Pesanan Berdasarkan Tipe Pembayaran
order_count_by_payment_type = df['payment_type'].value_counts().reset_index()
order_count_by_payment_type.columns = ['payment_type', 'order_count']
fig = px.bar(order_count_by_payment_type, x='payment_type', y='order_count', 
             title='Distribusi Pesanan Berdasarkan Tipe Pembayaran', 
             color='payment_type', labels={'order_count': 'Jumlah Pesanan'})
st.plotly_chart(fig)

# Distribusi status pesanan
order_status_count = df['order_status'].value_counts().reset_index()
order_status_count.columns = ['order_status', 'count']
fig = px.pie(order_status_count, names='order_status', values='count', 
             title='Distribusi Status Pesanan')
st.plotly_chart(fig)

# Menghitung waktu pengiriman dan apakah tepat waktu
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
df['delivery_time_diff'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
df['on_time'] = df['delivery_time_diff'] <= 0  # True jika tepat waktu

# Visualisasi pengiriman tepat waktu
on_time_count = df['on_time'].value_counts().reset_index()
on_time_count.columns = ['on_time', 'count']
fig = px.pie(on_time_count, names='on_time', values='count', 
             title='Pengiriman Tepat Waktu vs Terlambat')
st.plotly_chart(fig)

# Distribusi skor ulasan
fig = px.histogram(df, x='review_score', nbins=5, title='Distribusi Skor Ulasan')
st.plotly_chart(fig)


# Sidebar untuk customers
st.sidebar.header("⚙️ Pengaturan Visualisasi Customers")
all_customer_states = sorted(customers_df['customer_state'].unique())
selected_customer_states = st.sidebar.multiselect(
    "Pilih state untuk ditampilkan:",
    options=all_customer_states,
    default=all_customer_states  # default: semua state
)

# Sidebar untuk sellers
st.sidebar.header("⚙️ Pengaturan Visualisasi Sellers")
all_seller_states = sorted(sellers_df['seller_state'].unique())
selected_seller_states = st.sidebar.multiselect(
    "Pilih state untuk ditampilkan:",
    options=all_seller_states,
    default=all_seller_states  # default: semua state
)

# Filter data sesuai pilihan state (customers)
filtered_customer_df = customers_df[customers_df['customer_state'].isin(selected_customer_states)]

# Filter data sesuai pilihan state (sellers)
filtered_seller_df = sellers_df[sellers_df['seller_state'].isin(selected_seller_states)]

# Hitung jumlah customer per state (customers)
customer_per_state = filtered_customer_df['customer_state'].value_counts().sort_values(ascending=False)

# Hitung jumlah seller per state (sellers)
seller_per_state = filtered_seller_df['seller_state'].value_counts().sort_values(ascending=False)

# Tampilkan judul
st.title("📊 Jumlah Customers dan Sellers per State")

# Tampilkan chart Customers per State (Plotly)
st.subheader("Jumlah Customers per State")
fig_customers = px.bar(
    x=customer_per_state.index,
    y=customer_per_state.values,
    labels={'x': 'State', 'y': 'Jumlah Customers'},
    title='Jumlah Customers per State',
    color_discrete_sequence=['green']  # Set warna hijau untuk customers
)
st.plotly_chart(fig_customers)

# Tampilkan chart Sellers per State (Plotly)
st.subheader("Jumlah Sellers per State")
fig_sellers = px.bar(
    x=seller_per_state.index,
    y=seller_per_state.values,
    labels={'x': 'State', 'y': 'Jumlah Sellers'},
    title='Jumlah Sellers per State',
    color_discrete_sequence=['red']  # Set warna merah untuk sellers
)
st.plotly_chart(fig_sellers)

