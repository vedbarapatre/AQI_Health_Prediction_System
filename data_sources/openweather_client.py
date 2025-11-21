"""
OpenWeatherMap API Client
Handles fetching air quality data from OpenWeatherMap API
"""

import requests
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
import time

class OpenWeatherClient:
    """Client for OpenWeatherMap Air Pollution API"""
    
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    # Indian cities with coordinates
    CITIES = {
        "Delhi": {"lat": 28.6139, "lon": 77.2090},
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946},
        "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Chennai": {"lat": 13.0827, "lon": 80.2707},
        "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
        "Jaipur": {"lat": 26.9124, "lon": 75.7873},
        "Lucknow": {"lat": 26.8467, "lon": 80.9462}
    }
    
    def __init__(self, api_key: str):
        """Initialize the client with API key"""
        self.api_key = api_key
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """Make API request with error handling"""
        params['appid'] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
    
    def get_current_pollution(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current air pollution data for coordinates"""
        data = self._make_request("air_pollution", {"lat": lat, "lon": lon})
        
        if data and "list" in data and len(data["list"]) > 0:
            return self._format_pollution_data(data["list"][0])
        return None
    
    def get_current_pollution_by_city(self, city_name: str) -> Optional[Dict]:
        """Get current air pollution data for a city"""
        if city_name not in self.CITIES:
            st.error(f"City '{city_name}' not found")
            return None
        
        coords = self.CITIES[city_name]
        data = self.get_current_pollution(coords["lat"], coords["lon"])
        
        if data:
            data["city"] = city_name
            data["lat"] = coords["lat"]
            data["lon"] = coords["lon"]
        
        return data
    
    def get_forecast_pollution(self, lat: float, lon: float) -> Optional[List[Dict]]:
        """Get 5-day air pollution forecast"""
        data = self._make_request("air_pollution/forecast", {"lat": lat, "lon": lon})
        
        if data and "list" in data:
            return [self._format_pollution_data(item) for item in data["list"]]
        return None
    
    def get_all_cities_data(self) -> List[Dict]:
        """Get current pollution data for all Indian cities"""
        cities_data = []
        
        for city_name, coords in self.CITIES.items():
            data = self.get_current_pollution(coords["lat"], coords["lon"])
            if data:
                data["city"] = city_name
                data["lat"] = coords["lat"]
                data["lon"] = coords["lon"]
                cities_data.append(data)
            
            # Rate limiting: avoid hitting API limits
            time.sleep(0.1)
        
        return cities_data
    
    def _format_pollution_data(self, raw_data: Dict) -> Dict:
        """Format raw API data into usable structure"""
        main = raw_data.get("main", {})
        components = raw_data.get("components", {})
        timestamp = raw_data.get("dt", 0)
        
        # AQI mapping (OpenWeatherMap scale: 1-5)
        aqi = main.get("aqi", 0)
        aqi_category = self._get_aqi_category(aqi)
        
        # Convert to Indian AQI scale (0-500)
        indian_aqi = self._convert_to_indian_aqi(components)
        
        return {
            "timestamp": datetime.fromtimestamp(timestamp),
            "aqi": indian_aqi,
            "aqi_level": aqi,  # OpenWeather scale (1-5)
            "category": aqi_category,
            "pm2_5": components.get("pm2_5", 0),
            "pm10": components.get("pm10", 0),
            "co": components.get("co", 0),
            "no": components.get("no", 0),
            "no2": components.get("no2", 0),
            "o3": components.get("o3", 0),
            "so2": components.get("so2", 0),
            "nh3": components.get("nh3", 0)
        }
    
    def _get_aqi_category(self, aqi_level: int) -> str:
        """Get AQI category from OpenWeather level (1-5)"""
        categories = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return categories.get(aqi_level, "Unknown")
    
    def _convert_to_indian_aqi(self, components: Dict) -> int:
        """Convert pollutant values to Indian AQI scale (0-500)"""
        pm2_5 = components.get("pm2_5", 0)
        pm10 = components.get("pm10", 0)
        
        # Simplified conversion based on PM2.5 (primary indicator)
        if pm2_5 <= 30:
            aqi = int((pm2_5 / 30) * 50)  # Good (0-50)
        elif pm2_5 <= 60:
            aqi = int(50 + ((pm2_5 - 30) / 30) * 50)  # Satisfactory (51-100)
        elif pm2_5 <= 90:
            aqi = int(100 + ((pm2_5 - 60) / 30) * 100)  # Moderate (101-200)
        elif pm2_5 <= 120:
            aqi = int(200 + ((pm2_5 - 90) / 30) * 100)  # Poor (201-300)
        elif pm2_5 <= 250:
            aqi = int(300 + ((pm2_5 - 120) / 130) * 100)  # Very Poor (301-400)
        else:
            aqi = int(400 + min((pm2_5 - 250) / 2, 100))  # Severe (401-500)
        
        return min(aqi, 500)  # Cap at 500


# Cached function to get OpenWeather client
@st.cache_resource
def get_openweather_client() -> Optional[OpenWeatherClient]:
    """Get cached OpenWeather client instance"""
    try:
        api_key = st.secrets.get("openweather_api_key")
        if not api_key:
            st.warning("⚠️ OpenWeather API key not found in secrets.toml")
            return None
        return OpenWeatherClient(api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenWeather client: {str(e)}")
        return None


# Cached function to fetch city data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_city_data(city_name: str) -> Optional[Dict]:
    """Fetch and cache pollution data for a city"""
    client = get_openweather_client()
    if client:
        return client.get_current_pollution_by_city(city_name)
    return None


# Cached function to fetch all cities
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_all_cities() -> List[Dict]:
    """Fetch and cache pollution data for all cities"""
    client = get_openweather_client()
    if client:
        return client.get_all_cities_data()
    return []


# Cached function to fetch forecast
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_forecast(city_name: str) -> Optional[List[Dict]]:
    """Fetch and cache 5-day forecast for a city"""
    client = get_openweather_client()
    if client and city_name in OpenWeatherClient.CITIES:
        coords = OpenWeatherClient.CITIES[city_name]
        return client.get_forecast_pollution(coords["lat"], coords["lon"])
    return None
