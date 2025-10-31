"""
SPTool - System Performance Troubleshooting Tool
Flask application for diagnosing and fixing system issues
"""
from flask import Flask, render_template, jsonify, request
from config import Config
from system_diagnostics import SystemDiagnostics
from command_executor import CommandExecutor
from issue_diagnosis import IssueDiagnoser
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Initialize modules
diagnostics = SystemDiagnostics()
executor = CommandExecutor()
diagnoser = IssueDiagnoser()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/system/info')
def get_system_info():
    """Get basic system information"""
    try:
        info = diagnostics.get_system_info()
        return jsonify({'success': True, 'data': info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/system/diagnostic')
def get_diagnostic():
    """Get full system diagnostic"""
    try:
        diagnostic = diagnostics.get_full_diagnostic()
        return jsonify({'success': True, 'data': diagnostic})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/diagnosis/full')
def diagnose_full():
    """Run full system diagnosis and identify issues"""
    try:
        diagnosis = diagnoser.diagnose_all()
        return jsonify({'success': True, 'data': diagnosis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/diagnosis/symptom', methods=['POST'])
def diagnose_symptom():
    """Diagnose based on user-described symptom"""
    try:
        data = request.get_json()
        symptom = data.get('symptom', '')
        
        if not symptom:
            return jsonify({'success': False, 'error': 'No symptom provided'}), 400
        
        diagnosis = diagnoser.diagnose_symptom(symptom)
        return jsonify({'success': True, 'data': diagnosis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fixes/available')
def get_available_fixes():
    """Get list of available fixes"""
    try:
        fixes = executor.get_available_fixes()
        return jsonify({'success': True, 'data': fixes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fixes/preview', methods=['POST'])
def preview_fix():
    """Preview a fix without executing it"""
    try:
        data = request.get_json()
        fix_id = data.get('fix_id')
        params = data.get('params', {})
        
        if not fix_id:
            return jsonify({'success': False, 'error': 'No fix_id provided'}), 400
        
        result = executor.execute_fix(fix_id, params, dry_run=True)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fixes/execute', methods=['POST'])
def execute_fix():
    """Execute a fix command"""
    try:
        data = request.get_json()
        fix_id = data.get('fix_id')
        params = data.get('params', {})
        confirmed = data.get('confirmed', False)
        
        if not fix_id:
            return jsonify({'success': False, 'error': 'No fix_id provided'}), 400
        
        if not confirmed and Config.REQUIRE_CONFIRMATION:
            return jsonify({
                'success': False, 
                'error': 'Execution requires confirmation',
                'requires_confirmation': True
            }), 400
        
        result = executor.execute_fix(fix_id, params, dry_run=False)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/processes/top')
def get_top_processes():
    """Get top CPU and memory consuming processes"""
    try:
        processes = diagnostics.get_top_processes(limit=15)
        return jsonify({'success': True, 'data': processes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/processes/validate/<int:pid>')
def validate_process(pid):
    """Validate a process ID"""
    try:
        validation = executor.validate_pid(pid)
        return jsonify({'success': True, 'data': validation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'SPTool'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   SPTool - System Performance Troubleshooting Tool   ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    
    🚀 Starting server on http://{app.config['HOST']}:{app.config['PORT']}
    
    📊 Dashboard: http://{app.config['HOST']}:{app.config['PORT']}/
    ⚕️  Health Check: http://{app.config['HOST']}:{app.config['PORT']}/health
    
    Press CTRL+C to stop the server
    """)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
