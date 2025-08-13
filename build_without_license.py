import os
import shutil
import subprocess
import sys

def build_without_license():
    """Build the package without the LICENSE file to avoid license-file metadata"""
    
    # Check if LICENSE file exists
    if not os.path.exists('LICENSE'):
        print("LICENSE file not found, proceeding with normal build")
        subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
        return
    
    # Backup original LICENSE file
    license_backup = 'LICENSE.backup'
    shutil.copy2('LICENSE', license_backup)
    
    try:
        # Remove LICENSE file temporarily
        os.remove('LICENSE')
        
        # Also remove any backup files that might exist
        if os.path.exists('LICENSE.backup'):
            os.remove('LICENSE.backup')
        
        # Clean up any existing build artifacts
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('libgen_api_refhub.egg-info'):
            shutil.rmtree('libgen_api_refhub.egg-info')
        
        # Build the package
        print("Building package without LICENSE file...")
        subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
        
    finally:
        # Restore LICENSE file
        shutil.copy2(license_backup, 'LICENSE')
        os.remove(license_backup)
        print("LICENSE file restored")

if __name__ == "__main__":
    build_without_license()
