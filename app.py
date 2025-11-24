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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with vibrant colors
st.markdown("""
    <style>
    .big-price {
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 20px 0;
    }
    .savings {
        font-size: 24px;
        text-align: center;
        color: #10b981;
        font-weight: 600;
    }
    .price-increase {
        font-size: 24px;
        text-align: center;
        color: #f59e0b;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid #667eea30;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize model
@st.cache_resource
def load_model():
    return SockPriceModel()

model = load_model()

# Title and description
st.markdown("""
# Crew Sock Price Predictor
### Time-based predictive pricing model
""")

st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 30px;'>
    <p style='margin: 0; font-size: 18px; font-weight: 500;'>Advanced temporal analysis for optimal purchase timing</p>
    <p style='margin: 8px 0 0 0; opacity: 0.9;'>Leveraging machine learning to forecast crew sock costs based on day-of-week, hourly, and seasonal demand patterns.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Prediction Parameters")

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
st.sidebar.subheader("Special Events")
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
        st.markdown(f'<div class="savings">Save ${prediction["savings"]:.2f} from base price</div>', unsafe_allow_html=True)
    elif prediction["savings"] < 0:
        st.markdown(f'<div class="price-increase">${abs(prediction["savings"]):.2f} above base price</div>', unsafe_allow_html=True)

# Price factors
if prediction["factors"]:
    st.subheader("Price Factors")
    for factor in prediction["factors"]:
        st.markdown(f"• {factor}")
else:
    st.info("Base price applies — no special factors at this time")

# Visualizations
st.markdown("---")
st.header("Price Analysis")

tab1, tab2, tab3 = st.tabs(["24-Hour View", "Weekly View", "Optimal Purchase Time"])

with tab1:
    st.subheader(f"Price Throughout {selected_date.strftime('%A')}")
    
    # Get hourly prices
    daily_prices = model.get_daily_prices(day_of_week, month, special_events)
    df_daily = pd.DataFrame(daily_prices)
    
    # Create line chart with gradient colors
    fig_daily = px.line(
        df_daily,
        x="hour",
        y="price",
        title=f"Hourly Sock Prices — {selected_date.strftime('%A, %B %d')}",
        labels={"hour": "Hour of Day", "price": "Price ($)"},
        markers=True
    )
    
    fig_daily.update_traces(
        line_color='#667eea',
        marker=dict(size=8, color='#764ba2', line=dict(width=2, color='white'))
    )
    
    # Add current time marker
    fig_daily.add_vline(
        x=selected_hour,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text="Current Time",
        line_width=3
    )
    
    fig_daily.update_layout(
        yaxis_range=[df_daily['price'].min() - 0.5, df_daily['price'].max() + 0.5],
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Show min/max times
    min_price_hour = df_daily.loc[df_daily['price'].idxmin()]
    max_price_hour = df_daily.loc[df_daily['price'].idxmax()]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Lowest Price Today",
            f"${min_price_hour['price']:.2f}",
            f"at {int(min_price_hour['hour'])}:00"
        )
    with col2:
        st.metric(
            "Highest Price Today",
            f"${max_price_hour['price']:.2f}",
            f"at {int(max_price_hour['hour'])}:00"
        )

with tab2:
    st.subheader(f"Weekly Prices at {selected_hour}:00")
    
    # Get weekly prices
    weekly_prices = model.get_weekly_prices(selected_hour, month, special_events)
    df_weekly = pd.DataFrame(weekly_prices)
    
    # Create bar chart with custom colors
    fig_weekly = px.bar(
        df_weekly,
        x="day",
        y="price",
        title=f"Sock Prices by Day of Week (at {selected_hour}:00)",
        labels={"day": "Day of Week", "price": "Price ($)"},
        color="price",
        color_continuous_scale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']]
    )
    
    fig_weekly.update_layout(
        yaxis_range=[df_weekly['price'].min() - 0.5, df_weekly['price'].max() + 0.5],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Show best day
    best_day = df_weekly.loc[df_weekly['price'].idxmin()]
    worst_day = df_weekly.loc[df_weekly['price'].idxmax()]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Best Day This Week",
            best_day['day'],
            f"${best_day['price']:.2f}"
        )
    with col2:
        st.metric(
            "Most Expensive Day",
            worst_day['day'],
            f"${worst_day['price']:.2f}"
        )

with tab3:
    st.subheader("Optimal Purchase Strategy")
    
    # Find best time
    best_time = model.find_best_time(month, special_events)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #10b98120 0%, #059669 20 100%); padding: 30px; border-radius: 15px; border: 2px solid #10b981;'>
        <h3 style='color: #065f46; margin-top: 0;'>Best Time to Buy This Month</h3>
        <h2 style='color: #047857; font-size: 32px;'>{best_time['day']} at {best_time['hour']}:00</h2>
        <p style='font-size: 28px; color: #059669; font-weight: bold; margin: 15px 0;'>Predicted Price: ${best_time['price']:.2f}</p>
        <p style='font-size: 18px; color: #065f46;'>Potential savings of <strong>${prediction['price'] - best_time['price']:.2f}</strong> compared to current selection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create heatmap of all prices
    st.subheader("Weekly Price Heatmap")
    
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
    
    # Create heatmap with custom colorscale
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=price_matrix,
        x=hours,
        y=days,
        colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
        text=[[f'${price:.2f}' for price in day] for day in price_matrix],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Price ($)", tickprefix="$")
    ))
    
    fig_heatmap.update_layout(
        title="Complete Weekly Price Distribution",
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p style='font-size: 16px;'><strong>Crew Sock Price Predictor</strong></p>
    <p style='font-size: 14px;'>Built with Streamlit, Plotly, and scikit-learn</p>
    <p style='font-size: 13px; margin-top: 10px; font-style: italic;'>Predictive model based on temporal patterns and seasonal demand cycles</p>
</div>
""", unsafe_allow_html=True)
