"""
Smoking & Tobacco Data Cleaning Script
Combines 2008, 2010, 2012, 2014 CSVs into one clean, long-format dataset.

Before running:
- Put this script in the SAME folder as the 4 CSV files.
- Make sure pandas is installed: pip install pandas
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------
# STEP 1: Load all 4 files and stack them with a Year column
# ---------------------------------------------------------
files = {
    2008: 'SmokingAndTobaccoData2008.csv',
    2010: 'SmokingAndTobaccoData2010.csv',
    2012: 'SmokingAndTobaccoData2012.csv',
    2014: 'SmokingAndTobaccoData2014.csv',
}

dfs = []
for year, path in files.items():
    d = pd.read_csv(path)
    d['Year'] = year
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)
print(f"Combined shape: {df.shape}  (should be 596 rows = 149 countries x 4 years)")

# ---------------------------------------------------------
# STEP 2: Standardize all "missing data" tokens into real NaN
# ---------------------------------------------------------
# Includes 'x', which only appears in the 2014 BanOn... columns as a
# placeholder for missing data.
missing_tokens = ['Not available', 'Not applicable', 'Data not available', 'x']
df = df.replace(missing_tokens, np.nan)

# ---------------------------------------------------------
# STEP 3: Split the "value [low - high]" prevalence columns
# into 3 separate numeric columns each
# ---------------------------------------------------------
def split_prevalence(series):
    pattern = r'([\d.]+)\s*\[([\d.]+)\s*[-–]\s*([\d.]+)\]'
    extracted = series.str.extract(pattern)
    extracted.columns = ['estimate', 'ci_low', 'ci_high']
    return extracted.astype(float)

prevalence_cols = ['CigaretteSmokingPrevalence', 'TobaccoSmokingPrevalence', 'TobaccoUsePrevalance']

for col in prevalence_cols:
    new_cols = split_prevalence(df[col])
    new_cols.columns = [f'{col}_{c}' for c in new_cols.columns]
    df = pd.concat([df.drop(columns=[col]), new_cols], axis=1)

# ---------------------------------------------------------
# STEP 4: Clean the price column (remove commas, convert to number)
# ---------------------------------------------------------
df['MostSoldBrandCigarettePrice'] = pd.to_numeric(
    df['MostSoldBrandCigarettePrice'].astype(str).str.replace(',', '', regex=False),
    errors='coerce'
)

# ---------------------------------------------------------
# STEP 5: Convert numeric-scale columns (0-10 style ratings) to numbers
# ---------------------------------------------------------
ban_cols = [c for c in df.columns if c.startswith('BanOn')]
numeric_scale_cols = ['RegulationsOnSmokeFreeEnvironments'] + ban_cols

for c in numeric_scale_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# ---------------------------------------------------------
# STEP 6: Quick sanity checks
# ---------------------------------------------------------
print("\nRows per year:")
print(df['Year'].value_counts().sort_index())

print("\nMissing value % by column (overall):")
print((df.isna().mean() * 100).round(1))

print("\nPreview:")
print(df.head())

# ---------------------------------------------------------
# STEP 7: Save the cleaned, combined file
# ---------------------------------------------------------
output_path = 'smoking_tobacco_combined_2008_2014.csv'
df.to_csv(output_path, index=False)
print(f"\nSaved cleaned file to: {output_path}")