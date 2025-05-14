#!/usr/bin/python3
import psutil
from tabulate import tabulate  # You may need to install this library if not already installed

# Get list of all processes
processes = []
for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
    try:
        process_info = proc.info
        if process_info['name'].lower() != 'kernel':  # Exclude kernel processes
            processes.append(process_info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Sort by memory usage
processes = sorted(processes, key=lambda proc: proc['memory_info'].rss, reverse=True)

# Prepare data for output
data = [{'PID': proc['pid'], 'Name': proc['name'], 'Memory Usage': proc['memory_info'].rss / (1024 * 1024)} for proc in processes]

# Print the table with tabulate
print(tabulate(data, headers='keys', floatfmt=".2f", tablefmt="pretty"))
