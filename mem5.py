#!/usr/bin/python3
import psutil
from tabulate import tabulate

# Get list of all processes
processes = []
for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
    try:
        process_info = proc.info
        if process_info['name'].lower() != 'kernel' and process_info['memory_info'].rss > 0:  # Exclude kernel processes and exclude 0 values
            processes.append(process_info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Sort by memory usage excluding 0 values
processes = sorted([proc for proc in processes if proc['memory_info'].rss > 0], key=lambda proc: proc['memory_info'].rss, reverse=True)

# Prepare data for output
data = [{'PID': proc['pid'], 'Name': proc['name'], 'Memory Usage': proc['memory_info'].rss / (1024 * 1024)} for proc in processes]

# Print the table with tabulate
print(tabulate(data, headers='keys', floatfmt=".2f", tablefmt="pretty"))
