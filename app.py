import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="QuCreate Streamlit Lab", layout="wide")
st.sidebar.image("assets/images/company_logo.jpg") # Replace with your logo path if you have one. Or remove if not needed.
st.sidebar.divider()
st.title("QuCreate Streamlit Lab: Alternative Investment Features, Methods, and Structures")
st.divider()

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("Investment Parameters")
    st.markdown("Adjust the following parameters to see how the catch-up clause impacts General Partner (GP) returns.")

    investment_amount = st.number_input("Total Investment Amount ($)", min_value=100000, value=1000000, step=100000, format="%d")
    st.sidebar.markdown("Enter the total capital invested in the fund.")

    investment_period = st.slider("Investment Period (Years)", min_value=1, max_value=20, value=10, step=1)
    st.sidebar.markdown("Select the duration of the investment in years.")

    gp_preferred_return_percent = st.slider("GP Preferred Return (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.5) / 100.0
    st.sidebar.markdown("Choose the annual preferred return percentage for the General Partner (GP).")

    catchup_percent = st.slider("Catch-up Percentage (%)", min_value=0.0, max_value=100.0, value=20.0, step=5.0) / 100.0
    st.sidebar.markdown("Set the percentage of profits allocated to the GP during the catch-up phase.")

    lp_returns_percent = st.number_input("LP Returns (%)", min_value=0.0, value=150.0, step=10.0) / 100.0
    st.sidebar.markdown("Specify the total return percentage for the Limited Partners (LPs).")
    st.sidebar.divider()

    st.info("Adjust the parameters in the sidebar to dynamically update the visualizations and understand the impact of the catch-up clause on GP returns.")

# --- Explanation Section ---
st.header("Understanding the Catch-Up Clause in Alternative Investments")
st.markdown("""
In alternative investments, particularly in private equity and hedge funds, the **catch-up clause** is a crucial component that defines how profits are distributed between the **Limited Partners (LPs)** and the **General Partner (GP)**. This application demonstrates the impact of this clause on GP returns.

**Key Concepts:**

- **Preferred Return:**  A hurdle rate that LPs must receive before the GP starts receiving performance-based compensation (carried interest). It's like an interest payment on the LP's investment.
- **Catch-up Clause:** After LPs receive their preferred return, the catch-up clause allows the GP to receive a proportionally larger share of the profits until they have 'caught up' to their agreed-upon carried interest split.
- **Carried Interest:** The share of profits that the GP receives as incentive compensation, typically after the preferred return and catch-up are satisfied.

This application visualizes two scenarios:
1. **With Catch-up Clause:** Demonstrates how the GP benefits from the catch-up clause after LPs receive their preferred return.
2. **Without Catch-up Clause:** Shows a more straightforward profit distribution without the catch-up mechanism.

By adjusting the investment parameters in the sidebar, you can observe how these clauses affect the GP's overall returns under different conditions.
""")

st.divider()

# --- Calculation Logic ---
def calculate_gp_returns(investment, preferred_return_rate, catchup_rate, lp_return_rate, with_catchup=True):
    """
    Calculates GP returns with and without the catch-up clause.

    Parameters:
        investment (float): Total investment amount.
        preferred_return_rate (float): GP preferred return percentage (e.g., 0.08 for 8%).
        catchup_rate (float): Catch-up percentage (e.g., 0.20 for 20%).
        lp_return_rate (float): LP total return percentage (e.g., 1.5 for 150%).
        with_catchup (bool): If True, calculates with catch-up clause; otherwise, without.

    Returns:
        tuple: Total LP return, GP return with catch-up (if applicable), GP return without catch-up.
    """
    total_return = investment * lp_return_rate
    profit = total_return - investment

    if profit <= 0:
        return 0, 0 # No profit, no GP return

    preferred_return_amount = investment * preferred_return_rate
    remaining_profit_after_preferred = profit - preferred_return_amount

    if remaining_profit_after_preferred <= 0:
        gp_return_without_catchup = 0
        gp_return_with_catchup = 0
    else:
        # Without Catch-up Clause
        gp_return_without_catchup = remaining_profit_after_preferred * 0.20 # Assuming 20% carried interest for simplicity

        # With Catch-up Clause
        catchup_amount = remaining_profit_after_preferred * catchup_rate # GP Catch-up to reach their carried interest target.
        gp_return_with_catchup = catchup_amount
        remaining_profit_after_catchup = remaining_profit_after_preferred - catchup_amount
        lp_share_after_catchup = remaining_profit_after_catchup # Remaining profit goes to LPs after GP catch-up and preferred return.

    # Total GP and LP Returns Calculation
    lp_total_return = investment + preferred_return_amount + (lp_share_after_catchup if with_catchup and remaining_profit_after_preferred > 0 else remaining_profit_after_preferred if not with_catchup and remaining_profit_after_preferred > 0 else 0 ) # LPs get initial investment + preferred return + remaining after GP catchup (or remaining after preferred return if no catchup)

    gp_total_return_with_catchup = gp_return_with_catchup if with_catchup and remaining_profit_after_preferred > 0 else 0
    gp_total_return_without_catchup = gp_return_without_catchup if not with_catchup and remaining_profit_after_preferred > 0 else 0


    if profit > 0:
        if with_catchup:
            gp_total_return_with_catchup = gp_return_with_catchup
        else:
            gp_total_return_without_catchup = gp_return_without_catchup
    else:
        gp_total_return_with_catchup = 0
        gp_total_return_without_catchup = 0

    return lp_total_return, gp_total_return_with_catchup, gp_total_return_without_catchup


# --- Generate Data for Visualization ---
investment_years = np.arange(1, investment_period + 1)
gp_returns_catchup = []
gp_returns_no_catchup = []
lp_returns_over_time = []

for year in investment_years:
    lp_return, gp_return_catchup, gp_return_no_catchup = calculate_gp_returns(investment_amount, gp_preferred_return_percent, catchup_percent, lp_returns_percent, with_catchup=True)
    lp_return_nc, gp_return_catchup_nc, gp_return_no_catchup_nc = calculate_gp_returns(investment_amount, gp_preferred_return_percent, catchup_percent, lp_returns_percent, with_catchup=False) # Recalculate without catchup for no catchup scenario line
    gp_returns_catchup.append(gp_return_catchup)
    gp_returns_no_catchup.append(gp_return_no_catchup_nc) # Using _nc version as we want 'no catchup' scenario
    lp_returns_over_time.append(lp_return)


# --- Visualization Section ---
st.header("Visualizing GP Returns: With and Without Catch-Up Clause")
st.markdown("The following charts illustrate the GP returns under two different scenarios, based on the investment parameters you've set.")

# --- Chart 1: GP Returns Comparison ---
st.subheader("Comparison of GP Returns")
st.markdown("This chart compares the GP returns with and without the catch-up clause over the investment period.")

fig_comparison, ax_comparison = plt.subplots(figsize=(10, 6))
ax_comparison.plot(investment_years, gp_returns_catchup, label='GP Return (With Catch-up Clause)', marker='o')
ax_comparison.plot(investment_years, gp_returns_no_catchup, label='GP Return (Without Catch-up Clause)', marker='x')
ax_comparison.set_xlabel("Investment Period (Years)")
ax_comparison.set_ylabel("GP Return ($)")
ax_comparison.set_title("GP Returns: Catch-up vs. No Catch-up Clause")
ax_comparison.grid(True)
ax_comparison.legend()

# Annotate key differences (Example - annotation needs to be more dynamic and context aware in real app)
if gp_returns_catchup[-1] > gp_returns_no_catchup[-1]:
    y_pos = max(gp_returns_catchup[-1], gp_returns_no_catchup[-1]) + (max(gp_returns_catchup[-1], gp_returns_no_catchup[-1]) * 0.05) # Position annotation slightly above higher value
    ax_comparison.annotate(
        'Catch-up Clause Benefit',
        xy=(investment_years[-1], gp_returns_catchup[-1]), xytext=(investment_years[-1] - 1, y_pos),
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        fontsize=9
    )

st.pyplot(fig_comparison)
st.markdown("""
**Chart Explanation:**
- The blue line represents the GP's return when the catch-up clause is in effect.
- The orange line shows the GP's return without the catch-up clause.
- Observe how the catch-up clause can significantly enhance GP returns, especially when the fund performance exceeds the preferred return.

**Key Observations:**
- When the fund performs well (LP returns are high), the catch-up clause leads to a higher GP return compared to the scenario without it.
- The catch-up clause is designed to incentivize the GP to achieve higher returns, as they are rewarded more significantly once the LP's preferred return is met.
""")

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "To access the full legal documentation, please visit this link. Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
