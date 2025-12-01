"""
Additional utility functions for the enhanced IHIP system
Export, analytics, and advanced features
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

def export_to_csv(data, filename="aqi_data.csv"):
    """Export data to CSV format"""
    return data.to_csv(index=False).encode('utf-8')

def export_to_excel(data, filename="aqi_data.xlsx"):
    """Export data to Excel format"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='AQI Data')
    return output.getvalue()

def create_heatmap_calendar(data):
    """Create a calendar heatmap of AQI values"""
    # Prepare data for heatmap
    data['day'] = data['date'].dt.day_name()
    data['week'] = data['date'].dt.isocalendar().week
    
    # Create pivot table
    pivot = data.pivot_table(values='aqi', index='day', columns='week', aggfunc='mean')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[
            [0, '#11998e'],
            [0.2, '#f7b731'],
            [0.4, '#ee5a6f'],
            [0.6, '#eb3349'],
            [0.8, '#c0392b'],
            [1, '#8e2de2']
        ],
        colorbar=dict(
            title='AQI',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        hovertemplate='<b>Week %{x}</b><br>%{y}<br>AQI: %{z:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': 'AQI Calendar Heatmap', 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        font={'color': 'white', 'family': 'Poppins'},
        height=400,
        margin=dict(l=100, r=40, t=60, b=40)
    )
    
    return fig

def create_forecast_chart(historical_data, forecast_days=7):
    """Create forecast visualization with confidence intervals"""
    # Simple moving average forecast (placeholder for actual ML model)
    last_values = historical_data['aqi'].tail(30)
    forecast_mean = last_values.mean()
    forecast_std = last_values.std()
    
    forecast_dates = pd.date_range(
        start=historical_data['date'].iloc[-1] + pd.Timedelta(days=1),
        periods=forecast_days
    )
    
    forecast_values = [forecast_mean + (i * 2) for i in range(forecast_days)]
    upper_bound = [v + forecast_std for v in forecast_values]
    lower_bound = [v - forecast_std for v in forecast_values]
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_data['date'].tail(30),
        y=historical_data['aqi'].tail(30),
        mode='lines',
        name='Historical',
        line=dict(color='#667eea', width=3),
        hovertemplate='<b>Date:</b> %{x}<br><b>AQI:</b> %{y:.1f}<extra></extra>'
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_values,
        mode='lines',
        name='Forecast',
        line=dict(color='#11998e', width=3, dash='dash'),
        hovertemplate='<b>Date:</b> %{x}<br><b>Forecast AQI:</b> %{y:.1f}<extra></extra>'
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=list(forecast_dates) + list(forecast_dates)[::-1],
        y=upper_bound + lower_bound[::-1],
        fill='toself',
        fillcolor='rgba(17, 153, 142, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title={'text': f'{forecast_days}-Day AQI Forecast', 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        font={'color': 'white', 'family': 'Poppins'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True, 'title': 'AQI'},
        hovermode='x unified',
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    return fig

def create_multi_city_trend(cities_data_dict):
    """Create multi-city comparison trend chart"""
    fig = go.Figure()
    
    colors = ['#667eea', '#11998e', '#f7b731', '#eb3349', '#ee5a6f', '#764ba2']
    
    for idx, (city, data) in enumerate(cities_data_dict.items()):
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['aqi'],
            mode='lines',
            name=city,
            line=dict(color=colors[idx % len(colors)], width=2.5),
            hovertemplate=f'<b>{city}</b><br>Date: %{{x}}<br>AQI: %{{y:.1f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title={'text': 'Multi-City AQI Comparison', 'font': {'size': 22, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        font={'color': 'white', 'family': 'Poppins'},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True},
        yaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'showgrid': True, 'title': 'AQI'},
        hovermode='x unified',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig

def calculate_health_risk_score(aqi, age, has_respiratory_issues, has_heart_disease, is_pregnant):
    """Calculate personalized health risk score"""
    base_risk = aqi / 100
    
    # Age factor
    if age < 5 or age > 65:
        age_factor = 1.5
    elif age < 18 or age > 50:
        age_factor = 1.2
    else:
        age_factor = 1.0
    
    # Health conditions
    health_factor = 1.0
    if has_respiratory_issues:
        health_factor += 0.5
    if has_heart_disease:
        health_factor += 0.3
    if is_pregnant:
        health_factor += 0.4
    
    risk_score = min(base_risk * age_factor * health_factor * 10, 10)
    
    return risk_score

def get_risk_recommendations(risk_score, aqi):
    """Get personalized recommendations based on risk score"""
    if risk_score < 2:
        level = "Low Risk"
        color = "#11998e"
        icon = "😊"
        actions = [
            "Safe to engage in outdoor activities",
            "No special precautions needed",
            "Maintain regular exercise routine"
        ]
    elif risk_score < 4:
        level = "Moderate Risk"
        color = "#f7b731"
        icon = "🙂"
        actions = [
            "Sensitive individuals should reduce prolonged outdoor exertion",
            "Consider wearing a mask if exercising outdoors",
            "Monitor symptoms if you have respiratory conditions"
        ]
    elif risk_score < 6:
        level = "Elevated Risk"
        color = "#ee5a6f"
        icon = "😐"
        actions = [
            "Limit outdoor activities, especially if you're sensitive",
            "Wear N95 masks when going outside",
            "Keep windows closed and use air purifiers",
            "Monitor health symptoms closely"
        ]
    elif risk_score < 8:
        level = "High Risk"
        color = "#eb3349"
        icon = "😷"
        actions = [
            "Avoid outdoor activities",
            "Stay indoors with air purification",
            "Wear high-quality masks if you must go out",
            "Consult doctor if experiencing symptoms",
            "Keep emergency medications handy"
        ]
    else:
        level = "Very High Risk"
        color = "#8e2de2"
        icon = "⚠️"
        actions = [
            "Stay indoors at all times",
            "Seal windows and doors",
            "Use multiple air purifiers",
            "Seek immediate medical attention if symptoms worsen",
            "Consider temporary relocation if possible"
        ]
    
    return {
        'level': level,
        'score': risk_score,
        'color': color,
        'icon': icon,
        'actions': actions
    }

def create_wind_rose(wind_speed_data, wind_direction_data, aqi_data):
    """Create wind rose diagram showing pollution patterns"""
    # This is a placeholder - actual implementation would need wind data
    # For now, create a sample wind rose
    
    fig = go.Figure()
    
    # Sample wind rose (8 directions)
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    theta = [0, 45, 90, 135, 180, 225, 270, 315]
    
    # Sample data - in real implementation, this would use actual wind data
    r = [3, 4, 2, 5, 3, 6, 4, 3]
    colors_list = ['#11998e', '#f7b731', '#ee5a6f', '#eb3349', '#11998e', '#f7b731', '#ee5a6f', '#eb3349']
    
    fig.add_trace(go.Barpolar(
        r=r,
        theta=theta,
        marker=dict(
            color=colors_list,
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Direction:</b> %{theta}°<br><b>Frequency:</b> %{r}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': 'Wind Rose - Pollution Sources', 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'family': 'Poppins'},
        polar=dict(
            radialaxis=dict(
                showticklabels=True,
                gridcolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white')
            ),
            angularaxis=dict(
                showticklabels=True,
                gridcolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white'),
                direction='clockwise'
            ),
            bgcolor='rgba(255,255,255,0.05)'
        ),
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
