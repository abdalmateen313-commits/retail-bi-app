import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail KPI Intelligence App", layout="wide")

st.title("📊 Retail KPI Intelligence App (AI-Powered)")

uploaded_file = st.file_uploader("Upload your Retail CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("File Uploaded Successfully!")

    total_revenue = df["Revenue"].sum()
    total_cost = df["Cost"].sum()
    total_profit = total_revenue - total_cost
    avg_conversion = df["Conversion_Rate"].mean()
    total_units = df["Units_Sold"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("Units Sold", f"{total_units}")
    col4.metric("Avg Conversion", f"{avg_conversion:.2%}")

    st.divider()

    st.subheader("📈 Sales by City")
    city_sales = df.groupby("Store_City")["Revenue"].sum().reset_index()
    fig1 = px.bar(city_sales, x="Store_City", y="Revenue")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Category Performance")
    cat_sales = df.groupby("Category")["Revenue"].sum().reset_index()
    fig2 = px.pie(cat_sales, names="Category", values="Revenue")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📉 Sales Trend")
    df["Date"] = pd.to_datetime(df["Date"])
    trend = df.groupby(df["Date"].dt.date)["Revenue"].sum().reset_index()
    fig3 = px.line(trend, x="Date", y="Revenue")
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Insights & Recommendations")

    insights = []

    if avg_conversion < 0.3:
        insights.append("⚠️ Low conversion rate. Improve staff training or in-store experience.")

    if total_profit < total_revenue * 0.2:
        insights.append("⚠️ Low profitability. Check discount strategy and cost control.")

    top_city = city_sales.sort_values("Revenue", ascending=False).iloc[0]["Store_City"]
    insights.append(f"🏆 Top performing city: {top_city}")

    low_category = cat_sales.sort_values("Revenue").iloc[0]["Category"]
    insights.append(f"📉 Lowest category: {low_category}. Consider promotions or product revamp.")

    for i in insights:
        st.write(i)

    st.divider()

    st.subheader("📂 Data Preview")
    st.dataframe(df.head())

else:
    st.info("Please upload a CSV file to begin.")
