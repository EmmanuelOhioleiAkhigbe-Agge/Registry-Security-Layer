import winreg


def list_subkeys(hive, path):
    key = winreg.OpenKey(hive, path)

    print(f"\nSubkeys inside {path}:\n")

    index = 0

    while True:
        try:
            subkey = winreg.EnumKey(key, index)
            print(index, "-", subkey)
            index += 1
        except OSError:
            break

    winreg.CloseKey(key)


list_subkeys(
    winreg.HKEY_CURRENT_USER,
    r"Software"
)