"""
EDA: Does Tobacco Control Policy Reduce Smoking?
Uses the cleaned, combined 2008-2014 dataset.

Before running:
- Put this script in the SAME folder as smoking_tobacco_combined_2008_2014.csv
- Install needed libraries: pip install pandas matplotlib seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

# ---------------------------------------------------------
# STEP 1: Load the cleaned data
# ---------------------------------------------------------
df = pd.read_csv('smoking_tobacco_combined_2008_2014.csv')
print("Shape:", df.shape)
print(df.head())

# ---------------------------------------------------------
# STEP 2: Summary statistics
# ---------------------------------------------------------
print("\n--- Summary stats: prevalence & regulation columns ---")
key_cols = [
    'CigaretteSmokingPrevalence_estimate',
    'TobaccoSmokingPrevalence_estimate',
    'RegulationsOnSmokeFreeEnvironments',
]
print(df[key_cols].describe())

# ---------------------------------------------------------
# STEP 3: Distribution of smoking prevalence
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.histplot(df['CigaretteSmokingPrevalence_estimate'].dropna(), bins=25, kde=True)
plt.title('Distribution of Cigarette Smoking Prevalence (all years combined)')
plt.xlabel('Prevalence (%)')
plt.tight_layout()
plt.savefig('01_prevalence_distribution.png')
plt.close()

# ---------------------------------------------------------
# STEP 4: Trend over time (global average by year)
# ---------------------------------------------------------
yearly_avg = df.groupby('Year')['CigaretteSmokingPrevalence_estimate'].mean()
print("\n--- Global average cigarette prevalence by year ---")
print(yearly_avg)

plt.figure(figsize=(8, 5))
yearly_avg.plot(marker='o')
plt.title('Global Average Cigarette Smoking Prevalence Over Time')
plt.xlabel('Year')
plt.ylabel('Average Prevalence (%)')
plt.tight_layout()
plt.savefig('02_prevalence_trend.png')
plt.close()

# ---------------------------------------------------------
# STEP 5: Regulation strength over time
# ---------------------------------------------------------
yearly_reg = df.groupby('Year')['RegulationsOnSmokeFreeEnvironments'].mean()
print("\n--- Average regulation score by year ---")
print(yearly_reg)

plt.figure(figsize=(8, 5))
yearly_reg.plot(marker='o', color='darkorange')
plt.title('Average Smoke-Free Regulation Score Over Time')
plt.xlabel('Year')
plt.ylabel('Avg Regulation Score (0-10 scale)')
plt.tight_layout()
plt.savefig('03_regulation_trend.png')
plt.close()

# ---------------------------------------------------------
# STEP 6: Does higher regulation relate to lower prevalence?
# ---------------------------------------------------------
plot_df = df.dropna(subset=['RegulationsOnSmokeFreeEnvironments', 'CigaretteSmokingPrevalence_estimate'])

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=plot_df,
    x='RegulationsOnSmokeFreeEnvironments',
    y='CigaretteSmokingPrevalence_estimate',
    hue='Year',
    palette='viridis',
    alpha=0.7
)
plt.title('Regulation Strength vs Cigarette Smoking Prevalence')
plt.xlabel('Regulation Score (0-10)')
plt.ylabel('Cigarette Prevalence (%)')
plt.tight_layout()
plt.savefig('04_regulation_vs_prevalence.png')
plt.close()

correlation = plot_df['RegulationsOnSmokeFreeEnvironments'].corr(
    plot_df['CigaretteSmokingPrevalence_estimate']
)
print(f"\nCorrelation between regulation score and prevalence: {correlation:.3f}")

# ---------------------------------------------------------
# STEP 7: Countries with strongest policy but still high prevalence
# (interesting outliers worth writing about)
# ---------------------------------------------------------
outliers = plot_df[
    (plot_df['RegulationsOnSmokeFreeEnvironments'] >= 7) &
    (plot_df['CigaretteSmokingPrevalence_estimate'] >= 25)
][['Location', 'Year', 'RegulationsOnSmokeFreeEnvironments', 'CigaretteSmokingPrevalence_estimate']]

print("\n--- Countries with strong regulation (>=7) but still high prevalence (>=25%) ---")
print(outliers.sort_values('CigaretteSmokingPrevalence_estimate', ascending=False))

# ---------------------------------------------------------
# STEP 8: Top and bottom 10 countries by prevalence (latest year)
# ---------------------------------------------------------
latest = df[df['Year'] == df['Year'].max()]
top10 = latest.nlargest(10, 'CigaretteSmokingPrevalence_estimate')[['Location', 'CigaretteSmokingPrevalence_estimate']]
bottom10 = latest.nsmallest(10, 'CigaretteSmokingPrevalence_estimate')[['Location', 'CigaretteSmokingPrevalence_estimate']]

print(f"\n--- Top 10 highest smoking prevalence countries ({df['Year'].max()}) ---")
print(top10)
print(f"\n--- Top 10 lowest smoking prevalence countries ({df['Year'].max()}) ---")
print(bottom10)

print("\nAll charts saved as PNG files in this folder. EDA complete.")