#!/usr/bin/env python3
"""
Script to analyze the student-scores.xlsx dataset and understand its structure
"""

import pandas as pd
import numpy as np
import os

def analyze_dataset():
    """Analyze the dataset structure and provide insights for schema configuration"""
    
    try:
        # Read the Excel file
        dataset_path = 'data/student-scores.xlsx'
        print(f"Reading dataset from: {dataset_path}")
        
        if not os.path.exists(dataset_path):
            print(f"Error: Dataset file not found at {dataset_path}")
            return
        
        df = pd.read_excel(dataset_path)
        
        print("="*50)
        print("DATASET ANALYSIS REPORT")
        print("="*50)
        
        print(f"\n1. BASIC INFO:")
        print(f"   - Shape: {df.shape}")
        print(f"   - Rows: {df.shape[0]}")
        print(f"   - Columns: {df.shape[1]}")
        
        print(f"\n2. COLUMN NAMES:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n3. DATA TYPES:")
        for col, dtype in df.dtypes.items():
            print(f"   {col:<30}: {dtype}")
        
        print(f"\n4. MISSING VALUES:")
        missing = df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                print(f"   {col:<30}: {count} ({count/len(df)*100:.1f}%)")
        
        print(f"\n5. NUMERICAL COLUMNS:")
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numerical_cols:
            print(f"   - {col}")
        
        print(f"\n6. CATEGORICAL COLUMNS:")
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        for col in categorical_cols:
            unique_vals = df[col].unique()
            print(f"   - {col}: {len(unique_vals)} unique values")
            if len(unique_vals) <= 10:
                print(f"     Values: {list(unique_vals)}")
            else:
                print(f"     Sample values: {list(unique_vals[:5])}...")
        
        print(f"\n7. SAMPLE DATA (First 5 rows):")
        print(df.head().to_string())
        
        print(f"\n8. STATISTICAL SUMMARY:")
        print(df.describe().to_string())
        
        print(f"\n9. SUGGESTED TARGET COLUMN:")
        # Look for common target column names
        potential_targets = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['score', 'grade', 'performance', 'result', 'mark']):
                potential_targets.append(col)
        
        if potential_targets:
            print(f"   Potential target columns: {potential_targets}")
        else:
            print(f"   No obvious target column found. Please specify manually.")
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE")
        print("="*50)
        
        return df
        
    except Exception as e:
        print(f"Error analyzing dataset: {str(e)}")
        return None

if __name__ == "__main__":
    analyze_dataset()
