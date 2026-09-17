import winreg
import time
from security_engine import analyze_change

REGISTRY_PATH = r"Software\RegistrySecurityTest_New"


def get_values(hive, path):
    key = winreg.OpenKey(hive, path)

    values = {}

    index = 0

    while True:
        try:
            name, value, value_type = winreg.EnumValue(key, index)

            values[name] = value

            index += 1

        except OSError:
            break

    winreg.CloseKey(key)

    return values


def compare_values(old_values, new_values):

    # Check for added or modified values
    for name in new_values:

        if name not in old_values:

            change = f"Added value {name} = {new_values[name]}"

            print("\nCHANGE DETECTED")
            print(change)

            analyze_change(
                change,
                change_type="added",
                value_name=name,
                old_value="",
                new_value=str(new_values[name])
            )

        elif old_values[name] != new_values[name]:

            change = (
                f"Changed value {name} "
                f"from {old_values[name]} "
                f"to {new_values[name]}"
            )

            print("\nCHANGE DETECTED")
            print(change)

            analyze_change(
                change,
                change_type="modified",
                value_name=name,
                old_value=str(old_values[name]),
                new_value=str(new_values[name])
            )

    # Check for removed values
    for name in old_values:

        if name not in new_values:

            change = f"Removed value {name}"

            print("\nCHANGE DETECTED")
            print(change)

            analyze_change(
                change,
                change_type="removed",
                value_name=name,
                old_value=str(old_values[name]),
                new_value=""
            )


def create_test_key():

    key = winreg.CreateKey(
        winreg.HKEY_CURRENT_USER,
        REGISTRY_PATH
    )

    winreg.SetValueEx(
        key,
        "TestValue",
        0,
        winreg.REG_SZ,
        "Safe"
    )

    winreg.CloseKey(key)


# Create the safe testing registry key
create_test_key()


# Take the initial snapshot
previous_values = get_values(
    winreg.HKEY_CURRENT_USER,
    REGISTRY_PATH
)


print("===================================")
print(" Registry Security Layer")
print("===================================")

print("Monitoring:", REGISTRY_PATH)
print("Checking every 3 seconds...")
print("Press CTRL+C to stop.\n")


# Continuous monitoring
while True:

    time.sleep(3)

    current_values = get_values(
        winreg.HKEY_CURRENT_USER,
        REGISTRY_PATH
    )

    compare_values(
        previous_values,
        current_values
    )

    previous_values = current_values