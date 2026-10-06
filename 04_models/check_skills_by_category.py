import pandas as pd

df = pd.read_csv("data/cleaned/jobs_clean.csv")
df["skill"] = df["required_skills"].str.split("|")
ex = df.explode("skill")
ex["skill"] = ex["skill"].str.strip()

# For each category, its 5 most common skills
for cat, g in ex.groupby("job_category"):
    print(cat, "->", g["skill"].value_counts().head(5).to_dict())

# How many skills appear in only ONE category
per_skill = ex.groupby("skill")["job_category"].nunique()
print("\nSkills that appear in only one category:", int((per_skill == 1).sum()),
      "of", len(per_skill))