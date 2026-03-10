import plotly.express as px

def rule_3d_plot(rules):

    fig = px.scatter_3d(
        rules,
        x="support",
        y="confidence",
        z="lift",
        color="lift",
        hover_data=["antecedents","consequents"]
    )

    fig.update_layout(
        height=600,
        title="3D Association Rule Explorer"
    )

    return fig


def interpret_rule(rule):

    antecedent = rule["antecedents"]
    consequent = rule["consequents"]

    support = round(rule["support"],3)
    confidence = round(rule["confidence"],3)
    lift = round(rule["lift"],2)

    interpretation = f"""
### Rule Interpretation

Customers who buy **{antecedent}** also tend to buy **{consequent}**.

• **Support:** {support}  
{support*100:.1f}% of all transactions contain this item combination.

• **Confidence:** {confidence}  
{confidence*100:.1f}% of customers buying **{antecedent}** also buy **{consequent}**.

• **Lift:** {lift}  
This relationship is **{lift} times stronger than random purchasing**.
"""

    return interpretation

with tab4:

    st.header("Interactive Association Rule Explorer")

    st.write(
        "Explore rules using filters and interpret them."
    )

    min_lift = st.slider("Minimum Lift",1.0,5.0,1.2)

    min_conf = st.slider("Minimum Confidence",0.0,1.0,0.3)

    min_support = st.slider("Minimum Support",0.0,0.5,0.02)

    filtered_rules = rules[
        (rules["lift"] >= min_lift) &
        (rules["confidence"] >= min_conf) &
        (rules["support"] >= min_support)
    ]

    st.subheader("3D Rule Space")

    st.plotly_chart(
        rule_3d_plot(filtered_rules),
        use_container_width=True
    )

    st.subheader("Select Rule for Interpretation")

    if not filtered_rules.empty:

        selected_rule = st.selectbox(
            "Choose Rule",
            filtered_rules.index
        )

        rule_data = filtered_rules.loc[selected_rule]

        st.markdown(
            interpret_rule(rule_data)
        )

    else:

        st.warning("No rules match the filters.")
