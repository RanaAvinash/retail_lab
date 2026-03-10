import streamlit as st
import pandas as pd

from modules.dataset_generator import generate_dataset
from modules.preprocessing import create_basket
from modules.mba_engine import run_mba
from modules.visualization import plot_rule_scatter, plot_3d_rules
from modules.recommendation import recommend_products
from modules.insight_generator import generate_insights
from modules.network_graph import build_network
from modules.sequential_patterns import next_product_prediction
from modules.layout_optimizer import optimize_layout
from modules.segmentation import run_segmentation

st.set_page_config(layout="wide")

st.title("Retail Analytics & Market Basket Intelligence Lab")

# ------------------------------
# Sidebar Controls
# ------------------------------

st.sidebar.header("Model Parameters")

support = st.sidebar.slider(
    "Minimum Support",
    0.01,
    0.5,
    0.05
)

confidence = st.sidebar.slider(
    "Minimum Confidence",
    0.1,
    1.0,
    0.3
)

file = st.sidebar.file_uploader(
    "Upload Retail Dataset"
)

generate = st.sidebar.button(
    "Generate Synthetic Dataset"
)

# ------------------------------
# Load Dataset
# ------------------------------

if file:

    df = pd.read_csv(file)

elif generate:

    df = generate_dataset()

else:

    st.info("Upload a dataset or generate synthetic data.")
    st.stop()

# ------------------------------
# Dataset Preview
# ------------------------------

st.header("Dataset Preview")

st.dataframe(df.head())

# ------------------------------
# Market Basket Analysis
# ------------------------------

st.header("Market Basket Analysis")

basket = create_basket(df)

rules = run_mba(
    basket,
    support,
    confidence
)

# Convert frozenset to string (important for Plotly)

rules["antecedents"] = rules["antecedents"].apply(
    lambda x: ", ".join(list(x))
)

rules["consequents"] = rules["consequents"].apply(
    lambda x: ", ".join(list(x))
)

if rules.empty:

    st.warning(
        "No rules generated. Try lowering support or confidence."
    )

else:

    st.subheader("Association Rules")

    st.dataframe(rules)

# ------------------------------
# Rule Visualization
# ------------------------------

if not rules.empty:

    st.header("Rule Visualization Dashboard")

    fig = plot_rule_scatter(rules)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------
# 3D Rule Visualization
# ------------------------------

if not rules.empty:

    st.header("3D Rule Visualization")

    fig3 = plot_3d_rules(rules)

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ------------------------------
# Recommendation Engine
# ------------------------------

if not rules.empty:

    st.header("Product Recommendation Engine")

    product_list = list(basket.columns)

    product = st.selectbox(
        "Select Product",
        product_list
    )

    recommendations = recommend_products(
        product,
        rules
    )

    st.dataframe(recommendations)

# ------------------------------
# Insight Generator
# ------------------------------

if not rules.empty:

    st.header("Retail Insights")

    insights = generate_insights(rules)

    for insight in insights:

        st.write(insight)

# ------------------------------
# Network Graph
# ------------------------------

if not rules.empty:

    st.header("Product Association Network")

    fig_net = build_network(rules)

    st.plotly_chart(
        fig_net,
        use_container_width=True
    )

# ------------------------------
# Sequential Pattern Prediction
# ------------------------------

st.header("Sequential Pattern Prediction")

product_seq = st.selectbox(
    "Select Product for Sequential Prediction",
    df["Item"].unique()
)

prediction = next_product_prediction(
    df,
    product_seq
)

st.bar_chart(prediction)

# ------------------------------
# Customer Segmentation
# ------------------------------

st.header("Customer Segmentation")

customer_matrix = (
    df.groupby(['CustomerID','Item'])['Item']
    .count()
    .unstack()
    .fillna(0)
)

segmented = run_segmentation(customer_matrix)

st.subheader("Segment Distribution")

st.bar_chart(
    segmented["Segment"].value_counts()
)

# ------------------------------
# Store Layout Optimizer
# ------------------------------

if not rules.empty:

    st.header("Retail Store Layout Optimization")

    layout = optimize_layout(rules)

    for rec in layout:

        st.write(rec)
