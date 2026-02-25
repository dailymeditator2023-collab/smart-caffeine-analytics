#!/usr/bin/env python3
"""
Test Facebook API and get Ad Account ID
"""

import requests
import sys
import os

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import FACEBOOK_ADS_API_KEY

def test_facebook_api():
    """Test Facebook API connection and get ad accounts"""
    
    if not FACEBOOK_ADS_API_KEY:
        print("❌ No Facebook API key found in .env")
        return
    
    print("🔍 Testing Facebook API connection...")
    print(f"Using token: {FACEBOOK_ADS_API_KEY[:20]}...")
    
    # Test basic user info
    try:
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            'access_token': FACEBOOK_ADS_API_KEY,
            'fields': 'name,id'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ API connection successful!")
            print(f"   User: {user_data.get('name')} (ID: {user_data.get('id')})")
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return
    
    # Get ad accounts
    print("\n📊 Getting ad accounts...")
    
    try:
        url = "https://graph.facebook.com/v18.0/me/adaccounts"
        params = {
            'access_token': FACEBOOK_ADS_API_KEY,
            'fields': 'id,name,currency,account_status,business'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            accounts_data = response.json()
            accounts = accounts_data.get('data', [])
            
            if accounts:
                print(f"✅ Found {len(accounts)} ad accounts:")
                for account in accounts:
                    account_id = account.get('id')
                    name = account.get('name')
                    status = account.get('account_status')
                    currency = account.get('currency')
                    
                    print(f"   • {name}")
                    print(f"     ID: {account_id}")
                    print(f"     Status: {status}, Currency: {currency}")
                    print()
                
                # Suggest the first active account
                active_accounts = [acc for acc in accounts if acc.get('account_status') == 1]
                if active_accounts:
                    suggested_id = active_accounts[0]['id']
                    print(f"💡 Suggested Ad Account ID: {suggested_id}")
                    print(f"   Add this to your .env file:")
                    print(f"   FACEBOOK_AD_ACCOUNT_ID={suggested_id}")
                
            else:
                print("⚠️  No ad accounts found")
                print("   Make sure this app has access to Smart Caffeine ad accounts")
        
        else:
            print(f"❌ Failed to get ad accounts: {response.status_code}")
            print(f"   Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error getting ad accounts: {e}")

if __name__ == "__main__":
    test_facebook_api()