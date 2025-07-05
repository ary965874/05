#!/usr/bin/env python3
"""
Test script for the enhanced movie bot with subtitle support
"""

import asyncio
import logging
from subtitle_handler import subtitle_handler
from language_config import get_language_display_name, get_all_languages, get_language_channels

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_subtitle_functionality():
    """Test subtitle search and download functionality"""
    print("🧪 Testing Enhanced Movie Bot with Subtitle Support")
    print("=" * 60)
    
    # Test language configuration
    print("\n1. Testing Language Configuration:")
    languages = get_all_languages()
    print(f"   Supported languages: {len(languages)}")
    for lang in languages[:5]:  # Show first 5
        display_name = get_language_display_name(lang)
        channels = get_language_channels(lang)
        print(f"   {display_name}: {len(channels)} channels")
    
    # Test subtitle search
    print("\n2. Testing Subtitle Search:")
    test_movies = [
        "Avengers Endgame 2019",
        "Parasite 2019",
        "The Dark Knight 2008"
    ]
    
    for movie in test_movies:
        print(f"   🎬 Searching subtitles for: {movie}")
        try:
            # Test English subtitles
            subtitles = await subtitle_handler.search_subtitles(movie, "english")
            print(f"      Found {len(subtitles)} English subtitles")
            
            # Test Korean subtitles
            subtitles_kr = await subtitle_handler.search_subtitles(movie, "korean")
            print(f"      Found {len(subtitles_kr)} Korean subtitles")
            
        except Exception as e:
            print(f"      Error: {e}")
    
    # Test movie info extraction
    print("\n3. Testing Movie Info Extraction:")
    test_filenames = [
        "Avengers.Endgame.2019.1080p.BluRay.x264-SPARKS.mkv",
        "Parasite (2019) [1080p] [WEBRip] [5.1] [YTS.MX].mp4",
        "The.Dark.Knight.2008.720p.BrRip.x264.YIFY.mp4"
    ]
    
    for filename in test_filenames:
        movie_info = subtitle_handler.extract_movie_info(filename)
        print(f"   📁 {filename}")
        print(f"      Movie: {movie_info['name']}")
        print(f"      Year: {movie_info['year']}")
    
    # Clean up
    await subtitle_handler.close_session()
    print("\n✅ All tests completed!")

def test_channel_configuration():
    """Test channel configuration without async"""
    print("\n4. Testing Channel Configuration:")
    
    # Test all language channels
    for lang in get_all_languages():
        channels = get_language_channels(lang)
        display_name = get_language_display_name(lang)
        print(f"   {display_name}: {channels}")
    
    print("\n✅ Channel configuration test completed!")

if __name__ == "__main__":
    print("🚀 Starting Bot Tests...")
    
    # Test channel configuration (sync)
    test_channel_configuration()
    
    # Test subtitle functionality (async)
    print("\n🔄 Running async tests...")
    try:
        asyncio.run(test_subtitle_functionality())
    except Exception as e:
        print(f"❌ Async test failed: {e}")
    
    print("\n🎉 Testing completed!")
    print("\n📝 Next Steps:")
    print("1. Update info.py with your actual bot token and API credentials")
    print("2. Update language_config.py with your actual channel IDs")
    print("3. Install required packages: pip install -r requirements.txt")
    print("4. Run the bot: python bot.py")
    print("5. Test the bot by sending a movie name in a connected group")