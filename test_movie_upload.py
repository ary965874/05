#!/usr/bin/env python3
"""
Test if bot can send files it uploads itself
"""

import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN

async def test_fresh_file_upload():
    print("🎬 Testing Fresh File Upload")
    print("=" * 40)
    
    # Create bot client
    bot = Client(
        "test_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    
    await bot.start()
    print("✅ Bot connected")
    
    try:
        # Get bot info
        me = await bot.get_me()
        print(f"✅ Bot: @{me.username}")
        
        # Test with a small text file
        test_content = """This is a test movie file for subtitle bot.

Movie: Test Movie 2023
Language: English
Subtitle: Available

This file was uploaded by the current bot instance to test file sending capability."""
        
        # Create test file
        with open("test_movie.txt", "w") as f:
            f.write(test_content)
        
        print("✅ Test file created")
        
        # Upload to a test channel or chat (use one of your channels)
        test_channel = -1002614174192  # Your test channel
        
        # Send file to channel
        try:
            msg = await bot.send_document(
                chat_id=test_channel,
                document="test_movie.txt",
                caption="🧪 Test file for bot capability check"
            )
            
            file_id = msg.document.file_id
            print(f"✅ File uploaded successfully!")
            print(f"📁 New file_id: {file_id}")
            
            # Test sending back immediately
            try:
                # Try sending to the same channel
                await bot.send_document(
                    chat_id=test_channel,
                    document=file_id,
                    caption="🔄 Testing file resend capability"
                )
                print("✅ File resend successful! Bot can send files it uploads.")
                
            except Exception as e:
                print(f"❌ File resend failed: {e}")
                
        except Exception as e:
            print(f"❌ File upload failed: {e}")
            print("⚠️ Bot might not be admin in the test channel")
        
        # Clean up
        import os
        try:
            os.remove("test_movie.txt")
            print("✅ Test file cleaned up")
        except:
            pass
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    await bot.stop()
    print("\n🎯 Test Results:")
    print("If file upload/resend worked:")
    print("✅ Bot can send files - database has old/invalid file IDs")
    print("🔧 Solution: Re-upload movies with current bot")
    print("\nIf file upload/resend failed:")
    print("❌ Bot lacks permissions or other issues")
    print("🔧 Solution: Check bot permissions in channels")

if __name__ == "__main__":
    asyncio.run(test_fresh_file_upload())