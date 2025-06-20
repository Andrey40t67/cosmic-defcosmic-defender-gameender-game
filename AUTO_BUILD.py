#!/usr/bin/env python3
"""
🚀 COSMIC DEFENDER - Automatic Build Script
Created by AndreyVV

This script automatically builds .exe and .apk files from the source code.
Run this script to generate ready-to-play game files!

Usage:
    python AUTO_BUILD.py

Requirements:
    - Python 3.8+
    - pygame
    - cx-Freeze (for Windows .exe)
    - buildozer (for Android .apk)
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install required packages"""
    print("🔧 Installing requirements...")
    
    packages = [
        "pygame==2.5.2",
        "cx-Freeze==6.15.10"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def create_setup_py():
    """Create setup.py for cx-Freeze"""
    setup_content = '''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pygame", "random", "math", "sys"],
    "excludes": ["tkinter"],
    "include_files": [],
    "optimize": 2
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CosmicDefender",
    version="1.0",
    description="🚀 Epic Space Shooter Game by AndreyVV",
    options={"build_exe": build_exe_options},
    executables=[Executable("cosmic_defender_game.py", base=base, target_name="CosmicDefender.exe")]
)
'''
    
    with open("setup.py", "w") as f:
        f.write(setup_content)
    print("✅ Created setup.py")

def create_buildozer_spec():
    """Create buildozer.spec for Android"""
    spec_content = '''[app]
title = Cosmic Defender
package.name = cosmicdefender
package.domain = org.andreyvv.cosmicdefender

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy,pygame-ce

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
'''
    
    with open("buildozer.spec", "w") as f:
        f.write(spec_content)
    print("✅ Created buildozer.spec")

def build_windows_exe():
    """Build Windows .exe file"""
    print("🖥️ Building Windows .exe...")
    
    try:
        # Create setup.py
        create_setup_py()
        
        # Build the executable
        subprocess.check_call([sys.executable, "setup.py", "build"])
        
        # Find the built exe
        build_dir = "build"
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                if file.endswith(".exe"):
                    exe_path = os.path.join(root, file)
                    print(f"✅ Windows .exe built successfully: {exe_path}")
                    return exe_path
        
        print("❌ Could not find built .exe file")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build Windows .exe: {e}")
        return None

def build_android_apk():
    """Build Android .apk file"""
    print("📱 Building Android .apk...")
    
    try:
        # Install buildozer if not present
        subprocess.check_call([sys.executable, "-m", "pip", "install", "buildozer"])
        
        # Create buildozer.spec
        create_buildozer_spec()
        
        # Build the APK
        subprocess.check_call(["buildozer", "android", "debug"])
        
        # Find the built apk
        bin_dir = "bin"
        if os.path.exists(bin_dir):
            for file in os.listdir(bin_dir):
                if file.endswith(".apk"):
                    apk_path = os.path.join(bin_dir, file)
                    print(f"✅ Android .apk built successfully: {apk_path}")
                    return apk_path
        
        print("❌ Could not find built .apk file")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build Android .apk: {e}")
        print("Note: Android building requires additional setup (Android SDK, NDK)")
        return None

def create_download_ready_files():
    """Create download-ready files with instructions"""
    
    # Create Windows download package
    windows_content = '''
🚀 COSMIC DEFENDER - Windows Version
Created by AndreyVV

READY TO PLAY .EXE FILE!

📁 This package contains:
- CosmicDefender.exe (Ready to run!)
- README.txt (This file)

🎮 HOW TO PLAY:
1. Double-click CosmicDefender.exe
2. If Windows shows a security warning, click "More info" then "Run anyway"
3. Enjoy the game!

🕹️ CONTROLS:
- WASD or Arrow Keys: Move your ship
- SPACE: Shoot
- ESC: Pause game

🎯 OBJECTIVE:
Defend the galaxy from alien invaders! Collect power-ups, upgrade your ship, and survive as long as possible!

Created with ❤️ by AndreyVV
'''
    
    with open("CosmicDefender_Windows_README.txt", "w") as f:
        f.write(windows_content)
    
    # Create Android download package
    android_content = '''
🚀 COSMIC DEFENDER - Android Version
Created by AndreyVV

READY TO INSTALL .APK FILE!

📁 This package contains:
- CosmicDefender.apk (Ready to install!)
- README.txt (This file)

📱 HOW TO INSTALL:
1. Enable "Install from unknown sources" in Settings > Security
2. Tap on CosmicDefender.apk to install
3. Launch the game from your app drawer

🕹️ CONTROLS:
- Touch screen to move your ship
- Tap to shoot
- Pinch to pause (if supported)

🎯 OBJECTIVE:
Defend the galaxy from alien invaders! Collect power-ups, upgrade your ship, and survive as long as possible!

📋 REQUIREMENTS:
- Android 7.0+ (API level 24)
- 2GB RAM minimum
- 50MB storage space

Created with ❤️ by AndreyVV
'''
    
    with open("CosmicDefender_Android_README.txt", "w") as f:
        f.write(android_content)
    
    print("✅ Created download-ready documentation")

def main():
    """Main build function"""
    print("🚀 COSMIC DEFENDER - Automatic Build System")
    print("Created by AndreyVV")
    print("=" * 50)
    
    # Check if source file exists
    if not os.path.exists("cosmic_defender_game.py"):
        print("❌ cosmic_defender_game.py not found!")
        print("Please make sure the game source file is in the same directory.")
        return
    
    print("📋 Build Options:")
    print("1. Install requirements only")
    print("2. Build Windows .exe")
    print("3. Build Android .apk")
    print("4. Build both .exe and .apk")
    print("5. Create download packages")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        install_requirements()
    elif choice == "2":
        install_requirements()
        build_windows_exe()
    elif choice == "3":
        install_requirements()
        build_android_apk()
    elif choice == "4":
        install_requirements()
        build_windows_exe()
        build_android_apk()
    elif choice == "5":
        create_download_ready_files()
    else:
        print("❌ Invalid choice!")
        return
    
    print("\n🎉 Build process completed!")
    print("Check the generated files in the current directory.")
    print("\nFor manual building:")
    print("Windows: python setup.py build")
    print("Android: buildozer android debug")

if __name__ == "__main__":
    main()
