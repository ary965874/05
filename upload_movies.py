#!/usr/bin/env python3
"""
Upload movies to your new database
"""

import asyncio
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, DATABASE_NAME, COLLECTION_NAME
from pymongo import MongoClient

async def upload_test_movies():
    print("Movie Upload Tool for New Database")
    print("=" * 50)
    
    # Connect to your new MongoDB
    print(f"Connecting to: {DATABASE_URL[:50]}...")
    client = MongoClient(DATABASE_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print(f"Connected to database: {DATABASE_NAME}")
    print(f"Using collection: {COLLECTION_NAME}")
    
    # Connect bot
    bot = Client("upload_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    print(f"Bot connected: @{(await bot.get_me()).username}")
    
    # Check current database status
    current_count = collection.count_documents({})
    print(f"Current movies in database: {current_count}")
    
    if current_count > 0:
        print("Sample movies in database:")
        for i, movie in enumerate(collection.find().limit(3)):
            print(f"   {i+1}. {movie.get('file_name', 'Unknown')}")
        print("   ...")
    
    print(f"\nYour Database Information:")
    print(f"Database URL: {DATABASE_URL}")
    print(f"Database Name: {DATABASE_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    
    print(f"\nTo Add Movies to Your Database:")
    print("1. Upload movie files to your channels using current bot")
    print("2. Get the file IDs from uploaded movies")
    print("3. Add records to MongoDB manually or via script")
    
    print(f"\nExample Movie Record Structure:")
    example_record = {
        "_id": "BQACAgUAAyEGAASb0SHwAAMDaGlyH76bpV9v805vECjNT1dYgm4AAt4ZAAJ4LElXk2GdBMVYoZIeBA",
        "file_name": "Avengers Endgame 2019 1080p BluRay x264.mkv",
        "file_size": 2147483648,
        "file_type": "video",
        "mime_type": "video/x-matroska"
    }
    
    for key, value in example_record.items():
        print(f"   {key}: {value}")
    
    print(f"\nSteps to Populate Database:")
    print("1. Choose 5-10 popular movies")
    print("2. Upload them to your movie channels")
    print("3. Copy file IDs from uploaded movies")
    print("4. Insert records into MongoDB")
    print("5. Test bot with those movies")
    
    await bot.stop()
    client.close()
    
    print(f"\nDatabase connection test successful!")
    print(f"Your new database is ready for movies!")

if __name__ == "__main__":
    asyncio.run(upload_test_movies())