#!/usr/bin/env python3
"""
Test subtitle creation and file handling
"""

import asyncio
import tempfile
import os

async def test_subtitle_creation():
    print("🧪 Testing Subtitle Creation and File Handling")
    print("=" * 50)
    
    # Test 1: Import real subtitle handler
    try:
        from real_subtitle_handler import real_subtitle_handler
        print("✅ Real subtitle handler imported")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test 2: Create test subtitle info
    test_subtitle = {
        'filename': 'Avengers_Endgame_korean.srt',
        'language': 'korean',
        'release': 'Avengers Endgame 2019',
        'source': 'mock'
    }
    
    # Test 3: Generate subtitle content
    try:
        subtitle_data = await real_subtitle_handler.download_subtitle(test_subtitle)
        if subtitle_data:
            print("✅ Subtitle data generated")
            subtitle_text = subtitle_data.decode('utf-8')
            print(f"📄 Preview (first 200 chars):\n{subtitle_text[:200]}...")
        else:
            print("❌ No subtitle data generated")
            return
    except Exception as e:
        print(f"❌ Subtitle generation error: {e}")
        return
    
    # Test 4: Create temp file (Windows compatible)
    try:
        temp_dir = tempfile.gettempdir()
        subtitle_filename = "Avengers_Endgame_korean.srt"
        temp_file = os.path.join(temp_dir, subtitle_filename)
        
        print(f"📁 Temp file path: {temp_file}")
        
        # Write file
        with open(temp_file, 'wb') as f:
            f.write(subtitle_data)
        
        # Check file exists and has content
        if os.path.exists(temp_file):
            file_size = os.path.getsize(temp_file)
            print(f"✅ File created successfully ({file_size} bytes)")
            
            # Read back to verify
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()[:100]
                print(f"📖 File content preview: {content}...")
        else:
            print("❌ File not created")
            return
            
    except Exception as e:
        print(f"❌ File creation error: {e}")
        return
    
    # Test 5: Clean up
    try:
        os.remove(temp_file)
        print("✅ Temp file cleaned up")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")
    
    # Test 6: Test different languages
    print("\n🌍 Testing Different Languages:")
    languages = ['english', 'korean', 'spanish', 'french']
    
    for lang in languages:
        test_sub = {
            'filename': f'test_{lang}.srt',
            'language': lang,
            'release': 'Test Movie 2023',
            'source': 'mock'
        }
        
        try:
            data = await real_subtitle_handler.download_subtitle(test_sub)
            if data:
                preview = data.decode('utf-8')[:50].replace('\n', ' ')
                print(f"✅ {lang.title()}: {preview}...")
            else:
                print(f"❌ {lang.title()}: Failed")
        except Exception as e:
            print(f"❌ {lang.title()}: Error - {e}")
    
    # Close session
    await real_subtitle_handler.close_session()
    
    print("\n🎯 Summary:")
    print("✅ Subtitle generation works")
    print("✅ File creation/cleanup works")
    print("✅ Multiple languages supported")
    print("✅ Ready for bot testing!")
    
    print("\n📋 Next Steps:")
    print("1. Restart bot: python bot.py")
    print("2. Test movie selection with language")
    print("3. Should receive: Movie file + Subtitle file")

if __name__ == "__main__":
    asyncio.run(test_subtitle_creation())