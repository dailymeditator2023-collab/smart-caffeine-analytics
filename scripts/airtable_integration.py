#!/usr/bin/env python3
"""
Smart Caffeine Airtable Integration
Connects to Airtable and manages data sync for Smart Caffeine analytics
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
from pyairtable import Api
from dotenv import load_dotenv

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import AIRTABLE_PAT, AIRTABLE_BASE_ID, AIRTABLE_TABLES

class AirtableClient:
    def __init__(self):
        """Initialize Airtable client"""
        if not AIRTABLE_PAT:
            raise ValueError("AIRTABLE_PAT environment variable is required")
        
        self.api = Api(AIRTABLE_PAT)
        self.base_id = AIRTABLE_BASE_ID
        self.base = None
        
        if self.base_id:
            self.base = self.api.base(self.base_id)
    
    def list_bases(self) -> List[Dict]:
        """List all accessible Airtable bases"""
        try:
            bases = self.api.bases()
            print(f"Found {len(bases)} accessible bases:")
            for base in bases:
                print(f"  - {base['name']} (ID: {base['id']})")
            return bases
        except Exception as e:
            print(f"Error listing bases: {e}")
            return []
    
    def list_tables(self, base_id: str = None) -> List[Dict]:
        """List tables in a specific base"""
        try:
            target_base_id = base_id or self.base_id
            if not target_base_id:
                print("No base ID provided")
                return []
            
            base = self.api.base(target_base_id)
            schema = base.schema()
            tables = schema.tables
            
            print(f"Tables in base {target_base_id}:")
            for table in tables:
                print(f"  - {table.name} (ID: {table.id})")
            return tables
        except Exception as e:
            print(f"Error listing tables: {e}")
            return []
    
    def get_table_data(self, table_name: str, base_id: str = None) -> pd.DataFrame:
        """Get all records from a specific table"""
        try:
            target_base_id = base_id or self.base_id
            if not target_base_id:
                print("No base ID configured")
                return pd.DataFrame()
            
            base = self.api.base(target_base_id)
            table = base.table(table_name)
            records = table.all()
            
            # Convert to DataFrame
            data = []
            for record in records:
                row = record['fields'].copy()
                row['airtable_id'] = record['id']
                row['created_time'] = record.get('createdTime', '')
                data.append(row)
            
            df = pd.DataFrame(data)
            print(f"Retrieved {len(df)} records from {table_name}")
            return df
            
        except Exception as e:
            print(f"Error getting table data: {e}")
            return pd.DataFrame()
    
    def create_record(self, table_name: str, fields: Dict, base_id: str = None) -> Optional[str]:
        """Create a new record in a table"""
        try:
            target_base_id = base_id or self.base_id
            if not target_base_id:
                print("No base ID configured")
                return None
            
            base = self.api.base(target_base_id)
            table = base.table(table_name)
            record = table.create(fields)
            
            print(f"Created record {record['id']} in {table_name}")
            return record['id']
            
        except Exception as e:
            print(f"Error creating record: {e}")
            return None
    
    def update_record(self, table_name: str, record_id: str, fields: Dict, base_id: str = None) -> bool:
        """Update an existing record"""
        try:
            target_base_id = base_id or self.base_id
            if not target_base_id:
                print("No base ID configured")
                return False
            
            base = self.api.base(target_base_id)
            table = base.table(table_name)
            table.update(record_id, fields)
            
            print(f"Updated record {record_id} in {table_name}")
            return True
            
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

def main():
    """Main Airtable integration function"""
    load_dotenv()
    
    print("Smart Caffeine Airtable Integration")
    print("=" * 40)
    
    try:
        client = AirtableClient()
        
        # List available bases
        print("\n1. Listing accessible bases...")
        bases = client.list_bases()
        
        if not client.base_id and bases:
            print(f"\nSuggestion: Set AIRTABLE_BASE_ID to one of the base IDs above")
            print("Example: export AIRTABLE_BASE_ID='appXXXXXXXXXXXXXX'")
        
        # If base is configured, list its tables
        if client.base_id:
            print(f"\n2. Listing tables in base {client.base_id}...")
            tables = client.list_tables()
            
            # Try to get sample data from first table
            if tables:
                first_table = tables[0].name
                print(f"\n3. Getting sample data from '{first_table}'...")
                df = client.get_table_data(first_table)
                if not df.empty:
                    print(f"Sample columns: {list(df.columns)[:5]}")
        
        print("\nAirtable integration setup complete!")
        
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()