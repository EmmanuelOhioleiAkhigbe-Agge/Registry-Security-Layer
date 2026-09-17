import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load training dataset
data = pd.read_csv(
    "security_dataset.csv",
    keep_default_na=False
)

# Make sure text columns are strings
for column in ["change_type", "value_name", "old_value", "new_value"]:
    data[column] = data[column].astype(str)

# Build the same features used during training
data["features"] = (
    data["change_type"] + " "
    + data["value_name"] + " "
    + data["old_value"] + " "
    + data["new_value"]
)

X = data["features"]
y = data["classification"]

# Create the same ML pipeline
model = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

# Train using the complete training dataset
model.fit(X, y)

print("Model trained on full dataset.")
print()
print("Testing NEW registry changes")
print("================================")

# These examples were NOT included in the training dataset
test_examples = [
    ["modified", "DesktopTheme", "Blue", "Dark"],
    ["added", "UnknownProgram", "", "Normal Application"],
    ["modified", "StartupEntry", "Disabled", "Unknown Script"],
    ["added", "PowerShellEntry", "", "Encoded PowerShell Script"],
    ["modified", "ScreenBrightness", "40", "80"],
    ["added", "LoginScript", "", "Unknown Script"],
    ["modified", "ServiceCommand", "Normal", "PowerShell Persistence Script"],
    ["modified", "KeyboardLayout", "US", "DE"],
]

for change_type, value_name, old_value, new_value in test_examples:

    test_text = (
        change_type + " "
        + value_name + " "
        + old_value + " "
        + new_value
    )

    prediction = model.predict([test_text])[0]

    probabilities = model.predict_proba([test_text])[0]
    classes = model.classes_

    confidence = max(probabilities) * 100

    print()
    print("Change:")
    print(" ", test_text)

    print("Prediction:")
    print(" ", prediction)

    print("Confidence:")
    print(f"  {confidence:.2f}%")

    print("--------------------------------")