# System Management and API   
import os
import requests
import socket
import cpuinfo
import psutil
import GPUtil
import platform
from getmac import get_mac_address
from dotenv import load_dotenv

load_dotenv()

# Bot info and chat id 
API_TOKEN = os.getenv('API_TOKEN') 
CHAT_ID  = os.getenv('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

# Get MAC address
def get_mac() -> str: 
    mac = get_mac_address()
    return mac

# Get System Information
class SystemInfo:
    def __init__(self):
        self.cpu_info = self.get_cpu_info()
        self.ram_info = self.get_ram_info()
        self.disk_info = self.get_disk_info()  
        self.gpu_info = self.get_gpu_info()    
        self.os_info = self.get_os_info()      
    
    def get_cpu_info(self) -> str:
        '''Retrieve CPU information'''
        cpu = cpuinfo.get_cpu_info()
        return cpu.get('brand_raw', "Unable to retrieve CPU info")
    
    def get_ram_info(self) -> str:
        '''Retrieve RAM information'''
        ram_bytes = psutil.virtual_memory().total
        ram_gb = ram_bytes / (1024 ** 3)                # Convert bytes ->  GB 
        return f'{ram_gb:.2f} GB'
    
    def get_disk_info(self) -> list: 
        '''Retrieve disk information'''
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions: 
            usage = psutil.disk_usage(partition.mountpoint) 
            disk_type = 'SSD' if 'ssd' in partition.opts else "HDD"
            disk_size = usage.total / (1024 ** 3) 
            disk_info.append(f'{disk_type}: {disk_size:.2f} GB ({partition.mountpoint})')

        if not disk_info: 
            disk_info.append('No SSD or HDD detected')
        
        return disk_info
    
    def get_gpu_info(self) -> list:
        '''Retrieve GPU information'''
        gpus = GPUtil.getGPUs()
        if gpus:
            return [f"{gpu.name} - {gpu.memoryTotal:.2f} MB" for gpu in gpus]
        return ["No GPU detected"]

    def get_os_info(self) -> str:
        '''Retrieve operating system information'''
        return f"{platform.system()} {platform.release()}"
    
    def display_info(self) -> str:
        '''Display all system information'''
        system_info = (
            f"CPU: {self.cpu_info}\n"
            f"RAM: {self.ram_info}\n"
            "Disks:\n" + "\n".join(self.disk_info) + "\n" +
            "GPU(s):\n" + "\n".join(self.gpu_info) + "\n"
        )
        return system_info
        
class IPAddress:
    @staticmethod
    def get_local_ip() -> str:
        """Return the local IP address of the host."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    @staticmethod
    def get_public_ip() -> str:
        """Return the public IP address of the host."""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get('ip', 'No IP found')
        except requests.RequestException:
            return 'Unable to retrieve public IP address.'

    @staticmethod
    def get_location(ip: str) -> str:
        """Return the geographical location of the given IP address."""
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}')
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            if data.get('status') == 'success':
                return f"{data['city']}, {data['regionName']}, {data['country']}"
            return 'Unable to determine location'
        except requests.RequestException as e:
            return f"Error fetching location: {str(e)}"

if __name__ == '__main__':
    # Display MAC, IP and Location 
    mac = get_mac()
    local_ip = IPAddress.get_local_ip() 
    public_ip = IPAddress.get_public_ip()
    location = IPAddress.get_location(public_ip)
    
    print(f'Mac Address: {mac}')
    print(f'Local IP: {local_ip}')
    print(f'Public IP: {public_ip}')
    print(f'Location: {location}')

    # Display system information
    system = SystemInfo()
    system_info = system.display_info()
    print(system_info)