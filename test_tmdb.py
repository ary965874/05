#!/usr/bin/env python3
"""
Test TheMovieDB API integration
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_tmdb_api():
    """Test TheMovieDB API functionality"""
    print("🔍 Testing TheMovieDB API...")
    
    try:
        from sinhala_subtitle_downloader import sinhala_subtitle_downloader
        
        # Test movie search
        test_movies = ["KGF", "Avengers", "Bahubali", "RRR"]
        
        for movie in test_movies:
            print(f"\n📽️ Testing: {movie}")
            
            movie_info = await sinhala_subtitle_downloader.search_movie_tmdb(movie)
            
            if movie_info:
                print(f"✅ Found: {movie_info['title']} ({movie_info['year']})")
                print(f"   🎬 Original: {movie_info['original_title']}")
                print(f"   🆔 TMDB ID: {movie_info['id']}")
            else:
                print(f"❌ No results for {movie}")
        
        # Close session
        await sinhala_subtitle_downloader.close_session()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tmdb_api())