# Smart Caffeine Analytics Configuration

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable Configuration
AIRTABLE_PAT = os.getenv('AIRTABLE_PAT')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')

# Meta/Facebook API Keys (supports both new and legacy variable names)
META_APP_ID = os.getenv('META_APP_ID') or os.getenv('FACEBOOK_APP_ID')
META_APP_SECRET = os.getenv('META_APP_SECRET') or os.getenv('FACEBOOK_APP_SECRET') 
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN') or os.getenv('FACEBOOK_ADS_API_KEY')
META_AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID') or os.getenv('FACEBOOK_AD_ACCOUNT_ID')

# Legacy variable names for backward compatibility
FACEBOOK_ADS_API_KEY = META_ACCESS_TOKEN
FACEBOOK_APP_ID = META_APP_ID
FACEBOOK_APP_SECRET = META_APP_SECRET
FACEBOOK_AD_ACCOUNT_ID = META_AD_ACCOUNT_ID

# Shopify API Keys (supports both new and legacy variable names)
SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME') or os.getenv('SHOPIFY_STORE_URL')
SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN') or os.getenv('SHOPIFY_API_KEY')

# Legacy variable names for backward compatibility
SHOPIFY_API_KEY = SHOPIFY_ACCESS_TOKEN
SHOPIFY_STORE_URL = SHOPIFY_SHOP_NAME

# Google Ads API Keys
GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID')
GOOGLE_ADS_CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET')
GOOGLE_ADS_REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN')

# Data sources
DATA_SOURCES = {
    'airtable': True,
    'facebook_ads': True,   # ✅ ACTIVE - Smart Caffeine ad account
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