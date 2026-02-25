#!/usr/bin/env python3
"""
Smart Caffeine Facebook Ads Integration
Collects ad performance data from Facebook Marketing API
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    FACEBOOK_ADS_API_KEY, 
    FACEBOOK_AD_ACCOUNT_ID,
    ANALYSIS_PERIOD_DAYS
)

class FacebookAdsClient:
    def __init__(self):
        """Initialize Facebook Ads client"""
        if not FACEBOOK_ADS_API_KEY:
            raise ValueError("FACEBOOK_ADS_API_KEY environment variable is required")
        if not FACEBOOK_AD_ACCOUNT_ID:
            raise ValueError("FACEBOOK_AD_ACCOUNT_ID environment variable is required")
        
        self.access_token = FACEBOOK_ADS_API_KEY
        self.ad_account_id = FACEBOOK_AD_ACCOUNT_ID
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make API request to Facebook"""
        params['access_token'] = self.access_token
        
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_account_info(self) -> Dict:
        """Get ad account information"""
        try:
            endpoint = self.ad_account_id
            params = {
                'fields': 'id,name,currency,account_status,business'
            }
            
            result = self._make_request(endpoint, params)
            print(f"Account: {result.get('name')} ({result.get('currency')})")
            return result
            
        except Exception as e:
            print(f"Error getting account info: {e}")
            return {}
    
    def get_campaigns(self, limit: int = 25) -> pd.DataFrame:
        """Get campaigns data"""
        try:
            endpoint = f"{self.ad_account_id}/campaigns"
            params = {
                'fields': 'id,name,status,objective,created_time,updated_time',
                'limit': limit
            }
            
            result = self._make_request(endpoint, params)
            campaigns = result.get('data', [])
            
            print(f"Retrieved {len(campaigns)} campaigns")
            return pd.DataFrame(campaigns)
            
        except Exception as e:
            print(f"Error getting campaigns: {e}")
            return pd.DataFrame()
    
    def get_ads(self, limit: int = 50) -> pd.DataFrame:
        """Get ads data"""
        try:
            endpoint = f"{self.ad_account_id}/ads"
            params = {
                'fields': 'id,name,status,campaign_id,adset_id,created_time,updated_time',
                'limit': limit
            }
            
            result = self._make_request(endpoint, params)
            ads = result.get('data', [])
            
            print(f"Retrieved {len(ads)} ads")
            return pd.DataFrame(ads)
            
        except Exception as e:
            print(f"Error getting ads: {e}")
            return pd.DataFrame()
    
    def get_ad_insights(self, days_back: int = 30, limit: int = 100) -> pd.DataFrame:
        """Get ad performance insights"""
        try:
            # Date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            endpoint = f"{self.ad_account_id}/insights"
            params = {
                'fields': ','.join([
                    'ad_id', 'ad_name', 'campaign_id', 'campaign_name',
                    'adset_id', 'adset_name', 'impressions', 'clicks',
                    'ctr', 'cpc', 'cpm', 'spend', 'reach', 'frequency',
                    'actions', 'cost_per_action_type', 'date_start', 'date_stop'
                ]),
                'time_range': json.dumps({
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d')
                }),
                'level': 'ad',
                'limit': limit
            }
            
            result = self._make_request(endpoint, params)
            insights = result.get('data', [])
            
            print(f"Retrieved {len(insights)} ad insights for last {days_back} days")
            return pd.DataFrame(insights)
            
        except Exception as e:
            print(f"Error getting ad insights: {e}")
            return pd.DataFrame()
    
    def get_campaign_insights(self, days_back: int = 30) -> pd.DataFrame:
        """Get campaign level insights"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            endpoint = f"{self.ad_account_id}/insights"
            params = {
                'fields': ','.join([
                    'campaign_id', 'campaign_name', 'impressions', 'clicks',
                    'ctr', 'cpc', 'cpm', 'spend', 'reach', 'frequency',
                    'actions', 'cost_per_action_type'
                ]),
                'time_range': json.dumps({
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d')
                }),
                'level': 'campaign'
            }
            
            result = self._make_request(endpoint, params)
            insights = result.get('data', [])
            
            print(f"Retrieved campaign insights for {len(insights)} campaigns")
            return pd.DataFrame(insights)
            
        except Exception as e:
            print(f"Error getting campaign insights: {e}")
            return pd.DataFrame()

def collect_facebook_data():
    """Main function to collect Facebook Ads data"""
    print("Smart Caffeine Facebook Ads Data Collection")
    print("=" * 50)
    
    try:
        client = FacebookAdsClient()
        
        # Get account info
        print("1. Getting account information...")
        account_info = client.get_account_info()
        
        # Collect data
        print("\n2. Collecting campaigns...")
        campaigns_df = client.get_campaigns()
        
        print("\n3. Collecting ads...")
        ads_df = client.get_ads()
        
        print("\n4. Collecting ad insights...")
        insights_df = client.get_ad_insights(days_back=ANALYSIS_PERIOD_DAYS)
        
        print("\n5. Collecting campaign insights...")
        campaign_insights_df = client.get_campaign_insights(days_back=ANALYSIS_PERIOD_DAYS)
        
        # Save data
        today = datetime.now().strftime('%Y%m%d')
        data_saved = {}
        
        if not campaigns_df.empty:
            filename = f"data/raw/facebook_campaigns_{today}.csv"
            campaigns_df.to_csv(filename, index=False)
            data_saved['campaigns'] = len(campaigns_df)
            print(f"  Saved campaigns: {filename}")
        
        if not ads_df.empty:
            filename = f"data/raw/facebook_ads_{today}.csv"
            ads_df.to_csv(filename, index=False)
            data_saved['ads'] = len(ads_df)
            print(f"  Saved ads: {filename}")
        
        if not insights_df.empty:
            filename = f"data/raw/facebook_ad_insights_{today}.csv"
            insights_df.to_csv(filename, index=False)
            data_saved['insights'] = len(insights_df)
            print(f"  Saved insights: {filename}")
        
        if not campaign_insights_df.empty:
            filename = f"data/raw/facebook_campaign_insights_{today}.csv"
            campaign_insights_df.to_csv(filename, index=False)
            data_saved['campaign_insights'] = len(campaign_insights_df)
            print(f"  Saved campaign insights: {filename}")
        
        print(f"\n✅ Facebook data collection completed!")
        print(f"   Total data points: {sum(data_saved.values())}")
        
        return data_saved
        
    except Exception as e:
        print(f"❌ Error during Facebook data collection: {e}")
        return {}

if __name__ == "__main__":
    collect_facebook_data()