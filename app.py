import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail KPI Command Center", layout="wide")

# --- TITLE ---
st.title("🚀 Retail KPI Command Center (AI Edition)")
st.caption("Upload your data. Get insights. Take action.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload your Retail CSV", type=["csv"])

if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file)

        st.success("File Uploaded Successfully!")

        # --- REQUIRED COLUMNS CHECK ---
        required_columns = [
            "Date", "Store_ID", "Store_City", "Category", "Product_ID",
            "Units_Sold", "Revenue", "Cost", "Discount",
            "Customer_Footfall", "Conversion_Rate", "Employee_Count"
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
            st.stop()

        # --- DATA PREP ---
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

        # --- KPI CALCULATIONS ---
        total_revenue = df["Revenue"].sum()
        total_cost = df["Cost"].sum()
        total_profit = total_revenue - total_cost
        avg_conversion = df["Conversion_Rate"].mean()
        total_units = df["Units_Sold"].sum()

        # --- KPI DISPLAY ---
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
        col2.metric("Total Profit", f"₹{total_profit:,.0f}")
        col3.metric("Units Sold", f"{total_units}")
        col4.metric("Avg Conversion", f"{avg_conversion:.2%}")

        st.divider()

        # --- KPI SCORE ENGINE ---
        profit_margin = total_profit / total_revenue if total_revenue != 0 else 0
        conversion_score = avg_conversion
        sales_performance = total_units / len(df)

        score = (
            (profit_margin * 40) +
            (conversion_score * 30) +
            (min(sales_performance / 10, 1) * 30)
        ) * 100

        score = min(score, 100)

        # --- SCORE DISPLAY ---
        st.subheader("🏆 Retail Health Score")

        if score >= 80:
            st.success(f"🔥 Excellent Performance: {score:.0f}/100")
        elif score >= 60:
            st.warning(f"⚠️ Average Performance: {score:.0f}/100")
        else:
            st.error(f"🚨 Critical Performance: {score:.0f}/100")

        st.divider()

        # --- CHARTS ---
        st.subheader("📈 Sales by City")
        city_sales = df.groupby("Store_City")["Revenue"].sum().reset_index()
        fig1 = px.bar(city_sales, x="Store_City", y="Revenue")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("📊 Category Performance")
        cat_sales = df.groupby("Category")["Revenue"].sum().reset_index()
        fig2 = px.pie(cat_sales, names="Category", values="Revenue")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📉 Sales Trend")
        trend = df.groupby(df["Date"].dt.date)["Revenue"].sum().reset_index()
        fig3 = px.line(trend, x="Date", y="Revenue")
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # --- AI INSIGHTS ---
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

        # --- MANAGER ACTION PLAN ---
        st.subheader("📋 Manager Action Plan")

        actions = []

        if avg_conversion < 0.3:
            actions.append("Train staff on customer engagement & closing techniques.")

        if profit_margin < 0.2:
            actions.append("Reduce discount dependency and renegotiate supplier costs.")

        if low_category:
            actions.append(f"Run targeted promotions for {low_category} category.")

        if total_units < 1000:
            actions.append("Increase footfall via local marketing or in-store events.")

        if not actions:
            actions.append("Maintain current strategy and scale best-performing stores.")

        for a in actions:
            st.write("✅", a)

        st.divider()

        # --- DATA PREVIEW ---
        st.subheader("📂 Data Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
