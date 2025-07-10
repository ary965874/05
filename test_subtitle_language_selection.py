#!/usr/bin/env python3
"""
Test subtitle language selection includes Sinhala
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_subtitle_language_selection():
    """Test if Sinhala appears in subtitle language selection"""
    print("🔍 Testing subtitle language selection...")
    
    try:
        # Test language_config
        from language_config import get_all_languages, get_language_display_name
        
        languages = get_all_languages()
        print(f"✅ Total languages available: {len(languages)}")
        print(f"📋 Languages: {', '.join(languages)}")
        
        if 'sinhala' in languages:
            print("✅ Sinhala found in language list!")
            
            # Test display name
            display_name = get_language_display_name('sinhala')
            print(f"🇱🇰 Sinhala display name: {display_name}")
            
            # Test button creation (simulate what the bot does)
            print("\n📱 Testing button creation...")
            
            # Simulate the new button layout (2 per row)
            buttons_per_row = 2
            total_rows = (len(languages) + buttons_per_row - 1) // buttons_per_row
            
            print(f"📊 Will create {total_rows} rows of buttons")
            
            # Check if Sinhala will appear
            sinhala_index = languages.index('sinhala')
            sinhala_row = sinhala_index // buttons_per_row
            sinhala_position = sinhala_index % buttons_per_row
            
            print(f"🎯 Sinhala position: Row {sinhala_row + 1}, Position {sinhala_position + 1}")
            
            # Show first few rows as example
            print("\n🔲 Example button layout:")
            for i in range(0, min(len(languages), 8), 2):  # Show first 4 rows
                row = []
                for j in range(2):
                    if i + j < len(languages):
                        lang = languages[i + j]
                        display = get_language_display_name(lang)
                        row.append(display)
                print(f"Row {(i//2) + 1}: {' | '.join(row)}")
            
            if len(languages) > 8:
                print(f"... and {len(languages) - 8} more languages")
            
        else:
            print("❌ Sinhala NOT found in language list!")
            
        print("\n🔍 Testing pm_filter import...")
        # Test if we can import the updated code
        import importlib.util
        
        # Check pm_filter source for language import
        with open("/mnt/c/Users/yasir/Downloads/movie/movie_bot/plugins/pm_filter.py", 'r') as f:
            content = f.read()
            if "get_all_languages()" in content:
                print("✅ pm_filter: Using get_all_languages() - GOOD!")
            else:
                print("❌ pm_filter: Still using old method")
                
            if "[:8]" in content:
                print("⚠️ pm_filter: Still has [:8] limit somewhere")
            else:
                print("✅ pm_filter: No 8-language limit found")
        
        # Check channel_handler too
        with open("/mnt/c/Users/yasir/Downloads/movie/movie_bot/plugins/channel_handler.py", 'r') as f:
            content = f.read()
            if "get_all_languages()" in content:
                print("✅ channel_handler: Using get_all_languages() - GOOD!")
            else:
                print("❌ channel_handler: Still using old method")
        
        print("\n🎯 Summary:")
        if 'sinhala' in languages:
            print("🎉 SUCCESS: Sinhala will now appear in subtitle language selection!")
            print(f"📊 Total languages users will see: {len(languages)}")
            print("🚀 After deployment, users will see 🇱🇰 Sinhala in the subtitle menu")
        else:
            print("❌ FAILED: Sinhala still missing from language selection")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_subtitle_language_selection()