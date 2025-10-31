#!/usr/bin/env python3
"""
Basic test script for SPTool
Tests module imports and basic functionality
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        import flask
        print("✅ Flask imported")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import psutil
        print("✅ psutil imported")
    except ImportError as e:
        print(f"❌ psutil import failed: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config imported")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from system_diagnostics import SystemDiagnostics
        print("✅ SystemDiagnostics imported")
    except ImportError as e:
        print(f"❌ SystemDiagnostics import failed: {e}")
        return False
    
    try:
        from command_executor import CommandExecutor
        print("✅ CommandExecutor imported")
    except ImportError as e:
        print(f"❌ CommandExecutor import failed: {e}")
        return False
    
    try:
        from issue_diagnosis import IssueDiagnoser
        print("✅ IssueDiagnoser imported")
    except ImportError as e:
        print(f"❌ IssueDiagnoser import failed: {e}")
        return False
    
    return True

def test_system_diagnostics():
    """Test system diagnostics functionality"""
    print("\nTesting SystemDiagnostics...")
    
    try:
        from system_diagnostics import SystemDiagnostics
        
        diag = SystemDiagnostics()
        print(f"✅ Detected OS: {diag.os_type}")
        
        # Test CPU
        cpu = diag.get_cpu_usage()
        if 'usage' in cpu:
            print(f"✅ CPU Usage: {cpu['usage']}%")
        else:
            print(f"⚠️  CPU data: {cpu}")
        
        # Test Memory
        memory = diag.get_memory_usage()
        if 'percent' in memory:
            print(f"✅ Memory Usage: {memory['percent']}%")
        else:
            print(f"⚠️  Memory data: {memory}")
        
        # Test System Info
        info = diag.get_system_info()
        if 'hostname' in info:
            print(f"✅ Hostname: {info['hostname']}")
        else:
            print(f"⚠️  System info: {info}")
        
        return True
    except Exception as e:
        print(f"❌ SystemDiagnostics test failed: {e}")
        return False

def test_command_executor():
    """Test command executor functionality"""
    print("\nTesting CommandExecutor...")
    
    try:
        from command_executor import CommandExecutor
        
        executor = CommandExecutor()
        print(f"✅ Initialized for OS: {executor.os_type}")
        
        # Get available fixes
        fixes = executor.get_available_fixes()
        print(f"✅ Available fixes: {len(fixes)}")
        
        for fix in fixes[:3]:  # Show first 3
            print(f"   - {fix['id']}: {fix['description']} (Risk: {fix['risk']})")
        
        # Test dry run
        if fixes:
            test_fix = fixes[0]['id']
            result = executor.execute_fix(test_fix, dry_run=True)
            if result.get('dry_run'):
                print(f"✅ Dry run successful for: {test_fix}")
            else:
                print(f"⚠️  Dry run result: {result}")
        
        return True
    except Exception as e:
        print(f"❌ CommandExecutor test failed: {e}")
        return False

def test_issue_diagnosis():
    """Test issue diagnosis functionality"""
    print("\nTesting IssueDiagnoser...")
    
    try:
        from issue_diagnosis import IssueDiagnoser
        
        diagnoser = IssueDiagnoser()
        print("✅ IssueDiagnoser initialized")
        
        # Test symptom diagnosis
        result = diagnoser.diagnose_symptom("slow performance")
        if 'symptom' in result or 'issues' in result:
            print("✅ Symptom diagnosis working")
        else:
            print(f"⚠️  Diagnosis result: {result}")
        
        return True
    except Exception as e:
        print(f"❌ IssueDiagnoser test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application initialization"""
    print("\nTesting Flask App...")
    
    try:
        import app as sptool_app
        
        if sptool_app.app:
            print("✅ Flask app initialized")
            
            # Check routes
            routes = [str(rule) for rule in sptool_app.app.url_map.iter_rules()]
            print(f"✅ Registered routes: {len(routes)}")
            
            # Show some key routes
            key_routes = [r for r in routes if '/api/' in r]
            for route in key_routes[:5]:
                print(f"   - {route}")
            
            return True
        else:
            print("❌ Flask app not initialized")
            return False
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SPTool Basic Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Module Imports", test_imports()))
    results.append(("System Diagnostics", test_system_diagnostics()))
    results.append(("Command Executor", test_command_executor()))
    results.append(("Issue Diagnosis", test_issue_diagnosis()))
    results.append(("Flask Application", test_flask_app()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {len(results)} tests | Passed: {passed} | Failed: {failed}")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! SPTool is ready to run.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nThen open: http://127.0.0.1:5000")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the output above.")
        print("\nMissing dependencies? Try:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

