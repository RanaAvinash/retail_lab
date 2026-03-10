import pandas as pd

def filter_rules(rules, min_lift, min_conf, min_support):

    filtered = rules[
        (rules["lift"] >= min_lift) &
        (rules["confidence"] >= min_conf) &
        (rules["support"] >= min_support)
    ]

    return filtered


def interpret_rule(row):

    antecedent = row["antecedents"]
    consequent = row["consequents"]

    support = round(row["support"],3)
    confidence = round(row["confidence"],3)
    lift = round(row["lift"],2)

    interpretation = f"""
Customers who buy **{antecedent}** are likely to also buy **{consequent}**.

• Support: {support} → {support*100}% of all transactions contain this combination  
• Confidence: {confidence} → {confidence*100}% of customers buying {antecedent} also buy {consequent}  
• Lift: {lift} → The relationship is **{lift} times stronger** than random chance.
"""

    return interpretation
