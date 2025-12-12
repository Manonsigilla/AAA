"""
Challenge Triple A - System Monitoring Script
This script collects system information and generates an HTML dashboard
Author: [Manon Alex Angie]
Date: 2025-12-09
"""

import psutil
import platform
import socket
import time
import json
from datetime import datetime
import os
from pathlib import Path

def get_system_info():
    """
    Collect general system information
    Returns:  dict with hostname, OS name, boot time, uptime, and user count
    """
    # Get hostname
    hostname = socket.gethostname()
    
    # Get operating system information
    os_name = f"{platform.system()} {platform.release()}"
    try:
        # Try to get distribution info on Linux
        with open('/etc/os-release') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('PRETTY_NAME'):
                    os_name = line.split('=')[1].strip().replace('"', '')
                    break
    except (FileNotFoundError, PermissionError, IOError):
        pass
    
    # Get boot time
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # Calculate uptime
    uptime_seconds = datetime.now().timestamp() - boot_timestamp
    uptime_hours = int(uptime_seconds // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    uptime = f"{uptime_hours} hours, {uptime_minutes} minutes"
    
    # Get number of connected users
    users = psutil.users()
    user_count = len(set([user.name for user in users]))
    
    return {
        'hostname': hostname,
        'os_name': os_name,
        'boot_time': boot_time,
        'uptime': uptime,
        'user_count': str(user_count)
    }

def get_cpu_info():
    """
    Collect CPU information
    Returns:  dict with CPU cores, frequency, and usage percentage
    """
    # Get number of CPU cores
    cpu_cores = psutil.cpu_count(logical=True)
    
    # Get CPU frequency (in MHz)
    cpu_freq = psutil.cpu_freq()
    cpu_freq_current = round(cpu_freq.current, 2) if cpu_freq else 0
    
    # Get CPU usage percentage (wait 1 second for accurate measurement)
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    
    # Generate per-core usage HTML
    cores_html = ""
    for i, percent in enumerate(cpu_per_core):
        cores_html += f'<div>Core {i}: {percent}%</div>'
    
    return {
        'cpu_cores': str(cpu_cores),
        'cpu_freq': str(cpu_freq_current),
        'cpu_percent': str(round(cpu_percent, 1)),
        'cpu_cores_html': cores_html
    }

def get_memory_info():
    """
    Collect memory (RAM) information
    Returns: dict with total RAM, used RAM, and usage percentage
    """
    # Get memory statistics
    memory = psutil.virtual_memory()
    
    # Convert bytes to GB
    ram_total = round(memory.total / (1024 ** 3), 2)
    ram_used = round(memory.used / (1024 ** 3), 2)
    ram_percent = round(memory.percent, 1)
    
    return {
        'ram_total': str(ram_total),
        'ram_used': str(ram_used),
        'ram_percent': str(ram_percent)
    }

def get_network_info():
    """
    Get primary IP address using socket connection simulation
    Returns: dict with IP address
    """
    try:
        # Create a UDP socket (no actual connection established)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to Google DNS (doesn't send data, just determines route)
            s.connect(("8.8.8.8", 80))
            # Get the local IP that would be used for this route
            ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"   [WARN] Could not determine IP:  {e}")
        ip_address = "127.0.0.1"
    
    return {
        'ip_address': ip_address
    }
    
def get_load_average():
    """
    Get system load average (1, 5, 15 minutes)
    Returns: dict with load averages
    """
    if hasattr(os, 'getloadavg'):
        load1, load5, load15 = os.getloadavg()
        return {
            'load_1min': str(round(load1, 2)),
            'load_5min': str(round(load5, 2)),
            'load_15min': str(round(load15, 2))
        }
    else:
        print("   [WARN] Load average not supported on this OS.")
        return {
            'load_1min': 'N/A',
            'load_5min': 'N/A',
            'load_15min': 'N/A'
        }

def get_processes():
    """
    Get all processes sorted by CPU and memory usage
    Returns: dict with HTML table rows for top 3 and all processes
    """
    print("   [INFO] Measuring CPU usage (this takes a moment)...")
    
    # First call to initialize CPU measurement
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Wait for accurate CPU measurement
    time.sleep(2)
    
    # Get list of all running processes with updated CPU values
    processes = []
    
    for proc in psutil.process_iter(['name']):
        try:
            cpu_val = proc.cpu_percent()
            mem_val = proc.memory_percent()
            
            if cpu_val > 0 or mem_val > 0:  # Only include active processes
                processes.append({
                    'name': proc.info['name'],
                    'cpu': cpu_val,
                    'memory': mem_val
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort processes by combined CPU + memory usage
    processes.sort(key=lambda x: x['cpu'] + x['memory'], reverse=True)
    
    # Generate HTML for TOP 3
    top_3_rows = ""
    for i, proc in enumerate(processes[:3], start=1):
        top_3_rows += f"""                        <tr>
                            <td class="rank-cell">#{i}</td>
                            <td>{proc['name']}</td>
                            <td>{round(proc['cpu'], 1)}%</td>
                            <td>{round(proc['memory'], 1)}%</td>
                        </tr>
"""
    
    # Generate HTML for ALL remaining processes (after top 3, with rank numbers)
    all_other_rows = ""
    for i, proc in enumerate(processes[3:], start=4):  # Skip the first 3
        all_other_rows += f"""                        <tr>
                            <td class="rank-cell">#{i}</td>
                            <td>{proc['name']}</td>
                            <td>{round(proc['cpu'], 1)}%</td>
                            <td>{round(proc['memory'], 1)}%</td>
                        </tr>
"""
    
    return {
        'top_processes': top_3_rows,
        'all_processes': all_other_rows,
        'total_processes': str(len(processes))
    }

def analyze_files(directory):
    """
    Analyze files in a directory and count by extension
    Args:  
        directory:  path to the directory to analyze
    Returns:  dict with file counts, sizes, and percentages
    """
    # Define file extensions to analyze
    extensions = {
        '.txt':  {'count': 0, 'size': 0},
        '.py': {'count': 0, 'size': 0},
        '.pdf': {'count': 0, 'size': 0},
        '.jpg': {'count': 0, 'size':  0},
        '.jpeg':  {'count': 0, 'size': 0},
        '.png': {'count': 0, 'size': 0},
        '.docx': {'count':  0, 'size': 0},
        '.xls':  {'count': 0, 'size': 0},
        '.doc': {'count': 0, 'size': 0},
        '.zip': {'count': 0, 'size': 0},
        '.rar': {'count': 0, 'size': 0},
        '.mp3': {'count': 0, 'size': 0},
        '.mp4': {'count':  0, 'size': 0}
    }
    
    # Convert to Path object
    dir_path = Path(directory)
    
    # Check if directory exists
    if not dir_path.exists():
        print(f"   [WARN] Directory not found:  {directory}")
        dir_path = Path(".")
    
    print(f"   [>>] Scanning:  {dir_path.absolute()}")
    
    # Count files by extension (ONE LOOP ONLY)
    total_scanned = 0
    try:
        for file in dir_path.rglob('*'):
            if file.is_file():
                total_scanned += 1
                ext = file.suffix.lower()
                if ext in extensions:
                    extensions[ext]['count'] += 1
                    extensions[ext]['size'] += file.stat().st_size
        
        print(f"   [OK] Total files scanned: {total_scanned}")
        
    except PermissionError as e:
        print(f"   [WARN] Permission denied: {e}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    # Convert bytes to MB
    for ext in extensions:
        extensions[ext]['size'] = round(extensions[ext]['size'] / (1024 ** 2), 2)
    
    # Calculate total matching files
    total_files = sum(ext['count'] for ext in extensions.values())
    
    print(f"   [OK] Found:  {total_files} matching files")
    
    # Avoid division by zero
    if total_files == 0:
        print("   [WARN] No matching files found. Using demo values.")
        extensions = {
            '.txt': {'count': 10, 'size': 0.5},
            '.py': {'count': 5, 'size': 0.2},
            '.pdf': {'count': 3, 'size':  1.5},
            '.jpg':  {'count': 2, 'size': 0.8}
        }
        total_files = 20
    
    # Calculate percentages
    txt_percent = round((extensions['.txt']['count'] / total_files) * 100, 1)
    py_percent = round((extensions['.py']['count'] / total_files) * 100, 1)
    pdf_percent = round((extensions['.pdf']['count'] / total_files) * 100, 1)
    jpg_percent = round((extensions['.jpg']['count'] / total_files) * 100, 1)
    
    return {
        'analyzed_folder': str(dir_path.absolute()),
        'txt_count': str(extensions['.txt']['count']),
        'txt_size': str(extensions['.txt']['size']),
        'txt_percent': str(txt_percent),
        'py_count': str(extensions['.py']['count']),
        'py_size':  str(extensions['.py']['size']),
        'py_percent': str(py_percent),
        'pdf_count': str(extensions['.pdf']['count']),
        'pdf_size': str(extensions['.pdf']['size']),
        'pdf_percent':  str(pdf_percent),
        'jpg_count': str(extensions['.jpg']['count']),
        'jpg_size': str(extensions['.jpg']['size']),
        'jpg_percent': str(jpg_percent),
        'total_files': str(total_files)
    }
    
def save_to_json(data):
    """
    Save collected data to JSON file
    Args:
        data: dictionary containing all system information
    """
    # Clean data for JSON (remove HTML content)
    json_data = data.copy()
    
    # Remove HTML table rows from JSON
    if 'top_processes' in json_data: 
        del json_data['top_processes']
    if 'all_processes' in json_data:
        del json_data['all_processes']
    
    # Write to JSON file
    with open('system_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    
    print("[OK] system_data.json generated successfully!")

def generate_html(data):
    """
    Generate HTML file from template and collected data
    Args:
        data: dictionary containing all system information
    """
    # Read HTML template
    try:
        with open('template.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("[ERROR] template.html not found!")
        return
    
    # Replace all variables in template (support only {{ }})
    for key, value in data.items():
        # Replace {{ variable }}
        placeholder_double = '{{ ' + key + ' }}'
        html_content = html_content.replace(placeholder_double, str(value))
    
    # Write generated HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[OK] index.html generated successfully!")

def main():
    """
    Main function - orchestrates data collection and HTML generation
    """
    print("\n" + "=" * 60)
    print("  Challenge Triple A - System Monitor")
    print("=" * 60)
    print("[>>] Collecting system information.. .\n")
    
    # Collect all data
    data = {}
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Collect system information
    print("[>>] Collecting system info...")
    data.update(get_system_info())
    
    # Collect load average
    print("[>>] Collecting load average...")
    data.update(get_load_average())
    
    # Collect CPU information
    print("[>>] Collecting CPU info...")
    data.update(get_cpu_info())
    
    # Collect memory information
    print("[>>] Collecting memory info...")
    data.update(get_memory_info())
    
    # Collect network information
    print("[>>] Collecting network info...")
    data.update(get_network_info())
    
    # Collect process information
    print("[>>] Collecting process info...")
    data.update(get_processes())
    
    # Analyze files
    print("[>>] Analyzing files...")
    if platform.system() == "Windows":
        analyze_directory = os.path.join(os.path.expanduser("~"), "Documents")
    else:
        analyze_directory = os.path.expanduser("~/Documents")
    
    if not os.path.exists(analyze_directory):
        analyze_directory = "."
        print(f"[INFO] Documents folder not found, analyzing current directory instead.")
    
    data.update(analyze_files(analyze_directory))
    
    # Save to JSON
    print("\n[>>] Saving data to JSON...")
    save_to_json(data)
    
    # Generate HTML
    print("[>>] Generating HTML dashboard...")
    generate_html(data)
    
    print("\n" + "=" * 60)
    print("[OK] Done! Open index.html in your browser to view the dashboard.")
    print(f"[>>] HTML file: {os.path.abspath('index.html')}")
    print(f"[>>] JSON file: {os.path.abspath('system_data.json')}")
    print("=" * 60 + "\n")

# Entry point
if __name__ == "__main__":
    main()