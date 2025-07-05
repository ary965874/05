#!/usr/bin/env python3
"""
Simple Channel Indexing Tool
"""

import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, CHANNELS
from database.ia_filterdb import save_file, get_database_count
from hydrogram import enums
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def index_channel(channel_id, max_messages=100):
    """Index a specific channel"""
    print(f"\nStarting to index channel: {channel_id}")
    
    bot = Client("indexer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    
    try:
        # Get channel info
        channel = await bot.get_chat(channel_id)
        print(f"Channel: {channel.title}")
        
        # Index files
        total_files = 0
        duplicate = 0
        errors = 0
        processed = 0
        
        # Use get_chat_history with limit
        async for message in bot.get_chat_history(channel_id, limit=max_messages):
            processed += 1
            
            if processed % 20 == 0:
                print(f"   Processed: {processed}, Saved: {total_files}, Duplicates: {duplicate}")
            
            # Check if message has media
            if not message.media:
                continue
                
            # Check media type
            if message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                continue
                
            # Get media object
            media = getattr(message, message.media.value, None)
            if not media:
                continue
                
            # Set properties
            media.file_type = message.media.value
            media.caption = message.caption
            
            # Save to database
            try:
                saved, status = await save_file(media)
                if saved:
                    total_files += 1
                    logger.info(f"Saved: {media.file_name}")
                elif status == 0:
                    duplicate += 1
                else:
                    errors += 1
            except Exception as e:
                errors += 1
                logger.error(f"Error saving {media.file_name}: {e}")
        
        print(f"\nIndexing Complete!")
        print(f"Total processed: {processed}")
        print(f"Movies saved: {total_files}")
        print(f"Duplicates skipped: {duplicate}")
        print(f"Errors: {errors}")
        
    except Exception as e:
        print(f"Error indexing channel {channel_id}: {e}")
        
    finally:
        await bot.stop()

async def index_all_channels():
    """Index all configured channels"""
    print("Channel Indexing Tool")
    print("=" * 50)
    
    # Show current database status
    primary_count, secondary_count = get_database_count()
    total_before = primary_count + secondary_count
    print(f"Movies in database before: {total_before}")
    
    print(f"\nFound {len(CHANNELS)} channels to index:")
    for i, channel_id in enumerate(CHANNELS, 1):
        print(f"   {i}. {channel_id}")
    
    # Index each channel
    for channel_id in CHANNELS:
        await index_channel(channel_id, max_messages=200)
        await asyncio.sleep(2)  # Small delay between channels
    
    # Show final status
    primary_count, secondary_count = get_database_count()
    total_after = primary_count + secondary_count
    new_movies = total_after - total_before
    
    print(f"\nAll Channels Indexed!")
    print(f"Movies before: {total_before}")
    print(f"Movies after: {total_after}")
    print(f"New movies added: {new_movies}")

if __name__ == "__main__":
    asyncio.run(index_all_channels())