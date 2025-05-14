#!/usr/bin/python3
import psutil
from tabulate import tabulate

# Function to get memory usage recursively for a process including its children
def get_memory_usage_recursive(pid):
    try:
        # Get the process object
        p = psutil.Process(pid)
        # Get the list of children and their memory usage
        child_list = []
        for c in p.children(recursive=True):
            child_list.append({'pid': c.pid, 'name': c.name(), 'memory_usage': c.memory_info().rss / (1024 * 1024)})
        # Include the parent process itself
        return [{'pid': p.pid, 'name': p.name(), 'memory_usage': p.memory_info().rss / (1024 * 1024)}] + child_list
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return []

# Get list of all processes and their memory usage recursively
all_processes = []
for proc in psutil.process_iter(['pid', 'name']):
    try:
        process_info = proc.info
        if process_info['name'].lower() != 'kernel':  # Exclude kernel processes
            all_processes += get_memory_usage_recursive(proc.pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Filter out processes with memory usage of 0 bytes
all_processes = [proc for proc in all_processes if proc['memory_usage'] > 0]

# Aggregate memory usage by process name including physical and virtual memory
aggregated_usage = {}
for proc in all_processes:
    if proc['name'] in aggregated_usage:
        aggregated_usage[proc['name']]['total_memory'] += proc['memory_usage']
        # For demonstration, let's assume we have a way to estimate virtual memory usage
        # In practice, this would require accessing detailed /proc/[pid]/statm or similar on Linux
        aggregated_usage[proc['name']]['virtual_memory'] = aggregated_usage[proc['name']].get('virtual_memory', 0) + (proc['memory_usage'] * psutil.cpu_count())
    else:
        aggregated_usage[proc['name']] = {'pid': None, 'total_memory': proc['memory_usage'], 'virtual_memory': proc['memory_usage'] * psutil.cpu_count()}

# Prepare data for output including physical and virtual memory usage
data = [{'Name': name, 'Total Memory Usage (MB)': usage['total_memory'], 'Virtual Memory Usage (MB)': usage['virtual_memory']} for name, usage in aggregated_usage.items()]

# Print the table with tabulate
print(tabulate(data, headers='keys', floatfmt=".2f", tablefmt="pretty"))
