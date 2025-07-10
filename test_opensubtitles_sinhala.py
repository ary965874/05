#!/usr/bin/env python3
"""
Test OpenSubtitles API for Sinhala support
"""
import asyncio
import aiohttp
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_opensubtitles_sinhala():
    """Test OpenSubtitles API for Sinhala language support"""
    
    try:
        from subtitle_config import OPENSUBTITLES_API_KEY
        api_key = OPENSUBTITLES_API_KEY
    except:
        api_key = "Z7wZXFOP8Nty4UrefAdCoidFVPvTBnTy"
    
    if not api_key:
        print("❌ No OpenSubtitles API key found")
        return
    
    print(f"🔑 Testing with API key: {api_key[:8]}...")
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Check user info and limits
        print("\n📊 Testing API authentication...")
        user_url = "https://api.opensubtitles.com/api/v1/infos/user"
        headers = {
            'Api-Key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'SubtitleBot v1.0'
        }
        
        try:
            async with session.get(user_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    user_info = data.get('data', {})
                    print(f"✅ API working! User: {user_info.get('username', 'N/A')}")
                    print(f"📈 Daily downloads: {user_info.get('downloads_count', 0)}/{user_info.get('downloads_limit', 0)}")
                else:
                    print(f"❌ API auth failed: {response.status}")
                    return
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return
        
        # Test 2: Search for Sinhala subtitles
        print("\n🔍 Testing Sinhala subtitle search...")
        search_url = "https://api.opensubtitles.com/api/v1/subtitles"
        
        test_movies = ["KGF", "Bahubali", "RRR", "Avengers"]
        
        for movie in test_movies:
            print(f"\n🎬 Testing: {movie}")
            
            params = {
                'query': movie,
                'languages': 'si',  # Sinhala language code
                'type': 'movie'
            }
            
            try:
                async with session.get(search_url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get('data', [])
                        print(f"   📊 Found {len(results)} Sinhala subtitles")
                        
                        if results:
                            # Show first few results
                            for i, result in enumerate(results[:3]):
                                attrs = result.get('attributes', {})
                                print(f"   {i+1}. {attrs.get('release', 'N/A')}")
                                print(f"      🗣️ Language: {attrs.get('language', 'N/A')}")
                                print(f"      ⭐ Ratings: {attrs.get('ratings', 'N/A')}")
                        else:
                            print("   ❌ No Sinhala subtitles found")
                    else:
                        print(f"   ❌ Search failed: {response.status}")
                        
            except Exception as e:
                print(f"   ❌ Error searching {movie}: {e}")
        
        # Test 3: Check language support
        print("\n🌐 Testing language code support...")
        params = {
            'query': 'test',
            'languages': 'si,en,ta,hi',  # Test multiple languages including Sinhala
            'type': 'movie'
        }
        
        try:
            async with session.get(search_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('data', [])
                    
                    languages_found = set()
                    for result in results:
                        lang = result.get('attributes', {}).get('language')
                        if lang:
                            languages_found.add(lang)
                    
                    print(f"✅ Languages found in results: {', '.join(sorted(languages_found))}")
                    if 'si' in languages_found:
                        print("🇱🇰 Sinhala (si) IS supported by OpenSubtitles API!")
                    else:
                        print("❌ Sinhala (si) not found in results")
                else:
                    print(f"❌ Language test failed: {response.status}")
                    
        except Exception as e:
            print(f"❌ Language test error: {e}")

if __name__ == "__main__":
    asyncio.run(test_opensubtitles_sinhala())