# Smart Caffeine Analytics Configuration

# API Keys (use environment variables)
FACEBOOK_ADS_API_KEY = None
GOOGLE_ADS_API_KEY = None
SHOPIFY_API_KEY = None

# Data sources
DATA_SOURCES = {
    'facebook_ads': True,
    'google_ads': True, 
    'shopify': True,
    'email_marketing': False
}

# Analysis settings
ANALYSIS_PERIOD_DAYS = 30
REPORT_FREQUENCY = 'daily'

# Output settings
REPORT_FORMAT = 'pdf'
ALERT_THRESHOLD = 0.8  # 80% of target