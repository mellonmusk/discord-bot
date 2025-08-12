#!/usr/bin/env python3
"""
Test script for Discord Meme Recommendation Bot components
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_ai_analysis():
    """Test AI analysis functionality"""
    print("🧠 Testing AI Analysis...")
    
    # Test conversation
    test_messages = [
        "That was absolutely savage!",
        "You just got roasted so hard",
        "I can't believe you said that"
    ]
    
    try:
        # Import the meme recommender
        from main import MemeRecommender
        
        recommender = MemeRecommender()
        result = await recommender.analyze_conversation_mood(test_messages)
        
        print(f"✅ Analysis successful!")
        print(f"   Mood: {result.get('mood', 'N/A')}")
        print(f"   Search Query: {result.get('search_query', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Analysis failed: {e}")
        return False

async def test_gif_fetching():
    """Test GIF fetching functionality"""
    print("\n🎬 Testing GIF Fetching...")
    
    try:
        from main import MemeRecommender
        
        recommender = MemeRecommender()
        gif_url = await recommender.get_recommended_gif("savage roast gif")
        
        if gif_url:
            print(f"✅ GIF fetched successfully!")
            print(f"   URL: {gif_url}")
            return True
        else:
            print("❌ No GIF URL returned")
            return False
            
    except Exception as e:
        print(f"❌ GIF fetching failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("🔑 Testing Environment Variables...")
    
    required_vars = ['DISCORD_TOKEN']
    optional_vars = ['OPENAI_API_KEY', 'GEMINI_API_KEY', 'TENOR_API_KEY']
    
    all_good = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: Set")
        else:
            print(f"   ❌ {var}: Missing (Required)")
            all_good = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: Set")
        else:
            print(f"   ⚠️  {var}: Missing (Optional)")
    
    return all_good

async def main():
    """Run all tests"""
    print("🧪 Discord Meme Bot Component Tests")
    print("=" * 40)
    
    # Test environment
    env_ok = test_environment()
    
    if not env_ok:
        print("\n❌ Environment setup incomplete!")
        print("Please set up your .env file first.")
        return
    
    print("\n🚀 Running component tests...")
    
    # Test AI analysis
    ai_ok = await test_ai_analysis()
    
    # Test GIF fetching
    gif_ok = await test_gif_fetching()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   Environment: {'✅' if env_ok else '❌'}")
    print(f"   AI Analysis: {'✅' if ai_ok else '❌'}")
    print(f"   GIF Fetching: {'✅' if gif_ok else '❌'}")
    
    if all([env_ok, ai_ok, gif_ok]):
        print("\n🎉 All tests passed! Your bot is ready to run.")
        print("Run 'python main.py' to start the bot.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("Make sure all API keys are properly configured.")

if __name__ == "__main__":
    asyncio.run(main())
