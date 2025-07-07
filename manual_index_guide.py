#!/usr/bin/env python3
"""
Manual Indexing Guide - Since automatic methods have limitations
"""

from info import CHANNELS
from database.ia_filterdb import get_database_count

def show_indexing_guide():
    print("MOVIE BOT INDEXING GUIDE")
    print("=" * 50)
    
    # Show current status
    primary_count, secondary_count = get_database_count()
    total_movies = primary_count + secondary_count
    print(f"Current movies in database: {total_movies}")
    
    print(f"\nYour configured channels ({len(CHANNELS)}):")
    for i, channel_id in enumerate(CHANNELS, 1):
        print(f"   {i}. {channel_id}")
    
    print(f"\nTo index your movie channel (-1001565676692 'Film Land'):")
    print("=" * 60)
    
    print("\nMETHOD 1: Using Channel Message Link")
    print("-" * 40)
    print("1. Open your 'Film Land' channel")
    print("2. Right-click on ANY movie message")
    print("3. Select 'Copy Link'")
    print("4. You'll get: https://t.me/c/1565676692/123")
    print("5. Send this link to your bot @moviebotsub_bot")
    print("6. Click 'Accept Index' when prompted")
    print("7. Bot will scan entire channel automatically")
    
    print("\nMETHOD 2: Forward Message")
    print("-" * 40)
    print("1. Open your 'Film Land' channel")
    print("2. Forward ANY movie message to @moviebotsub_bot")
    print("3. Click 'Accept Index' when prompted")
    print("4. Bot will scan entire channel automatically")
    
    print("\nMETHOD 3: Direct Channel Link")
    print("-" * 40)
    print("Based on your channel ID -1001565676692:")
    print("Send this link to your bot:")
    channel_link = "https://t.me/c/1565676692/1"
    print(f"   {channel_link}")
    
    print(f"\nEXPECTED RESULTS:")
    print("- Bot will process ALL messages in the channel")
    print("- Movies will be added to your MongoDB database")
    print("- You'll see progress updates during indexing")
    print("- After completion, movies will be searchable")
    
    print(f"\nTROUBLESHOOTING:")
    print("- Make sure bot is admin in the channel")
    print("- Use any message ID (even /1 works)")
    print("- Bot will scan from that message backwards")
    print("- Process may take 5-30 minutes depending on channel size")
    
    print(f"\nSTEPS TO TEST AFTER INDEXING:")
    print("1. Run: python upload_movies.py")
    print("2. Check if 'Current movies in database' > 0")
    print("3. Search for a movie in your bot")
    print("4. Should find movies + provide subtitles")

if __name__ == "__main__":
    show_indexing_guide()