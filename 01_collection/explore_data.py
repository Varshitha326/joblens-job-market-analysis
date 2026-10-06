import pandas as pd

df = pd.read_csv("data/raw/ai_jobs_market_2025_2026.csv")

print("Sample required_skills:")
print(df["required_skills"].head(5).tolist())
print("\nCountries:")
print(df["country"].value_counts())
print("\nJob categories:")
print(df["job_category"].value_counts())
print("\nExperience levels:")
print(df["experience_level"].value_counts())