import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="QuCreate Streamlit Lab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Alternative Investment - Catch-up Clause Impact")
st.divider()

# Explanation of the Application
st.markdown("""
This application demonstrates the impact of the **catch-up clause** on General Partner (GP) returns in alternative investments. 
It allows you to input investment parameters and visualize how GP returns differ in scenarios with and without a catch-up clause.

**Understanding the Catch-up Clause:**

In many alternative investment agreements, particularly in private equity and hedge funds, a catch-up clause is included. 
This clause is designed to 'catch up' the GP's share of profits to the agreed-upon carried interest percentage (often 20%) after the Limited Partners (LPs) have received their preferred return.

**How to Use This Application:**

1.  **Input Investment Parameters:** Use the sidebar to adjust the investment parameters such as total investment, GP preferred return, catch-up percentage, and LP returns.
2.  **Visualize GP Returns:** Observe the two line charts generated in the main area.
    *   **Graph A: GP Returns with Catch-up Clause:** Shows the GP's return when the catch-up clause is applied.
    *   **Graph B: GP Returns without Catch-up Clause:** Shows the GP's return in the absence of a catch-up clause.
3.  **Compare Scenarios:** Analyze the differences between the two graphs to understand how the catch-up clause enhances GP returns, especially in scenarios with higher profitability.

**Important Note:** The calculations and visualizations in this application are based on a simplified model for educational purposes. Real-world catch-up clauses and waterfall structures can be more complex.
""")

st.sidebar.header("Investment Parameters")

# User Input Form in Sidebar
total_investment = st.sidebar.number_input("Total Investment Amount", min_value=0.0, format="%.2f", value=1000000.0)
investment_period = st.sidebar.slider("Investment Period (Years)", min_value=1, max_value=10, value=5)
gp_preferred_return_percent = st.sidebar.slider("GP Preferred Return (%)", min_value=0.0, max_value=20.0, value=8.0) / 100.0
catch_up_percentage = st.sidebar.slider("Catch-up Percentage (%)", min_value=0.0, max_value=100.0, value=50.0) / 100.0
lp_returns_percent = st.sidebar.slider("LP Total Return on Investment (%)", min_value=0.0, max_value=200.0, value=150.0) / 100.0

st.sidebar.divider()
st.sidebar.markdown("Adjust the parameters to see the impact on GP returns in real-time.")

# --- Backend Calculations ---
st.header("GP Return Scenarios and Visualizations")

# Explanation of Calculations
st.subheader("Understanding the Calculation Logic")
st.markdown("""
The application calculates GP returns under two scenarios: **with** and **without** a catch-up clause. 
The calculations are based on a simplified waterfall model:

1.  **Preferred Return:** First, Limited Partners (LPs) receive a preferred return on their investment.
2.  **Catch-up (if applicable):** Then, the General Partner (GP) receives a 'catch-up' allocation to reach a pre-defined profit split ratio (implicitly aimed for by the catch-up percentage).
3.  **Profit Split:** Finally, any remaining profits are split between LPs and GP according to an agreed ratio (simplified to a general profit split in this model).

**Formulas Used (Simplified):**

Let:
-   `TI` = Total Investment Amount
-   `PR` = GP Preferred Return Rate (e.g., 8% as 0.08)
-   `CU` = Catch-up Percentage (e.g., 50% as 0.50)
-   `LR` = LP Total Return on Investment Rate (e.g., 150% as 1.50)

**1. Total LP Returns Amount:** 
    `LP_Return_Amount = TI * LR`

**2. Total Profit:** 
    `Total_Profit = LP_Return_Amount - TI`

**3. Preferred Return Amount:** 
    `Preferred_Return = TI * PR`

**4. Remaining Profit after Preferred Return:** 
    `Profit_After_Preferred_Return = Total_Profit - Preferred_Return`

**5. GP Return with Catch-up Clause (Simplified):**
    `GP_Catch_up_Amount = Profit_After_Preferred_Return * CU`
    `GP_Return_With_Catch_up = Preferred_Return + GP_Catch_up_Amount + (Profit_After_Preferred_Return * (1-CU) * 0.2)`
    *(Note: The `0.2` factor implies a simplified 20% carried interest for GP after catch-up. This is for demonstration.)*

**6. GP Return without Catch-up Clause (Simplified):**
    `GP_Return_Without_Catch_up = Preferred_Return + (Profit_After_Preferred_Return * 0.2)`
    *(Again, `0.2` represents a simplified 20% carried interest.)*

**LP Returns (in both scenarios):** Calculated as the total profit minus the GP return for each scenario.

**Important Simplifications:** This model simplifies the complex waterfall structures found in real-world alternative investments. It's designed for educational purposes to illustrate the basic impact of a catch-up clause.
""")

# Calculate values based on user inputs
lp_return_amount = total_investment * lp_returns_percent
total_profit = lp_return_amount - total_investment
preferred_return_amount = total_investment * gp_preferred_return_percent

profit_after_preferred_return = max(0, total_profit - preferred_return_amount) # Ensure non-negative

# Scenario 1: With Catch-up Clause
gp_catch_up_amount = profit_after_preferred_return * catch_up_percentage
gp_return_with_catch_up = preferred_return_amount + gp_catch_up_amount + (profit_after_preferred_return * (1-catch_up_percentage) * 0.2)
lp_return_with_catch_up = total_profit - gp_return_with_catch_up

# Scenario 2: Without Catch-up Clause
gp_return_without_catch_up = preferred_return_amount + (profit_after_preferred_return * 0.2)
lp_return_without_catch_up = total_profit - gp_return_without_catch_up


# --- Visualization ---
st.subheader("Visual Comparison of GP Returns")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Graph A: GP Returns with Catch-up Clause")
    # Visualization for GP Returns with Catch-up
    labels_catch_up = ['Preferred Return', 'Catch-up Allocation', 'Carried Interest']
    sizes_catch_up = [preferred_return_amount, gp_catch_up_amount, (profit_after_preferred_return * (1-catch_up_percentage) * 0.2)]
    sizes_catch_up = [max(0, size) for size in sizes_catch_up] # Ensure no negative sizes for plotting
    colors_catch_up = ['skyblue', 'lightcoral', 'lightgreen']
    explode_catch_up = (0.1, 0.1, 0.1) if any(sizes_catch_up) else (0,0,0)  # explode 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes_catch_up, explode=explode_catch_up, labels=labels_catch_up, colors=colors_catch_up, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
    st.write(f"**Total GP Return (with Catch-up): ${gp_return_with_catch_up:,.2f}**")
    st.write(f"**LP Return (with Catch-up): ${lp_return_with_catch_up:,.2f}**")


with col2:
    st.markdown("### Graph B: GP Returns without Catch-up Clause")
    # Visualization for GP Returns without Catch-up
    labels_no_catch_up = ['Preferred Return', 'Carried Interest']
    sizes_no_catch_up = [preferred_return_amount, (profit_after_preferred_return * 0.2)]
    sizes_no_catch_up = [max(0, size) for size in sizes_no_catch_up] # Ensure no negative sizes for plotting
    colors_no_catch_up = ['skyblue', 'lightgreen']
    explode_no_catch_up = (0.1, 0) if any(sizes_no_catch_up) else (0,0)  # explode 1st slice

    fig2, ax2 = plt.subplots()
    ax2.pie(sizes_no_catch_up, explode=explode_no_catch_up, labels=labels_no_catch_up, colors=colors_no_catch_up, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig2)
    st.write(f"**Total GP Return (without Catch-up): ${gp_return_without_catch_up:,.2f}**")
    st.write(f"**LP Return (without Catch-up): ${lp_return_without_catch_up:,.2f}**")

st.divider()
st.subheader("Key Observations")
st.markdown("""
-   **Impact of Catch-up Clause:** By comparing Graph A and Graph B, you can clearly see how the catch-up clause increases the GP's share of the profits, especially in scenarios where the total profit exceeds the preferred return.
-   **GP Incentive Alignment:** The catch-up clause is a mechanism to align the GP's incentives with those of the LPs. It ensures that GPs are adequately rewarded for generating returns above the preferred return threshold.
-   **Simplified Model:** Remember that this is a simplified representation. Real-world investment structures and catch-up mechanisms can be significantly more complex and may include hurdle rates, multiple catch-up tiers, and different profit-sharing arrangements.
""")


st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "To access the full legal documentation, please visit this link. Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
