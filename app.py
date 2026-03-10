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
from modules.rule_explorer import rule_3d_plot, interpret_rule
from modules.rule_explorer import filter_rules, interpret_rule
st.set_page_config(layout="wide")

st.title("Retail Analytics & Market Basket Intelligence Lab")

# -------------------------------------------------
# SESSION STATE (prevents data reset)
# -------------------------------------------------

if "data" not in st.session_state:
    st.session_state.data = None

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("Controls")

support = st.sidebar.slider("Minimum Support",0.01,0.5,0.05)

confidence = st.sidebar.slider("Minimum Confidence",0.1,1.0,0.3)

uploaded_file = st.sidebar.file_uploader("Upload Retail Dataset")

generate_data = st.sidebar.button("Generate Synthetic Dataset")

reset = st.sidebar.button("Reset Data")

# Reset
if reset:
    st.session_state.data = None

# Upload
if uploaded_file:
    st.session_state.data = pd.read_csv(uploaded_file)

# Generate
if generate_data:
    st.session_state.data = generate_dataset()

# Stop if no data
if st.session_state.data is None:
    st.info("Upload a dataset or generate synthetic data from sidebar.")
    st.stop()

df = st.session_state.data

# -------------------------------------------------
# TABS
# -------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
"Dataset",
"Market Basket Analysis",
"Visualization",
"Recommendations",
"Customer Segmentation",
"Sequential Patterns"
])

# -------------------------------------------------
# DATASET TAB
# -------------------------------------------------

with tab1:

    st.header("Dataset Preview")

    st.dataframe(df.head())

    st.write("Dataset Size:", df.shape)

# -------------------------------------------------
# MARKET BASKET ANALYSIS
# -------------------------------------------------

basket = create_basket(df)

rules = run_mba(basket,support,confidence)

# Convert frozensets for plotting
rules["antecedents"] = rules["antecedents"].apply(lambda x:", ".join(list(x)))
rules["consequents"] = rules["consequents"].apply(lambda x:", ".join(list(x)))

# -------------------------------------------------
# MBA TAB
# -------------------------------------------------

with tab2:

    st.header("Association Rules")

    if rules.empty:

        st.warning("No rules generated. Reduce support or confidence.")

    else:

        st.dataframe(rules)

# -------------------------------------------------
# VISUALIZATION TAB
# -------------------------------------------------

with tab3:

    st.header("Rule Dashboard")

    if not rules.empty:

        st.plotly_chart(
            plot_rule_scatter(rules),
            use_container_width=True
        )

        st.header("3D Rule Visualization")

        st.plotly_chart(
            plot_3d_rules(rules),
            use_container_width=True
        )

        st.header("Product Association Network")

        st.plotly_chart(
            build_network(rules),
            use_container_width=True
        )

# -------------------------------------------------
# RECOMMENDATION TAB
# -------------------------------------------------

with tab4:

    st.header("Product Recommendation Engine")

    if not rules.empty:

        product = st.selectbox(
            "Select Product",
            basket.columns
        )

        rec = recommend_products(product,rules)

        st.dataframe(rec)

        st.header("Retail Insights")

        insights = generate_insights(rules)

        for i in insights:
            st.write(i)

        st.header("Store Layout Optimization")

        layout = optimize_layout(rules)

        for l in layout:
            st.write(l)

# -------------------------------------------------
# CUSTOMER SEGMENTATION
# -------------------------------------------------

with tab5:

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

# -------------------------------------------------
# SEQUENTIAL PATTERN TAB
# -------------------------------------------------

with tab6:

    st.header("Sequential Pattern Prediction")

    product_seq = st.selectbox(
        "Select Product",
        df["Item"].unique()
    )

    pred = next_product_prediction(
        df,
        product_seq
    )

    st.bar_chart(pred)
