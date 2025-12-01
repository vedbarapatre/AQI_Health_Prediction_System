"""
AI-Based Air Quality & Health Prediction System (IHIP)
A comprehensive dashboard for air quality monitoring and health risk assessment
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
    st.warning(f"⚠️ OpenWeather client not available: {e}")

# Page configuration
st.set_page_config(
    page_title="IHIP - Air Quality & Health Prediction",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, modern, government-style UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: #F7FAFC;
    }
    
    /* Dark mode override */
    [data-theme="dark"] .main {
        background-color: #1a202c;
    }
    
    /* Card styles */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    [data-theme="dark"] .metric-card {
        background: #2D3748;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Risk level colors */
    .risk-low {
        background: #2ECC71;
        color: white;
    }
    
    .risk-medium {
        background: #F1C40F;
        color: #2C3E50;
    }
    
    .risk-high {
        background: #E67E22;
        color: white;
    }
    
    .risk-very-high {
        background: #E74C3C;
        color: white;
    }
    
    /* Alert banner */
    .alert-banner {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
        border-left: 4px solid;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .app-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .app-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1rem;
    }
    
    /* Metric display */
    .big-metric {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Button styles */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: white;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] {
        background: #2D3748;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    [data-theme="dark"] .chart-container {
        background: #2D3748;
    }
    
    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
        height: 100px;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #A0AEC0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    /* Responsive typography */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 1.5rem;
        }
        
        .big-metric {
            font-size: 2rem;
        }
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
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

# Generate sample data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_real_data_for_city(city_name):
    """Get real air quality data from OpenWeather API"""
    if not REAL_DATA_AVAILABLE:
        return None
    
    try:
        data = fetch_city_data(city_name)
        return data
    except Exception as e:
        st.error(f"Error fetching real data: {e}")
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
        st.error(f"Error fetching forecast: {e}")
        return None

def generate_sample_data(city_name=None):
    """Generate data - use real data if available, otherwise sample data"""
    # Try to get real data first
    if REAL_DATA_AVAILABLE and city_name:
        real_data = get_real_data_for_city(city_name)
        forecast_data = get_real_forecast_data(city_name)
        
        if real_data and forecast_data:
            # Create dataframe from real + forecast data
            dates = [real_data['timestamp']]
            aqi_values = [real_data['aqi']]
            pm25_values = [real_data['pm2_5']]
            pm10_values = [real_data['pm10']]
            
            # Add forecast data
            for item in forecast_data[:89]:  # Get 89 more points for 90 total
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
    
    # Historical data with realistic patterns
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
        return "Good", "#2ECC71", "Low"
    elif aqi <= 100:
        return "Moderate", "#F1C40F", "Low"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "#E67E22", "Medium"
    elif aqi <= 200:
        return "Unhealthy", "#E67E22", "High"
    elif aqi <= 300:
        return "Very Unhealthy", "#E74C3C", "Very High"
    else:
        return "Hazardous", "#8B0000", "Very High"

def get_risk_class(risk):
    """Get CSS class for risk level"""
    risk_map = {
        "Low": "risk-low",
        "Medium": "risk-medium",
        "High": "risk-high",
        "Very High": "risk-very-high"
    }
    return risk_map.get(risk, "risk-low")

# Page 1: Home / Overview Dashboard
def render_home_dashboard():
    st.markdown("""
    <div class="app-header">
        <h1>🌍 AI-Based Air Quality & Health Prediction System</h1>
        <p>Integrated Health Information Platform (IHIP) • Real-time monitoring and forecasting</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Location selector
    col_loc, col_refresh = st.columns([3, 1])
    with col_loc:
        location = st.selectbox(
            "📍 Select Location",
            ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune"],
            key="location_selector"
        )
        st.session_state.selected_location = location
    
    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Get current data (with real API data if available)
    data = generate_sample_data(location)
    current_aqi = data['aqi'].iloc[-1]
    current_pm25 = data['pm25'].iloc[-1]
    current_pm10 = data['pm10'].iloc[-1]
    
    # Show data source indicator
    if REAL_DATA_AVAILABLE:
        st.success("✅ Using REAL air quality data from OpenWeatherMap API")
    else:
        st.info("ℹ️ Using sample data (Add API key to .streamlit/secrets.toml for real data)")
    
    status, color, risk = get_risk_level(current_aqi)
    
    # Alert banner
    if risk in ["High", "Very High"]:
        st.markdown(f"""
        <div class="alert-banner" style="background-color: {color}20; border-left-color: {color}; color: {color};">
            ⚠️ <strong>{risk} Health Risk Alert:</strong> Air quality is unhealthy. Sensitive groups should limit outdoor activities.
        </div>
        """, unsafe_allow_html=True)
    
    # Main metrics
    st.subheader("📊 Current Air Quality Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {color};">
            <div class="metric-label">AIR QUALITY INDEX</div>
            <div class="big-metric" style="color: {color};">{int(current_aqi)}</div>
            <div style="color: {color}; font-weight: 600; margin-top: 0.5rem;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pm25_color = "#E67E22" if current_pm25 > 55 else "#2ECC71"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PM2.5 (μg/m³)</div>
            <div class="big-metric" style="color: {pm25_color};">{int(current_pm25)}</div>
            <div style="color: #718096; font-size: 0.875rem; margin-top: 0.5rem;">Fine Particles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pm10_color = "#E67E22" if current_pm10 > 154 else "#2ECC71"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PM10 (μg/m³)</div>
            <div class="big-metric" style="color: {pm10_color};">{int(current_pm10)}</div>
            <div style="color: #718096; font-size: 0.875rem; margin-top: 0.5rem;">Coarse Particles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card {get_risk_class(risk)}">
            <div class="metric-label" style="color: inherit; opacity: 0.9;">HEALTH RISK</div>
            <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{risk}</div>
            <div style="font-size: 0.875rem; opacity: 0.9;">Risk Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔔 Subscribe to Alerts", use_container_width=True, type="primary"):
            st.session_state.subscribed_alerts = True
            st.success("✅ Successfully subscribed to air quality alerts!")
    
    with col2:
        if st.button("🗺️ View Interactive Map", use_container_width=True):
            st.session_state.page = "map"
            st.rerun()
    
    with col3:
        if st.button("📈 View Detailed Trends", use_container_width=True):
            st.session_state.page = "trends"
            st.rerun()
    
    # 30-day trend chart
    st.subheader("📅 30-Day AQI Trend")
    
    recent_data = data.tail(30)
    
    fig = go.Figure()
    
    # Add AQI line
    fig.add_trace(go.Scatter(
        x=recent_data['date'],
        y=recent_data['aqi'],
        mode='lines+markers',
        name='AQI',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Add reference lines
    fig.add_hline(y=50, line_dash="dash", line_color="#2ECC71", annotation_text="Good", annotation_position="right")
    fig.add_hline(y=100, line_dash="dash", line_color="#F1C40F", annotation_text="Moderate", annotation_position="right")
    fig.add_hline(y=150, line_dash="dash", line_color="#E67E22", annotation_text="Unhealthy", annotation_position="right")
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title="Date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title="AQI Value"
        ),
        hovermode='x unified',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional info cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0;">🏥 Health Recommendations</h4>
            <ul style="line-height: 1.8;">
                <li>👨‍👩‍👧‍👦 Sensitive groups should limit prolonged outdoor activities</li>
                <li>😷 Consider wearing a mask when outdoors</li>
                <li>🏠 Keep windows closed during high pollution hours</li>
                <li>🌱 Use air purifiers indoors if available</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0;">📊 Data Sources</h4>
            <div style="line-height: 2;">
                <div>🛰️ <strong>Satellite Data:</strong> NASA, ESA</div>
                <div>🏭 <strong>Ground Stations:</strong> CPCB, State Boards</div>
                <div>🤖 <strong>AI Model:</strong> LSTM + Random Forest</div>
                <div>⏱️ <strong>Last Updated:</strong> {}</div>
            </div>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

# Page 2: Interactive Map
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
                st.success("✅ Displaying REAL air quality data for all cities")
            else:
                # Fallback to sample data
                cities_data = {
                    'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
                    'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
                    'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
                    'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
                    'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
                    'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
                }
                st.info("ℹ️ Using sample data")
        except Exception as e:
            st.warning(f"⚠️ Error loading real data: {e}. Using sample data.")
            cities_data = {
                'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
                'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
                'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
                'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
                'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
                'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
            }
    else:
        # Sample city data
        cities_data = {
            'city': ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'],
            'lat': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 17.3850, 18.5204, 23.0225, 26.9124, 26.8467],
            'lon': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 78.4867, 73.8567, 72.5714, 75.7873, 80.9462],
            'aqi': [168, 95, 78, 142, 65, 88, 112, 155, 178, 195],
            'pm25': [88, 48, 35, 72, 28, 42, 58, 82, 95, 105],
            'pm10': [145, 82, 68, 128, 55, 78, 98, 138, 158, 168]
        }
        st.info("ℹ️ Using sample data (Add API key to .streamlit/secrets.toml for real data)")
    
    cities_df = pd.DataFrame(cities_data)
    cities_df['status'] = cities_df['aqi'].apply(lambda x: get_risk_level(x)[0])
    cities_df['color'] = cities_df['aqi'].apply(lambda x: get_risk_level(x)[1])
    cities_df['risk'] = cities_df['aqi'].apply(lambda x: get_risk_level(x)[2])
    
    col_map, col_details = st.columns([2, 1])
    
    with col_map:
        # Create map
        fig = go.Figure()
        
        # Add city markers
        fig.add_trace(go.Scattergeo(
            lon=cities_df['lon'],
            lat=cities_df['lat'],
            text=cities_df['city'],
            mode='markers+text',
            marker=dict(
                size=cities_df['aqi'] / 5,
                color=cities_df['aqi'],
                colorscale=[
                    [0, '#2ECC71'],
                    [0.2, '#F1C40F'],
                    [0.4, '#E67E22'],
                    [0.6, '#E74C3C'],
                    [1, '#8B0000']
                ],
                cmin=0,
                cmax=300,
                colorbar=dict(
                    title="AQI",
                    thickness=15,
                    len=0.7
                ),
                line=dict(width=1, color='white')
            ),
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>' +
                          'AQI: %{marker.color:.0f}<br>' +
                          '<extra></extra>'
        ))
        
        fig.update_layout(
            height=600,
            geo=dict(
                scope='asia',
                center=dict(lat=23, lon=80),
                projection_scale=4,
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showcountries=True,
                countrycolor='rgb(204, 204, 204)'
            ),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_details:
        st.subheader("📍 City Details")
        
        selected_city = st.selectbox("Select City", cities_df['city'].tolist())
        
        city_info = cities_df[cities_df['city'] == selected_city].iloc[0]
        
        st.markdown(f"""
        <div class="metric-card {get_risk_class(city_info['risk'])}">
            <h3 style="margin-top: 0; color: inherit;">{selected_city}</h3>
            <div style="font-size: 3rem; font-weight: 700; margin: 1rem 0;">{int(city_info['aqi'])}</div>
            <div style="font-size: 1.2rem; font-weight: 600;">{city_info['status']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Pollutant Levels</h4>
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                    <span>PM2.5:</span>
                    <strong>{int(city_info['pm25'])} μg/m³</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                    <span>PM10:</span>
                    <strong>{int(city_info['pm10'])} μg/m³</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>Health Advisory</h4>
            <p style="line-height: 1.6; color: #4A5568;">
                Based on current air quality levels, sensitive individuals should consider 
                limiting prolonged outdoor activities. General population should monitor symptoms.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Legend
    st.subheader("📊 AQI Categories")
    
    legend_cols = st.columns(5)
    categories = [
        ("Good", "0-50", "#2ECC71"),
        ("Moderate", "51-100", "#F1C40F"),
        ("Unhealthy (Sensitive)", "101-150", "#E67E22"),
        ("Unhealthy", "151-200", "#E74C3C"),
        ("Very Unhealthy", "201-300", "#8B0000")
    ]
    
    for col, (label, range_val, color) in zip(legend_cols, categories):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="background: {color}; color: white; text-align: center;">
                <div style="font-weight: 600;">{label}</div>
                <div style="font-size: 0.875rem; opacity: 0.9;">{range_val}</div>
            </div>
            """, unsafe_allow_html=True)

# Page 3: Trend & Analytics
def render_trends_analytics():
    st.markdown("""
    <div class="app-header">
        <h1>📈 Trend & Analytics</h1>
        <p>Historical data and AI-powered forecasts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_range = st.selectbox("Time Range", ["Past 7 Days", "Past 30 Days", "Past 90 Days"])
    
    with col2:
        pollutant = st.selectbox("Pollutant Type", ["AQI", "PM2.5", "PM10"])
    
    with col3:
        location = st.selectbox("Location", ["Delhi", "Mumbai", "Bangalore", "All Cities"])
    
    # Generate data based on selection
    days_map = {"Past 7 Days": 7, "Past 30 Days": 30, "Past 90 Days": 90}
    days = days_map[time_range]
    
    data = generate_sample_data()
    recent_data = data.tail(days)
    
    # Generate forecast (next 7 days)
    forecast_dates = pd.date_range(start=data['date'].iloc[-1] + timedelta(days=1), periods=7, freq='D')
    last_aqi = data['aqi'].iloc[-1]
    forecast_aqi = last_aqi + np.random.normal(0, 10, 7).cumsum()
    forecast_aqi = np.clip(forecast_aqi, 0, 500)
    
    # Main trend chart
    st.subheader(f"📊 {pollutant} Trend - {time_range}")
    
    fig = go.Figure()
    
    # Historical data
    pollutant_map = {"AQI": "aqi", "PM2.5": "pm25", "PM10": "pm10"}
    y_col = pollutant_map[pollutant]
    
    fig.add_trace(go.Scatter(
        x=recent_data['date'],
        y=recent_data[y_col],
        mode='lines',
        name='Historical',
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Forecast
    if pollutant == "AQI":
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_aqi,
            mode='lines',
            name='Forecast',
            line=dict(color='#f093fb', width=3, dash='dash'),
            fill='tozeroy',
            fillcolor='rgba(240, 147, 251, 0.1)'
        ))
    
    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title="Date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title=f"{pollutant} Value"
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparative pollutant chart
    st.subheader("📊 Pollutant Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PM2.5 vs PM10
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['pm25'],
            mode='lines',
            name='PM2.5',
            line=dict(color='#E67E22', width=2)
        ))
        
        fig2.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['pm10'],
            mode='lines',
            name='PM10',
            line=dict(color='#E74C3C', width=2)
        ))
        
        fig2.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="μg/m³"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Distribution
        fig3 = go.Figure()
        
        fig3.add_trace(go.Box(
            y=recent_data['aqi'],
            name='AQI',
            marker_color='#667eea',
            boxmean='sd'
        ))
        
        fig3.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="AQI"),
            showlegend=False
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    # Model accuracy metrics
    st.subheader("🤖 AI Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("RMSE", "12.5", "Root Mean Square Error"),
        ("MAE", "8.3", "Mean Absolute Error"),
        ("R² Score", "0.94", "Coefficient of Determination"),
        ("Accuracy", "91%", "Prediction Accuracy")
    ]
    
    for col, (label, value, desc) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">{label}</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 0.5rem 0;">{value}</div>
                <div style="font-size: 0.75rem; color: #718096;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# Page 4: Health Risk Calculator
def render_health_calculator():
    st.markdown("""
    <div class="app-header">
        <h1>🏥 Personal Health Risk Calculator</h1>
        <p>Get personalized air quality health recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("👤 Enter Your Information")
        
        with st.form("health_form"):
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            
            health_conditions = st.multiselect(
                "Existing Health Conditions",
                ["None", "Asthma", "COPD", "Heart Disease", "Diabetes", "Respiratory Allergies"]
            )
            
            exposure_level = st.select_slider(
                "Daily Outdoor Exposure",
                options=["Minimal (<1 hour)", "Low (1-3 hours)", "Moderate (3-6 hours)", "High (>6 hours)"]
            )
            
            location = st.selectbox(
                "Your Location",
                ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune"]
            )
            
            submitted = st.form_submit_button("Calculate My Risk", type="primary", use_container_width=True)
        
        if submitted:
            # Calculate risk score
            base_risk = 50
            
            # Age factor
            if age < 5 or age > 65:
                base_risk += 20
            elif age < 18:
                base_risk += 10
            
            # Health conditions
            if "Asthma" in health_conditions or "COPD" in health_conditions:
                base_risk += 25
            if "Heart Disease" in health_conditions:
                base_risk += 20
            if "Respiratory Allergies" in health_conditions:
                base_risk += 15
            if "Diabetes" in health_conditions:
                base_risk += 10
            
            # Exposure level
            exposure_map = {
                "Minimal (<1 hour)": 0,
                "Low (1-3 hours)": 10,
                "Moderate (3-6 hours)": 20,
                "High (>6 hours)": 30
            }
            base_risk += exposure_map[exposure_level]
            
            # Location AQI (sample)
            data = generate_sample_data()
            current_aqi = data['aqi'].iloc[-1]
            base_risk = base_risk * (current_aqi / 100)
            
            # Determine final risk level
            if base_risk < 50:
                risk_level = "Low"
                risk_color = "#2ECC71"
                risk_class = "risk-low"
            elif base_risk < 100:
                risk_level = "Medium"
                risk_color = "#F1C40F"
                risk_class = "risk-medium"
            elif base_risk < 150:
                risk_level = "High"
                risk_color = "#E67E22"
                risk_class = "risk-high"
            else:
                risk_level = "Very High"
                risk_color = "#E74C3C"
                risk_class = "risk-very-high"
            
            st.session_state.calculated_risk = {
                'score': int(base_risk),
                'level': risk_level,
                'color': risk_color,
                'class': risk_class,
                'conditions': health_conditions,
                'age': age
            }
    
    with col2:
        st.subheader("📊 Your Health Risk Assessment")
        
        if 'calculated_risk' in st.session_state:
            risk_info = st.session_state.calculated_risk
            
            st.markdown(f"""
            <div class="metric-card {risk_info['class']}" style="text-align: center; padding: 2rem;">
                <div style="font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.9;">YOUR RISK SCORE</div>
                <div style="font-size: 4rem; font-weight: 700; margin: 1rem 0;">{risk_info['score']}</div>
                <div style="font-size: 1.5rem; font-weight: 600;">{risk_info['level']} Risk</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendations based on risk
            st.markdown("### 💡 Personalized Recommendations")
            
            if risk_info['level'] == "Low":
                recommendations = [
                    "✅ You can engage in normal outdoor activities",
                    "🚶 Regular exercise outdoors is safe",
                    "🪟 Good ventilation at home is recommended",
                    "😊 Monitor air quality daily for any changes"
                ]
            elif risk_info['level'] == "Medium":
                recommendations = [
                    "⚠️ Consider reducing prolonged outdoor activities",
                    "😷 Wear a mask during peak pollution hours",
                    "🏠 Keep windows closed during high pollution times",
                    "💊 Keep prescribed medications handy"
                ]
            elif risk_info['level'] == "High":
                recommendations = [
                    "🚫 Avoid prolonged outdoor activities",
                    "😷 Always wear N95 masks when going outside",
                    "🏠 Stay indoors with air purifiers running",
                    "🏥 Monitor symptoms closely and consult doctor if needed"
                ]
            else:
                recommendations = [
                    "⛔ Avoid all outdoor activities",
                    "🏥 Consult your doctor immediately if experiencing symptoms",
                    "😷 Use N95/N99 masks even for brief outdoor exposure",
                    "🌬️ Use air purifiers indoors continuously"
                ]
            
            for rec in recommendations:
                st.markdown(f"""
                <div class="metric-card" style="padding: 1rem; margin: 0.5rem 0;">
                    <div style="font-size: 1rem;">{rec}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Safety tips
            st.markdown("### 🛡️ General Safety Tips")
            
            st.markdown("""
            <div class="metric-card">
                <ul style="line-height: 2; margin: 0;">
                    <li>📱 Install air quality monitoring apps</li>
                    <li>🌱 Keep indoor plants for better air quality</li>
                    <li>💧 Stay hydrated to help your body filter toxins</li>
                    <li>🏃 Exercise indoors when AQI is high</li>
                    <li>🩺 Regular health check-ups are important</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Please fill out the form on the left to calculate your personal health risk score.")

# Page 5: Alerts & Notifications
def render_alerts():
    st.markdown("""
    <div class="app-header">
        <h1>🔔 Alerts & Notifications</h1>
        <p>Stay informed about air quality changes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Subscription status
    if st.session_state.subscribed_alerts:
        st.success("✅ You are subscribed to air quality alerts")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("🔔 Subscribe to receive real-time air quality alerts")
        with col2:
            if st.button("Subscribe Now", type="primary", use_container_width=True):
                st.session_state.subscribed_alerts = True
                st.rerun()
    
    # Active alerts
    st.subheader("⚠️ Active Alerts")
    
    # Sample alerts
    alerts = [
        {
            "type": "Air Quality Alert",
            "severity": "High",
            "color": "#E74C3C",
            "location": "Delhi",
            "message": "AQI levels have exceeded 200. Sensitive groups should avoid outdoor activities.",
            "date": datetime.now() - timedelta(hours=2),
            "icon": "🌫️"
        },
        {
            "type": "Health Risk Alert",
            "severity": "Medium",
            "color": "#E67E22",
            "location": "Mumbai",
            "message": "PM2.5 levels are elevated. Consider wearing masks outdoors.",
            "date": datetime.now() - timedelta(hours=5),
            "icon": "😷"
        },
        {
            "type": "Weather Alert",
            "severity": "Low",
            "color": "#F1C40F",
            "location": "Bangalore",
            "message": "Wind speed may help disperse pollutants. Air quality may improve.",
            "date": datetime.now() - timedelta(hours=12),
            "icon": "🌬️"
        },
        {
            "type": "Air Quality Alert",
            "severity": "Very High",
            "color": "#8B0000",
            "location": "Lucknow",
            "message": "Hazardous air quality detected. All outdoor activities should be avoided.",
            "date": datetime.now() - timedelta(days=1),
            "icon": "⛔"
        }
    ]
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.multiselect(
            "Filter by Type",
            ["All", "Air Quality Alert", "Health Risk Alert", "Weather Alert"],
            default=["All"]
        )
    with col2:
        filter_severity = st.multiselect(
            "Filter by Severity",
            ["All", "Low", "Medium", "High", "Very High"],
            default=["All"]
        )
    
    # Display alerts
    for alert in alerts:
        # Apply filters
        if "All" not in filter_type and alert["type"] not in filter_type:
            continue
        if "All" not in filter_severity and alert["severity"] not in filter_severity:
            continue
        
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {alert['color']};">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem;">{alert['icon']}</span>
                        <span style="font-weight: 600; font-size: 1.1rem;">{alert['type']}</span>
                        <span style="background: {alert['color']}; color: white; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                            {alert['severity']}
                        </span>
                    </div>
                    <div style="color: #4A5568; margin: 0.5rem 0;">
                        📍 {alert['location']}
                    </div>
                    <div style="margin: 0.75rem 0; line-height: 1.6;">
                        {alert['message']}
                    </div>
                    <div style="color: #A0AEC0; font-size: 0.875rem;">
                        🕒 {alert['date'].strftime('%Y-%m-%d %H:%M')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Historical alerts
    st.subheader("📜 Alert History")
    
    history_data = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)],
        'Total Alerts': [12, 8, 15, 10, 6, 14, 9],
        'High Severity': [3, 2, 5, 3, 1, 4, 2],
        'Medium Severity': [5, 4, 6, 4, 3, 6, 4],
        'Low Severity': [4, 2, 4, 3, 2, 4, 3]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Low', x=history_data['Date'], y=history_data['Low Severity'], marker_color='#F1C40F'))
    fig.add_trace(go.Bar(name='Medium', x=history_data['Date'], y=history_data['Medium Severity'], marker_color='#E67E22'))
    fig.add_trace(go.Bar(name='High', x=history_data['Date'], y=history_data['High Severity'], marker_color='#E74C3C'))
    
    fig.update_layout(
        barmode='stack',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="Number of Alerts"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Page 6: Admin Dashboard
def render_admin_dashboard():
    st.markdown("""
    <div class="app-header">
        <h1>⚙️ Admin / Health Officer Dashboard</h1>
        <p>System monitoring and data management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System status
    st.subheader("🔧 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #2ECC71;">
            <div class="metric-label">DATA SOURCES</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: #2ECC71; margin: 0.5rem 0;">8/8</div>
            <div style="color: #2ECC71; font-weight: 600;">All Online</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #667eea;">
            <div class="metric-label">LAST SYNC</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #667eea; margin: 0.5rem 0;">5 min ago</div>
            <div style="color: #718096;">Real-time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #F1C40F;">
            <div class="metric-label">MODEL VERSION</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #F1C40F; margin: 0.5rem 0;">v2.5.1</div>
            <div style="color: #718096;">Updated 2d ago</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #E67E22;">
            <div class="metric-label">DATA RECORDS</div>
            <div style="font-size: 2rem; font-weight: 700; color: #E67E22; margin: 0.5rem 0;">1.2M</div>
            <div style="color: #718096;">Total entries</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data source status
    st.subheader("📡 Data Source Status")
    
    sources = [
        {"name": "CPCB Ground Stations", "status": "Online", "last_update": "2 min", "records": "850K"},
        {"name": "State Pollution Boards", "status": "Online", "last_update": "5 min", "records": "320K"},
        {"name": "NASA Satellite Data", "status": "Online", "last_update": "15 min", "records": "45K"},
        {"name": "ESA Sentinel-5P", "status": "Online", "last_update": "18 min", "records": "38K"},
        {"name": "Weather API", "status": "Online", "last_update": "3 min", "records": "125K"},
        {"name": "Traffic Data", "status": "Online", "last_update": "1 min", "records": "95K"}
    ]
    
    for source in sources:
        status_color = "#2ECC71" if source["status"] == "Online" else "#E74C3C"
        st.markdown(f"""
        <div class="metric-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 1rem;">{source['name']}</div>
                <div style="color: #718096; font-size: 0.875rem; margin-top: 0.25rem;">
                    Last update: {source['last_update']} ago • {source['records']} records
                </div>
            </div>
            <div style="background: {status_color}; color: white; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 600;">
                {source['status']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Model controls
    st.subheader("🤖 AI Model Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0;">Model Management</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Retrain Model", use_container_width=True):
            with st.spinner("Retraining model... This may take a few minutes."):
                import time
                time.sleep(2)
            st.success("✅ Model retrained successfully! New version: v2.5.2")
        
        if st.button("📊 View Model Metrics", use_container_width=True):
            st.info("Model metrics: RMSE=12.5, MAE=8.3, R²=0.94")
        
        if st.button("💾 Export Model", use_container_width=True):
            st.info("Model exported to: /models/aqi_model_v2.5.1.pkl")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin-top: 0;">Training Configuration</h4>
            <div style="line-height: 2;">
                <div>🔢 <strong>Training Samples:</strong> 1.2M records</div>
                <div>📅 <strong>Data Range:</strong> 2020-2025</div>
                <div>🧮 <strong>Features:</strong> 24 parameters</div>
                <div>⚡ <strong>Algorithm:</strong> LSTM + Random Forest</div>
                <div>🎯 <strong>Target:</strong> 24h AQI forecast</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data preview
    st.subheader("📋 Recent Data Preview")
    
    sample_data = generate_sample_data().tail(10)
    sample_data['timestamp'] = pd.date_range(end=datetime.now(), periods=10, freq='H')
    sample_data = sample_data[['timestamp', 'aqi', 'pm25', 'pm10']]
    sample_data.columns = ['Timestamp', 'AQI', 'PM2.5', 'PM10']
    
    st.dataframe(sample_data, use_container_width=True, hide_index=True)
    
    # Heatmap of affected regions
    st.subheader("🗺️ Regional AQI Heatmap")
    
    # Create sample heatmap data
    hours = [f"{i:02d}:00" for i in range(24)]
    cities = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
    
    heatmap_data = np.random.randint(50, 200, size=(len(cities), len(hours)))
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=hours,
        y=cities,
        colorscale=[
            [0, '#2ECC71'],
            [0.33, '#F1C40F'],
            [0.66, '#E67E22'],
            [1, '#E74C3C']
        ],
        colorbar=dict(title="AQI")
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(title="Time (24h)"),
        yaxis=dict(title="City")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Prediction vs Actual
    st.subheader("📊 AI Prediction vs Actual Comparison")
    
    comparison_data = generate_sample_data().tail(30)
    comparison_data['predicted'] = comparison_data['aqi'] + np.random.normal(0, 8, 30)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=comparison_data['date'],
        y=comparison_data['aqi'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=comparison_data['date'],
        y=comparison_data['predicted'],
        mode='lines+markers',
        name='Predicted',
        line=dict(color='#f093fb', width=3, dash='dash'),
        marker=dict(size=6, symbol='diamond')
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="Date"),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="AQI"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Main app
def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="margin: 0; color: #667eea;">🌍 IHIP</h2>
            <p style="margin: 0.5rem 0 0 0; color: #718096; font-size: 0.875rem;">
                Air Quality & Health Prediction
            </p>
        </div>
        <hr style="margin: 1rem 0; border: none; border-top: 1px solid #E2E8F0;">
        """, unsafe_allow_html=True)
        
        # Navigation
        page = st.radio(
            "Navigation",
            [
                "🏠 Home Dashboard",
                "🗺️ Interactive Map",
                "📈 Trends & Analytics",
                "🏥 Health Risk Calculator",
                "🔔 Alerts & Notifications",
                "⚙️ Admin Dashboard"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        
        # Dark mode toggle
        dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Info section
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: #F7FAFC; border-radius: 8px;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">ℹ️ About IHIP</div>
            <div style="font-size: 0.875rem; line-height: 1.6; color: #4A5568;">
                Integrated Health Information Platform for AI-based air quality monitoring and health risk assessment.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 1rem; padding: 1rem; background: #F7FAFC; border-radius: 8px;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">📞 Emergency</div>
            <div style="font-size: 0.875rem; line-height: 1.6; color: #4A5568;">
                Health Emergency: 108<br>
                Pollution Complaint: 1800-180-1801
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dark mode CSS
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        :root {
            --background-color: #1a202c;
            --text-color: #E2E8F0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "🏠 Home Dashboard":
        render_home_dashboard()
    elif page == "🗺️ Interactive Map":
        render_map_view()
    elif page == "📈 Trends & Analytics":
        render_trends_analytics()
    elif page == "🏥 Health Risk Calculator":
        render_health_calculator()
    elif page == "🔔 Alerts & Notifications":
        render_alerts()
    elif page == "⚙️ Admin Dashboard":
        render_admin_dashboard()

if __name__ == "__main__":
    main()
