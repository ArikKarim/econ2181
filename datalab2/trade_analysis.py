#!/usr/bin/env python3
"""
World Bank Trade Data Analysis: USA vs China (1990-2024)
Analysis of Trade (% of GDP) data for United States and China
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set non-interactive backend at the start
import matplotlib
matplotlib.use('Agg')

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
    
    # Remove empty rows and reset index
    df_clean = df.dropna(subset=['Series Name']).reset_index(drop=True)
    print(f"Cleaned data shape: {df_clean.shape}")
    
    # Filter for Trade (% of GDP) data
    trade_rows = df_clean[df_clean['Series Name'] == 'Trade (% of GDP)']
    print(f"Found {len(trade_rows)} rows with Trade (% of GDP) data")
    
    # Get USA and China data
    usa_row = trade_rows[trade_rows['Country Name'] == 'United States']
    chn_row = trade_rows[trade_rows['Country Name'] == 'China']
    
    if usa_row.empty:
        print("USA data not found. Available countries:")
        print(trade_rows['Country Name'].unique())
        return None
        
    if chn_row.empty:
        print("China data not found. Available countries:")
        print(trade_rows['Country Name'].unique())
        return None
    
    print("Found USA and China data")
    
    # Get year columns (from 1990 to 2024) - FIX: operator precedence issue
    year_columns = [col for col in df_clean.columns 
                   if isinstance(col, str) and (col.startswith('19') or col.startswith('20'))]
    # Clean year column names to extract year numbers
    year_numbers = []
    cleaned_year_cols = []
    
    for col in year_columns:
        # Extract year from column name like "1990 [YR1990]"
        if '[YR' in col:
            year_str = col.split('[YR')[1].split(']')[0]
            try:
                year_num = int(year_str)
                if 1990 <= year_num <= 2024:
                    year_numbers.append(year_num)
                    cleaned_year_cols.append(col)
            except ValueError:
                continue
    
    year_numbers.sort()
    cleaned_year_cols.sort(key=lambda x: int(x.split('[YR')[1].split(']')[0]))
    
    print(f"Year columns found: {len(year_numbers)} years from {min(year_numbers)} to {max(year_numbers)}")
    
    # Extract data for USA and China
    usa_values = usa_row[cleaned_year_cols].values.flatten()
    chn_values = chn_row[cleaned_year_cols].values.flatten()
    
    # Create long format data
    data_long = []
    
    for i, year in enumerate(year_numbers):
        if not pd.isna(usa_values[i]) and usa_values[i] != '':
            data_long.append({
                'year': year,
                'country': 'United States',
                'trade_pct_gdp': float(usa_values[i])
            })
        
        if not pd.isna(chn_values[i]) and chn_values[i] != '':
            data_long.append({
                'year': year,
                'country': 'China', 
                'trade_pct_gdp': float(chn_values[i])
            })
    
    df_long = pd.DataFrame(data_long)
    print(f"\nTransformed data shape: {df_long.shape}")
    print("\nTransformed data:")
    print(df_long.head(10))
    
    return df_long

def create_plot(df_long):
    """Create matplotlib line chart"""
    print("\nCreating visualization...")
    
    # Set up the plot (backend already set globally)
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
    
    # Don't show plot in interactive mode since we're saving it
    # plt.show()  # Commented out to prevent hanging in non-GUI environments

def save_to_csv(df_long):
    """Save transformed dataset as CSV"""
    print("\nSaving transformed data to CSV...")
    df_long.to_csv('trade_data_usa_china_long.csv', index=False)
    print("Data saved as 'trade_data_usa_china_long.csv'")

def lab_median_growth_gap(trade_xlsx_path, growth_xlsx_path):
    """
    Complete Data Lab 2 analysis matching the slides:
    - Load Trade and GDP per capita growth data
    - Melt both to long format
    - Merge on country/year
    - Compute above/below median trade grouping by year
    - Calculate average growth by group and pivot
    - Plot difference series with mean and zero lines
    """
    print("\n" + "="*60)
    print("DATA LAB 2 ANALYSIS: MEDIAN GROWTH GAP")
    print("="*60)
    
    # Load WDI Excel extracts (Data sheets)
    print("Loading Trade data...")
    trade = pd.read_excel(trade_xlsx_path, sheet_name="Data")
    print("Loading Growth data...")
    growth = pd.read_excel(growth_xlsx_path, sheet_name="Data")

    def tidy(df, value_name):
        """Convert WDI data to long format"""
        id_cols = ['Country Name','Country Code','Series Name','Series Code']
        year_cols = [c for c in df.columns 
                     if isinstance(c, str) and (c.startswith('19') or c.startswith('20')) and '[YR' in c]
        
        if df.empty:
            return pd.DataFrame()
            
        df = df[id_cols + year_cols].copy()
        
        # Filter correct indicator
        if value_name == 'Trade':
            df = df[df['Series Code'] == 'NE.TRD.GNFS.ZS']
        else:  # Growth
            df = df[df['Series Code'] == 'NY.GDP.PCAP.KD.ZG']
            
        if df.empty:
            return pd.DataFrame()
            
        # Melt to long
        long = df.melt(id_vars=['Country Name','Country Code','Series Name','Series Code'],
                       value_vars=year_cols, var_name='Year', value_name=value_name)
        
        # Clean Year
        long['Year'] = long['Year'].str.extract(r'(\d{4})').astype(int)
        return long[['Country Name','Country Code','Year', value_name]]

    # Convert both datasets to long format
    trade_long = tidy(trade, 'Trade')
    growth_long = tidy(growth, 'Growth')
    
    print(f"Trade data: {len(trade_long)} observations")
    print(f"Growth data: {len(growth_long)} observations")

    # Merge on country and year
    frame = pd.merge(trade_long, growth_long, on=['Country Name','Country Code','Year'])
    frame = frame.dropna(subset=['Trade','Growth'])
    print(f"After merge: {len(frame)} observations")

    # Above/Below median trade by year
    med = frame.groupby('Year')['Trade'].transform('median')
    frame['group'] = (frame['Trade'] > med).map({True:'Above Median', False:'Below Median'})
    
    # Count countries in each group by year
    group_counts = frame.groupby(['Year','group']).size().reset_index(name='count')
    print(f"Group distribution:\n{group_counts.head(10)}")

    # Average growth by group → pivot → difference
    result = (frame.groupby(['Year','group'])['Growth'].mean()
                    .reset_index())
    pivot = result.pivot(index='Year', columns='group', values='Growth')
    pivot = pivot.sort_index()
    
    # Calculate difference: Above Median - Below Median
    if 'Above Median' in pivot.columns and 'Below Median' in pivot.columns:
        pivot['difference'] = pivot['Above Median'] - pivot['Below Median']
    else:
        print("Warning: Both Above and Below Median groups not found")
        return None
        
    print(f"Pivot table shape: {pivot.shape}")
    print(f"Average difference: {pivot['difference'].mean():.3f} percentage points")

    # Plot the difference series (the slide's chart)
    plt.figure(figsize=(12, 8))
    
    # Main difference line
    plt.plot(pivot.index, pivot['difference'], marker='o', linewidth=2, 
             label='Growth Gap (Above - Below Median Trade)', color='blue')
    
    # Mean line
    plt.axhline(pivot['difference'].mean(), linewidth=2, linestyle='--', 
                color='red', alpha=0.7, label=f'Mean Gap ({pivot["difference"].mean():.2f} pp)')
    
    # Zero line
    plt.axhline(0, linewidth=1, color='black', alpha=0.5, label='Zero Gap')
    
    # Customize plot
    plt.title('Difference in GDP per Capita Growth by High vs Low Trade Countries', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('GDP per Capita Growth (percentage points)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Format x-axis
    plt.xticks(pivot.index[::5], rotation=45)
    
    plt.tight_layout()
    plt.savefig('lab_growth_gap_difference.png', dpi=300, bbox_inches='tight')
    print("Difference plot saved as 'lab_growth_gap_difference.png'")
    
    return pivot

def print_summary():
    """Print summary paragraph explaining importance of the comparison"""
    summary = """

SUMMARY:
This comparison between U.S. and Chinese trade openness (Trade:% of GDP) is critically important 
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
        
        print("\n" + "="*60)
        print("TO RUN COMPLETE DATA LAB 2 ANALYSIS:")
        print("="*60)
        print("# If you have both Trade and Growth Excel files:")
        print("# pivot_result = lab_median_growth_gap(")
        print("#     'API_NE.TRD.GNFS_ZS.xlsx',  # Trade data")
        print("#     'API_NY.GDP.PCAP.KD.ZG.xlsx'  # Growth data") 
        print("# )")
        print("# This will create 'lab_growth_gap_difference.png'")
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check the Excel file format and try again.")

if __name__ == "__main__":
    main()
