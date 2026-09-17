import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from security_events import save_event


DATASET_FILE = "security_dataset.csv"


# ==========================================
# RULE-BASED SECURITY ANALYSIS
# ==========================================

def calculate_risk(change):

    change_text = change.lower()

    risk = 0

    suspicious_words = [
        "powershell",
        "command",
        "script",
        "shell",
        "startup",
        "run"
    ]

    for word in suspicious_words:

        if word in change_text:
            risk += 20

    if "changed value" in change_text:
        risk += 10

    if "removed value" in change_text:
        risk += 15

    if "added value" in change_text:
        risk += 5

    if risk > 100:
        risk = 100

    return risk


def classify_risk(risk):

    if risk >= 70:
        return "HIGH RISK"

    elif risk >= 40:
        return "SUSPICIOUS"

    else:
        return "LOW RISK"


# ==========================================
# SECURITY DECISION
# ==========================================

def make_security_decision(classification):

    if classification == "HIGH RISK":

        return (
            "SECURITY ALERT: High-risk registry activity detected. "
            "Manual investigation recommended."
        )

    elif classification == "SUSPICIOUS":

        return (
            "SECURITY WARNING: Suspicious registry activity detected. "
            "Review recommended."
        )

    else:

        return (
            "SECURITY LOG: Registry activity appears low risk."
        )


# ==========================================
# TRAIN MACHINE-LEARNING MODEL
# ==========================================

def train_ml_model():

    data = pd.read_csv(
        DATASET_FILE,
        keep_default_na=False
    )

    for column in [
        "change_type",
        "value_name",
        "old_value",
        "new_value"
    ]:

        data[column] = data[column].astype(str)

    data["features"] = (
        data["change_type"] + " "
        + data["value_name"] + " "
        + data["old_value"] + " "
        + data["new_value"]
    )

    X = data["features"]
    y = data["classification"]

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

    model.fit(X, y)

    return model


# Train model when security engine starts
ml_model = train_ml_model()


# ==========================================
# SECURITY ANALYSIS
# ==========================================

def analyze_change(
    change,
    change_type="unknown",
    value_name="unknown",
    old_value="",
    new_value=""
):

    # --------------------------------------
    # Rule-based analysis
    # --------------------------------------

    risk = calculate_risk(change)

    rule_classification = classify_risk(risk)


    # --------------------------------------
    # Machine-learning analysis
    # --------------------------------------

    ml_text = (
        str(change_type) + " "
        + str(value_name) + " "
        + str(old_value) + " "
        + str(new_value)
    )

    ml_prediction = ml_model.predict(
        [ml_text]
    )[0]

    probabilities = ml_model.predict_proba(
        [ml_text]
    )[0]

    ml_confidence = max(probabilities) * 100


    # --------------------------------------
    # Security decision
    # --------------------------------------

    security_decision = make_security_decision(
        rule_classification
    )


    # --------------------------------------
    # Display results
    # --------------------------------------

    print("\n===================================")
    print(" Security Analysis")
    print("===================================")

    print("\nRegistry change:")
    print(change)

    print("\nRule-based analysis:")
    print("Risk score:", risk, "/ 100")
    print("Classification:", rule_classification)

    print("\nMachine-learning analysis:")
    print("Prediction:", ml_prediction)
    print(f"Confidence: {ml_confidence:.2f}%")

    print("\nSecurity decision:")
    print(security_decision)


    # --------------------------------------
    # Explain indicators
    # --------------------------------------

    indicators = []

    text_lower = ml_text.lower()

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
            "Startup-related activity detected"
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


    # --------------------------------------
    # Save live security event
    # --------------------------------------

    save_event(
        change_type,
        value_name,
        old_value,
        new_value,
        risk,
        rule_classification
    )


    return rule_classification