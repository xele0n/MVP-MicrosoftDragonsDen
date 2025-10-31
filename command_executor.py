"""
Secure Command Executor Module
Handles safe execution of system fix commands with whitelisting
"""
import subprocess
import platform
import logging
from datetime import datetime
from config import Config

# Configure logging
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CommandExecutor:
    def __init__(self):
        self.os_type = platform.system()
        self.whitelisted_commands = self._get_whitelisted_commands()
    
    def _get_whitelisted_commands(self):
        """Define whitelisted commands per operating system"""
        
        linux_commands = {
            'clear_cache': {
                'command': 'sync && echo 3 | sudo tee /proc/sys/vm/drop_caches',
                'description': 'Clear system cache',
                'requires_sudo': True,
                'risk': 'low'
            },
            'clear_temp': {
                'command': 'find /tmp -type f -atime +7 -delete',
                'description': 'Clear temporary files older than 7 days',
                'requires_sudo': False,
                'risk': 'low'
            },
            'restart_network': {
                'command': 'sudo systemctl restart NetworkManager',
                'description': 'Restart network manager',
                'requires_sudo': True,
                'risk': 'medium'
            },
            'flush_dns': {
                'command': 'sudo systemd-resolve --flush-caches',
                'description': 'Flush DNS cache',
                'requires_sudo': True,
                'risk': 'low'
            },
            'kill_process': {
                'command': 'kill -9 {pid}',
                'description': 'Kill a specific process by PID',
                'requires_sudo': False,
                'risk': 'high',
                'parameterized': True
            },
            'update_system': {
                'command': 'sudo pacman -Syu --noconfirm',
                'description': 'Update system packages (Arch Linux)',
                'requires_sudo': True,
                'risk': 'medium'
            },
            'check_disk': {
                'command': 'df -h',
                'description': 'Check disk usage',
                'requires_sudo': False,
                'risk': 'none'
            },
            'free_memory': {
                'command': 'free -h',
                'description': 'Display memory usage',
                'requires_sudo': False,
                'risk': 'none'
            }
        }
        
        windows_commands = {
            'clear_temp': {
                'command': 'del /q /f /s %TEMP%\\*',
                'description': 'Clear temporary files',
                'requires_sudo': False,
                'risk': 'low'
            },
            'flush_dns': {
                'command': 'ipconfig /flushdns',
                'description': 'Flush DNS cache',
                'requires_sudo': True,
                'risk': 'low'
            },
            'restart_service': {
                'command': 'net stop {service} && net start {service}',
                'description': 'Restart a Windows service',
                'requires_sudo': True,
                'risk': 'medium',
                'parameterized': True
            },
            'kill_process': {
                'command': 'taskkill /F /PID {pid}',
                'description': 'Kill a specific process by PID',
                'requires_sudo': True,
                'risk': 'high',
                'parameterized': True
            },
            'check_disk': {
                'command': 'wmic logicaldisk get size,freespace,caption',
                'description': 'Check disk space',
                'requires_sudo': False,
                'risk': 'none'
            },
            'disk_cleanup': {
                'command': 'cleanmgr /sagerun:1',
                'description': 'Run disk cleanup utility',
                'requires_sudo': True,
                'risk': 'low'
            }
        }
        
        if self.os_type == 'Linux':
            return linux_commands
        elif self.os_type == 'Windows':
            return windows_commands
        else:
            return {}
    
    def get_available_fixes(self):
        """Return list of available fixes for current OS"""
        fixes = []
        for cmd_id, cmd_info in self.whitelisted_commands.items():
            fixes.append({
                'id': cmd_id,
                'description': cmd_info['description'],
                'requires_sudo': cmd_info['requires_sudo'],
                'risk': cmd_info['risk'],
                'parameterized': cmd_info.get('parameterized', False)
            })
        return fixes
    
    def execute_fix(self, fix_id, params=None, dry_run=False):
        """
        Execute a whitelisted fix command
        
        Args:
            fix_id: ID of the fix to execute
            params: Dictionary of parameters for parameterized commands
            dry_run: If True, don't actually execute, just return what would be run
        
        Returns:
            Dictionary with execution results
        """
        if fix_id not in self.whitelisted_commands:
            return {
                'success': False,
                'error': f'Command "{fix_id}" is not whitelisted',
                'timestamp': datetime.now().isoformat()
            }
        
        cmd_info = self.whitelisted_commands[fix_id]
        command = cmd_info['command']
        
        # Handle parameterized commands
        if cmd_info.get('parameterized', False):
            if not params:
                return {
                    'success': False,
                    'error': 'This command requires parameters',
                    'timestamp': datetime.now().isoformat()
                }
            try:
                command = command.format(**params)
            except KeyError as e:
                return {
                    'success': False,
                    'error': f'Missing required parameter: {e}',
                    'timestamp': datetime.now().isoformat()
                }
        
        # Log the attempted command
        log_msg = f"Fix attempted: {fix_id} | Command: {command} | Params: {params} | Dry run: {dry_run}"
        logging.info(log_msg)
        
        if dry_run:
            return {
                'success': True,
                'dry_run': True,
                'command': command,
                'description': cmd_info['description'],
                'requires_sudo': cmd_info['requires_sudo'],
                'risk': cmd_info['risk'],
                'timestamp': datetime.now().isoformat()
            }
        
        # Execute the command
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            log_result = f"Fix executed: {fix_id} | Success: {success} | Return code: {result.returncode}"
            if success:
                logging.info(log_result)
            else:
                logging.error(log_result + f" | Error: {result.stderr}")
            
            return {
                'success': success,
                'fix_id': fix_id,
                'description': cmd_info['description'],
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            logging.error(f"Fix timed out: {fix_id}")
            return {
                'success': False,
                'error': 'Command execution timed out',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Fix failed: {fix_id} | Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def validate_pid(self, pid):
        """Validate that a PID exists and can be killed"""
        try:
            import psutil
            proc = psutil.Process(int(pid))
            return {
                'valid': True,
                'name': proc.name(),
                'cpu_percent': proc.cpu_percent(),
                'memory_percent': proc.memory_percent()
            }
        except (psutil.NoSuchProcess, ValueError):
            return {'valid': False, 'error': 'Process not found'}
        except psutil.AccessDenied:
            return {'valid': False, 'error': 'Access denied'}

