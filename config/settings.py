# Smart Caffeine Analytics Configuration

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable Configuration
AIRTABLE_PAT = os.getenv('AIRTABLE_PAT')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')

# API Keys (use environment variables)
FACEBOOK_ADS_API_KEY = os.getenv('FACEBOOK_ADS_API_KEY')
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')

GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID')
GOOGLE_ADS_CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET')
GOOGLE_ADS_REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN')

SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL')

# Data sources
DATA_SOURCES = {
    'airtable': True,
    'facebook_ads': False,  # TODO: Enable when keys are added
    'google_ads': False,    # TODO: Enable when keys are added
    'shopify': False,       # TODO: Enable when keys are added
    'email_marketing': False
}

# Airtable table names (customize based on your base structure)
AIRTABLE_TABLES = {
    'data': 'Table 1'
}

# Analysis settings
ANALYSIS_PERIOD_DAYS = 30
REPORT_FREQUENCY = 'daily'

# Output settings
REPORT_FORMAT = 'pdf'
ALERT_THRESHOLD = 0.8  # 80% of target

# Logging
LOG_LEVEL = 'INFO'