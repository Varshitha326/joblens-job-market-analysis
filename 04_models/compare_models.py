import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("data/cleaned/jobs_clean.csv")

# Features: required skills (split on "|"). Label: job_category.
vec = TfidfVectorizer(tokenizer=lambda s: [t.strip() for t in s.split("|")],
                      token_pattern=None, lowercase=True)
X = vec.fit_transform(df["required_skills"])
y = df["job_category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    "Baseline (always most common class)": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42,
                                            class_weight="balanced"),
    "Naive Bayes": MultinomialNB(),
}

rows = []
for name, m in models.items():
    m.fit(X_train, y_train)
    p = m.predict(X_test)
    rows.append([
        name,
        accuracy_score(y_test, p),
        precision_score(y_test, p, average="macro", zero_division=0),
        recall_score(y_test, p, average="macro", zero_division=0),
        f1_score(y_test, p, average="macro", zero_division=0),
    ])

result = pd.DataFrame(rows, columns=["Model", "Accuracy", "Macro Precision",
                                     "Macro Recall", "Macro F1"])
result = result.round(3)
result.to_csv("reports/model_comparison.csv", index=False)
print(result.to_string(index=False))
print("\nTraining rows:", X_train.shape[0], "| Test rows:", X_test.shape[0])