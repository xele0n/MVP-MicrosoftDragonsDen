# 🚀 SPTool - Quick Start Guide

## Installation & Running (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
Navigate to: **http://127.0.0.1:5000**

---

## Alternative: Use Setup Script

```bash
chmod +x setup.sh
./setup.sh
python app.py
```

---

## Quick Demo Workflow

### 1️⃣ Test Symptom Diagnosis
1. Open http://127.0.0.1:5000
2. Type in symptom box: **"my pc is slow"**
3. Click **"Diagnose"**
4. Review detected issues

### 2️⃣ Run Full System Scan
1. Click **"Run Full Diagnosis"** button (top right)
2. Wait for analysis to complete
3. Review all detected issues with severity levels

### 3️⃣ Execute a Safe Fix
1. Scroll to **"Available System Fixes"**
2. Click **"Execute Fix"** on "check_disk" (safe, read-only)
3. Review the command preview
4. Click **"Execute"**
5. View results

### 4️⃣ Monitor Processes
1. Scroll to **"Top Processes"**
2. Switch between CPU and Memory tabs
3. Identify resource-intensive processes
4. (Optional) Click **"Kill"** to terminate a process

### 5️⃣ Test Process Management
1. Find a high CPU process in the list
2. Click **"Kill"** button
3. Confirm the action
4. Process will be terminated
5. List refreshes automatically

---

## Common Use Cases

### 🐌 "My Computer is Slow"
```
Symptom: my pc is slow
↓
SPTool diagnoses:
- High CPU usage (92%)
- Process "chrome" consuming 45% CPU
↓
Suggested fix: Kill process or clear cache
↓
One-click fix executed
```

### 💾 "Running Out of Memory"
```
Symptom: high memory usage
↓
SPTool diagnoses:
- Memory at 89%
- 5 heavy processes identified
↓
Suggested fix: Clear cache, kill processes
↓
Fix executed, memory freed
```

### 💿 "Low Disk Space"
```
Symptom: low disk space
↓
SPTool diagnoses:
- Disk usage at 94%
- /tmp directory analysis
↓
Suggested fix: Clear temp files
↓
Old temp files removed automatically
```

### 🌐 "Network Not Working"
```
Symptom: network problems
↓
SPTool diagnoses:
- Network connectivity issues
↓
Suggested fixes:
1. Flush DNS cache
2. Restart network manager
↓
Both executed sequentially
```

---

## API Testing (Advanced)

Test endpoints using curl:

```bash
# Get system info
curl http://127.0.0.1:5000/api/system/info | jq

# Get full diagnostic
curl http://127.0.0.1:5000/api/system/diagnostic | jq

# Run full diagnosis
curl http://127.0.0.1:5000/api/diagnosis/full | jq

# Diagnose symptom
curl -X POST http://127.0.0.1:5000/api/diagnosis/symptom \
  -H "Content-Type: application/json" \
  -d '{"symptom": "my pc is slow"}' | jq

# List available fixes
curl http://127.0.0.1:5000/api/fixes/available | jq

# Preview a fix (dry run)
curl -X POST http://127.0.0.1:5000/api/fixes/preview \
  -H "Content-Type: application/json" \
  -d '{"fix_id": "check_disk"}' | jq

# Get top processes
curl http://127.0.0.1:5000/api/processes/top | jq
```

---

## Safety Tips

✅ **Safe to Try:**
- `check_disk` - Just displays disk usage
- `free_memory` - Just displays memory info
- Viewing diagnostics and metrics

⚠️ **Use with Caution:**
- `clear_cache` - Clears system cache (reversible)
- `clear_temp` - Deletes old temp files
- `flush_dns` - Clears DNS cache

🚨 **Requires Confirmation:**
- `kill_process` - Terminates a running process
- `restart_network` - Restarts network services
- Any fix marked as "high risk"

---

## Troubleshooting

### Port 5000 Already in Use
Edit `.env` and change:
```env
PORT=8080
```

### Permission Denied
Some fixes need sudo:
```bash
sudo python app.py
```

### Module Not Found
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Can't Connect to Server
Check if it's running:
```bash
curl http://127.0.0.1:5000/health
```

---

## Demo for Presentation

**5-Minute Live Demo Script:**

1. **[00:00-00:30]** Open browser, show dashboard
2. **[00:30-01:30]** Type "my pc is slow", click diagnose
3. **[01:30-02:30]** Show detected issues and metrics
4. **[02:30-03:30]** Execute a safe fix (check_disk)
5. **[03:30-04:30]** Show process monitoring
6. **[04:30-05:00]** Review action logs and security features

**Key Points to Highlight:**
- ✅ Real system interaction (not simulation)
- ✅ Command-line execution with safety
- ✅ Modern, user-friendly interface
- ✅ Comprehensive logging
- ✅ Cross-platform ready
- ✅ Microsoft integration ready

---

## Next Steps

- [ ] Add more whitelisted commands
- [ ] Integrate with OpenAI API for AI diagnosis
- [ ] Set up scheduled scans
- [ ] Connect to Power Automate
- [ ] Add email/SMS alerts
- [ ] Multi-machine dashboard

---

**Happy Troubleshooting! 🔧**

