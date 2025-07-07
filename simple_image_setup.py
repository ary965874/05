#!/usr/bin/env python3
"""
Simple Image Setup - Manual method
"""

import os

def show_image_setup_guide():
    print("SIMPLE IMAGE SETUP GUIDE")
    print("=" * 40)
    
    # Check images
    images_folder = "images"
    image_files = []
    
    if os.path.exists(images_folder):
        for file in os.listdir(images_folder):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_files.append(file)
    
    print(f"Found {len(image_files)} images in folder")
    
    print("\nMANUAL UPLOAD METHOD:")
    print("=" * 30)
    print("1. Open any Telegram channel where your bot is admin")
    print("2. Upload your 6 anime/cute girl images to that channel")
    print("3. Right-click each image -> 'Copy Link'")
    print("4. You'll get URLs like: https://t.me/c/1234567890/123")
    print("5. Replace 't.me/c/' with 'cdn4.telesco.pe/file/'")
    print("6. Add '.jpg' at the end")
    print("\nExample transformation:")
    print("From: https://t.me/c/1234567890/123")
    print("To: https://cdn4.telesco.pe/file/1234567890/123.jpg")
    
    print("\nALTERNATIVE - Use Your Movie Channel:")
    print("=" * 40)
    print("Your movie channel: -1001565676692")
    print("1. Upload your 6 images to this channel")
    print("2. Forward each image to any private chat")
    print("3. Right-click -> Copy Link")
    print("4. Transform the URLs as shown above")
    print("5. Give me the 6 transformed URLs")
    
    print("\nSAMPLE PICS LINE:")
    print("=" * 20)
    sample_urls = [
        "https://cdn4.telesco.pe/file/1565676692/001.jpg",
        "https://cdn4.telesco.pe/file/1565676692/002.jpg", 
        "https://cdn4.telesco.pe/file/1565676692/003.jpg",
        "https://cdn4.telesco.pe/file/1565676692/004.jpg",
        "https://cdn4.telesco.pe/file/1565676692/005.jpg",
        "https://cdn4.telesco.pe/file/1565676692/006.jpg"
    ]
    
    urls_string = " ".join(sample_urls)
    print(f"PICS = (environ.get('PICS', '{urls_string}')).split()")
    
    print("\nREADY TO UPDATE:")
    print("Once you have your 6 URLs, tell me and I'll update the bot!")

if __name__ == "__main__":
    show_image_setup_guide()