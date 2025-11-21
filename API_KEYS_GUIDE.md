# 🔑 How to Add API Keys

## Quick Setup (2 minutes)

### Step 1: Get Your Free API Key

#### OpenWeatherMap (Recommended - Start Here)
1. Visit: https://openweathermap.org/api
2. Click **"Sign Up"** (top right)
3. Create free account with your email
4. After login, go to: https://home.openweathermap.org/api_keys
5. Click **"Generate"** to create a new API key
6. Copy the API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Free Tier Includes:**
- ✅ 1,000 API calls per day
- ✅ Current air pollution data
- ✅ 5-day forecast
- ✅ No credit card required

### Step 2: Create Your Secrets File

**Option A: Use the Template (Easiest)**
1. Open `.streamlit/secrets.template.toml`
2. Replace `your_api_key_here` with your actual key
3. Save as `.streamlit/secrets.toml` (remove `.template`)

**Option B: I'll Create It For You**
Just provide your API key and I'll create the file!

---

## Complete secrets.toml Template

Copy this and replace `YOUR_ACTUAL_API_KEY_HERE` with your key:

```toml
# OpenWeatherMap API Key (Required for real data)
openweather_api_key = "YOUR_ACTUAL_API_KEY_HERE"

# Optional: Other API keys (add later if needed)
# cpcb_api_key = "your_cpcb_key_here"
# nasa_api_key = "your_nasa_key_here"

# Email Configuration (Optional - for alerts)
# Uncomment and fill these when you want to enable email alerts
# [email]
# smtp_server = "smtp.gmail.com"
# smtp_port = 587
# sender_email = "your_email@gmail.com"
# sender_password = "your_app_password"
```

---

## Test Your API Key

After adding your key, test it:

```python
# Run this in Python to test
import requests

api_key = "YOUR_API_KEY"
lat, lon = 28.6139, 77.2090  # Delhi coordinates

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
response = requests.get(url)

if response.status_code == 200:
    print("✅ API key works!")
    print(response.json())
else:
    print("❌ Error:", response.status_code)
```

---

## Security Checklist

- ✅ Created `.streamlit/secrets.toml` (not `.template`)
- ✅ Added your actual API key
- ✅ File is in `.gitignore` (already done)
- ⚠️ Never commit secrets.toml to GitHub
- ⚠️ Never share your API key publicly

---

## What Happens Next?

Once you add your API key:

1. **Restart the app**
   ```bash
   streamlit run app.py
   ```

2. **App will automatically use real data**
   - Real-time AQI from OpenWeatherMap
   - Live PM2.5, PM10 values
   - Actual air quality for Indian cities

3. **See the difference**
   - Before: Sample/mock data
   - After: REAL air quality readings!

---

## Troubleshooting

### "API key not found"
- Make sure file is named `secrets.toml` (not `secrets.template.toml`)
- File must be in `.streamlit/` folder
- Restart the Streamlit app

### "Invalid API key"
- Check you copied the entire key
- No extra spaces or quotes
- Key should be 32 characters long

### "API rate limit exceeded"
- Free tier: 1,000 calls/day
- App caches data for 5 minutes (300 seconds)
- Don't refresh too frequently

---

## Next Steps After Adding API Key

1. ✅ Add API key to secrets.toml
2. 🔄 Restart app: `streamlit run app.py`
3. 🌐 Open: http://localhost:8501
4. 👀 See REAL air quality data!
5. 📖 Follow ROADMAP.md Phase 1 for data collection

---

## Need Help?

Tell me:
- "I have my API key, create the secrets file"
- "How do I test if my API key works?"
- "The API key isn't working, help debug"
- "Show me how to integrate the API into app.py"

Ready to add your key! 🚀
