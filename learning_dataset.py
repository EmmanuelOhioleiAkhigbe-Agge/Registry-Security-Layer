import csv
import os


DATASET_FILE = "security_dataset.csv"


def save_event(
    change_type,
    value_name,
    old_value,
    new_value,
    risk_score,
    classification
):

    file_exists = os.path.exists(DATASET_FILE)

    with open(
        DATASET_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Create the column headings the first time
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

    print("Security event saved to dataset.")