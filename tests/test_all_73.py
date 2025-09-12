#!/usr/bin/env python3
import os
import glob
import subprocess
import sys

def test_all_configs():
    """Test all 73 config files systematically"""
    config_dir = "../src/generated_configs"
    test_script = "test_complex_config_validation.py"
    
    # Get all config files
    config_files = glob.glob(os.path.join(config_dir, "REC*.json"))
    config_files.sort()
    
    print(f"Found {len(config_files)} config files to test")
    
    passed = 0
    failed = 0
    results = []
    
    for i, config_file in enumerate(config_files, 1):
        config_name = os.path.basename(config_file)
        print(f"\n[{i}/{len(config_files)}] Testing: {config_name}")
        
        try:
            # Run test
            result = subprocess.run([
                sys.executable, test_script, config_file
            ], capture_output=True, text=True, timeout=30)
            
            if "CONFIG TEST PASSED" in result.stdout:
                print("✅ PASSED")
                passed += 1
                results.append((config_name, "PASSED", ""))
            else:
                print("❌ FAILED")
                failed += 1
                error_info = result.stderr[:200] if result.stderr else result.stdout[-200:]
                results.append((config_name, "FAILED", error_info))
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:100]}")
            failed += 1
            results.append((config_name, "ERROR", str(e)[:200]))
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TESTING COMPLETE!")
    print(f"Total configs: {len(config_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/len(config_files)*100:.1f}%")
    
    if failed > 0:
        print(f"\n{'='*60}")
        print("FAILED CONFIGS:")
        for name, status, error in results:
            if status != "PASSED":
                print(f"❌ {name}: {status}")
                if error:
                    print(f"   Error: {error[:100]}...")

if __name__ == "__main__":
    test_all_configs()