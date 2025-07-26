import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Read the Excel file
    df = pd.read_excel('data/student-scores.xlsx')
    
    print("Dataset Analysis:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 3 rows:")
    print(df.head(3))
    print("\nCategorical columns unique values:")
    for col in df.select_dtypes(include=['object']).columns:
        print(f"{col}: {df[col].unique()}")
        
except Exception as e:
    print(f"Error: {e}")
