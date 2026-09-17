import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import accuracy_score, classification_report


# ---------------------------------------------
# LOAD DATASET
# ---------------------------------------------

data = pd.read_csv(
    "security_dataset.csv",
    keep_default_na=False
)


# Make sure the important columns are text
for column in [
    "change_type",
    "value_name",
    "old_value",
    "new_value"
]:
    data[column] = data[column].astype(str)


# Combine registry information
data["features"] = (
    data["change_type"]
    + " "
    + data["value_name"]
    + " "
    + data["old_value"]
    + " "
    + data["new_value"]
)


# ---------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------

X = data["features"]
y = data["classification"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)


print("Total examples:", len(data))
print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))


# ---------------------------------------------
# CREATE MODEL
# ---------------------------------------------

model = Pipeline([
    (
        "vectorizer",
        TfidfVectorizer()
    ),
    (
        "classifier",
        LogisticRegression()
    )
])


# ---------------------------------------------
# TRAIN
# ---------------------------------------------

model.fit(
    X_train,
    y_train
)


print("\nModel trained successfully.")


# ---------------------------------------------
# TEST
# ---------------------------------------------

predictions = model.predict(X_test)


# ---------------------------------------------
# ACCURACY
# ---------------------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\nModel accuracy:")
print(f"{accuracy * 100:.2f}%")


# ---------------------------------------------
# DETAILED REPORT
# ---------------------------------------------

print("\nClassification report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ---------------------------------------------
# SHOW INDIVIDUAL TEST RESULTS
# ---------------------------------------------

print("\nIndividual test results:")
print("--------------------------------")

for actual, predicted, text in zip(
    y_test,
    predictions,
    X_test
):

    print("Change:", text)
    print("Actual:", actual)
    print("Predicted:", predicted)
    print("--------------------------------")
    