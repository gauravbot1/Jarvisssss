"""
Deployment script for free hosting platforms
"""
import os
import subprocess
import sys

def setup_mobile_assistant():
    """Setup script for deployment"""
    print("🚀 Setting up Mobile AI Assistant...")
    
    # Install dependencies
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check environment variables
    required_env_vars = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET']
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"⚠️  Warning: {var} not set")
    
    print("✅ Mobile Assistant setup complete!")
    print("📱 Run: python mobile_assistant.py")

if __name__ == "__main__":
    setup_mobile_assistant()