#!/usr/bin/env python3
"""
Debug test to check bot configuration and flow
"""

print("🔍 Debug Test - Bot Flow Analysis")
print("=" * 50)

# Test 1: Check if bot is configured
try:
    from info import BOT_TOKEN, ADMINS
    print(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
    print(f"✅ Admin ID: {ADMINS[0]}")
except Exception as e:
    print(f"❌ Configuration error: {e}")

# Test 2: Check language configuration
try:
    from language_config import get_language_channels, get_all_languages
    languages = get_all_languages()
    print(f"✅ Languages supported: {len(languages)}")
    
    # Test specific language
    korean_channels = get_language_channels('korean')
    print(f"✅ Korean channels: {korean_channels}")
    
    english_channels = get_language_channels('english')
    print(f"✅ English channels: {english_channels}")
    
except Exception as e:
    print(f"❌ Language config error: {e}")

# Test 3: Check subtitle handler
try:
    from subtitle_handler import subtitle_handler
    print("✅ Subtitle handler imported")
    
    # Test language channels
    test_channels = subtitle_handler.get_language_channels('korean')
    print(f"✅ Subtitle handler Korean channels: {test_channels}")
    
except Exception as e:
    print(f"❌ Subtitle handler error: {e}")

# Test 4: Bot permissions check
print("\n🔧 Bot Requirements Check:")
print("1. ✅ Bot must be admin in these channels:")
print("   - -1002614174192")
print("   - -1001641168678")
print("2. ✅ Bot must have permission to:")
print("   - Create invite links")
print("   - Send messages")
print("   - Read channel info")

# Test 5: Expected flow
print("\n🎬 Expected Bot Flow:")
print("1. User searches movie in group")
print("2. User selects movie → Language options appear")
print("3. User selects language → Gets alert + URL redirect")
print("4. User clicks 'Open' → Goes to bot DM")
print("5. Bot asks to join test channels")
print("6. After joining → Bot sends movie + subtitles")

print("\n🚨 Common Issues:")
print("1. Bot not admin in test channels")
print("2. Test channels are private/invalid")
print("3. Bot doesn't have invite link permissions")
print("4. User doesn't click 'Open' after language selection")

print("\n📋 Next Steps:")
print("1. Make sure bot is admin in both test channels")
print("2. Give bot 'Invite Users via Link' permission")
print("3. Test by selecting language and clicking 'Open'")
print("4. Check bot logs for error messages")

print("\n✅ No API keys needed - uses free APIs only!")