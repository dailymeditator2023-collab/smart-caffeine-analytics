# Smart Caffeine Analytics

Analytics pipeline for Smart Caffeine ads and sales performance tracking.

## Features

- **✅ Airtable Integration** - Data sync and management
- **🔄 Ad Performance Monitoring** (Facebook/Google - pending API keys)
- **📊 Sales Data Analysis** (Shopify - pending API keys)
- **🎯 Conversion Tracking** 
- **📈 ROI Insights**
- **📋 Automated Reporting**

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/dailymeditator2023-collab/smart-caffeine-analytics.git
cd smart-caffeine-analytics
python setup.py
```

### 2. Configure Environment

Edit `.env` file with your API credentials:

```bash
# Required: Airtable
AIRTABLE_PAT=your_airtable_token_here
AIRTABLE_BASE_ID=your_base_id_here

# Optional: Other integrations
FACEBOOK_ADS_API_KEY=...
SHOPIFY_API_KEY=...
```

### 3. Test Airtable Connection

```bash
python scripts/airtable_integration.py
```

### 4. Collect Data

```bash
python scripts/collect_data.py
```

## Project Structure

```
smart-caffeine-analytics/
├── data/
│   ├── raw/              # Raw data from APIs
│   └── processed/        # Cleaned & processed data
├── scripts/
│   ├── airtable_integration.py  # Airtable client & operations
│   ├── collect_data.py          # Main data collection pipeline
│   └── analyze_data.py          # Analysis & reporting (TODO)
├── reports/              # Generated reports & visualizations
├── config/
│   └── settings.py       # Configuration & environment variables
├── docs/                 # Documentation
├── .env                  # Environment variables (create from .env.example)
└── requirements.txt      # Python dependencies
```

## Airtable Integration

The Airtable integration supports:

- **Listing accessible bases** - Find your base IDs
- **Table schema discovery** - Automatic table detection
- **Data extraction** - Export to CSV/DataFrame
- **Record creation/updates** - Write data back to Airtable

### Default Table Structure

Configure in `config/settings.py`:

```python
AIRTABLE_TABLES = {
    'campaigns': 'Campaigns',
    'ads': 'Ads', 
    'metrics': 'Metrics',
    'conversions': 'Conversions',
    'customers': 'Customers'
}
```

## API Integrations Status

| Integration | Status | Requirements |
|------------|--------|-------------|
| **Airtable** | ✅ Active | AIRTABLE_PAT |
| **Facebook Ads** | 🔄 Pending | API keys needed |
| **Google Ads** | 🔄 Pending | API keys needed |
| **Shopify** | 🔄 Pending | API keys needed |

## Data Flow

1. **Collection** - APIs → `data/raw/`
2. **Processing** - Clean & transform → `data/processed/`
3. **Analysis** - Generate insights
4. **Reporting** - Export visualizations → `reports/`

## Development

### Requirements

- Python 3.8+
- pip dependencies (see `requirements.txt`)
- API credentials for data sources

### Testing

```bash
# Test individual components
python scripts/airtable_integration.py
python scripts/collect_data.py

# View logs
tail -f logs/app.log
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

Private repository - Smart Caffeine analytics pipeline.

## Support

For issues with:
- **Airtable**: Check PAT token and base ID
- **API integrations**: Verify credentials in `.env`
- **Data processing**: Check logs in `logs/` directory

Created by: dailymeditator2023-collab