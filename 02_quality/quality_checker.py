import pandas as pd

df = pd.read_csv("data/raw/ai_jobs_market_2025_2026.csv")
report = []

# ---- Checks before cleaning ----
report.append("=== BEFORE CLEANING ===")
report.append(f"Total rows: {len(df)}")
report.append(f"Duplicate rows: {df.duplicated().sum()}")
report.append(f"Duplicate job_ids: {df['job_id'].duplicated().sum()}")
report.append("Missing values per column:")
report.append(df.isnull().sum().to_string())

salary_bad = df[(df["annual_salary_usd"] < df["salary_min_usd"]) |
                (df["annual_salary_usd"] > df["salary_max_usd"])]
report.append(f"Salary outside its own min-max range: {len(salary_bad)}")
report.append(f"Negative years of experience: {(df['years_of_experience'] < 0).sum()}")
report.append(f"Zero or negative salary: {(df['annual_salary_usd'] <= 0).sum()}")

# ---- Cleaning ----
df = df.drop_duplicates(subset="job_id")
for col in ["job_title", "job_category", "experience_level", "city", "country",
            "remote_work", "company_size", "industry", "required_skills"]:
    df[col] = df[col].astype(str).str.strip()
df = df.dropna(subset=["job_title", "job_category"])
df = df[df["annual_salary_usd"] > 0]
df = df[df["years_of_experience"] >= 0]

# Flag (do not delete) rows whose salary is outside their own min-max range
df["salary_outside_range"] = ((df["annual_salary_usd"] < df["salary_min_usd"]) |
                              (df["annual_salary_usd"] > df["salary_max_usd"]))

# ---- Summary after cleaning ----
report.append("\n=== AFTER CLEANING ===")
report.append(f"Rows remaining: {len(df)}")
report.append(f"Rows flagged salary_outside_range: {int(df['salary_outside_range'].sum())}")
report.append("Job category counts:")
report.append(df["job_category"].value_counts().to_string())

df.to_csv("data/cleaned/jobs_clean.csv", index=False)
with open("reports/quality_report.txt", "w") as f:
    f.write("\n".join(report))
print("\n".join(report))