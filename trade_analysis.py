#!/usr/bin/env python3
"""
World Bank Trade Data Analysis: USA vs China (1990-2024)
Analysis of Trade (% of GDP) data for United States and China
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def import_and_explore_data(filename):
    """Import Excel file and explore its structure"""
    print("Importing Excel file and exploring structure...")
    
    # Import the Excel file
    df = pd.read_excel(filename)
    
    print(f"Shape of imported data: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
    
    return df

def transform_data(df):
    """Transform data to long format with proper filtering"""
    print("\nTransforming data to long format...")
    
    # Check for the Trade as % of GDP indicator
    # The indicator code is NE.TRD.GNFS.ZS for Trade (% of GDP)
    trade_indicator = 'NE.TRD.GNFS.ZS'
    
    # Identify which columns contain this indicator
    indicator_rows = df[df.iloc[:, 0] == trade_indicator]
    
    if indicator_rows.empty:
        print(f"Indicator {trade_indicator} not found. Available indicators:")
        unique_indicators = df.iloc[:, 0].unique()[:10]  # Show first 10
        print(unique_indicators)
        return None
    
    print(f"Found {len(indicator_rows)} rows for indicator {trade_indicator}")
    
    # Get the row for USA and CHN
    usa_data = indicator_rows[indicator_rows.iloc[:, 1] == 'United States']
    chn_data = indicator_rows[indicator_rows.iloc[:, 1] == 'China']
    
    if usa_data.empty:
        print("USA data not found. Checking available countries...")
        countries = indicator_rows.iloc[:, 1].unique()[:10]
        print(countries)
        return None
        
    if chn_data.empty:
        print("China data not found. Checking available countries...")
        countries = indicator_rows.iloc[:, 1].unique()[:10]
        print(countries)
        return None
    
    # Get year columns (assuming they start from column 4 onwards)
    # This might need adjustment based on actual Excel structure
    year_columns = [col for col in df.columns if isinstance(col, (int, float)) and 1990 <= col <= 2024]
    
    if not year_columns:
        # Try alternative approach - look for column names that are years
        year_columns = [col for col in df.columns if str(col).isdigit() and 1990 <= int(str(col)) <= 2024]
    
    if not year_columns:
        print("Year columns not found. Available columns:")
        print([col for col in df.columns])
        return None
    
    print(f"Year columns found: {year_columns}")
    
    # Extract data for USA and China
    usa_values = usa_data[year_columns].values.flatten()
    chn_values = chn_data[year_columns].values.flatten()
    
    # Create long format data
    data_long = []
    
    for i, year in enumerate(year_columns):
        if not pd.isna(usa_values[i]):
            data_long.append({
                'year': year,
                'country': 'United States',
                'trade_pct_gdp': usa_values[i]
            })
        
        if not pd.isna(chn_values[i]):
            data_long.append({
                'year': year,
                'country': 'China', 
                'trade_pct_gdp': chn_values[i]
            })
    
    df_long = pd.DataFrame(data_long)
    print(f"\nTransformed data shape: {df_long.shape}")
    print("\nTransformed data:")
    print(df_long.head(10))
    
    return df_long

def create_plot(df_long):
    """Create matplotlib line chart"""
    print("\nCreating visualization...")
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Plot lines for each country
    for country in df_long['country'].unique():
        country_data = df_long[df_long['country'] == country].sort_values('year')
        plt.plot(country_data['year'], country_data['trade_pct_gdp'], 
                marker='o', linewidth=2, label=country, markersize=4)
    
    # Customize the plot
    plt.title('Trade (% of GDP): United States vs China (1990-2024)', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Trade (% of GDP)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Set axis limits and ticks
    plt.xlim(1990, 2025)
    plt.xticks(range(1990, 2025, 5))
    
    # Add some padding
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('trade_comparison_usa_china.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'trade_comparison_usa_china.png'")
    
    plt.show()

def save_to_csv(df_long):
    """Save transformed dataset as CSV"""
    print("\nSaving transformed data to CSV...")
    df_long.to_csv('trade_data_usa_china_long.csv', index=False)
    print("Data saved as 'trade_data_usa_china_long.csv'")

def print_summary():
    """Print summary paragraph explaining importance of the comparison"""
    summary = """
    
SUMMARY:
This comparison between U.S. and Chinese trade openness (Trade % of GDP) is critically important 
for understanding global economic dynamics. The United States, as the world's largest economy, 
traditionally maintained relatively stable trade openness levels, reflecting its diversified domestic 
economy and historical emphasis on consumption-driven growth. China's remarkable transformation 
from a closed economy to one of the world's most trade-dependent nations illustrates the profound 
impact of globalization and export-oriented development strategies. The dramatic increase in China's 
trade openness since the 1990s mirrors its evolution into the "world's factory" and highlights how 
developing economies can leverage international trade for rapid economic growth. This comparison 
provides insights into different economic models - the U.S. consumption-focused economy versus 
China's export-driven growth strategy - and helps policymakers understand the trade-offs between 
domestic self-sufficiency and international economic integration. As trade wars and protectionism 
shape current global politics, analyzing these trends is essential for forecasting future economic 
relationships and understanding the shifting balance of global trade power.
    """
    print(summary)

def main():
    """Main function to run the complete analysis"""
    filename = 'us_china_trade_gdp_1990_2024.xlsx'
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found in current directory.")
        print("Please ensure the Excel file is in the same directory as this script.")
        print(f"Expected file: {filename}")
        return
    
    try:
        # Step 1: Import and explore data
        df = import_and_explore_data(filename)
        
        # Step 2: Transform data to long format
        df_long = transform_data(df)
        
        if df_long is None:
            print("Data transformation failed. Please check the file structure.")
            return
        
        # Step 3: Create visualization
        create_plot(df_long)
        
        # Step 4: Save to CSV
        save_to_csv(df_long)
        
        # Step 5: Print summary
        print_summary()
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check the Excel file format and try again.")

if __name__ == "__main__":
    main()
