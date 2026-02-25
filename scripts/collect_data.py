#!/usr/bin/env python3
"""
Smart Caffeine Data Collection Script
Collects ads and sales data from various sources
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import DATA_SOURCES, ANALYSIS_PERIOD_DAYS

# Import integrations
from airtable_integration import AirtableClient
from facebook_ads_integration import collect_facebook_data

def collect_airtable_data():
    """Collect data from Airtable"""
    print("Collecting Airtable data...")
    try:
        client = AirtableClient()
        
        # Get data from configured tables
        all_data = {}
        from config.settings import AIRTABLE_TABLES
        
        for table_type, table_name in AIRTABLE_TABLES.items():
            df = client.get_table_data(table_name)
            if not df.empty:
                # Save to data/raw
                filename = f"data/raw/airtable_{table_type}_{datetime.now().strftime('%Y%m%d')}.csv"
                df.to_csv(filename, index=False)
                all_data[table_type] = df
                print(f"  Saved {table_type}: {len(df)} records → {filename}")
        
        return all_data
        
    except Exception as e:
        print(f"Error collecting Airtable data: {e}")
        return {}

def collect_facebook_ads():
    """Collect Facebook Ads data"""
    print("Collecting Facebook Ads data...")
    try:
        return collect_facebook_data()
    except Exception as e:
        print(f"  Error collecting Facebook Ads data: {e}")
        return {}

def collect_google_ads():
    """Collect Google Ads data"""
    print("Collecting Google Ads data...")
    # TODO: Implement Google Ads API integration
    print("  Google Ads integration pending API keys")
    pass

def collect_shopify_sales():
    """Collect Shopify sales data"""
    print("Collecting Shopify sales data...")
    # TODO: Implement Shopify API integration
    print("  Shopify integration pending API keys")
    pass

def process_collected_data(airtable_data):
    """Process and analyze collected data"""
    print("\nProcessing collected data...")
    
    if not airtable_data:
        print("No data to process")
        return
    
    # Basic analysis
    for table_type, df in airtable_data.items():
        print(f"  {table_type}: {len(df)} records, {len(df.columns)} columns")
        
        # Save processed summary
        summary = {
            'table': table_type,
            'record_count': len(df),
            'columns': list(df.columns),
            'last_updated': datetime.now().isoformat()
        }
        
        summary_file = f"data/processed/summary_{table_type}_{datetime.now().strftime('%Y%m%d')}.json"
        import json
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"    Summary saved: {summary_file}")

def main():
    """Main data collection pipeline"""
    print(f"Smart Caffeine Data Collection")
    print(f"Started at: {datetime.now()}")
    print("=" * 50)
    
    # Ensure data directories exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    collected_data = {}
    
    try:
        # Collect from enabled sources
        if DATA_SOURCES.get('airtable'):
            collected_data['airtable'] = collect_airtable_data()
        
        if DATA_SOURCES.get('facebook_ads'):
            collected_data['facebook'] = collect_facebook_ads()
            
        if DATA_SOURCES.get('google_ads'):
            collect_google_ads()
            
        if DATA_SOURCES.get('shopify'):
            collect_shopify_sales()
        
        # Process collected data
        process_collected_data(collected_data.get('airtable', {}))
        
        print("\nData collection completed successfully")
        print(f"Ended at: {datetime.now()}")
        
    except Exception as e:
        print(f"Error during data collection: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()