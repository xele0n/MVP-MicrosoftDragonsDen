"""
Issue Diagnosis Module
Analyzes system data and identifies problems with suggested fixes
"""
from config import Config
from system_diagnostics import SystemDiagnostics

class IssueDiagnoser:
    def __init__(self):
        self.diagnostics = SystemDiagnostics()
        self.config = Config()
    
    def diagnose_all(self):
        """Run full system diagnosis and return identified issues"""
        issues = []
        
        # Get system data
        data = self.diagnostics.get_full_diagnostic()
        
        # Check CPU issues
        cpu_issues = self._check_cpu(data.get('cpu', {}))
        issues.extend(cpu_issues)
        
        # Check memory issues
        memory_issues = self._check_memory(data.get('memory', {}))
        issues.extend(memory_issues)
        
        # Check disk issues
        disk_issues = self._check_disk(data.get('disk', []))
        issues.extend(disk_issues)
        
        # Check temperature issues
        temp_issues = self._check_temperature(data.get('temperature', {}))
        issues.extend(temp_issues)
        
        # Check process issues
        process_issues = self._check_processes(data.get('processes', {}))
        issues.extend(process_issues)
        
        return {
            'total_issues': len(issues),
            'issues': issues,
            'system_data': data
        }
    
    def _check_cpu(self, cpu_data):
        """Check for CPU-related issues"""
        issues = []
        
        if 'error' in cpu_data:
            return issues
        
        cpu_usage = cpu_data.get('usage', 0)
        
        if cpu_usage > self.config.CPU_THRESHOLD:
            issues.append({
                'severity': 'high' if cpu_usage > 95 else 'medium',
                'category': 'cpu',
                'title': 'High CPU Usage',
                'description': f'CPU usage is at {cpu_usage}%, which may cause performance issues',
                'metrics': {'cpu_usage': cpu_usage},
                'suggested_fixes': [
                    {
                        'fix_id': 'kill_process',
                        'description': 'Kill resource-intensive processes',
                        'requires_params': True
                    }
                ]
            })
        
        return issues
    
    def _check_memory(self, memory_data):
        """Check for memory-related issues"""
        issues = []
        
        if 'error' in memory_data:
            return issues
        
        memory_percent = memory_data.get('percent', 0)
        swap_percent = memory_data.get('swap_percent', 0)
        
        if memory_percent > self.config.MEMORY_THRESHOLD:
            issues.append({
                'severity': 'high' if memory_percent > 95 else 'medium',
                'category': 'memory',
                'title': 'High Memory Usage',
                'description': f'Memory usage is at {memory_percent}%, system may slow down',
                'metrics': {
                    'memory_percent': memory_percent,
                    'memory_used_gb': memory_data.get('used', 0),
                    'memory_total_gb': memory_data.get('total', 0)
                },
                'suggested_fixes': [
                    {
                        'fix_id': 'clear_cache',
                        'description': 'Clear system cache to free memory',
                        'requires_params': False
                    },
                    {
                        'fix_id': 'kill_process',
                        'description': 'Kill memory-intensive processes',
                        'requires_params': True
                    }
                ]
            })
        
        if swap_percent > 50:
            issues.append({
                'severity': 'medium',
                'category': 'memory',
                'title': 'High Swap Usage',
                'description': f'Swap usage is at {swap_percent}%, indicating memory pressure',
                'metrics': {'swap_percent': swap_percent},
                'suggested_fixes': [
                    {
                        'fix_id': 'clear_cache',
                        'description': 'Clear system cache',
                        'requires_params': False
                    }
                ]
            })
        
        return issues
    
    def _check_disk(self, disk_data):
        """Check for disk-related issues"""
        issues = []
        
        if isinstance(disk_data, dict) and 'error' in disk_data:
            return issues
        
        for disk in disk_data:
            disk_percent = disk.get('percent', 0)
            
            if disk_percent > self.config.DISK_THRESHOLD:
                issues.append({
                    'severity': 'high' if disk_percent > 95 else 'medium',
                    'category': 'disk',
                    'title': f'Low Disk Space on {disk.get("mountpoint", "Unknown")}',
                    'description': f'Disk usage is at {disk_percent}% ({disk.get("free", 0)} GB free)',
                    'metrics': {
                        'disk_percent': disk_percent,
                        'disk_free_gb': disk.get('free', 0),
                        'mountpoint': disk.get('mountpoint', 'Unknown')
                    },
                    'suggested_fixes': [
                        {
                            'fix_id': 'clear_temp',
                            'description': 'Clear temporary files',
                            'requires_params': False
                        }
                    ]
                })
        
        return issues
    
    def _check_temperature(self, temp_data):
        """Check for temperature-related issues"""
        issues = []
        
        if not temp_data.get('available', False):
            return issues
        
        temps = temp_data.get('temperatures', {})
        
        for sensor_name, readings in temps.items():
            for reading in readings:
                temp = reading.get('current', 0)
                if temp > self.config.TEMP_THRESHOLD:
                    issues.append({
                        'severity': 'high' if temp > 90 else 'medium',
                        'category': 'temperature',
                        'title': f'High Temperature: {sensor_name}',
                        'description': f'{reading.get("label", sensor_name)} is at {temp}°C',
                        'metrics': {'temperature': temp, 'sensor': sensor_name},
                        'suggested_fixes': [
                            {
                                'fix_id': 'kill_process',
                                'description': 'Kill CPU-intensive processes to reduce heat',
                                'requires_params': True
                            }
                        ]
                    })
        
        return issues
    
    def _check_processes(self, process_data):
        """Check for problematic processes"""
        issues = []
        
        if 'error' in process_data:
            return issues
        
        top_cpu = process_data.get('top_cpu', [])
        
        # Check if any single process is consuming excessive CPU
        for proc in top_cpu[:3]:  # Check top 3 CPU consumers
            cpu_percent = proc.get('cpu_percent', 0)
            if cpu_percent > 50:  # Single process using > 50% CPU
                issues.append({
                    'severity': 'medium',
                    'category': 'process',
                    'title': f'High CPU Process: {proc.get("name", "Unknown")}',
                    'description': f'Process {proc.get("name")} (PID: {proc.get("pid")}) is using {cpu_percent}% CPU',
                    'metrics': {
                        'process_name': proc.get('name'),
                        'pid': proc.get('pid'),
                        'cpu_percent': cpu_percent
                    },
                    'suggested_fixes': [
                        {
                            'fix_id': 'kill_process',
                            'description': f'Kill process {proc.get("name")} (PID: {proc.get("pid")})',
                            'requires_params': True,
                            'default_params': {'pid': proc.get('pid')}
                        }
                    ]
                })
        
        return issues
    
    def diagnose_symptom(self, symptom):
        """Diagnose based on user-described symptom"""
        symptom_lower = symptom.lower()
        
        # Get current system data
        data = self.diagnostics.get_full_diagnostic()
        
        # Map symptoms to checks
        if any(word in symptom_lower for word in ['slow', 'sluggish', 'lag', 'performance']):
            return {
                'symptom': symptom,
                'likely_causes': self._check_cpu(data['cpu']) + self._check_memory(data['memory']),
                'system_data': data
            }
        
        elif any(word in symptom_lower for word in ['memory', 'ram', 'out of memory']):
            return {
                'symptom': symptom,
                'likely_causes': self._check_memory(data['memory']),
                'system_data': data
            }
        
        elif any(word in symptom_lower for word in ['disk', 'space', 'storage', 'full']):
            return {
                'symptom': symptom,
                'likely_causes': self._check_disk(data['disk']),
                'system_data': data
            }
        
        elif any(word in symptom_lower for word in ['network', 'internet', 'connection', 'wifi']):
            return {
                'symptom': symptom,
                'likely_causes': [{
                    'severity': 'medium',
                    'category': 'network',
                    'title': 'Network Issues',
                    'description': 'Network connectivity problems detected',
                    'suggested_fixes': [
                        {
                            'fix_id': 'flush_dns',
                            'description': 'Flush DNS cache',
                            'requires_params': False
                        },
                        {
                            'fix_id': 'restart_network',
                            'description': 'Restart network manager',
                            'requires_params': False
                        }
                    ]
                }],
                'system_data': data
            }
        
        else:
            # General diagnosis
            return self.diagnose_all()

