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
