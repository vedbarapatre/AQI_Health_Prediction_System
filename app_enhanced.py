"""
Enhanced AI-Based Air Quality & Health Prediction System (IHIP)
Modern UI with advanced features and real-time monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import sys
import os
from io import BytesIO
import base64

# Add data_sources to path
sys.path.append(os.path.dirname(__file__))

# Import OpenWeather client
try:
    from data_sources.openweather_client import (
        get_openweather_client, 
        fetch_city_data, 
        fetch_all_cities,
        fetch_forecast,
        OpenWeatherClient
    )
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    REAL_DATA_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="IHIP - Air Quality Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS with Glassmorphism
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background with Gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    [data-theme="dark"] .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Animated Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 45px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Modern Headers */
    .app-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .app-header h1 {
        color: white;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #fff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Risk Level Badges with Glow */
    .risk-badge {
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .risk-good {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #f7b731, #f9ca24);
        color: #2c3e50;
        box-shadow: 0 4px 15px rgba(247, 183, 49, 0.4);
    }
    
    .risk-unhealthy {
        background: linear-gradient(135deg, #ee5a6f, #f7b731);
        color: white;
        box-shadow: 0 4px 15px rgba(238, 90, 111, 0.4);
    }
    
    .risk-very-unhealthy {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
        box-shadow: 0 4px 15px rgba(235, 51, 73, 0.4);
    }
    
    .risk-hazardous {
        background: linear-gradient(135deg, #8e2de2, #4a00e0);
        color: white;
        box-shadow: 0 4px 15px rgba(142, 45, 226, 0.4);
    }
    
    /* Alert Banner */
    .alert-banner {
        background: linear-gradient(135deg, rgba(235, 51, 73, 0.9), rgba(244, 92, 67, 0.9));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #eb3349;
        margin: 1rem 0;
        color: white;
        font-weight: 500;
        box-shadow: 0 8px 32px rgba(235, 51, 73, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    /* Stats Box */
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255,255,255,0.7);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Progress Bar */
    .progress-bar {
        height: 8px;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #11998e, #38ef7d);
        border-radius: 10px;
        transition: width 1s ease;
        box-shadow: 0 0 10px rgba(17, 153, 142, 0.5);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Success/Info Messages */
    .success-msg {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.2), rgba(56, 239, 125, 0.2));
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #11998e;
        color: white;
        margin: 1rem 0;
    }
    
    /* Loading Animation */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: rotate 1s linear infinite;
        margin: 2rem auto;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 2rem;
        }
        
        .stat-number {
            font-size: 1.8rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = "Delhi"
    if 'subscribed_alerts' not in st.session_state:
        st.session_state.subscribed_alerts = False
    if 'favorite_cities' not in st.session_state:
        st.session_state.favorite_cities = ["Delhi", "Mumbai"]
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False

# Get real data with caching
@st.cache_data(ttl=300)
def get_real_data_for_city(city_name):
    """Get real air quality data from OpenWeather API"""
    if not REAL_DATA_AVAILABLE:
        return None
    
    try:
        data = fetch_city_data(city_name)
        return data
    except Exception as e:
        return None

@st.cache_data(ttl=300)
def get_real_forecast_data(city_name):
    """Get forecast data from OpenWeather API"""
    if not REAL_DATA_AVAILABLE:
        return None
    
    try:
        forecast = fetch_forecast(city_name)
        return forecast
    except Exception as e:
        return None

def generate_sample_data(city_name=None):
    """Generate data - use real data if available, otherwise sample data"""
    if REAL_DATA_AVAILABLE and city_name:
        real_data = get_real_data_for_city(city_name)
        forecast_data = get_real_forecast_data(city_name)
        
        if real_data and forecast_data:
            dates = [real_data['timestamp']]
            aqi_values = [real_data['aqi']]
            pm25_values = [real_data['pm2_5']]
            pm10_values = [real_data['pm10']]
            
            for item in forecast_data[:89]:
                dates.append(item['timestamp'])
                aqi_values.append(item['aqi'])
                pm25_values.append(item['pm2_5'])
                pm10_values.append(item['pm10'])
            
            return pd.DataFrame({
                'date': dates,
                'aqi': aqi_values,
                'pm25': pm25_values,
                'pm10': pm10_values
            })
    
    # Fallback to sample data
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    np.random.seed(42)
    base_aqi = 150
    seasonal_pattern = 30 * np.sin(np.linspace(0, 4*np.pi, 90))
    noise = np.random.normal(0, 15, 90)
    aqi_values = np.clip(base_aqi + seasonal_pattern + noise, 0, 500)
    
    pm25_values = aqi_values * 0.4 + np.random.normal(0, 10, 90)
    pm10_values = aqi_values * 0.6 + np.random.normal(0, 15, 90)
    
    return pd.DataFrame({
        'date': dates,
        'aqi': aqi_values,
        'pm25': pm25_values,
        'pm10': pm10_values
    })

def get_risk_level(aqi):
    """Determine health risk level based on AQI"""
    if aqi <= 50:
        return "Good", "#11998e", "good"
    elif aqi <= 100:
        return "Moderate", "#f7b731", "moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "#ee5a6f", "unhealthy"
    elif aqi <= 200:
        return "Unhealthy", "#eb3349", "very-unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy", "#c0392b", "very-unhealthy"
    else:
        return "Hazardous", "#8e2de2", "hazardous"

def get_health_recommendations(aqi, category):
    """Get health recommendations based on AQI level"""
    recommendations = {
        "Good": {
            "icon": "😊",
            "message": "Air quality is great! Perfect for outdoor activities.",
            "actions": ["Enjoy outdoor activities", "Open windows for fresh air", "Exercise outside"]
        },
        "Moderate": {
            "icon": "🙂",
            "message": "Air quality is acceptable for most people.",
            "actions": ["Unusually sensitive people should consider reducing prolonged outdoor exertion", "General public can enjoy outdoor activities"]
        },
        "Unhealthy for Sensitive": {
            "icon": "😐",
            "message": "Sensitive groups may experience health effects.",
            "actions": ["Children, elderly, and people with respiratory issues should limit outdoor activities", "Wear masks if going outside", "Keep windows closed"]
        },
        "Unhealthy": {
            "icon": "😷",
            "message": "Everyone may begin to experience health effects.",
            "actions": ["Limit prolonged outdoor exertion", "Keep windows closed", "Use air purifiers indoors", "Wear N95 masks outside"]
        },
        "Very Unhealthy": {
            "icon": "😨",
            "message": "Health alert: everyone may experience serious effects.",
            "actions": ["Avoid outdoor activities", "Stay indoors with air purifiers", "Keep all windows closed", "Seek medical attention if feeling unwell"]
        },
        "Hazardous": {
            "icon": "☠️",
            "message": "Health emergency: entire population affected.",
            "actions": ["Stay indoors at all times", "Use high-quality air purifiers", "Seal windows and doors", "Seek immediate medical attention if experiencing symptoms"]
        }
    }
    return recommendations.get(category, recommendations["Good"])

def create_aqi_gauge(aqi_value, title="Current AQI"):
    """Create an animated gauge chart for AQI"""
    category, color, _ = get_risk_level(aqi_value)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=aqi_value,
        title={'text': title, 'font': {'size': 24, 'color': 'white'}},
        delta={'reference': 50, 'increasing': {'color': "#eb3349"}, 'decreasing': {'color': "#11998e"}},
        gauge={
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(17, 153, 142, 0.3)'},
                {'range': [50, 100], 'color': 'rgba(247, 183, 49, 0.3)'},
                {'range': [100, 150], 'color': 'rgba(238, 90, 111, 0.3)'},
                {'range': [150, 200], 'color': 'rgba(235, 51, 73, 0.3)'},
                {'range': [200, 300], 'color': 'rgba(192, 57, 43, 0.3)'},
                {'range': [300, 500], 'color': 'rgba(142, 45, 226, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Poppins"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_trend_chart(data, metric='aqi', title='AQI Trend'):
    """Create modern trend chart with gradient fill"""
    fig = go.Figure()
    
    # Add gradient fill
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data[metric],
        mode='lines',
        name=metric.upper(),
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillgradient=dict(
            type='vertical',
            colorscale=['rgba(102, 126, 234, 0)', 'rgba(102, 126, 234, 0.5)']
        ),
        hovertemplate='<b>Date:</b> %{x}<br><b>Value:</b> %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': title, 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        font={'color': 'white', 'family': 'Poppins'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True},
        hovermode='x unified',
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

def create_comparison_chart(cities_data):
    """Create city comparison bar chart"""
    cities = [d['city'] for d in cities_data]
    aqis = [d['aqi'] for d in cities_data]
    colors = [get_risk_level(aqi)[1] for aqi in aqis]
    
    fig = go.Figure(data=[
        go.Bar(
            x=cities,
            y=aqis,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.3)', width=2)
            ),
            text=aqis,
            textposition='outside',
            textfont=dict(color='white', size=14, family='Poppins'),
            hovertemplate='<b>%{x}</b><br>AQI: %{y:.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={'text': 'City AQI Comparison', 'font': {'size': 22, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        font={'color': 'white', 'family': 'Poppins'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'title': 'AQI', 'gridcolor': 'rgba(255,255,255,0.1)'},
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    
    return fig

def create_pollutant_breakdown(pm25, pm10, co=0, no2=0, o3=0, so2=0):
    """Create pollutant breakdown pie chart"""
    labels = ['PM2.5', 'PM10', 'CO', 'NO2', 'O3', 'SO2']
    values = [pm25, pm10, max(co, 1), max(no2, 1), max(o3, 1), max(so2, 1)]
    
    colors = ['#667eea', '#764ba2', '#f7b731', '#eb3349', '#11998e', '#ee5a6f']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hole=0.4,
        textfont=dict(size=14, color='white', family='Poppins'),
        hovertemplate='<b>%{label}</b><br>%{value:.1f} μg/m³<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={'text': 'Pollutant Breakdown', 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'family': 'Poppins'},
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    return fig

# Page 1: Enhanced Home Dashboard
def render_home_dashboard():
    st.markdown("""
    <div class="app-header">
        <h1>🌍 AI Air Quality Analytics</h1>
        <p>Real-time monitoring • Predictive insights • Health protection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Location selector with favorites
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        all_cities = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
        location = st.selectbox(
            "📍 Select Location",
            all_cities,
            index=all_cities.index(st.session_state.selected_location),
            key="location_selector"
        )
        st.session_state.selected_location = location
    
    with col2:
        if st.button("⭐ Favorite", use_container_width=True):
            if location not in st.session_state.favorite_cities:
                st.session_state.favorite_cities.append(location)
                st.success(f"Added {location} to favorites!")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col4:
        comparison = st.checkbox("📊 Compare", value=st.session_state.comparison_mode)
        st.session_state.comparison_mode = comparison
    
    # Get current data
    data = generate_sample_data(location)
    current_aqi = data['aqi'].iloc[-1]
    current_pm25 = data['pm25'].iloc[-1]
    current_pm10 = data['pm10'].iloc[-1]
    
    # Get real-time data if available
    if REAL_DATA_AVAILABLE:
        real_data = get_real_data_for_city(location)
        if real_data:
            current_aqi = real_data['aqi']
            current_pm25 = real_data['pm2_5']
            current_pm10 = real_data['pm10']
    
    status, color, risk_class = get_risk_level(current_aqi)
    recommendations = get_health_recommendations(current_aqi, status)
    
    # Data source indicator
    if REAL_DATA_AVAILABLE:
        st.markdown("""
        <div class="success-msg">
            ✅ Live Data from OpenWeatherMap API • Updated every 5 minutes
        </div>
        """, unsafe_allow_html=True)
    
    # Alert banner for high AQI
    if current_aqi > 150:
        st.markdown(f"""
        <div class="alert-banner">
            <h3 style="margin:0;">⚠️ Air Quality Alert</h3>
            <p style="margin:0.5rem 0 0 0;">AQI is at hazardous levels in {location}. Limit outdoor activities and use air purifiers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main metrics with glassmorphism cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-box">
                <p class="stat-number">{current_aqi:.0f}</p>
                <p class="stat-label">AQI Level</p>
                <span class="risk-badge risk-{risk_class}">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-box">
                <p class="stat-number">{current_pm25:.1f}</p>
                <p class="stat-label">PM2.5 (μg/m³)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-box">
                <p class="stat-number">{current_pm10:.1f}</p>
                <p class="stat-label">PM10 (μg/m³)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate AQI change
        if len(data) > 1:
            prev_aqi = data['aqi'].iloc[-2]
            change = current_aqi - prev_aqi
            trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        else:
            change = 0
            trend = "➡️"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-box">
                <p class="stat-number">{trend} {abs(change):.1f}</p>
                <p class="stat-label">24h Change</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Health Recommendations
    st.markdown(f"""
    <div class="glass-card">
        <h2 style="color:white; margin-top:0;">{recommendations['icon']} Health Advisory</h2>
        <p style="color:rgba(255,255,255,0.9); font-size:1.1rem; margin:1rem 0;">{recommendations['message']}</p>
        <h3 style="color:white; margin-top:1.5rem;">Recommended Actions:</h3>
        <ul style="color:rgba(255,255,255,0.9); font-size:1rem;">
    """ + "".join([f"<li>{action}</li>" for action in recommendations['actions']]) + """
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_gauge = create_aqi_gauge(current_aqi, f"Current AQI - {location}")
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_pollutants = create_pollutant_breakdown(current_pm25, current_pm10)
        st.plotly_chart(fig_pollutants, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trend Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_trend = create_trend_chart(data.tail(30), 'aqi', f'30-Day AQI Trend - {location}')
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparison mode
    if st.session_state.comparison_mode and REAL_DATA_AVAILABLE:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        try:
            all_cities_data = fetch_all_cities()
            if all_cities_data:
                fig_comparison = create_comparison_chart(all_cities_data)
                st.plotly_chart(fig_comparison, use_container_width=True)
        except:
            pass
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📊 Today's Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_aqi = data['aqi'].tail(7).mean()
        st.markdown(f"""
        <div class="stat-box">
            <p class="stat-number">{avg_aqi:.0f}</p>
            <p class="stat-label">7-Day Average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        max_aqi = data['aqi'].tail(7).max()
        st.markdown(f"""
        <div class="stat-box">
            <p class="stat-number">{max_aqi:.0f}</p>
            <p class="stat-label">Weekly Peak</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        min_aqi = data['aqi'].tail(7).min()
        st.markdown(f"""
        <div class="stat-box">
            <p class="stat-number">{min_aqi:.0f}</p>
            <p class="stat-label">Weekly Low</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        good_days = len(data[data['aqi'] <= 50].tail(7))
        st.markdown(f"""
        <div class="stat-box">
            <p class="stat-number">{good_days}</p>
            <p class="stat-label">Good Air Days</p>
        </div>
        """, unsafe_allow_html=True)

# Continue with other pages...
# (I'll add the remaining pages in the next part)

def render_map_view():
    st.markdown("""
    <div class="app-header">
        <h1>🗺️ Interactive Air Quality Map</h1>
        <p>Real-time AQI hotspots across India</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get real data if available
    if REAL_DATA_AVAILABLE:
        try:
            all_cities = fetch_all_cities()
            
            if all_cities and len(all_cities) > 0:
                cities_data = {
                    'city': [c['city'] for c in all_cities],
                    'lat': [c['lat'] for c in all_cities],
                    'lon': [c['lon'] for c in all_cities],
                    'aqi': [c['aqi'] for c in all_cities],
                    'pm25': [c['pm2_5'] for c in all_cities],
                    'pm10': [c['pm10'] for c in all_cities]
                }
            else:
                cities_data = {
                    'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
                    'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
                    'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
                    'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
                    'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
                    'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
                }
        except:
            cities_data = {
                'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
                'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
                'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
                'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
                'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
                'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
            }
    else:
        cities_data = {
            'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
            'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
            'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
            'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
            'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
            'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
        }
    
    cities_df = pd.DataFrame(cities_data)
    cities_df['status'] = cities_df['aqi'].apply(lambda x: get_risk_level(x)[0])
    cities_df['color'] = cities_df['aqi'].apply(lambda x: get_risk_level(x)[1])
    
    col_map, col_details = st.columns([2, 1])
    
    with col_map:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon=cities_df['lon'],
            lat=cities_df['lat'],
            text=cities_df['city'],
            mode='markers+text',
            marker=dict(
                size=cities_df['aqi'] / 5,
                color=cities_df['aqi'],
                colorscale=[
                    [0, '#11998e'],
                    [0.2, '#f7b731'],
                    [0.4, '#ee5a6f'],
                    [0.6, '#eb3349'],
                    [0.8, '#c0392b'],
                    [1, '#8e2de2']
                ],
                cmin=0,
                cmax=300,
                colorbar=dict(
                    title="AQI",
                    thickness=15,
                    len=0.7,
                    bgcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white')
                ),
                line=dict(width=2, color='white')
            ),
            textposition="top center",
            textfont=dict(size=12, color='white', family='Poppins'),
            hovertemplate='<b>%{text}</b><br>AQI: %{marker.color:.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=600,
            geo=dict(
                scope='asia',
                center=dict(lat=23, lon=80),
                projection_scale=4,
                showland=True,
                landcolor='rgba(200, 200, 200, 0.3)',
                coastlinecolor='rgba(255, 255, 255, 0.5)',
                showcountries=True,
                countrycolor='rgba(255, 255, 255, 0.3)',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Poppins'),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_details:
        st.markdown("### 📍 City Details")
        
        selected_city = st.selectbox("Select City", cities_df['city'].tolist())
        
        city_info = cities_df[cities_df['city'] == selected_city].iloc[0]
        
        st.markdown(f"""
        <div class="glass-card">
            <h2 style="color:white; margin:0;">{selected_city}</h2>
            <div style="margin-top:1.5rem;">
                <span class="risk-badge risk-{get_risk_level(city_info['aqi'])[2]}">{city_info['status']}</span>
            </div>
            <div style="margin-top:1.5rem; color:white;">
                <p style="font-size:3rem; margin:0; font-weight:700;">{city_info['aqi']:.0f}</p>
                <p style="font-size:1rem; opacity:0.8; margin:0;">Air Quality Index</p>
            </div>
            <div style="margin-top:1.5rem; color:rgba(255,255,255,0.9);">
                <p><strong>PM2.5:</strong> {city_info['pm25']:.1f} μg/m³</p>
                <p><strong>PM10:</strong> {city_info['pm10']:.1f} μg/m³</p>
                <p><strong>Location:</strong> {city_info['lat']:.2f}°N, {city_info['lon']:.2f}°E</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 View Detailed Analysis", use_container_width=True):
            st.session_state.selected_location = selected_city
            st.session_state.page = "Home"
            st.rerun()

# Main app logic
def main():
    load_custom_css()
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h2 style="color:white; margin:0;">🌍 IHIP</h2>
            <p style="color:rgba(255,255,255,0.7); font-size:0.9rem;">Air Quality Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Home", "🗺️ Map View", "📈 Trends", "🧮 Health Calculator", "🔔 Alerts", "⚙️ Admin"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Favorites section
        if st.session_state.favorite_cities:
            st.markdown("### ⭐ Favorites")
            for city in st.session_state.favorite_cities:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(city, key=f"fav_{city}", use_container_width=True):
                        st.session_state.selected_location = city
                        st.rerun()
                with col2:
                    if st.button("✖", key=f"remove_{city}"):
                        st.session_state.favorite_cities.remove(city)
                        st.rerun()
        
        st.markdown("---")
        
        # Quick stats in sidebar
        st.markdown("### 📊 Quick Stats")
        if REAL_DATA_AVAILABLE:
            try:
                all_cities = fetch_all_cities()
                if all_cities:
                    avg_aqi = np.mean([c['aqi'] for c in all_cities])
                    max_aqi = max([c['aqi'] for c in all_cities])
                    worst_city = max(all_cities, key=lambda x: x['aqi'])['city']
                    
                    st.markdown(f"""
                    <div class="stat-box" style="margin:0.5rem 0;">
                        <p style="color:white; font-size:1.5rem; margin:0;">{avg_aqi:.0f}</p>
                        <p style="color:rgba(255,255,255,0.7); font-size:0.8rem; margin:0;">National Avg AQI</p>
                    </div>
                    <div class="stat-box" style="margin:0.5rem 0;">
                        <p style="color:#eb3349; font-size:1.5rem; margin:0;">{max_aqi:.0f}</p>
                        <p style="color:rgba(255,255,255,0.7); font-size:0.8rem; margin:0;">Highest ({worst_city})</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; padding:1rem; color:rgba(255,255,255,0.5); font-size:0.8rem;">
            <p>Data updated every 5 min</p>
            <p>© 2025 IHIP System</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to pages
    if page == "🏠 Home":
        render_home_dashboard()
    elif page == "🗺️ Map View":
        render_map_view()
    elif page == "📈 Trends":
        st.info("Trends page - Under construction")
    elif page == "🧮 Health Calculator":
        st.info("Health Calculator page - Under construction")
    elif page == "🔔 Alerts":
        st.info("Alerts page - Under construction")
    elif page == "⚙️ Admin":
        st.info("Admin page - Under construction")

if __name__ == "__main__":
    main()
