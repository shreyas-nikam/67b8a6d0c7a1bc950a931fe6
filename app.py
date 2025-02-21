import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Application Title and Introduction ---
st.title("Alternative Investment: Catch-Up Clause Impact")

st.write("""
This application demonstrates the impact of the catch-up clause on General Partner (GP) returns in alternative investments.
By adjusting the input parameters in the sidebar, you can visualize how the catch-up clause affects GP returns compared to scenarios without it.
""")

st.markdown("---")

# --- Sidebar for User Inputs ---
st.sidebar.header("Investment Parameters")

investment_amount = st.sidebar.number_input("Total Investment Amount", value=1000000, min_value=0, step=100000)
investment_period = st.sidebar.number_input("Investment Period (Years)", value=10, min_value=1, step=1)
gp_preferred_return_percent = st.sidebar.slider("GP Preferred Return (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.5)
catch_up_percent = st.sidebar.slider("Catch-up Percentage (%)", min_value=0.0, max_value=100.0, value=100.0, step=5.0)
lp_return_multiple = st.sidebar.number_input("LP Return Multiple (x of Investment)", value=2.0, min_value=0.0, step=0.1)

gp_preferred_return = gp_preferred_return_percent / 100.0
catch_up_percentage = catch_up_percent / 100.0

st.sidebar.markdown("---")
st.sidebar.markdown("### Explanation of Parameters")
st.sidebar.markdown(
    """
    - **Total Investment Amount**: The initial capital invested in the project or fund.
    - **Investment Period**: The duration of the investment in years.
    - **GP Preferred Return**: The minimum annual return percentage that Limited Partners (LPs) must receive before the General Partner (GP) starts receiving carried interest.
    - **Catch-up Percentage**: The percentage of profits allocated to the GP after LPs receive their preferred return, until the GP 'catches up' to a pre-agreed profit split. Typically, it's 100%, meaning GP gets 100% of profits after preferred return until the agreed split is reached.
    - **LP Return Multiple**: The multiple of the initial investment that LPs expect to receive back. For example, '2.0' means LPs expect to receive twice their initial investment back over the investment period.
    """
)

st.markdown("---")

# --- Calculation Logic ---
st.header("GP Return Scenarios")

st.subheader("Understanding the Catch-Up Clause")
st.write("""
In alternative investments, especially in private equity and venture capital, a 'catch-up clause' is a common provision in the Limited Partnership Agreement (LPA).
It dictates how profits are distributed between the Limited Partners (LPs) and the General Partner (GP).
Typically, LPs receive a 'preferred return' first. After this, the catch-up clause comes into play.

**Without Catch-Up Clause**:  After LPs receive their preferred return, the remaining profits are split according to a pre-agreed ratio (e.g., 80/20 split in favor of LPs).

**With Catch-Up Clause**: After LPs receive their preferred return, the GP receives a disproportionately larger share of the subsequent profits until they have 'caught up' to the intended overall profit split.
After the catch-up is complete, the profits are then split according to the standard carried interest split (e.g., 80/20).

This application focuses on visualizing the GP's returns under both scenarios to highlight the impact of the catch-up clause.
""")

# Sample Calculation Logic (Simplified for demonstration)
years = np.arange(1, investment_period + 1)
cumulative_investment_value = investment_amount * (1 + 0.1)**years # Assuming a hypothetical 10% growth for total investment value for simplicity

lp_preferred_return_value_cumulative = investment_amount * (1 + gp_preferred_return)**years
total_profit_cumulative = cumulative_investment_value - investment_amount

gp_return_with_catchup = np.zeros_like(years, dtype=float)
gp_return_without_catchup = np.zeros_like(years, dtype=float)

gp_carry_percentage = 0.2  # Standard 20% carried interest for GP after catch-up/preferred return


for i, year in enumerate(years):
    profit_year = cumulative_investment_value[i] - investment_amount

    # --- Scenario WITHOUT Catch-Up ---
    lp_preferred_return_no_catchup = min(lp_preferred_return_value_cumulative[i] - investment_amount, profit_year)
    remaining_profit_no_catchup = profit_year - lp_preferred_return_no_catchup
    gp_return_without_catchup[i] = gp_carry_percentage * remaining_profit_no_catchup

    # --- Scenario WITH Catch-Up ---
    lp_preferred_return_catchup = min(lp_preferred_return_value_cumulative[i] - investment_amount, profit_year)
    profit_after_preferred_return = profit_year - lp_preferred_return_catchup

    # Catch-up phase: GP gets catch_up_percentage of remaining profit until target split is achieved.
    # Simplified catch-up: GP gets full catch-up % of profit after preferred return for demonstration.
    catch_up_allocation = catch_up_percentage * profit_after_preferred_return
    gp_return_with_catchup[i] = catch_up_allocation


    # After catch-up (simplified: assuming catch-up completes within first few years for demonstration, or always applies in this simplified model)
    # In a more complex model, you'd need to track cumulative distributions to determine when catch-up is complete.
    # For this simplified example, we assume catch-up is always "in effect" as per slider, demonstrating its potential impact.
    # In reality, catch-up is a phase, not a continuous application.


# --- Visualization ---
st.subheader("Visual Comparison of GP Returns")
st.write("The charts below illustrate the cumulative GP returns over the investment period for both scenarios:")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(years, np.cumsum(gp_return_with_catchup), label=f'GP Return with Catch-up ({catch_up_percent}%)', marker='o')
ax.plot(years, np.cumsum(gp_return_without_catchup), label='GP Return without Catch-up', marker='x')

ax.set_xlabel("Investment Year")
ax.set_ylabel("Cumulative GP Return (USD)")
ax.set_title("Cumulative GP Returns: With vs Without Catch-Up Clause")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.markdown("""
**Chart Explanation:**

- **X-axis**: Represents the investment year, from year 1 to the total investment period.
- **Y-axis**: Shows the cumulative GP return in US dollars.
- **Lines**:
    - **Blue Line (with Catch-up)**:  Illustrates the cumulative GP returns when the catch-up clause is applied at the specified percentage.
    - **Orange Line (without Catch-up)**: Shows the cumulative GP returns in a scenario where the catch-up clause is not in effect.

**Key Observations:**

- **Impact of Catch-up Percentage**: Observe how changing the 'Catch-up Percentage' slider in the sidebar dynamically alters the blue line (GP return with catch-up). A higher catch-up percentage generally leads to higher GP returns, especially in the initial years after the preferred return is met.
- **Comparison**: By comparing the blue and orange lines, you can clearly see the financial advantage for the GP due to the catch-up clause. The gap between the lines represents the additional return the GP receives because of the catch-up mechanism.
- **Simplified Model**: Please note that this is a simplified model for educational purposes. Real-world investment return calculations and catch-up clause mechanics can be more complex, involving hurdle rates, different tiers of profit sharing, and more intricate distribution waterfalls.

**Formula Explanation (Simplified Model):**

For each year:

1.  **Total Profit Calculation**: `Total Profit = Investment Amount * (1 + Growth Rate)^Year - Investment Amount` (Here, a constant 10% growth rate is assumed for simplicity).
2.  **LP Preferred Return**: `LP Preferred Return = Investment Amount * (1 + GP Preferred Return %)^Year - Investment Amount`. This is the return LPs get first.
3.  **GP Return without Catch-up**:  `GP Return = 20% * (Total Profit - LP Preferred Return)`.  Assuming a standard 20% carried interest split after LP preferred return.
4.  **GP Return with Catch-up**: `GP Return = (Catch-up Percentage %) * (Total Profit - LP Preferred Return)`. In this simplified model, GP gets the catch-up percentage of the profit after preferred return. In a real scenario, this 'catch-up' would continue until the GP reaches their target share of the overall profit split.

**Important Disclaimer**: This application provides a simplified illustration of the catch-up clause. Actual investment agreements and return distributions can be significantly more complex and depend on specific legal and financial terms. Consult with financial professionals for investment decisions.
""")

st.markdown("---")
st.subheader("Conclusion")
st.write("""
This application helps visualize the potential impact of the catch-up clause on GP returns in a simplified investment scenario.
By interactively adjusting the parameters, users can gain a better understanding of how this clause can significantly enhance GP compensation, especially in successful investments.
""")
