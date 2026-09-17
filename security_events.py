import csv
import os

EVENTS_FILE = "security_events.csv"


def save_event(
    change_type,
    value_name,
    old_value,
    new_value,
    risk_score,
    classification
):
    file_exists = os.path.exists(EVENTS_FILE)

    with open(
        EVENTS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "change_type",
                "value_name",
                "old_value",
                "new_value",
                "risk_score",
                "classification"
            ])

        writer.writerow([
            change_type,
            value_name,
            old_value,
            new_value,
            risk_score,
            classification
        ])

    print("Security event saved.")