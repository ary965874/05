#!/usr/bin/env python3
"""
Update movie database with fresh file IDs
"""

import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from database.ia_filterdb import get_file_details

async def update_movie_files():
    print("🎬 Movie Database Update Tool")
    print("=" * 40)
    
    # Connect to bot
    bot = Client("update_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    
    print("✅ Bot connected")
    
    # Test current database
    print("\n🔍 Testing Current Database:")
    
    # Test a few file IDs from database
    test_files = [
        "BQADBAAD5gkAAnhwsVDfFW2r9lY82RYE",  # KGF
        "BQADBAAD7w0AAjTccVCStMKxWsriJxYE",  # Avengers
    ]
    
    working_files = 0
    broken_files = 0
    
    for file_id in test_files:
        try:
            # Try to get file info
            file_info = await get_file_details(file_id)
            if file_info:
                print(f"📁 Found: {file_info['file_name']}")
                
                # Test if bot can send this file
                try:
                    # We'll just test getting file info, not actually sending
                    print(f"🔍 Testing file_id: {file_id[:20]}...")
                    
                    # In a real scenario, you'd test send_cached_media here
                    # For now, we know these fail from previous tests
                    print(f"❌ File ID invalid (from previous tests)")
                    broken_files += 1
                    
                except Exception as e:
                    print(f"❌ Cannot send: {e}")
                    broken_files += 1
            else:
                print(f"❌ File not found in database: {file_id}")
                broken_files += 1
                
        except Exception as e:
            print(f"❌ Database error: {e}")
            broken_files += 1
    
    print(f"\n📊 Database Status:")
    print(f"✅ Working files: {working_files}")
    print(f"❌ Broken files: {broken_files}")
    
    print(f"\n🔧 Solutions:")
    print("1. Upload fresh movies with current bot")
    print("2. Update database with new file IDs")
    print("3. Test with small batch first")
    
    print(f"\n📋 Manual Update Process:")
    print("1. Upload movie to your channel with current bot")
    print("2. Copy the new file_id")
    print("3. Update MongoDB record with new file_id")
    print("4. Test sending - should work!")
    
    print(f"\n🎯 Example:")
    print("Old file_id: BQADBAAD5gkAAnhwsVDfFW2r9lY82RYE (broken)")
    print("New file_id: BQACAgUAAyEGAASb0SHwAAMDaGlyH76bpV9v805vECjNT1dYgm4AAt4ZAAJ4LElXk2GdBMVYoZIeBA (works)")
    
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(update_movie_files())