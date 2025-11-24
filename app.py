"""
Crew Sock Price Predictor
Interactive web app for time-based sock pricing predictions
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from model import SockPriceModel

# Page configuration
st.set_page_config(
    page_title="Crew Sock Price Predictor",
    page_icon="🧦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-price {
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .savings {
        font-size: 24px;
        text-align: center;
        color: #2ca02c;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize model
@st.cache_resource
def load_model():
    return SockPriceModel()

model = load_model()

# Title and description
st.title("🧦 Crew Sock Price Predictor")
st.markdown("""
**Time-based predictive pricing model** that forecasts crew sock costs based on temporal patterns.
Find the optimal time to purchase and maximize your savings!
""")

# Sidebar controls
st.sidebar.header("⚙️ Prediction Parameters")

# Current date/time as default
now = datetime.now()

# Date and time inputs
selected_date = st.sidebar.date_input(
    "Select Date",
    value=now,
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2025, 12, 31)
)

selected_hour = st.sidebar.slider(
    "Select Hour",
    min_value=0,
    max_value=23,
    value=now.hour,
    format="%d:00"
)

# Special events
st.sidebar.subheader("🎉 Special Events")
special_events = []

if st.sidebar.checkbox("Back-to-School Season", value=(selected_date.month == 9)):
    special_events.append("back_to_school")

if st.sidebar.checkbox("Black Friday", value=(selected_date.month == 11 and 24 <= selected_date.day <= 25)):
    special_events.append("black_friday")

if st.sidebar.checkbox("Post-Holiday Clearance", value=(selected_date.month == 12 and selected_date.day >= 26)):
    special_events.append("post_holiday")

if st.sidebar.checkbox("National Sock Day (Dec 4)", value=(selected_date.month == 12 and selected_date.day == 4)):
    special_events.append("sock_day")

# Get prediction
day_of_week = selected_date.weekday()
month = selected_date.month
prediction = model.predict_price(day_of_week, selected_hour, month, special_events)

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"### {selected_date.strftime('%A, %B %d, %Y')} at {selected_hour}:00")
    st.markdown(f'<div class="big-price">${prediction["price"]}</div>', unsafe_allow_html=True)
    
    if prediction["savings"] > 0:
        st.markdown(f'<div class="savings">💰 Save ${prediction["savings"]} from base price!</div>', unsafe_allow_html=True)
    elif prediction["savings"] < 0:
        st.markdown(f'<div class="savings" style="color: #d62728;">📈 ${abs(prediction["savings"])} above base price</div>', unsafe_allow_html=True)

# Price factors
if prediction["factors"]:
    st.subheader("📊 Price Factors")
    for factor in prediction["factors"]:
        st.markdown(f"- {factor}")
else:
    st.info("Base price applies - no special factors at this time")

# Visualizations
st.markdown("---")
st.header("📈 Price Analysis")

tab1, tab2, tab3 = st.tabs(["24-Hour View", "Weekly View", "Best Time to Buy"])

with tab1:
    st.subheader(f"Price Throughout {selected_date.strftime('%A')}")
    
    # Get hourly prices
    daily_prices = model.get_daily_prices(day_of_week, month, special_events)
    df_daily = pd.DataFrame(daily_prices)
    
    # Create line chart
    fig_daily = px.line(
        df_daily,
        x="hour",
        y="price",
        title=f"Hourly Sock Prices - {selected_date.strftime('%A, %B %d')}",
        labels={"hour": "Hour of Day", "price": "Price ($)"},
        markers=True
    )
    
    # Add current time marker
    fig_daily.add_vline(
        x=selected_hour,
        line_dash="dash",
        line_color="red",
        annotation_text="Current Time"
    )
    
    fig_daily.update_layout(
        yaxis_range=[df_daily['price'].min() - 0.5, df_daily['price'].max() + 0.5],
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Show min/max times
    min_price_hour = df_daily.loc[df_daily['price'].idxmin()]
    max_price_hour = df_daily.loc[df_daily['price'].idxmax()]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "🟢 Cheapest Time Today",
            f"${min_price_hour['price']:.2f}",
            f"at {int(min_price_hour['hour'])}:00"
        )
    with col2:
        st.metric(
            "🔴 Most Expensive Time",
            f"${max_price_hour['price']:.2f}",
            f"at {int(max_price_hour['hour'])}:00"
        )

with tab2:
    st.subheader(f"Weekly Prices at {selected_hour}:00")
    
    # Get weekly prices
    weekly_prices = model.get_weekly_prices(selected_hour, month, special_events)
    df_weekly = pd.DataFrame(weekly_prices)
    
    # Create bar chart
    fig_weekly = px.bar(
        df_weekly,
        x="day",
        y="price",
        title=f"Sock Prices by Day of Week (at {selected_hour}:00)",
        labels={"day": "Day of Week", "price": "Price ($)"},
        color="price",
        color_continuous_scale="RdYlGn_r"
    )
    
    fig_weekly.update_layout(
        yaxis_range=[df_weekly['price'].min() - 0.5, df_weekly['price'].max() + 0.5]
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Show best day
    best_day = df_weekly.loc[df_weekly['price'].idxmin()]
    worst_day = df_weekly.loc[df_weekly['price'].idxmax()]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "🟢 Best Day This Week",
            best_day['day'],
            f"${best_day['price']:.2f}"
        )
    with col2:
        st.metric(
            "🔴 Most Expensive Day",
            worst_day['day'],
            f"${worst_day['price']:.2f}"
        )

with tab3:
    st.subheader("🎯 Optimal Purchase Time")
    
    # Find best time
    best_time = model.find_best_time(month, special_events)
    
    st.success(f"""
    ### Best Time to Buy This Month:
    **{best_time['day']} at {best_time['hour']}:00**
    
    **Price: ${best_time['price']:.2f}**
    
    💡 You could save **${prediction['price'] - best_time['price']:.2f}** by waiting for the optimal time!
    """)
    
    # Create heatmap of all prices
    st.subheader("📅 Price Heatmap - All Week")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = list(range(24))
    
    # Generate price matrix
    price_matrix = []
    for day_idx in range(7):
        day_prices = []
        for hour in range(24):
            result = model.predict_price(day_idx, hour, month, special_events)
            day_prices.append(result['price'])
        price_matrix.append(day_prices)
    
    # Create heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=price_matrix,
        x=hours,
        y=days,
        colorscale='RdYlGn_r',
        text=[[f'${price:.2f}' for price in day] for day in price_matrix],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Price ($)")
    ))
    
    fig_heatmap.update_layout(
        title="Sock Prices Throughout the Week",
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        height=400
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧦 Sock Price Predictor | Built with Streamlit & Machine Learning</p>
    <p><em>Predictive model based on temporal patterns and seasonal demand cycles</em></p>
</div>
""", unsafe_allow_html=True)
