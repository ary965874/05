#!/usr/bin/env python3
"""
Test Sinhala language support in bot
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_language_support():
    """Test if Sinhala is properly supported"""
    print("🔍 Testing Sinhala language support...")
    
    try:
        # Test language_config
        from language_config import get_all_languages, get_language_display_name
        
        languages = get_all_languages()
        print(f"✅ Total languages supported: {len(languages)}")
        print(f"📋 Languages: {', '.join(languages)}")
        
        if 'sinhala' in languages:
            print("✅ Sinhala found in language_config!")
            display_name = get_language_display_name('sinhala')
            print(f"🇱🇰 Display name: {display_name}")
        else:
            print("❌ Sinhala NOT found in language_config!")
        
        # Test subtitle handlers
        from real_subtitle_handler import real_subtitle_handler
        from real_subtitle_fetcher import real_subtitle_fetcher
        from subtitle_downloader import subtitle_downloader
        
        handlers = [
            ("real_subtitle_handler", real_subtitle_handler),
            ("real_subtitle_fetcher", real_subtitle_fetcher),
            ("subtitle_downloader", subtitle_downloader)
        ]
        
        for name, handler in handlers:
            try:
                supported = handler.get_supported_languages()
                if 'sinhala' in supported:
                    print(f"✅ {name}: Sinhala supported")
                else:
                    print(f"❌ {name}: Sinhala NOT supported")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
        
        # Test pm_filter languages
        from plugins.pm_filter import LANGUAGES
        if 'sinhala' in LANGUAGES:
            print("✅ pm_filter: Sinhala supported")
        else:
            print("❌ pm_filter: Sinhala NOT supported")
        
        print("\n🎯 Summary:")
        if 'sinhala' in languages:
            print("✅ Sinhala language support is properly configured!")
            print("🚀 Users should now see Sinhala in the language selection menu")
        else:
            print("❌ Sinhala language support needs fixing")
            
    except Exception as e:
        print(f"❌ Error testing language support: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_language_support()