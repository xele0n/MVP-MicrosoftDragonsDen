// SPTool Frontend Application
class SPTool {
    constructor() {
        this.currentTab = 'cpu';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadSystemInfo();
        this.loadDiagnostics();
        this.loadProcesses();
        this.loadAvailableFixes();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            this.loadDiagnostics();
            this.loadProcesses();
        }, 30000);
    }

    bindEvents() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadSystemInfo();
            this.loadDiagnostics();
            this.loadProcesses();
            this.showMessage('Refreshing...', 'info');
        });

        // Full diagnosis button
        document.getElementById('diagnosisBtn').addEventListener('click', () => {
            this.runFullDiagnosis();
        });

        // Symptom input
        document.getElementById('diagnoseSymptomBtn').addEventListener('click', () => {
            this.diagnoseSymptom();
        });

        document.getElementById('symptomInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.diagnoseSymptom();
            }
        });

        // Quick symptom tags
        document.querySelectorAll('.symptom-tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const symptom = tag.dataset.symptom;
                document.getElementById('symptomInput').value = symptom;
                this.diagnoseSymptom();
            });
        });

        // Process tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                this.currentTab = tab.dataset.tab;
                this.renderProcesses();
            });
        });

        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModals();
            });
        });

        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModals();
                }
            });
        });

        // Cancel button
        document.getElementById('cancelBtn').addEventListener('click', () => {
            this.closeModals();
        });
    }

    async loadSystemInfo() {
        try {
            const response = await fetch('/api/system/info');
            const data = await response.json();
            
            if (data.success) {
                this.renderSystemInfo(data.data);
            }
        } catch (error) {
            console.error('Error loading system info:', error);
        }
    }

    async loadDiagnostics() {
        try {
            const response = await fetch('/api/system/diagnostic');
            const data = await response.json();
            
            if (data.success) {
                this.diagnosticData = data.data;
                this.renderMetrics(data.data);
            }
        } catch (error) {
            console.error('Error loading diagnostics:', error);
        }
    }

    async loadProcesses() {
        try {
            const response = await fetch('/api/processes/top');
            const data = await response.json();
            
            if (data.success) {
                this.processesData = data.data;
                this.renderProcesses();
            }
        } catch (error) {
            console.error('Error loading processes:', error);
        }
    }

    async loadAvailableFixes() {
        try {
            const response = await fetch('/api/fixes/available');
            const data = await response.json();
            
            if (data.success) {
                this.renderAvailableFixes(data.data);
            }
        } catch (error) {
            console.error('Error loading fixes:', error);
        }
    }

    async runFullDiagnosis() {
        const btn = document.getElementById('diagnosisBtn');
        btn.disabled = true;
        btn.innerHTML = '<span class="icon">⏳</span> Diagnosing...';
        
        try {
            const response = await fetch('/api/diagnosis/full');
            const data = await response.json();
            
            if (data.success) {
                this.renderIssues(data.data.issues);
                this.showMessage(`Diagnosis complete. Found ${data.data.total_issues} issue(s).`, 'success');
            } else {
                this.showMessage('Diagnosis failed: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error running diagnosis:', error);
            this.showMessage('Error running diagnosis', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<span class="icon">🔍</span> Run Full Diagnosis';
        }
    }

    async diagnoseSymptom() {
        const symptom = document.getElementById('symptomInput').value.trim();
        
        if (!symptom) {
            this.showMessage('Please enter a symptom', 'error');
            return;
        }

        try {
            const response = await fetch('/api/diagnosis/symptom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptom })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const issues = data.data.likely_causes || data.data.issues || [];
                this.renderIssues(issues);
                
                if (issues.length === 0) {
                    this.showMessage('No specific issues found for that symptom. System appears healthy.', 'success');
                } else {
                    this.showMessage(`Found ${issues.length} potential issue(s) related to: "${symptom}"`, 'info');
                }
            } else {
                this.showMessage('Diagnosis failed: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error diagnosing symptom:', error);
            this.showMessage('Error diagnosing symptom', 'error');
        }
    }

    renderSystemInfo(info) {
        const container = document.getElementById('systemInfo');
        container.innerHTML = `
            <div class="info-item">
                <span class="info-label">Operating System</span>
                <span class="info-value">${info.os_version || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Hostname</span>
                <span class="info-value">${info.hostname || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Architecture</span>
                <span class="info-value">${info.architecture || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Boot Time</span>
                <span class="info-value">${info.boot_time || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Uptime</span>
                <span class="info-value">${info.uptime_hours ? Math.floor(info.uptime_hours) + ' hours' : 'Unknown'}</span>
            </div>
        `;
    }

    renderMetrics(data) {
        // CPU Metric
        const cpuUsage = data.cpu?.usage || 0;
        const cpuMetric = document.getElementById('cpuMetric');
        const cpuValue = cpuMetric.querySelector('.metric-value');
        const cpuFill = cpuMetric.querySelector('.metric-fill');
        
        cpuValue.textContent = `${cpuUsage.toFixed(1)}%`;
        cpuFill.style.width = `${cpuUsage}%`;
        cpuFill.className = 'metric-fill ' + this.getMetricClass(cpuUsage);

        // Memory Metric
        const memoryUsage = data.memory?.percent || 0;
        const memoryMetric = document.getElementById('memoryMetric');
        const memoryValue = memoryMetric.querySelector('.metric-value');
        const memoryFill = memoryMetric.querySelector('.metric-fill');
        
        memoryValue.textContent = `${memoryUsage.toFixed(1)}% (${data.memory?.used || 0}GB / ${data.memory?.total || 0}GB)`;
        memoryFill.style.width = `${memoryUsage}%`;
        memoryFill.className = 'metric-fill ' + this.getMetricClass(memoryUsage);

        // Disk Metric
        const disks = data.disk || [];
        const diskMetric = document.getElementById('diskMetric');
        
        if (disks.length > 0) {
            const primaryDisk = disks[0];
            const diskUsage = primaryDisk.percent || 0;
            const diskValue = diskMetric.querySelector('.metric-value');
            const diskFill = diskMetric.querySelector('.metric-fill');
            
            diskValue.textContent = `${diskUsage.toFixed(1)}% (${primaryDisk.free || 0}GB free)`;
            diskFill.style.width = `${diskUsage}%`;
            diskFill.className = 'metric-fill ' + this.getMetricClass(diskUsage);
        }
    }

    getMetricClass(value) {
        if (value > 90) return 'danger';
        if (value > 75) return 'warning';
        return '';
    }

    renderIssues(issues) {
        const container = document.getElementById('issuesList');
        
        if (!issues || issues.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <span class="icon">✅</span>
                    <p>No issues detected. Your system is running well!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = issues.map(issue => `
            <div class="issue-item ${issue.severity}">
                <div class="issue-header">
                    <div>
                        <div class="issue-title">${issue.title}</div>
                        <div class="issue-description">${issue.description}</div>
                    </div>
                    <span class="issue-severity ${issue.severity}">${issue.severity}</span>
                </div>
                <div class="issue-fixes">
                    ${issue.suggested_fixes ? issue.suggested_fixes.map(fix => `
                        <button class="fix-button" onclick="app.executeFix('${fix.fix_id}', ${JSON.stringify(fix.default_params || {}).replace(/"/g, '&quot;')})">
                            🛠️ ${fix.description}
                        </button>
                    `).join('') : ''}
                </div>
            </div>
        `).join('');
    }

    renderProcesses() {
        const container = document.getElementById('processesTable');
        
        if (!this.processesData) {
            container.innerHTML = '<div class="loading">Loading processes...</div>';
            return;
        }

        const processes = this.currentTab === 'cpu' 
            ? this.processesData.top_cpu 
            : this.processesData.top_memory;

        container.innerHTML = `
            <table class="process-table">
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Name</th>
                        <th>CPU %</th>
                        <th>Memory %</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    ${processes.map(proc => `
                        <tr>
                            <td>${proc.pid}</td>
                            <td>${proc.name || 'Unknown'}</td>
                            <td>${(proc.cpu_percent || 0).toFixed(1)}%</td>
                            <td>${(proc.memory_percent || 0).toFixed(1)}%</td>
                            <td>
                                <button class="kill-process-btn" onclick="app.executeFix('kill_process', {pid: ${proc.pid}})">
                                    Kill
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    renderAvailableFixes(fixes) {
        const container = document.getElementById('fixesList');
        
        container.innerHTML = fixes.map(fix => `
            <div class="fix-card">
                <div class="fix-card-header">
                    <div class="fix-name">${fix.id}</div>
                    <span class="fix-risk ${fix.risk}">${fix.risk}</span>
                </div>
                <div class="fix-description">${fix.description}</div>
                <div class="fix-meta">
                    ${fix.requires_sudo ? '🔐 Requires elevated privileges' : '👤 User level'}
                </div>
                <button class="btn btn-primary" onclick="app.executeFix('${fix.id}', {})">
                    Execute Fix
                </button>
            </div>
        `).join('');
    }

    async executeFix(fixId, params = {}) {
        // First, get preview
        try {
            const previewResponse = await fetch('/api/fixes/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fix_id: fixId, params })
            });
            
            const previewData = await previewResponse.json();
            
            if (previewData.success) {
                this.showConfirmationModal(fixId, params, previewData.data);
            } else {
                this.showMessage('Error previewing fix: ' + previewData.error, 'error');
            }
        } catch (error) {
            console.error('Error previewing fix:', error);
            this.showMessage('Error previewing fix', 'error');
        }
    }

    showConfirmationModal(fixId, params, previewData) {
        const modal = document.getElementById('confirmModal');
        const message = document.getElementById('confirmMessage');
        const command = document.getElementById('commandPreview');
        const riskWarning = document.getElementById('riskWarning');
        const riskLevel = document.getElementById('riskLevel');
        const executeBtn = document.getElementById('confirmExecuteBtn');

        message.textContent = `Are you sure you want to execute: ${previewData.description}?`;
        command.textContent = previewData.command;

        if (previewData.risk && previewData.risk !== 'none') {
            riskWarning.style.display = 'block';
            riskLevel.textContent = previewData.risk.toUpperCase();
            riskLevel.className = `fix-risk ${previewData.risk}`;
        } else {
            riskWarning.style.display = 'none';
        }

        // Remove old event listener and add new one
        const newExecuteBtn = executeBtn.cloneNode(true);
        executeBtn.parentNode.replaceChild(newExecuteBtn, executeBtn);
        
        newExecuteBtn.addEventListener('click', () => {
            this.confirmExecution(fixId, params);
        });

        modal.classList.add('active');
    }

    async confirmExecution(fixId, params) {
        this.closeModals();
        
        try {
            const response = await fetch('/api/fixes/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    fix_id: fixId, 
                    params,
                    confirmed: true 
                })
            });
            
            const data = await response.json();
            
            if (data.success && data.data.success) {
                this.showResultModal('Success', `
                    <div class="message success">
                        <strong>✅ Fix executed successfully!</strong>
                        <p>${data.data.description}</p>
                    </div>
                    ${data.data.stdout ? `<div><strong>Output:</strong><pre>${data.data.stdout}</pre></div>` : ''}
                `, 'success');
                
                // Refresh diagnostics
                setTimeout(() => {
                    this.loadDiagnostics();
                    this.loadProcesses();
                }, 2000);
            } else {
                this.showResultModal('Error', `
                    <div class="message error">
                        <strong>❌ Fix execution failed!</strong>
                        <p>${data.data?.error || data.error || 'Unknown error'}</p>
                    </div>
                    ${data.data?.stderr ? `<div><strong>Error output:</strong><pre>${data.data.stderr}</pre></div>` : ''}
                `, 'error');
            }
        } catch (error) {
            console.error('Error executing fix:', error);
            this.showResultModal('Error', `
                <div class="message error">
                    <strong>❌ Error executing fix</strong>
                    <p>${error.message}</p>
                </div>
            `, 'error');
        }
    }

    showResultModal(title, content, type) {
        const modal = document.getElementById('resultModal');
        const titleEl = document.getElementById('resultTitle');
        const contentEl = document.getElementById('resultContent');

        titleEl.textContent = title;
        contentEl.innerHTML = content;

        modal.classList.add('active');
    }

    closeModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('active');
        });
    }

    showMessage(message, type) {
        // You could implement a toast notification system here
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// Initialize the application
const app = new SPTool();

// Integrated Chat Functionality
class IntegratedChat {
    constructor() {
        this.chatContainer = document.getElementById('integratedChat');
        this.askAiBtn = document.getElementById('askAiBtn');
        this.closeBtn = document.getElementById('closeChatInline');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInputInline');
        this.sendBtn = document.getElementById('chatSendInline');
        this.statusEl = document.getElementById('chatStatusInline');
        this.isOpen = false;
        
        this.bindEvents();
        this.checkChatStatus();
    }
    
    bindEvents() {
        // Ask AI button
        if (this.askAiBtn) {
            this.askAiBtn.addEventListener('click', () => this.toggle());
        }
        
        // Close button
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
        
        // Send button
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        // Enter key in input
        if (this.chatInput) {
            this.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    }
    
    async checkChatStatus() {
        try {
            const response = await fetch('/api/chat/status');
            const data = await response.json();
            
            if (!data.configured) {
                this.showStatus('AI chat not configured. Add OPENAI_API_KEY to .env file.');
                if (this.askAiBtn) {
                    this.askAiBtn.disabled = true;
                    this.askAiBtn.title = 'AI not configured';
                }
                if (this.sendBtn) {
                    this.sendBtn.disabled = true;
                }
            } else {
                this.showStatus('AI Assistant ready');
            }
        } catch (error) {
            console.error('Error checking chat status:', error);
        }
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        if (this.chatContainer) {
            this.chatContainer.style.display = 'block';
            this.isOpen = true;
            setTimeout(() => {
                if (this.chatInput) {
                    this.chatInput.focus();
                }
            }, 400);
        }
    }
    
    close() {
        if (this.chatContainer) {
            this.chatContainer.style.display = 'none';
            this.isOpen = false;
            // Clear messages except welcome
            const welcome = this.chatMessages.querySelector('.chat-welcome-inline');
            if (this.chatMessages && welcome) {
                this.chatMessages.innerHTML = '';
                this.chatMessages.appendChild(welcome);
            }
        }
    }
    
    async sendMessage(messageText = null) {
        const message = messageText || this.chatInput.value.trim();
        
        if (!message) return;
        
        // Clear input
        this.chatInput.value = '';
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTyping();
        
        // Disable send button
        this.sendBtn.disabled = true;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, include_context: true })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTyping();
            
            if (data.success && data.response) {
                this.addMessage(data.response, 'assistant');
                
                if (data.tokens_used) {
                    this.showStatus(`Tokens used: ${data.tokens_used}`);
                }
            } else {
                this.showError(data.error || 'Failed to get response');
            }
        } catch (error) {
            this.hideTyping();
            this.showError('Network error. Please try again.');
            console.error('Chat error:', error);
        } finally {
            this.sendBtn.disabled = false;
            this.chatInput.focus();
        }
    }
    
    addMessage(content, sender) {
        const messageEl = document.createElement('div');
        messageEl.className = `chat-message ${sender}`;
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageEl.innerHTML = `
            <div class="chat-message-content">${this.formatMessage(content)}</div>
            <div class="chat-message-time">${time}</div>
        `;
        
        if (this.chatMessages) {
            this.chatMessages.appendChild(messageEl);
            this.scrollToBottom();
        }
    }
    
    formatMessage(text) {
        // Convert markdown-style formatting
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        text = text.replace(/\n/g, '<br>');
        return text;
    }
    
    showTyping() {
        const typingEl = document.createElement('div');
        typingEl.className = 'chat-typing';
        typingEl.id = 'chatTyping';
        typingEl.innerHTML = `
            <div class="chat-typing-dot"></div>
            <div class="chat-typing-dot"></div>
            <div class="chat-typing-dot"></div>
        `;
        if (this.chatMessages) {
            this.chatMessages.appendChild(typingEl);
            this.scrollToBottom();
        }
    }
    
    hideTyping() {
        const typingEl = document.getElementById('chatTyping');
        if (typingEl) {
            typingEl.remove();
        }
    }
    
    showError(message) {
        const errorEl = document.createElement('div');
        errorEl.className = 'chat-error';
        errorEl.textContent = message;
        if (this.chatMessages) {
            this.chatMessages.appendChild(errorEl);
            this.scrollToBottom();
        }
    }
    
    showStatus(message) {
        if (this.statusEl) {
            this.statusEl.textContent = message;
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            if (this.chatMessages) {
                this.chatMessages.scrollTo({
                    top: this.chatMessages.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }, 100);
    }
}

// Initialize integrated chat
const chat = new IntegratedChat();

