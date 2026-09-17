import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATASET_FILE = "security_dataset.csv"

# Load training data
data = pd.read_csv(
    DATASET_FILE,
    keep_default_na=False
)

for column in ["change_type", "value_name", "old_value", "new_value"]:
    data[column] = data[column].astype(str)

# Create the same feature text used during training
data["features"] = (
    data["change_type"] + " "
    + data["value_name"] + " "
    + data["old_value"] + " "
    + data["new_value"]
)

X = data["features"]
y = data["classification"]

# Create and train the ML model
model = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

model.fit(X, y)


def explain_change(change_type, value_name, old_value, new_value):

    text = (
        change_type + " "
        + value_name + " "
        + old_value + " "
        + new_value
    )

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    print("\n===================================")
    print(" Registry Security AI Analysis")
    print("===================================")

    print("\nRegistry change:")
    print("Type:", change_type)
    print("Value:", value_name)
    print("Old value:", old_value)
    print("New value:", new_value)

    print("\nAI prediction:")
    print(prediction)

    print(f"Confidence: {confidence:.2f}%")

    # Rule-based explanation indicators
    indicators = []

    text_lower = text.lower()

    if "powershell" in text_lower:
        indicators.append(
            "PowerShell-related activity detected"
        )

    if "encoded" in text_lower:
        indicators.append(
            "Encoded content detected"
        )

    if "script" in text_lower:
        indicators.append(
            "Script-related activity detected"
        )

    if "startup" in text_lower:
        indicators.append(
            "Startup-related registry activity detected"
        )

    if "autorun" in text_lower:
        indicators.append(
            "Auto-run configuration detected"
        )

    if "persistence" in text_lower:
        indicators.append(
            "Possible persistence-related activity detected"
        )

    if "command" in text_lower:
        indicators.append(
            "Command-related activity detected"
        )

    if indicators:
        print("\nPotential indicators:")

        for indicator in indicators:
            print("-", indicator)

    else:
        print("\nPotential indicators:")
        print("- No known suspicious indicators detected")

    print("\n===================================")


# Test examples
test_examples = [
    [
        "modified",
        "DesktopTheme",
        "Blue",
        "Dark"
    ],
    [
        "modified",
        "StartupEntry",
        "Disabled",
        "Unknown Script"
    ],
    [
        "added",
        "PowerShellEntry",
        "",
        "Encoded PowerShell Script"
    ],
    [
        "modified",
        "KeyboardLayout",
        "US",
        "DE"
    ],
]

for example in test_examples:
    explain_change(*example)