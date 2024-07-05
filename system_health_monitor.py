"""
    Author: Siddharth Gupta
    email: gsiddharth47@gmail.com
    OS: Ubuntu 24.04
"""

import psutil

def get_cpu_usage():
    cpu_percentage = psutil.cpu_percent(interval=1)
    return cpu_percentage
    
def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    return memory_usage

def get_disk_space():
    disk_usage_info = psutil.disk_usage('/')
    return disk_usage_info.percent
    
def check_all_processes():
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        cpu_percentage = process.info['cpu_percent']
        memory_percentage = process.info['memory_percent']
        process_name = process.info['name']
        if(cpu_percentage > 0.5):
            print(f"ALERT:[{process_name}] exceeds the CPU usage threshold of 0.5%")
        if(memory_percentage > 1.0):
            print(f"ALERT:[{process_name}] exceeds the memory usage threshold of 1%")
        
def main():
    
    print(f"Total CPU Usage: {get_cpu_usage()}%")
    print(f"Total Memory Usage: {get_memory_usage()}%")
    print(f"Total Disk Usage: {get_disk_space()}% ")
    
    if(get_cpu_usage() > 2.0):
        print(f"ALERT: Total CPU Usage exceeds threshold of 2%: {get_cpu_usage()}%")
    if(get_memory_usage() > 50.0):
        print(f"ALERT: Total Memory Usage exceeds threshold of 50%: {get_memory_usage()}%")
    if(get_disk_space() > 1.0):
        print(f"ALERT: Total Disk Usage exceeds threshold of 1%: {get_memory_usage()}%")
    check_all_processes()
  
    
    
if __name__ == '__main__':
    main()