#!/usr/bin/env python3
"""
Smart Caffeine Analytics Setup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        sys.exit(1)

def setup_directories():
    """Create necessary directories"""
    print("Setting up directory structure...")
    directories = [
        "data/raw",
        "data/processed", 
        "reports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def setup_environment():
    """Setup environment file"""
    print("Setting up environment configuration...")
    
    if not os.path.exists(".env"):
        print("  Copying .env.example to .env")
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("  ✓ Please edit .env file with your API keys")
        else:
            print("  ✗ .env.example not found")
    else:
        print("  ✓ .env file already exists")

def test_airtable_connection():
    """Test Airtable connection"""
    print("Testing Airtable connection...")
    try:
        sys.path.append(".")
        from scripts.airtable_integration import AirtableClient
        from dotenv import load_dotenv
        
        load_dotenv()
        client = AirtableClient()
        bases = client.list_bases()
        
        if bases:
            print(f"  ✓ Connected successfully. Found {len(bases)} accessible bases")
        else:
            print("  ⚠ Connected but no bases found")
            
    except Exception as e:
        print(f"  ✗ Airtable connection failed: {e}")
        print("  Please check your AIRTABLE_PAT in .env file")

def main():
    """Main setup function"""
    print("Smart Caffeine Analytics Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Using Python {sys.version}")
    
    try:
        setup_directories()
        install_dependencies()
        setup_environment()
        test_airtable_connection()
        
        print("\n" + "=" * 40)
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys")
        print("2. Set AIRTABLE_BASE_ID in .env")
        print("3. Run: python scripts/airtable_integration.py")
        print("4. Run: python scripts/collect_data.py")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()