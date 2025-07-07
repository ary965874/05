#!/usr/bin/env python3
"""
Local Image Handler - Upload local images to Telegram and get file IDs
"""

import asyncio
import os
from hydrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN

async def upload_local_images():
    """Upload local images and get Telegram file IDs"""
    print("Local Image Uploader")
    print("=" * 30)
    
    # Check for images folder
    images_folder = "images"
    if not os.path.exists(images_folder):
        print(f"Images folder '{images_folder}' not found!")
        print("Please create 'images' folder and put your anime/cute girl images there")
        return
    
    # Get image files
    image_files = []
    for file in os.listdir(images_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_files.append(file)
    
    if not image_files:
        print("No image files found in 'images' folder!")
        print("Please add some .jpg, .png, or .gif files")
        return
    
    print(f"Found {len(image_files)} images:")
    for i, img in enumerate(image_files, 1):
        try:
            print(f"   {i}. {img}")
        except UnicodeEncodeError:
            print(f"   {i}. [Image file with special characters]")
    
    # Connect to bot
    bot = Client("image_uploader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await bot.start()
    
    print(f"\nBot connected: @{(await bot.get_me()).username}")
    print("Uploading images...")
    
    # Upload images and collect file IDs
    uploaded_urls = []
    
    for img_file in image_files:
        img_path = os.path.join(images_folder, img_file)
        try:
            # Upload to Telegram (to yourself)
            message = await bot.send_photo(
                chat_id="me",  # Send to yourself (Saved Messages)
                photo=img_path,
                caption=f"Bot image: {img_file}"
            )
            
            # Get file ID (can be used as image URL alternative)
            file_id = message.photo.file_id
            uploaded_urls.append(f"telegram_file:{file_id}")
            try:
                print(f"Uploaded: {img_file} -> {file_id}")
            except UnicodeEncodeError:
                print(f"Uploaded: [Image] -> {file_id}")
            
        except Exception as e:
            print(f"Failed to upload {img_file}: {e}")
    
    await bot.stop()
    
    if uploaded_urls:
        print(f"\nSuccessfully uploaded {len(uploaded_urls)} images!")
        print("\nCopy this line to update your bot:")
        print("=" * 50)
        urls_string = " ".join(uploaded_urls)
        print(f"PICS = (environ.get('PICS', '{urls_string}')).split()")
        print("=" * 50)
        print("\nInstructions:")
        print("1. Copy the PICS line above")
        print("2. Replace the PICS line in info.py") 
        print("3. Restart your bot")
    else:
        print("No images were uploaded successfully")

if __name__ == "__main__":
    asyncio.run(upload_local_images())