#!/usr/bin/env python3
"""
Debug exactly what languages will be shown in subtitle selection
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_language_output():
    """Debug the exact language output that users will see"""
    print("🔍 Debugging subtitle language selection output...")
    
    try:
        # Test what the actual code will produce
        from language_config import get_all_languages, get_language_display_name
        
        subtitle_languages = get_all_languages()
        print(f"✅ get_all_languages() returns: {len(subtitle_languages)} languages")
        print(f"📋 Full list: {subtitle_languages}")
        
        # Simulate the exact button creation logic from pm_filter.py
        btn = []
        
        # Add subtitle language options - show all languages in rows of 2
        for i in range(0, len(subtitle_languages), 2):
            row = []
            for j in range(2):
                if i + j < len(subtitle_languages):
                    lang = subtitle_languages[i + j]
                    display_name = get_language_display_name(lang)
                    row.append(f"{display_name}")  # Simulate button text
            if row:  # Only add row if it has buttons
                btn.append(row)
        
        # Add "No Subtitles" option
        btn.append(["🚫 No Subtitles Needed"])
        
        print("\n📱 Exact button layout users will see:")
        for i, row in enumerate(btn, 1):
            if len(row) == 1:
                print(f"Row {i}: {row[0]}")
            else:
                print(f"Row {i}: {' | '.join(row)}")
        
        # Check if Sinhala is included
        all_button_text = []
        for row in btn:
            all_button_text.extend(row)
        
        sinhala_found = any("Sinhala" in text for text in all_button_text)
        
        print(f"\n🎯 Total buttons: {len(all_button_text)}")
        print(f"🇱🇰 Sinhala included: {'✅ YES' if sinhala_found else '❌ NO'}")
        
        if sinhala_found:
            for i, text in enumerate(all_button_text):
                if "Sinhala" in text:
                    print(f"🎯 Sinhala button position: {i + 1} - '{text}'")
        
        # Show what the user reported seeing
        user_reported = [
            "english", "korean", "spanish", "french", 
            "german", "italian", "portuguese", "chinese", 
            "no subtitles needed"
        ]
        
        print(f"\n👤 User reported seeing: {len(user_reported)} options")
        print(f"📋 User saw: {', '.join(user_reported)}")
        
        # Compare
        if len(all_button_text) == len(user_reported):
            print("⚠️ SAME COUNT - User might be seeing old cached version")
        else:
            print(f"✅ DIFFERENT COUNT - New version should work ({len(all_button_text)} vs {len(user_reported)})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_language_output()