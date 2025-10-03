# ECON2181
Data lab submissions for International Trade Theory &amp; Policy @ GW.

## Data Lab 2: Trade Analysis (USA vs China)

This project analyzes World Bank data comparing trade openness (% of GDP) between the United States and China from 1990-2024.

### Files:
- `trade_analysis.py` - Main analysis script
- `requirements.txt` - Python dependencies
- `us_china_trade_gdp_1990_2024.xlsx` - World Bank data file

### Setup:
1. Install dependencies: `py -m pip install -r requirements.txt`
2. Place your renamed Excel file (`us_china_trade_gdp_1990_2024.xlsx`) in the same directory as `trade_analysis.py`
3. Run the analysis: `py trade_analysis.py`

### Output:
- `trade_data_usa_china_long.csv` - Transformed data in long format
- `trade_comparison_usa_china.png` - Visualization comparing USA and China trade data

### Complete Data Lab 2 Analysis (Full WDI Data):
For the complete median growth gap analysis matching the slides, you'll need:
1. The full Trade (% GDP) dataset: `API_NE.TRD.GNFS.ZS.xlsx`
2. The GDP per capita growth dataset: `API_NY.GDP.PCAP.KD.ZG.xlsx`

Then run:
```python
pivot_result = lab_median_growth_gap(
    'API_NE.TRD.GNFS.ZS.xlsx',     # Trade data
    'API_NY.GDP.PCAP.KD.ZG.xlsx'   # Growth data
)
```
This creates:
- `lab_growth_gap_difference.png` - Chart showing growth gap between high and low trade countries