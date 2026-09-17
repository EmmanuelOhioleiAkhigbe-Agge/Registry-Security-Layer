import wmi


def list_processes():
    computer = wmi.WMI()

    print("Running processes:\n")

    for process in computer.Win32_Process():
        print("Name:", process.Name)
        print("PID:", process.ProcessId)
        print("Path:", process.ExecutablePath)
        print()


list_processes()