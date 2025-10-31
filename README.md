# 🔧 SPTool - System Performance Troubleshooting Tool

A powerful, web-based system diagnostics and troubleshooting tool that helps you identify and fix performance issues on your Linux (or Windows) machine.

![SPTool Dashboard](https://img.shields.io/badge/Status-MVP-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)

## 🌟 Features

### 🔍 **Smart Diagnostics**
- Real-time system monitoring (CPU, Memory, Disk, Network)
- Automatic issue detection based on configurable thresholds
- Symptom-based diagnosis ("My PC is slow", "Network problems", etc.)
- Process monitoring with top CPU/Memory consumers

### 🛠️ **Automated Fixes**
- Whitelisted command execution for safety
- One-click system fixes:
  - Clear system cache
  - Clear temporary files
  - Flush DNS cache
  - Restart network services
  - Kill resource-intensive processes
  - And more...

### 🔐 **Security First**
- Command whitelisting - only safe, predefined commands can be executed
- Confirmation required before executing any fix
- Comprehensive action logging
- Risk level indicators for each fix
- Sudo/admin privilege management

### 🎨 **Modern UI**
- Beautiful, responsive web interface
- Real-time metrics visualization
- Color-coded severity levels
- Interactive process management
- Mobile-friendly design

## 📋 Requirements

- Python 3.8 or higher
- Linux (Arch, Ubuntu, Debian, etc.) or Windows
- Sudo/admin privileges for certain fixes

## 🚀 Quick Start

### 1. Clone or Download

```bash
cd /path/to/MVP-MicrosoftDragonsDen
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure (Optional)

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
nano .env  # Edit configuration
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` by default.

### 5. Open in Browser

Navigate to: **http://127.0.0.1:5000**

## 📖 Usage Guide

### Dashboard Overview

1. **Symptom Input**: Type what's wrong (e.g., "My PC is slow") and click "Diagnose"
2. **Quick Symptoms**: Click preset symptom buttons for instant diagnosis
3. **System Metrics**: View real-time CPU, Memory, and Disk usage
4. **Detected Issues**: See automatically identified problems with suggested fixes
5. **Top Processes**: Monitor and manage resource-intensive processes
6. **Available Fixes**: Browse and execute system optimization commands

### Running a Diagnosis

**Method 1: Symptom-Based**
1. Enter your problem in the symptom input box
2. Click "Diagnose" or press Enter
3. Review identified issues and suggested fixes

**Method 2: Full System Scan**
1. Click "Run Full Diagnosis" button
2. Wait for comprehensive system analysis
3. Review all detected issues

### Executing Fixes

1. Click on any "Execute Fix" button
2. Review the command preview and risk level
3. Confirm execution
4. View results and system logs

### Killing Processes

1. Navigate to "Top Processes" section
2. Switch between CPU and Memory tabs
3. Click "Kill" next to any process
4. Confirm the action

## 🏗️ Architecture

```
SPTool/
├── app.py                  # Flask application & API endpoints
├── config.py               # Configuration settings
├── system_diagnostics.py   # System data collection (cross-platform)
├── command_executor.py     # Secure command execution with whitelisting
├── issue_diagnosis.py      # Issue detection and diagnosis logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── templates/
│   └── index.html         # Web UI template
├── static/
│   ├── css/
│   │   └── styles.css     # Modern UI styling
│   └── js/
│       └── app.js         # Frontend JavaScript logic
└── sptool_actions.log     # Action log file (created on first run)
```

## 🔧 Configuration

Edit `.env` to customize:

```env
# Server Settings
HOST=127.0.0.1
PORT=5000
DEBUG=True

# Security
REQUIRE_CONFIRMATION=True
LOG_ACTIONS=True

# Thresholds
CPU_THRESHOLD=90        # % CPU usage to trigger warning
MEMORY_THRESHOLD=85     # % Memory usage to trigger warning
DISK_THRESHOLD=90       # % Disk usage to trigger warning
TEMP_THRESHOLD=80       # °C CPU temperature threshold
```

## 🛡️ Security Features

### Command Whitelisting
Only predefined, safe commands can be executed. Each command includes:
- Risk level (none, low, medium, high)
- Required permissions
- Description and purpose

### Action Logging
All executed commands are logged with:
- Timestamp
- Command executed
- Parameters used
- Success/failure status
- Output/errors

View logs in `sptool_actions.log`

### Confirmation Required
Every fix requires user confirmation before execution, preventing accidental system changes.

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system/info` | GET | Get basic system information |
| `/api/system/diagnostic` | GET | Get full system diagnostic data |
| `/api/diagnosis/full` | GET | Run complete diagnosis with issue detection |
| `/api/diagnosis/symptom` | POST | Diagnose based on user symptom |
| `/api/fixes/available` | GET | List all available fixes |
| `/api/fixes/preview` | POST | Preview a fix without executing |
| `/api/fixes/execute` | POST | Execute a fix command |
| `/api/processes/top` | GET | Get top CPU/Memory processes |
| `/api/processes/validate/<pid>` | GET | Validate process ID |

## 🎯 Use Cases

### 1. Performance Troubleshooting
User reports: "My computer is running slow"
- SPTool diagnoses: High CPU usage from process X
- Suggests: Kill process or clear cache
- User executes fix with one click

### 2. Disk Space Management
System alert: Low disk space
- SPTool identifies: /tmp directory full
- Suggests: Clear temporary files
- Automatically cleans old files

### 3. Network Issues
User reports: "Internet not working"
- SPTool suggests: Flush DNS cache, restart network manager
- Executes both fixes sequentially
- Monitors network status

### 4. Memory Optimization
System running out of RAM
- Identifies memory-hungry processes
- Suggests cache clearing
- Offers to kill unnecessary processes

## 🔄 Cross-Platform Support

### Linux (Current Focus)
- Full support for Arch Linux, Ubuntu, Debian, Fedora
- Uses: `systemctl`, `pacman`/`apt`, native commands

### Windows (Extendable)
- Uses: `wmic`, `net`, `ipconfig`, `taskkill`
- Requires admin privileges for most fixes

### Adding New Commands

Edit `command_executor.py`:

```python
'new_fix_name': {
    'command': 'your command here',
    'description': 'What this fix does',
    'requires_sudo': False,
    'risk': 'low',
    'parameterized': False
}
```

## 🚨 Troubleshooting

### Permission Denied Errors
Some fixes require sudo. Run:
```bash
sudo python app.py
```

### Port Already in Use
Change port in `.env`:
```env
PORT=8080
```

### Module Not Found
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## 🤝 Microsoft Integration Opportunities

This tool can integrate with:

- **Power Automate**: Trigger flows on system events
- **Power BI**: Visualize system health trends
- **Azure Monitor**: Remote system monitoring
- **Microsoft Defender**: Security scanning integration
- **Intune**: Enterprise device management

## 📊 Future Enhancements

- [ ] AI-powered diagnosis with ChatGPT API
- [ ] Scheduled automatic maintenance
- [ ] Email/SMS alerts for critical issues
- [ ] Historical data tracking and trends
- [ ] Multi-machine management dashboard
- [ ] Custom fix command builder
- [ ] Windows Task Scheduler integration
- [ ] Docker containerization

## 📝 License

This is an MVP/prototype tool. Use at your own risk. Always review commands before execution.

## 🙏 Acknowledgments

Built for Microsoft Dragons Den MVP presentation.

---

**⚠️ Important**: This tool executes system commands. Always review what will be executed before confirming. Keep your system backed up.

**🎓 Educational Purpose**: This MVP demonstrates system diagnostics and automation. For production use, implement additional security measures and testing.

---

Made with ❤️ for better system performance
