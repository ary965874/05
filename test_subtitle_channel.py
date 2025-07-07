#!/usr/bin/env python3
"""
Test Subtitle Channel System
"""
import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from subtitle_channel_manager import subtitle_channel_manager

async def test_subtitle_system():
    """Test the subtitle channel system"""
    app = Client(
        name='test_subtitle_channel',
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    
    await app.start()
    
    try:
        print("🧪 Testing Subtitle Channel System")
        print("=" * 50)
        
        # Test movie name
        test_movie = "KGF Kannada 2018HD"
        test_language = "english"
        
        print(f"📽️ Testing movie: {test_movie}")
        print(f"🗣️ Testing language: {test_language}")
        print()
        
        # Test subtitle retrieval
        print("🔍 Searching for subtitle...")
        subtitle_content = await subtitle_channel_manager.get_subtitle(app, test_movie, test_language)
        
        if subtitle_content:
            print(f"✅ Found subtitle! Size: {len(subtitle_content)} bytes")
            
            # Show first few lines
            try:
                text_content = subtitle_content.decode('utf-8')
                lines = text_content.split('\n')[:10]
                print("\n📄 First few lines:")
                for line in lines:
                    print(f"   {line}")
            except:
                print("   (Binary content)")
        else:
            print("❌ No subtitle found")
        
        print()
        
        # Test subtitle statistics
        print("📊 Getting subtitle statistics...")
        stats = await subtitle_channel_manager.get_subtitle_stats(app)
        
        if stats:
            print(f"📁 Total subtitles: {stats.get('total_subtitles', 0)}")
            print(f"🎬 Unique movies: {stats.get('unique_movies', 0)}")
            
            languages = stats.get('languages', {})
            if languages:
                print("🗣️ Languages:")
                for lang, count in languages.items():
                    print(f"   • {lang}: {count}")
            else:
                print("🗣️ No language statistics")
        else:
            print("❌ No statistics available")
        
        print()
        
        # Test search functionality
        print("🔍 Searching database for KGF subtitles...")
        search_results = await subtitle_channel_manager.search_channel_subtitles(app, "KGF")
        
        if search_results:
            print(f"✅ Found {len(search_results)} results in database:")
            for result in search_results:
                print(f"   • {result['language']}: {result['filename']}")
        else:
            print("❌ No search results in database")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await app.stop()
        await subtitle_channel_manager.close_session()

if __name__ == "__main__":
    asyncio.run(test_subtitle_system())