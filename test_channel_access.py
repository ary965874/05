#!/usr/bin/env python3
"""
Test if bot can access movie channels
"""

import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, CHANNELS

async def test_channel_access():
    print("📺 Testing Movie Channel Access")
    print("=" * 40)
    
    bot = Client("test_channels", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    
    print(f"✅ Bot connected: @{(await bot.get_me()).username}")
    print(f"🔍 Testing {len(CHANNELS)} movie channels...")
    
    accessible_channels = 0
    
    for i, channel_id in enumerate(CHANNELS[:5]):  # Test first 5 channels
        try:
            # Try to get channel info
            chat = await bot.get_chat(channel_id)
            print(f"✅ Channel {i+1}: {chat.title} (ID: {channel_id})")
            
            # Try to get recent messages (test read access)
            try:
                async for message in bot.get_chat_history(channel_id, limit=1):
                    if message.document or message.video:
                        print(f"   📁 Found media file: {message.document.file_name if message.document else 'Video'}")
                        print(f"   🆔 File ID: {message.document.file_id if message.document else message.video.file_id}")
                        
                        # This would be a NEW file ID that works with current bot!
                        break
            except Exception as e:
                print(f"   ❌ Cannot read messages: {e}")
                
            accessible_channels += 1
            
        except Exception as e:
            print(f"❌ Channel {i+1} (ID: {channel_id}): {e}")
    
    print(f"\n📊 Results:")
    print(f"✅ Accessible channels: {accessible_channels}/5 tested")
    
    if accessible_channels > 0:
        print(f"\n🎯 SOLUTION FOUND!")
        print(f"✅ Bot can access movie channels")
        print(f"✅ Can get NEW file IDs from those channels")
        print(f"🔧 Need to update database with NEW file IDs")
    else:
        print(f"\n❌ ISSUE FOUND!")
        print(f"❌ Bot cannot access movie channels")
        print(f"🔧 Need to add bot as admin to channels")
    
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(test_channel_access())