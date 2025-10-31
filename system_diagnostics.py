"""
System Diagnostics Module
Collects system information across different operating systems
"""
import subprocess
import platform
import psutil
from datetime import datetime

class SystemDiagnostics:
    def __init__(self):
        self.os_type = platform.system()  # 'Linux', 'Windows', 'Darwin' (macOS)
        
    def get_cpu_usage(self):
        """Get current CPU usage percentage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'usage': cpu_percent,
                'count': cpu_count,
                'frequency': cpu_freq.current if cpu_freq else 'N/A',
                'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_memory_usage(self):
        """Get memory usage statistics"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': self._bytes_to_gb(mem.total),
                'available': self._bytes_to_gb(mem.available),
                'used': self._bytes_to_gb(mem.used),
                'percent': mem.percent,
                'swap_total': self._bytes_to_gb(swap.total),
                'swap_used': self._bytes_to_gb(swap.used),
                'swap_percent': swap.percent
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_disk_usage(self):
        """Get disk usage for all partitions"""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': self._bytes_to_gb(usage.total),
                        'used': self._bytes_to_gb(usage.used),
                        'free': self._bytes_to_gb(usage.free),
                        'percent': usage.percent
                    })
                except PermissionError:
                    continue
            return disks
        except Exception as e:
            return {'error': str(e)}
    
    def get_network_info(self):
        """Get network interfaces and statistics"""
        try:
            net_io = psutil.net_io_counters()
            interfaces = psutil.net_if_addrs()
            
            return {
                'bytes_sent': self._bytes_to_gb(net_io.bytes_sent),
                'bytes_recv': self._bytes_to_gb(net_io.bytes_recv),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'interfaces': {name: [addr.address for addr in addrs] 
                              for name, addrs in interfaces.items()}
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_top_processes(self, limit=10):
        """Get top CPU and memory consuming processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:limit]
            # Sort by memory usage
            processes_by_mem = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:limit]
            
            return {
                'top_cpu': processes_by_cpu,
                'top_memory': processes_by_mem
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_system_info(self):
        """Get general system information"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            return {
                'os': self.os_type,
                'os_version': platform.platform(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
                'uptime_hours': (datetime.now() - boot_time).total_seconds() / 3600
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_temperature(self):
        """Get CPU temperature (Linux only, requires sensors)"""
        if self.os_type != 'Linux':
            return {'available': False}
        
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return {'available': False}
            
            temp_data = {}
            for name, entries in temps.items():
                temp_data[name] = [{'label': entry.label, 'current': entry.current} 
                                  for entry in entries]
            return {'available': True, 'temperatures': temp_data}
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def run_custom_command(self, command):
        """Run a custom diagnostic command (OS-specific)"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_full_diagnostic(self):
        """Get complete system diagnostic report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'cpu': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage(),
            'network': self.get_network_info(),
            'processes': self.get_top_processes(),
            'temperature': self.get_temperature()
        }
    
    @staticmethod
    def _bytes_to_gb(bytes_value):
        """Convert bytes to gigabytes"""
        return round(bytes_value / (1024 ** 3), 2)

