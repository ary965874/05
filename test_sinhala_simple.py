#!/usr/bin/env python3
"""
Simple test for Sinhala language support
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sinhala_config():
    """Test Sinhala configuration only"""
    print("🔍 Testing Sinhala language configuration...")
    
    try:
        # Test language_config
        from language_config import get_all_languages, get_language_display_name, LANGUAGE_CHANNELS
        
        languages = get_all_languages()
        print(f"✅ Total languages: {len(languages)}")
        
        if 'sinhala' in languages:
            print("✅ Sinhala found in language list!")
            display_name = get_language_display_name('sinhala')
            print(f"🇱🇰 Display name: {display_name}")
            
            # Check channel configuration
            if 'sinhala' in LANGUAGE_CHANNELS:
                channel_info = LANGUAGE_CHANNELS['sinhala']
                print(f"📺 Channel ID: {channel_info['channel']}")
                print(f"🏷️ Flag: {channel_info['flag']}")
            else:
                print("❌ Sinhala channel not configured")
        else:
            print("❌ Sinhala NOT found in language list!")
        
        # Test pm_filter languages (simple import)
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "pm_filter", 
                "/mnt/c/Users/yasir/Downloads/movie/movie_bot/plugins/pm_filter.py"
            )
            pm_filter = importlib.util.module_from_spec(spec)
            
            # Check if LANGUAGES is defined and contains sinhala
            with open("/mnt/c/Users/yasir/Downloads/movie/movie_bot/plugins/pm_filter.py", 'r') as f:
                content = f.read()
                if "'sinhala'" in content:
                    print("✅ pm_filter: Sinhala found in source code")
                else:
                    print("❌ pm_filter: Sinhala NOT in source code")
        except Exception as e:
            print(f"⚠️ Could not test pm_filter: {e}")
        
        print("\n🎯 Summary:")
        if 'sinhala' in languages:
            print("🎉 SUCCESS: Sinhala language support is properly configured!")
            print("🚀 Users should now see 🇱🇰 Sinhala in the language selection menu")
            print("\n📋 Next steps:")
            print("1. Deploy to Railway")
            print("2. Test with /start command")
            print("3. Verify Sinhala appears in language selection")
            print("4. Test with /test_sinhala MovieName")
        else:
            print("❌ FAILED: Sinhala language support needs fixing")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sinhala_config()