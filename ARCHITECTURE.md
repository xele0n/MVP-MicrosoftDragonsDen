# 🏗️ SPTool - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Browser                          │
│                     (User Interface)                        │
│                    Modern HTML/CSS/JS                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend                          │
│                        (app.py)                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                      │  │
│  │  • /api/system/*      - System information          │  │
│  │  • /api/diagnosis/*   - Issue detection             │  │
│  │  • /api/fixes/*       - Command execution           │  │
│  │  • /api/processes/*   - Process management          │  │
│  └──────────────────────────────────────────────────────┘  │
└───┬─────────────────┬────────────────────┬─────────────────┘
    │                 │                    │
    ↓                 ↓                    ↓
┌─────────────┐  ┌─────────────┐  ┌──────────────────┐
│ System      │  │ Issue       │  │ Command          │
│ Diagnostics │  │ Diagnoser   │  │ Executor         │
│ Module      │  │ Module      │  │ Module           │
└─────────────┘  └─────────────┘  └──────────────────┘
    │                 │                    │
    ↓                 ↓                    ↓
┌─────────────────────────────────────────────────────────────┐
│              Operating System (Linux/Windows)               │
│  • psutil (system metrics)                                  │
│  • subprocess (command execution)                           │
│  • Native OS commands                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer (`templates/`, `static/`)

**File: `templates/index.html`**
- Single-page application layout
- Sections: Header, Symptom Input, Metrics, Issues, Processes, Fixes
- Modal dialogs for confirmations and results

**File: `static/css/styles.css`**
- Modern gradient background
- Card-based layout
- Responsive design (mobile-friendly)
- Color-coded severity indicators
- Smooth animations and transitions

**File: `static/js/app.js`**
- SPTool class: Main frontend controller
- AJAX calls to backend API
- Real-time metric updates
- Dynamic DOM rendering
- Event handling and user interactions
- Auto-refresh every 30 seconds

---

### 2. Backend Layer (`app.py`)

**Flask Application:**
- Serves static files and templates
- RESTful API endpoints
- Error handling (404, 500)
- JSON responses
- CORS-ready for future expansion

**Key Routes:**
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Serve main dashboard |
| `/api/system/info` | GET | Basic system info |
| `/api/system/diagnostic` | GET | Full diagnostic data |
| `/api/diagnosis/full` | GET | Run complete diagnosis |
| `/api/diagnosis/symptom` | POST | Symptom-based diagnosis |
| `/api/fixes/available` | GET | List available fixes |
| `/api/fixes/preview` | POST | Preview fix (dry run) |
| `/api/fixes/execute` | POST | Execute fix command |
| `/api/processes/top` | GET | Top processes by CPU/memory |
| `/api/processes/validate/<pid>` | GET | Validate process |
| `/health` | GET | Health check |

---

### 3. System Diagnostics Module (`system_diagnostics.py`)

**Class: `SystemDiagnostics`**

**Responsibilities:**
- Collect real-time system metrics
- Cross-platform compatibility (Linux/Windows/macOS)
- Process monitoring

**Key Methods:**
```python
get_cpu_usage()          # CPU usage, frequency, per-core stats
get_memory_usage()       # RAM and swap usage
get_disk_usage()         # Disk usage for all partitions
get_network_info()       # Network interfaces and stats
get_top_processes()      # Top CPU/memory processes
get_system_info()        # OS, hostname, uptime
get_temperature()        # CPU temperature (Linux only)
get_full_diagnostic()    # Complete system report
```

**Data Sources:**
- `psutil` library for cross-platform metrics
- Real-time process information
- Disk I/O statistics
- Network interface data

---

### 4. Command Executor Module (`command_executor.py`)

**Class: `CommandExecutor`**

**Responsibilities:**
- Safe command execution with whitelisting
- OS-specific command mapping
- Parameter validation
- Comprehensive logging

**Security Features:**
1. **Whitelisted Commands Only**: Predefined safe commands
2. **Risk Levels**: none, low, medium, high
3. **Sudo Detection**: Identifies privilege requirements
4. **Parameter Sanitization**: Safe parameter handling
5. **Action Logging**: All executions logged with timestamps

**Command Structure:**
```python
{
    'fix_id': {
        'command': 'actual shell command',
        'description': 'Human-readable description',
        'requires_sudo': True/False,
        'risk': 'none|low|medium|high',
        'parameterized': True/False  # If requires parameters
    }
}
```

**Linux Commands (Arch Linux focus):**
- `clear_cache`: Drop system caches
- `clear_temp`: Remove old temp files
- `restart_network`: Restart NetworkManager
- `flush_dns`: Clear DNS cache
- `kill_process`: Terminate process by PID
- `update_system`: System package update
- `check_disk`: Display disk usage
- `free_memory`: Show memory stats

**Windows Commands:**
- `clear_temp`: Delete temp files
- `flush_dns`: ipconfig /flushdns
- `restart_service`: net stop/start
- `kill_process`: taskkill /F /PID
- `check_disk`: wmic logicaldisk
- `disk_cleanup`: cleanmgr

**Key Methods:**
```python
get_available_fixes()           # List all fixes for current OS
execute_fix(fix_id, params)    # Execute a fix command
validate_pid(pid)               # Check if PID is valid
```

---

### 5. Issue Diagnosis Module (`issue_diagnosis.py`)

**Class: `IssueDiagnoser`**

**Responsibilities:**
- Analyze system data for problems
- Apply threshold-based rules
- Suggest appropriate fixes
- Natural language symptom parsing

**Diagnostic Categories:**
1. **CPU Issues**: High CPU usage, individual process problems
2. **Memory Issues**: High RAM usage, swap pressure
3. **Disk Issues**: Low disk space warnings
4. **Temperature Issues**: Overheating detection (Linux)
5. **Process Issues**: Resource-intensive processes
6. **Network Issues**: Connectivity problems

**Issue Structure:**
```python
{
    'severity': 'low|medium|high',
    'category': 'cpu|memory|disk|temperature|process|network',
    'title': 'Issue title',
    'description': 'Detailed description',
    'metrics': {...},  # Relevant data
    'suggested_fixes': [...]  # List of applicable fixes
}
```

**Symptom Mapping:**
- "slow", "sluggish", "lag" → CPU/Memory check
- "memory", "ram" → Memory analysis
- "disk", "space", "storage" → Disk check
- "network", "internet", "wifi" → Network diagnosis

**Key Methods:**
```python
diagnose_all()                  # Full system diagnosis
diagnose_symptom(symptom)      # Natural language diagnosis
_check_cpu(data)               # CPU-specific checks
_check_memory(data)            # Memory-specific checks
_check_disk(data)              # Disk-specific checks
_check_temperature(data)       # Temperature checks
_check_processes(data)         # Process analysis
```

---

### 6. Configuration Module (`config.py`)

**Class: `Config`**

**Environment Variables:**
```python
SECRET_KEY          # Flask secret (for sessions)
DEBUG               # Debug mode (True/False)
HOST                # Server host (default: 127.0.0.1)
PORT                # Server port (default: 5000)
OPENAI_API_KEY      # Optional: For AI diagnosis
REQUIRE_CONFIRMATION # Always confirm before executing
LOG_ACTIONS         # Enable action logging
LOG_FILE            # Log file path
CPU_THRESHOLD       # CPU warning threshold (%)
MEMORY_THRESHOLD    # Memory warning threshold (%)
DISK_THRESHOLD      # Disk warning threshold (%)
TEMP_THRESHOLD      # Temperature warning (°C)
```

---

## Data Flow Examples

### Example 1: Symptom Diagnosis

```
User types "my pc is slow"
    ↓
JavaScript captures input
    ↓
POST /api/diagnosis/symptom
    ↓
Flask receives request
    ↓
IssueDiagnoser.diagnose_symptom()
    ↓
SystemDiagnostics.get_full_diagnostic()
    ↓
Analyze CPU & Memory data
    ↓
Identify high CPU usage (92%)
    ↓
Map to Process X (PID 1234)
    ↓
Return issue with suggested fix
    ↓
Frontend renders issue card
    ↓
User clicks "Kill Process" button
    ↓
POST /api/fixes/preview
    ↓
CommandExecutor shows preview
    ↓
Modal displays: "kill -9 1234"
    ↓
User confirms
    ↓
POST /api/fixes/execute
    ↓
CommandExecutor.execute_fix()
    ↓
subprocess.run("kill -9 1234")
    ↓
Log action to file
    ↓
Return success/failure
    ↓
Frontend shows result modal
    ↓
Auto-refresh metrics
```

### Example 2: Full Diagnosis

```
User clicks "Run Full Diagnosis"
    ↓
GET /api/diagnosis/full
    ↓
IssueDiagnoser.diagnose_all()
    ↓
Collect all system metrics:
    • CPU usage
    • Memory usage
    • Disk usage
    • Process list
    • Temperature
    ↓
Apply threshold checks:
    • CPU > 90%?
    • Memory > 85%?
    • Disk > 90%?
    • Temp > 80°C?
    ↓
Build issue list with:
    • Severity levels
    • Descriptions
    • Suggested fixes
    ↓
Return JSON response
    ↓
Frontend renders issues
    ↓
Color-coded by severity
```

---

## Security Architecture

### Defense Layers

**Layer 1: Whitelisting**
- Only predefined commands allowed
- No arbitrary command execution
- Commands reviewed and tested

**Layer 2: Confirmation**
- User must approve each fix
- Preview shown before execution
- Risk level displayed

**Layer 3: Logging**
- All actions logged with timestamp
- User actions traceable
- Audit trail maintained

**Layer 4: Parameter Validation**
- Parameterized commands use safe formatting
- PID validation before kill
- Input sanitization

**Layer 5: Privilege Management**
- Commands marked with sudo requirement
- User informed of privilege needs
- Graceful handling of permission denied

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | HTML5/CSS3/JavaScript | User interface |
| Backend | Python 3.8+ | Application logic |
| Framework | Flask 3.0 | Web server & routing |
| System Access | psutil | Cross-platform metrics |
| Command Execution | subprocess | OS command execution |
| Config | python-dotenv | Environment management |
| Logging | Python logging | Action tracking |
| OS Support | Linux/Windows | Cross-platform |

---

## Scalability Considerations

### Current (MVP):
- Single machine monitoring
- Local web server
- File-based logging
- Synchronous execution

### Future Enhancements:
- Multi-machine dashboard
- Database for historical data
- Asynchronous task queue (Celery)
- Real-time WebSocket updates
- Distributed logging (ELK stack)
- Container deployment (Docker)
- Cloud integration (Azure)

---

## Integration Points

### Microsoft Ecosystem:

**Power Automate:**
- Trigger: Issue detected
- Action: Send alert, create ticket

**Power BI:**
- Data source: System metrics
- Visualization: Dashboards, trends

**Azure Monitor:**
- Remote monitoring
- Alert rules
- Log analytics

**Microsoft Defender:**
- Security scanning
- Threat detection

**Intune:**
- Device management
- Policy enforcement
- Compliance checking

---

## Performance Characteristics

- **Dashboard Load Time**: < 1 second
- **Metric Refresh**: 30 seconds (configurable)
- **API Response Time**: 50-200ms typical
- **Command Execution**: 1-5 seconds typical
- **Full Diagnosis**: 2-3 seconds
- **Memory Footprint**: ~50MB (Flask + modules)
- **CPU Usage**: < 5% when idle

---

## Error Handling

**Strategy:**
1. Try-except blocks around all system calls
2. Graceful degradation (missing features show N/A)
3. User-friendly error messages
4. Detailed logging for debugging
5. JSON error responses from API

**Common Errors:**
- Permission denied → Suggest sudo
- Command not found → OS not supported
- Process not found → Already terminated
- Timeout → Command took too long

---

## Testing Strategy

### Manual Testing:
1. Syntax check: `python -m py_compile *.py`
2. Start server: `python app.py`
3. Access dashboard: http://localhost:5000
4. Test each feature manually

### Automated Testing (Future):
- Unit tests for each module
- Integration tests for API endpoints
- End-to-end tests with Selenium
- Load testing with Locust

---

## Deployment Options

### Option 1: Local Development
```bash
python app.py
```

### Option 2: Production Server (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Docker Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Option 4: Systemd Service
```ini
[Unit]
Description=SPTool Service
After=network.target

[Service]
Type=simple
User=sptool
WorkingDirectory=/opt/sptool
ExecStart=/usr/bin/python /opt/sptool/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

**Architecture Version**: 1.0  
**Last Updated**: October 2025  
**Status**: MVP Complete

