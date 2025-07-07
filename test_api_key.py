#!/usr/bin/env python3
"""
Test OpenSubtitles API Key
"""
import asyncio
import aiohttp
from subtitle_config import OPENSUBTITLES_API_KEY

async def test_opensubtitles_api():
    """Test if OpenSubtitles API key is working"""
    
    if not OPENSUBTITLES_API_KEY:
        print("❌ No API key found in subtitle_config.py")
        return
    
    print(f"🔑 Testing API key: {OPENSUBTITLES_API_KEY[:8]}...")
    
    try:
        async with aiohttp.ClientSession() as session:
            
            # Test API authentication
            url = "https://api.opensubtitles.com/api/v1/infos/user"
            headers = {
                'Api-Key': OPENSUBTITLES_API_KEY,
                'Content-Type': 'application/json',
                'User-Agent': 'SubtitleBot v1.0'
            }
            
            print("🔍 Testing API authentication...")
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    user_info = data.get('data', {})
                    print(f"✅ API key is valid!")
                    print(f"👤 User: {user_info.get('username', 'N/A')}")
                    print(f"📊 Downloads today: {user_info.get('downloads_count', 0)}")
                    print(f"📈 Downloads limit: {user_info.get('downloads_limit', 0)}")
                    
                elif response.status == 401:
                    print("❌ Invalid API key")
                elif response.status == 403:
                    print("❌ Access forbidden - API key may not have proper permissions")
                else:
                    print(f"❌ API returned status {response.status}")
                    
            # Test subtitle search
            print("\n🔍 Testing subtitle search...")
            search_url = "https://api.opensubtitles.com/api/v1/subtitles"
            params = {
                'query': 'KGF',
                'languages': 'en',
                'type': 'movie'
            }
            
            async with session.get(search_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('data', [])
                    print(f"✅ Search successful! Found {len(results)} results")
                    
                    if results:
                        first_result = results[0]
                        attrs = first_result.get('attributes', {})
                        print(f"📽️ First result: {attrs.get('release', 'N/A')}")
                        print(f"🗣️ Language: {attrs.get('language', 'N/A')}")
                else:
                    print(f"❌ Search failed with status {response.status}")
                    
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    asyncio.run(test_opensubtitles_api())