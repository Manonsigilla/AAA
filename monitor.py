#!/usr/bin/env python3
"""
Challenge Triple A - System Monitoring Script
This script collects system information and generates an HTML dashboard
Author: [Your Team Names]
Date: 2025-12-09
"""

import psutil
import platform
import socket
import time
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
    except:
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
    
    return {
        'cpu_cores': str(cpu_cores),
        'cpu_freq': str(cpu_freq_current),
        'cpu_percent': str(round(cpu_percent, 1))
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
    ram_percent = round(memory. percent, 1)
    
    return {
        'ram_total': str(ram_total),
        'ram_used': str(ram_used),
        'ram_percent': str(ram_percent)
    }

def get_network_info():
    """
    Get primary IP address
    Returns: dict with IP address
    """
    try:
        # Create a socket to determine the primary IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except:
        ip_address = "127.0.0.1"
    
    return {
        'ip_address': ip_address
    }

def get_top_processes():
    """
    Get top 3 processes by CPU and memory usage
    Returns:  dict with HTML table rows for top processes
    """
    print("   ⏳ Measuring CPU usage (this takes a moment)...")
    
    # First call to initialize CPU measurement
    for proc in psutil.process_iter():
        try:
            proc. cpu_percent()
        except:
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
    
    # Get top 3 processes
    top_3 = processes[:3]
    
    # Generate HTML table rows
    table_rows = ""
    for proc in top_3:
        table_rows += f"""                        <tr>
                            <td>{proc['name']}</td>
                            <td>{round(proc['cpu'], 1)}%</td>
                            <td>{round(proc['memory'], 1)}%</td>
                        </tr>
"""
    
    return {
        'top_processes': table_rows
    }

def analyze_files(directory):
    """
    Analyze files in a directory and count by extension
    Args: 
        directory:  path to the directory to analyze
    Returns:  dict with file counts and percentages
    """
    # Define file extensions to analyze
    extensions = {'. txt':  0, '.py': 0, '.pdf': 0, '.jpg': 0}
    
    # Convert to Path object
    dir_path = Path(directory)
    
    # Check if directory exists
    if not dir_path.exists():
        print(f"   ⚠️  Directory not found: {directory}")
        dir_path = Path(".")
    
    print(f"   📂 Scanning:  {dir_path. absolute()}")
    
    # Count files by extension
    file_count = 0
    try:
        for file in dir_path.rglob('*'):
            if file.is_file():
                file_count += 1
                ext = file.suffix.lower()
                if ext in extensions:
                    extensions[ext] += 1
        
        print(f"   ✅ Total files scanned: {file_count}")
        print(f"   📊 Found:  {sum(extensions.values())} matching files")
        
    except PermissionError as e:
        print(f"   ⚠️  Permission denied: {e}")
    except Exception as e:
        print(f"   ❌ Error:  {e}")
    
    # Calculate total files
    total_files = sum(extensions.values())
    
    # Avoid division by zero
    if total_files == 0:
        # Set default values for demo
        extensions = {'.txt': 10, '.py': 5, '.pdf': 3, '.jpg': 2}
        total_files = 20
        print("   ⚠️  No matching files found.  Using demo values.")
    
    # Calculate percentages
    txt_percent = round((extensions['.txt'] / total_files) * 100, 1)
    py_percent = round((extensions['.py'] / total_files) * 100, 1)
    pdf_percent = round((extensions['.pdf'] / total_files) * 100, 1)
    jpg_percent = round((extensions['.jpg'] / total_files) * 100, 1)
    
    return {
        'analyzed_folder': str(dir_path. absolute()),
        'txt_count': str(extensions['.txt']),
        'txt_percent': str(txt_percent),
        'py_count': str(extensions['.py']),
        'py_percent': str(py_percent),
        'pdf_count':  str(extensions['.pdf']),
        'pdf_percent': str(pdf_percent),
        'jpg_count': str(extensions['.jpg']),
        'jpg_percent': str(jpg_percent),
        'total_files':  str(total_files)
    }

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
        print("Error: template.html not found!")
        return
    
    # Replace all variables in template
    for key, value in data.items():
        placeholder = '{' + key + '}'
        html_content = html_content.replace(placeholder, str(value))
    
    # Write generated HTML file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ index.html generated successfully!")

def main():
    """
    Main function - orchestrates data collection and HTML generation
    """
    print("🖥️  Challenge Triple A - System Monitor")
    print("=" * 50)
    print("Collecting system information...")
    
    # Collect all data
    data = {}
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Collect system information
    print("📊 Collecting system info...")
    data.update(get_system_info())
    
    # Collect CPU information
    print("⚙️  Collecting CPU info...")
    data.update(get_cpu_info())
    
    # Collect memory information
    print("🧠 Collecting memory info...")
    data.update(get_memory_info())
    
    # Collect network information
    print("🌐 Collecting network info...")
    data.update(get_network_info())
    
    # Collect process information
    print("📈 Collecting process info...")
    data.update(get_top_processes())
    
    # Analyze files (you can change the directory here)
    print("📁 Analyzing files...")
    # Smart directory selection based on OS
    if platform.system() == "Windows":
        analyze_directory = os.path.join(os.path.expanduser("~"), "Documents")
    else:
        analyze_directory = os.path.expanduser("~/Documents")
    
    # Fallback to current directory if Documents doesn't exist
    if not os.path.exists(analyze_directory):
        analyze_directory = "."
        print(f"📁 Documents folder not found, analyzing current directory instead.")
    
    data.update(analyze_files(analyze_directory))
    
    # Generate HTML
    print("🎨 Generating HTML dashboard...")
    generate_html(data)
    
    print("=" * 50)
    print("✨ Done! Open index.html in your browser to view the dashboard.")
    print(f"📍 File location: {os.path.abspath('index.html')}")

# Entry point
if __name__ == "__main__":
    main()