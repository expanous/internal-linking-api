#!/usr/bin/env python3
"""
Setup script for the Interlink Service.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def install_spacy_model():
    """Install spaCy model if not already installed."""
    print("Installing spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy model installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing spaCy model: {e}")
        return False
    return True

def test_installation():
    """Test if the installation was successful."""
    print("Testing installation...")
    try:
        from interlink_service import InterlinkService
        service = InterlinkService()
        print("✓ InterlinkService imported and initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error testing installation: {e}")
        return False

def main():
    """Main setup function."""
    print("Interlink Service Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("interlink_service.py"):
        print("✗ Error: interlink_service.py not found in current directory")
        print("Please run this script from the MVP-demo directory")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Install spaCy model
    if not install_spacy_model():
        return False
    
    # Test installation
    if not test_installation():
        return False
    
    print("\n" + "=" * 40)
    print("✓ Setup completed successfully!")
    print("\nYou can now use the InterlinkService:")
    print("  python interlink_service.py  # Run example")
    print("  python test_interlink.py     # Run tests")
    print("\nFor usage examples, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 