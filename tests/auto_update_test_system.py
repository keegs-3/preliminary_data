#!/usr/bin/env python3
"""
Auto-Update Test System

This system automatically:
1. Monitors /src/generated_configs/ for new REC*.json files
2. Regenerates comprehensive test data when changes are detected
3. Updates test output files automatically
4. Can be integrated into CI/CD pipelines
5. Provides git hooks for automatic test updates

Usage:
- Run manually: python auto_update_test_system.py
- Set up git hook: python auto_update_test_system.py --setup-git-hook
- Check for changes: python auto_update_test_system.py --check-only
"""

import sys
import os
import glob
import json
import hashlib
from datetime import datetime
from pathlib import Path
import argparse

# Import our config-based test generator
from config_based_verification_test import run_config_based_verification

class AutoUpdateTestSystem:
    """Manages automatic updates of test data when configs change"""
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.config_dir = self.test_dir.parent / "src" / "generated_configs"
        self.cache_file = self.test_dir / ".config_cache.json"
        self.output_file = self.test_dir / "config_based_verification_output.txt"
        
    def get_config_fingerprint(self) -> dict:
        """Generate fingerprint of all config files for change detection"""
        fingerprint = {}
        
        pattern = str(self.config_dir / "REC*.json")
        config_files = glob.glob(pattern)
        
        for config_file in sorted(config_files):
            try:
                # Get file modification time and content hash
                stat = os.stat(config_file)
                with open(config_file, 'rb') as f:
                    content_hash = hashlib.md5(f.read()).hexdigest()
                
                rel_path = os.path.relpath(config_file, self.config_dir)
                fingerprint[rel_path] = {
                    'mtime': stat.st_mtime,
                    'size': stat.st_size,
                    'hash': content_hash
                }
            except Exception as e:
                print(f"Warning: Could not fingerprint {config_file}: {e}")
        
        return fingerprint
    
    def load_cached_fingerprint(self) -> dict:
        """Load previously cached config fingerprint"""
        if not self.cache_file.exists():
            return {}
        
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
                return cache_data.get('config_fingerprint', {})
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")
            return {}
    
    def save_fingerprint_cache(self, fingerprint: dict):
        """Save config fingerprint to cache"""
        cache_data = {
            'last_update': datetime.now().isoformat(),
            'config_fingerprint': fingerprint,
            'total_configs': len(fingerprint)
        }
        
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def detect_changes(self) -> tuple:
        """Detect changes in config files since last run"""
        current_fingerprint = self.get_config_fingerprint()
        cached_fingerprint = self.load_cached_fingerprint()
        
        if not cached_fingerprint:
            # First run - all configs are "new"
            return True, list(current_fingerprint.keys()), [], []
        
        new_configs = []
        modified_configs = []
        deleted_configs = []
        
        # Find new and modified configs
        for config_name, current_info in current_fingerprint.items():
            if config_name not in cached_fingerprint:
                new_configs.append(config_name)
            elif current_info != cached_fingerprint[config_name]:
                modified_configs.append(config_name)
        
        # Find deleted configs
        for config_name in cached_fingerprint:
            if config_name not in current_fingerprint:
                deleted_configs.append(config_name)
        
        has_changes = bool(new_configs or modified_configs or deleted_configs)
        
        return has_changes, new_configs, modified_configs, deleted_configs
    
    def update_test_data(self, force=False):
        """Update test data if changes are detected"""
        print("🔍 Checking for config file changes...")
        
        has_changes, new_configs, modified_configs, deleted_configs = self.detect_changes()
        
        if not has_changes and not force:
            print("✅ No changes detected. Test data is up to date.")
            return False
        
        if has_changes:
            print(f"📊 Changes detected:")
            if new_configs:
                print(f"  📁 New configs: {len(new_configs)}")
                for config in new_configs[:5]:  # Show first 5
                    print(f"    + {config}")
                if len(new_configs) > 5:
                    print(f"    + ... and {len(new_configs) - 5} more")
            
            if modified_configs:
                print(f"  🔄 Modified configs: {len(modified_configs)}")
                for config in modified_configs[:5]:
                    print(f"    ~ {config}")
                if len(modified_configs) > 5:
                    print(f"    ~ ... and {len(modified_configs) - 5} more")
            
            if deleted_configs:
                print(f"  🗑️ Deleted configs: {len(deleted_configs)}")
                for config in deleted_configs:
                    print(f"    - {config}")
        
        if force:
            print("🔄 Force update requested...")
        
        print("🧪 Regenerating comprehensive test data...")
        
        try:
            # Run the comprehensive test generation
            successful, failed = run_config_based_verification()
            
            # Update the cache
            current_fingerprint = self.get_config_fingerprint()
            self.save_fingerprint_cache(current_fingerprint)
            
            print(f"✅ Test data updated successfully!")
            print(f"📊 Results: {successful} configs processed, {failed} failed")
            print(f"📄 Output: {self.output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating test data: {e}")
            return False
    
    def setup_git_hook(self):
        """Set up git pre-commit hook to auto-update tests"""
        git_hooks_dir = Path(".git/hooks")
        if not git_hooks_dir.exists():
            print("❌ No .git/hooks directory found. Are you in a git repository?")
            return False
        
        hook_file = git_hooks_dir / "pre-commit"
        hook_content = '''#!/bin/bash
# Auto-update test data when config files change

echo "Checking for config file changes..."
cd "$(git rev-parse --show-toplevel)"

# Check if any REC config files are being committed
if git diff --cached --name-only | grep -q "src/generated_configs/REC.*\\.json"; then
    echo "Config files changed. Updating test data..."
    
    # Run the auto-update system
    python tests/auto_update_test_system.py --force
    
    # Add the updated test output to the commit
    git add tests/config_based_verification_output.txt
    
    echo "Test data updated and added to commit."
fi
'''
        
        try:
            with open(hook_file, 'w') as f:
                f.write(hook_content)
            
            # Make it executable
            os.chmod(hook_file, 0o755)
            
            print("✅ Git pre-commit hook installed successfully!")
            print(f"📁 Hook file: {hook_file}")
            print("🔄 Test data will auto-update when config files are committed")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up git hook: {e}")
            return False
    
    def generate_update_report(self):
        """Generate a report of the current state"""
        fingerprint = self.get_config_fingerprint()
        
        report_lines = [
            "=" * 60,
            "AUTO-UPDATE TEST SYSTEM REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"📁 Config directory: {self.config_dir}",
            f"📊 Total configs found: {len(fingerprint)}",
            f"🗄️ Cache file: {self.cache_file}",
            f"📄 Output file: {self.output_file}",
            "",
            "CONFIG FILES:",
            ""
        ]
        
        for config_name in sorted(fingerprint.keys()):
            report_lines.append(f"  ✓ {config_name}")
        
        report_lines.extend([
            "",
            "USAGE:",
            "  python auto_update_test_system.py                 # Check and update if needed",
            "  python auto_update_test_system.py --force         # Force update",
            "  python auto_update_test_system.py --check-only    # Check for changes only",
            "  python auto_update_test_system.py --setup-git-hook # Setup automatic git hook",
            "",
            "=" * 60
        ])
        
        return '\n'.join(report_lines)

def main():
    parser = argparse.ArgumentParser(description="Auto-update test system for WellPath configs")
    parser.add_argument('--force', action='store_true', help='Force update even if no changes detected')
    parser.add_argument('--check-only', action='store_true', help='Only check for changes, do not update')
    parser.add_argument('--setup-git-hook', action='store_true', help='Set up git pre-commit hook')
    parser.add_argument('--report', action='store_true', help='Generate status report')
    
    args = parser.parse_args()
    
    system = AutoUpdateTestSystem()
    
    if args.setup_git_hook:
        system.setup_git_hook()
        return
    
    if args.report:
        print(system.generate_update_report())
        return
    
    if args.check_only:
        has_changes, new_configs, modified_configs, deleted_configs = system.detect_changes()
        if has_changes:
            print(f"📊 Changes detected: {len(new_configs)} new, {len(modified_configs)} modified, {len(deleted_configs)} deleted")
            sys.exit(1)  # Exit code 1 indicates changes found
        else:
            print("✅ No changes detected")
            sys.exit(0)
    
    # Default behavior: update if needed
    updated = system.update_test_data(force=args.force)
    sys.exit(0 if updated or not system.detect_changes()[0] else 1)

if __name__ == "__main__":
    main()