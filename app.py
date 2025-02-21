import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="QuCreate Streamlit Lab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Alternative Investment Features, Methods, and Structures")
st.divider()

# --- Introduction and Explanation ---
st.markdown("""
    ## Understanding the Catch-Up Clause in Alternative Investments

    This application explores the impact of the **catch-up clause** in alternative investment agreements, 
    specifically focusing on how it affects the distribution of profits between **Limited Partners (LPs)** and 
    **General Partners (GPs)**.

    **What is a Catch-Up Clause?** 
    In many alternative investment structures, particularly in private equity and hedge funds, a catch-up clause 
    is designed to ensure that the GP receives their agreed-upon share of profits after the LP has received their 
    **preferred return**. The catch-up mechanism allows the GP to 'catch up' to their intended carried interest split 
    once the LP hurdle rate is achieved.

    **Why is it Important?**
    Understanding the catch-up clause is crucial for both LPs and GPs. It dictates the profit distribution structure 
    and can significantly impact the net returns for both parties. This tool helps visualize these impacts under 
    different investment scenarios.

    **Instructions:**
    Use the sidebar to input investment parameters such as total investment, preferred return, catch-up percentage, 
    and LP returns. Observe how these inputs dynamically affect the GP returns with and without a catch-up clause 
    in the charts below.
""")

st.sidebar.header("Investment Parameters")

# --- User Input Form in Sidebar ---
total_investment = st.sidebar.number_input("Total Investment Amount", min_value=100000, value=1000000, step=100000)
investment_period = st.sidebar.number_input("Investment Period (Years)", min_value=1, value=5, step=1)
gp_preferred_return_percent = st.sidebar.slider("GP Preferred Return (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.5) / 100.0
catch_up_percent = st.sidebar.slider("Catch-up Percentage (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100.0
lp_returns_percent = st.sidebar.slider("LP Returns (%) (Total Return over Investment Period)", min_value=0.0, max_value=200.0, value=50.0, step=5.0) / 100.0

st.sidebar.divider()
st.sidebar.markdown("""
    **Understanding the Inputs:**
    - **Total Investment Amount**: The initial capital invested in the project or fund.
    - **Investment Period**: The duration over which the investment is active, typically in years.
    - **GP Preferred Return (%)**: The minimum annual return percentage that LPs must receive before GPs receive carried interest.
    - **Catch-up Percentage (%)**: The portion of profits allocated to the GP to 'catch up' to their target carried interest after the LP preferred return is met.
    - **LP Returns (%)**: The total percentage return achieved by the investment for the LPs over the investment period. This represents the total profit to be distributed.
""")

# --- Calculations ---
total_profit = total_investment * lp_returns_percent
preferred_return_amount = total_investment * gp_preferred_return_percent

# Scenario 1: With Catch-up Clause
remaining_profit_catchup = max(0, total_profit - preferred_return_amount)
gp_catchup_return = preferred_return_amount + (remaining_profit_catchup * catch_up_percent)
lp_catchup_return = total_profit - gp_catchup_return

# Scenario 2: Without Catch-up Clause (Assuming a fixed GP carried interest of 20% for simplicity in 'no catch-up' scenario)
gp_carried_interest_no_catchup = 0.20 # Assuming 20% carried interest for GP in no catch-up scenario
remaining_profit_no_catchup = max(0, total_profit - preferred_return_amount)
gp_no_catchup_return = preferred_return_amount + (remaining_profit_no_catchup * gp_carried_interest_no_catchup)
lp_no_catchup_return = total_profit - gp_no_catchup_return

# --- Data for Visualization ---
scenario_data = {
    "Scenario": ["With Catch-up Clause", "Without Catch-up Clause"],
    "GP Return": [gp_catchup_return, gp_no_catchup_return],
    "LP Return": [lp_catchup_return, lp_no_catchup_return]
}
df_scenario = pd.DataFrame(scenario_data)

# --- Visualization: Bar Chart for GP and LP Returns Comparison ---
st.subheader("Comparison of Returns: With and Without Catch-Up Clause")
st.write("This chart visualizes the distribution of returns between GPs and LPs under two scenarios: one with a catch-up clause and one without.")

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df_scenario["Scenario"],
    y=df_scenario["GP Return"],
    name="GP Return",
    marker_color='rgb(55, 83, 109)'
))
fig_bar.add_trace(go.Bar(
    x=df_scenario["Scenario"],
    y=df_scenario["LP Return"],
    name="LP Return",
    marker_color='rgb(26, 118, 255)'
))

fig_bar.update_layout(
    yaxis_title='Return Amount ($)',
    xaxis_title='Scenario',
    barmode='stack'
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""
    **Interpretation of the Bar Chart:**
    - The chart clearly shows how the total profit is divided between the GP and LP in each scenario.
    - **With Catch-up Clause**: Observe how the GP's return is potentially higher compared to the 'Without Catch-up Clause' scenario, especially when the catch-up percentage is significant. This is because the catch-up clause is designed to prioritize the GP receiving their intended share after the LP's preferred return is met.
    - **Without Catch-up Clause**: Here, the GP's return is based on a fixed carried interest (in this example, 20%), leading to a different distribution of profits.

    **Key Takeaway:** The catch-up clause mechanism is designed to align incentives and fairly compensate GPs for performance, especially after delivering the promised preferred return to LPs. The impact of the catch-up clause is more pronounced in scenarios with higher overall returns.
""")

# --- Line Chart: Cumulative Returns over Investment Period (Simplified - Linear Growth for Illustration) ---
st.subheader("Cumulative Return Trajectory Over Investment Period (Illustrative)")
st.write("These line charts illustrate a simplified view of how returns might accumulate over the investment period for both scenarios. Note: This is a linear representation for educational purposes and does not reflect actual investment volatility.")

years = range(investment_period + 1) # Years from 0 to Investment Period
cumulative_lp_return_per_year = lp_returns_percent / investment_period if investment_period > 0 else 0
cumulative_preferred_return_per_year = gp_preferred_return_percent # Preferred return is typically annual, so it stays constant

# Calculate cumulative returns over time (linear growth for simplicity)
cumulative_gp_catchup_returns = []
cumulative_lp_catchup_returns = []
cumulative_gp_no_catchup_returns = []
cumulative_lp_no_catchup_returns = []

for year in years:
    current_total_profit = total_investment * (cumulative_lp_return_per_year * year)
    current_preferred_return_amount = total_investment * (cumulative_preferred_return_per_year * year) # Assuming preferred return accrues yearly

    # Catch-up Scenario Cumulative
    current_remaining_profit_catchup = max(0, current_total_profit - current_preferred_return_amount)
    current_gp_catchup_return = current_preferred_return_amount + (current_remaining_profit_catchup * catch_up_percent)
    current_lp_catchup_return = current_total_profit - current_gp_catchup_return
    cumulative_gp_catchup_returns.append(current_gp_catchup_return)
    cumulative_lp_catchup_returns.append(current_lp_catchup_return)

    # No Catch-up Scenario Cumulative
    current_remaining_profit_no_catchup = max(0, current_total_profit - current_preferred_return_amount)
    current_gp_no_catchup_return = current_preferred_return_amount + (current_remaining_profit_no_catchup * gp_carried_interest_no_catchup)
    current_lp_no_catchup_return = current_total_profit - current_gp_no_catchup_return
    cumulative_gp_no_catchup_returns.append(current_gp_no_catchup_return)
    cumulative_lp_no_catchup_returns.append(current_lp_no_catchup_return)


fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=list(years), y=cumulative_gp_catchup_returns, mode='lines', name='GP Return (Catch-up)', line=dict(color='rgb(55, 83, 109)')))
fig_line.add_trace(go.Scatter(x=list(years), y=cumulative_lp_catchup_returns, mode='lines', name='LP Return (Catch-up)', line=dict(color='rgb(26, 118, 255)', dash='dash')))
fig_line.add_trace(go.Scatter(x=list(years), y=cumulative_gp_no_catchup_returns, mode='lines', name='GP Return (No Catch-up)', line=dict(color='rgb(158, 202, 225)')))
fig_line.add_trace(go.Scatter(x=list(years), y=cumulative_lp_no_catchup_returns, mode='lines', name='LP Return (No Catch-up)', line=dict(color='rgb(107, 174, 214)', dash='dash')))

fig_line.update_layout(
    xaxis_title='Years',
    yaxis_title='Cumulative Return ($)',
    title='Cumulative Returns Over Investment Period',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("""
    **Interpretation of the Line Chart:**
    - This chart provides a simplified view of how GP and LP returns accumulate over the investment period.
    - **Cumulative Growth**: It illustrates the linear growth of returns (for simplicity). In reality, investment returns are rarely linear and involve more complex patterns.
    - **Scenario Comparison**: By comparing the solid and dashed lines, you can observe the cumulative impact of the catch-up clause on both GP and LP returns over time.
    - **Educational Tool**: This visualization is primarily for educational purposes to demonstrate the directional impact of the catch-up clause over an investment period.

    **Important Note:** These charts are based on simplified calculations and linear growth assumptions for illustrative purposes. Real-world investment scenarios are far more complex and involve risks, market fluctuations, and non-linear return patterns.
""")


st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "To access the full legal documentation, please visit this link. Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")
