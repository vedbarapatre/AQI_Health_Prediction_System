"""
Quick Setup Script for AQI Health Prediction System
Run this to create all necessary folders and initial files
"""

import os
import sys

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'data',
        'data_sources',
        'ml_models',
        'services',
        'utils',
        'database',
        'models',
        'tests',
        '.streamlit'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    # Create __init__.py files for Python packages
    packages = ['data_sources', 'ml_models', 'services', 'utils', 'database']
    for package in packages:
        init_file = os.path.join(package, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""{package.replace("_", " ").title()} Module"""\n')
            print(f"✓ Created {init_file}")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Streamlit
.streamlit/secrets.toml

# Data files
data/*.db
data/*.csv
data/*.xlsx

# Models
models/*.pkl
models/*.h5
models/*.joblib

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Logs
*.log
logs/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_requirements_dev():
    """Create requirements-dev.txt with additional development dependencies"""
    dev_requirements = """# Production dependencies
streamlit==1.31.0
pandas==2.2.0
numpy==1.26.3
plotly==5.18.0

# Data collection
requests==2.31.0
schedule==1.2.0

# Machine Learning
scikit-learn==1.4.0
joblib==1.3.2

# Optional: Deep Learning (uncomment if needed)
# tensorflow==2.15.0

# Database
sqlite3  # Built-in with Python

# Export functionality
openpyxl==3.1.2
# reportlab==4.0.7  # Uncomment for PDF export

# Testing
pytest==7.4.3
pytest-cov==4.1.0

# Code quality
flake8==7.0.0
black==23.12.1
"""
    
    with open('requirements-dev.txt', 'w') as f:
        f.write(dev_requirements)
    print("✓ Created requirements-dev.txt")

def create_env_template():
    """Create .env.template file"""
    env_template = """# API Keys
OPENWEATHER_API_KEY=your_api_key_here
CPCB_API_KEY=your_api_key_here
NASA_API_KEY=your_api_key_here

# Email Configuration (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=alerts@example.com
SENDER_PASSWORD=your_app_password

# SMS Configuration (optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Database
DATABASE_PATH=data/aqi_system.db

# Application
DEFAULT_CITY=Delhi
DATA_REFRESH_INTERVAL=300
CACHE_TTL=300
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    print("✓ Created .env.template")

def create_streamlit_config():
    """Create Streamlit configuration files"""
    config_toml = """[theme]
primaryColor = "#667eea"
backgroundColor = "#F7FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#2C3E50"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
"""
    
    secrets_template = """# Copy this to secrets.toml and add your actual keys
# DO NOT COMMIT secrets.toml to git!

openweather_api_key = "your_api_key_here"
cpcb_api_key = "your_api_key_here"
nasa_api_key = "your_api_key_here"

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "alerts@example.com"
sender_password = "your_app_password"
"""
    
    os.makedirs('.streamlit', exist_ok=True)
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config_toml)
    print("✓ Created .streamlit/config.toml")
    
    with open('.streamlit/secrets.template.toml', 'w') as f:
        f.write(secrets_template)
    print("✓ Created .streamlit/secrets.template.toml")

def create_readme_setup():
    """Create SETUP.md with getting started instructions"""
    setup_content = """# 🚀 Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -r requirements-dev.txt
```

## Step 2: Get API Keys

### OpenWeatherMap (Recommended - Free Tier)
1. Go to: https://openweathermap.org/api
2. Sign up for free account
3. Subscribe to "Air Pollution API" (Free - 1,000 calls/day)
4. Copy your API key

### CPCB (Optional - Indian Government Data)
1. Visit: https://app.cpcbccr.com/ccr_docs/
2. Register for API access
3. Documentation: https://api.data.gov.in/

## Step 3: Configure Secrets

Create `.streamlit/secrets.toml`:
```bash
cp .streamlit/secrets.template.toml .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your API keys:
```toml
openweather_api_key = "YOUR_ACTUAL_API_KEY"
```

## Step 4: Initialize Database

```bash
python database/schema.py
```

## Step 5: Run the Application

```bash
streamlit run app.py
```

Open browser to: http://localhost:8501

## Step 6: Start Data Collection (Optional)

In a separate terminal:
```bash
python data_sources/data_collector.py
```

## Step 7: Train ML Models (After collecting data)

```bash
python ml_models/train_pipeline.py
```

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Database Errors
Delete and recreate:
```bash
rm data/aqi_system.db
python database/schema.py
```

## Next Steps

1. ✅ App is running with sample data
2. 📡 Add your API key to get real data
3. 🤖 Collect data for 7+ days, then train ML models
4. 📧 Configure email alerts
5. 🚀 Deploy to production

See ROADMAP.md for complete implementation plan.
"""
    
    with open('SETUP.md', 'w') as f:
        f.write(setup_content)
    print("✓ Created SETUP.md")

def print_summary():
    """Print setup summary and next steps"""
    print("\n" + "="*70)
    print("✅ Setup Complete!")
    print("="*70)
    print("\n📁 Directory structure created:")
    print("   ├── data/              (SQLite databases)")
    print("   ├── data_sources/      (API clients)")
    print("   ├── ml_models/         (ML models & training)")
    print("   ├── services/          (Alert system, etc.)")
    print("   ├── utils/             (Helper functions)")
    print("   ├── database/          (Database schema)")
    print("   ├── models/            (Trained model files)")
    print("   └── tests/             (Unit tests)")
    
    print("\n📋 Next Steps:")
    print("\n1. Get API Key (5 minutes):")
    print("   → Visit: https://openweathermap.org/api")
    print("   → Sign up and get free API key")
    
    print("\n2. Configure Secrets:")
    print("   → Copy: cp .streamlit/secrets.template.toml .streamlit/secrets.toml")
    print("   → Add your API key to secrets.toml")
    
    print("\n3. Run the App:")
    print("   → streamlit run app.py")
    
    print("\n4. Follow the Roadmap:")
    print("   → See ROADMAP.md for complete implementation plan")
    print("   → See SETUP.md for detailed setup instructions")
    
    print("\n📚 Documentation Created:")
    print("   ✓ README.md              - Project overview")
    print("   ✓ ROADMAP.md             - Complete implementation plan")
    print("   ✓ SETUP.md               - Quick setup guide")
    print("   ✓ DESIGN_DOCUMENTATION.md - UI/UX specifications")
    print("   ✓ QUICKSTART.md          - User guide")
    print("   ✓ MOCKUPS.md             - Visual component layouts")
    
    print("\n" + "="*70)
    print("🎉 Ready to build a production-ready AQI system!")
    print("="*70 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("AQI Health Prediction System - Setup Script")
    print("="*70 + "\n")
    
    try:
        create_directory_structure()
        print()
        create_gitignore()
        create_requirements_dev()
        create_env_template()
        create_streamlit_config()
        create_readme_setup()
        print()
        print_summary()
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
