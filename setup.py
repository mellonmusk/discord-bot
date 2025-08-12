#!/usr/bin/env python3
"""
Setup script for Discord Meme Recommendation Bot
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file found!")
        return True
    else:
        print("❌ .env file not found!")
        print("📝 Please create a .env file with your API keys:")
        print("   Copy .env(example) to .env and fill in your keys")
        return False

def main():
    print("🤖 Discord Meme Recommendation Bot Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check environment file
    check_env_file()
    
    print("\n🚀 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Create a .env file with your API keys")
    print("2. Get your Discord bot token from https://discord.com/developers/applications")
    print("3. (Optional) Get OpenAI/Gemini API keys for AI analysis")
    print("4. (Optional) Get Tenor API key for GIF recommendations")
    print("5. Run: python main.py")
    
    print("\n💡 For help, check the README.md file")

if __name__ == "__main__":
    main()
