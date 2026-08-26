import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Bank Customer Retention Analytics",
    page_icon="🏦",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("European_Bank.csv")


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "European_Bank.csv was not found. "
        "Please upload European_Bank.csv to the same GitHub folder as app.py."
    )
    st.stop()
except Exception as e:
    st.error("There was an error loading the dataset.")
    st.write(e)
    st.stop()


# ==========================================================
# TITLE
# ==========================================================

st.title("🏦 Customer Engagement & Product Utilization Analytics")

st.markdown(
    """
    ### Retention Strategy Dashboard

    This dashboard analyzes customer demographics, financial characteristics,
    product utilization and engagement patterns to identify customers who
    may be at risk of leaving the bank.
    """
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🔎 Dashboard Filters")

filtered_df = df.copy()

# Geography filter
if "Geography" in df.columns:
    geography = st.sidebar.multiselect(
        "Select Geography",
        sorted(df["Geography"].dropna().unique()),
        default=sorted(df["Geography"].dropna().unique())
    )

    filtered_df = filtered_df[
        filtered_df["Geography"].isin(geography)
    ]


# Gender filter
if "Gender" in df.columns:
    gender = st.sidebar.multiselect(
        "Select Gender",
        sorted(df["Gender"].dropna().unique()),
        default=sorted(df["Gender"].dropna().unique())
    )

    filtered_df = filtered_df[
        filtered_df["Gender"].isin(gender)
    ]


# Active member filter
if "IsActiveMember" in df.columns:

    active_options = st.sidebar.multiselect(
        "Customer Activity",
        [0, 1],
        default=[0, 1],
        format_func=lambda x: "Active" if x == 1 else "Inactive"
    )

    filtered_df = filtered_df[
        filtered_df["IsActiveMember"].isin(active_options)
    ]


# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown("---")
st.header("📊 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

# Total customers
c1.metric(
    "Total Customers",
    f"{len(filtered_df):,}"
)

# Churn
if "Exited" in filtered_df.columns:

    churn_rate = filtered_df["Exited"].mean() * 100

    c2.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

else:

    c2.metric(
        "Churn Rate",
        "N/A"
    )


# Average balance
if "Balance" in filtered_df.columns:

    c3.metric(
        "Average Balance",
        f"€{filtered_df['Balance'].mean():,.0f}"
    )

else:

    c3.metric(
        "Average Balance",
        "N/A"
    )


# Average credit score
if "CreditScore" in filtered_df.columns:

    c4.metric(
        "Average Credit Score",
        f"{filtered_df['CreditScore'].mean():.0f}"
    )

else:

    c4.metric(
        "Average Credit Score",
        "N/A"
    )


# ==========================================================
# DATASET OVERVIEW
# ==========================================================

st.markdown("---")
st.header("📋 Dataset Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Customers",
    f"{len(filtered_df):,}"
)

c2.metric(
    "Variables",
    f"{len(filtered_df.columns):,}"
)

c3.metric(
    "Missing Values",
    f"{filtered_df.isnull().sum().sum():,}"
)

with st.expander("👁️ View Customer Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ==========================================================
# CUSTOMER DEMOGRAPHICS
# ==========================================================

st.markdown("---")
st.header("👥 Customer Demographics")

col1, col2 = st.columns(2)


# Age distribution
with col1:

    if "Age" in filtered_df.columns:

        st.subheader("Age Distribution")

        fig, ax = plt.subplots()

        ax.hist(
            filtered_df["Age"].dropna(),
            bins=20
        )

        ax.set_xlabel("Age")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Customer Age Distribution")

        st.pyplot(fig)

        plt.close(fig)


# Geography
with col2:

    if "Geography" in filtered_df.columns:

        st.subheader("Customers by Geography")

        geo_counts = filtered_df["Geography"].value_counts()

        fig, ax = plt.subplots()

        ax.bar(
            geo_counts.index,
            geo_counts.values
        )

        ax.set_xlabel("Country")
        ax.set_ylabel("Customers")
        ax.set_title("Customer Distribution by Geography")

        st.pyplot(fig)

        plt.close(fig)


# ==========================================================
# GENDER ANALYSIS
# ==========================================================

if "Gender" in filtered_df.columns:

    st.subheader("Gender Distribution")

    gender_counts = filtered_df["Gender"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        gender_counts.index,
        gender_counts.values
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Customers")
    ax.set_title("Customers by Gender")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# PRODUCT UTILIZATION
# ==========================================================

st.markdown("---")
st.header("🏦 Product Utilization")

col1, col2 = st.columns(2)


# Number of products
with col1:

    if "NumOfProducts" in filtered_df.columns:

        st.subheader("Banking Products Used")

        products = (
            filtered_df["NumOfProducts"]
            .value_counts()
            .sort_index()
        )

        fig, ax = plt.subplots()

        ax.bar(
            products.index.astype(str),
            products.values
        )

        ax.set_xlabel("Number of Products")
        ax.set_ylabel("Customers")
        ax.set_title("Customers by Number of Products")

        st.pyplot(fig)

        plt.close(fig)


# Active customers
with col2:

    if "IsActiveMember" in filtered_df.columns:

        st.subheader("Customer Engagement")

        active = filtered_df["IsActiveMember"].value_counts()

        active_count = active.get(1, 0)
        inactive_count = active.get(0, 0)

        fig, ax = plt.subplots()

        ax.bar(
            ["Active", "Inactive"],
            [active_count, inactive_count]
        )

        ax.set_xlabel("Customer Status")
        ax.set_ylabel("Customers")
        ax.set_title("Active vs Inactive Customers")

        st.pyplot(fig)

        plt.close(fig)


# ==========================================================
# CREDIT CARD UTILIZATION
# ==========================================================

if "HasCrCard" in filtered_df.columns:

    st.subheader("Credit Card Ownership")

    card = filtered_df["HasCrCard"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        ["No Credit Card", "Credit Card"],
        [
            card.get(0, 0),
            card.get(1, 0)
        ]
    )

    ax.set_ylabel("Customers")
    ax.set_title("Credit Card Ownership")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CHURN ANALYSIS
# ==========================================================

st.markdown("---")
st.header("🚨 Customer Churn Analysis")

if "Exited" in filtered_df.columns:

    col1, col2, col3 = st.columns(3)

    retained = (filtered_df["Exited"] == 0).sum()
    churned = (filtered_df["Exited"] == 1).sum()

    col1.metric(
        "Retained Customers",
        f"{retained:,}"
    )

    col2.metric(
        "Customers at Risk",
        f"{churned:,}"
    )

    col3.metric(
        "Retention Rate",
        f"{(retained / len(filtered_df) * 100):.2f}%"
    )


    # Churn distribution

    churn_counts = filtered_df["Exited"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        ["Retained", "Churned"],
        [
            churn_counts.get(0, 0),
            churn_counts.get(1, 0)
        ]
    )

    ax.set_ylabel("Customers")
    ax.set_title("Customer Retention vs Churn")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CHURN BY ACTIVITY
# ==========================================================

if (
    "Exited" in filtered_df.columns
    and "IsActiveMember" in filtered_df.columns
):

    st.subheader("Churn Rate by Customer Engagement")

    engagement = (
        filtered_df
        .groupby("IsActiveMember")["Exited"]
        .mean()
        * 100
    )

    fig, ax = plt.subplots()

    ax.bar(
        ["Inactive", "Active"],
        [
            engagement.get(0, 0),
            engagement.get(1, 0)
        ]
    )

    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Churn Rate: Active vs Inactive Customers")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CHURN BY NUMBER OF PRODUCTS
# ==========================================================

if (
    "Exited" in filtered_df.columns
    and "NumOfProducts" in filtered_df.columns
):

    st.subheader("Churn Rate by Number of Products")

    product_churn = (
        filtered_df
        .groupby("NumOfProducts")["Exited"]
        .mean()
        * 100
    )

    fig, ax = plt.subplots()

    ax.bar(
        product_churn.index.astype(str),
        product_churn.values
    )

    ax.set_xlabel("Number of Products")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Product Utilization vs Churn")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# BALANCE ANALYSIS
# ==========================================================

st.markdown("---")
st.header("💰 Financial Profile")

if (
    "Balance" in filtered_df.columns
    and "Exited" in filtered_df.columns
):

    balance = (
        filtered_df
        .groupby("Exited")["Balance"]
        .mean()
    )

    fig, ax = plt.subplots()

    ax.bar(
        ["Retained", "Churned"],
        [
            balance.get(0, 0),
            balance.get(1, 0)
        ]
    )

    ax.set_ylabel("Average Balance")
    ax.set_title("Average Balance of Retained vs Churned Customers")

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CREDIT SCORE ANALYSIS
# ==========================================================

if (
    "CreditScore" in filtered_df.columns
    and "Exited" in filtered_df.columns
):

    st.subheader("Credit Score & Churn")

    retained_scores = filtered_df[
        filtered_df["Exited"] == 0
    ]["CreditScore"].dropna()

    churned_scores = filtered_df[
        filtered_df["Exited"] == 1
    ]["CreditScore"].dropna()

    fig, ax = plt.subplots()

    ax.hist(
        retained_scores,
        bins=20,
        alpha=0.6,
        label="Retained"
    )

    ax.hist(
        churned_scores,
        bins=20,
        alpha=0.6,
        label="Churned"
    )

    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Customers")
    ax.set_title("Credit Score Distribution")
    ax.legend()

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# CUSTOMER SEGMENTS
# ==========================================================

st.markdown("---")
st.header("🎯 Customer Retention Segments")

if "Exited" in filtered_df.columns:

    segment_data = pd.DataFrame({
        "Segment": [
            "Low Risk - Retained",
            "High Risk - Churned"
        ],
        "Customers": [
            (filtered_df["Exited"] == 0).sum(),
            (filtered_df["Exited"] == 1).sum()
        ]
    })

    st.dataframe(
        segment_data,
        use_container_width=True
    )


# ==========================================================
# BUSINESS RECOMMENDATIONS
# ==========================================================

st.markdown("---")
st.header("💡 Business Recommendations")

st.markdown(
    """
    ### 1. Improve Customer Engagement

    - Identify inactive customers.
    - Encourage digital banking usage.
    - Send personalized engagement campaigns.
    - Provide targeted offers based on customer behavior.

    ### 2. Increase Product Utilization

    - Cross-sell suitable banking products.
    - Encourage customers with limited product usage to adopt
      additional relevant services.
    - Develop relationship-depth strategies.

    ### 3. Reduce Customer Churn

    - Identify high-risk customers early.
    - Create personalized retention offers.
    - Use customer activity and product utilization as early-warning
      indicators.

    ### 4. Strengthen Valuable Customer Relationships

    - Prioritize high-value customers.
    - Provide dedicated relationship-management services.
    - Offer customized financial products.

    ### 5. Data-Driven Retention Strategy

    - Monitor churn rate regularly.
    - Track customer engagement.
    - Analyze product adoption.
    - Build predictive churn models for proactive intervention.
    """
)


# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.markdown("---")
st.header("⬇️ Download")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Customer Data",
    data=csv,
    file_name="customer_retention_analysis.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Customer Engagement & Product Utilization Analytics "
    "| Bank Customer Retention Strategy"
)
