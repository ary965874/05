#!/usr/bin/env python3
"""
Check channel configuration and identify issues
"""

print("🔍 Channel Configuration Check")
print("=" * 40)

# Check info.py configuration
try:
    from info import AUTH_CHANNEL, CHANNELS, LOG_CHANNEL
    print(f"✅ AUTH_CHANNEL: {AUTH_CHANNEL}")
    print(f"✅ LOG_CHANNEL: {LOG_CHANNEL}")
    print(f"✅ CHANNELS count: {len(CHANNELS)}")
except Exception as e:
    print(f"❌ Info config error: {e}")

# Check language configuration
try:
    from language_config import TEST_CHANNELS, get_language_channels
    print(f"✅ TEST_CHANNELS: {TEST_CHANNELS}")
    
    korean_channels = get_language_channels('korean')
    print(f"✅ Korean channels: {korean_channels}")
    
    english_channels = get_language_channels('english')
    print(f"✅ English channels: {english_channels}")
    
except Exception as e:
    print(f"❌ Language config error: {e}")

# Expected configuration
print("\n🎯 Expected Configuration:")
print("AUTH_CHANNEL should be: [-1002614174192, -1001641168678]")
print("TEST_CHANNELS should be: ['-1002614174192', '-1001641168678']")
print("All language channels should use TEST_CHANNELS")

print("\n✅ Your test channels:")
print("1. -1002614174192")
print("2. -1001641168678")

print("\n🔧 Bot Requirements:")
print("1. @moviebotsub_bot must be admin in both channels")
print("2. Bot needs 'Invite Users via Link' permission")
print("3. Channels must be accessible to the bot")

print("\n🚨 Invalid Channel Found in Error:")
print("Channel: -1001712029193")
print("This channel is NOT in your test channels list!")
print("Bot tried to access this channel, causing the error.")

print("\n📋 Solution:")
print("1. Restart bot with updated config")
print("2. Test with language selection")
print("3. Should use only your 2 test channels now")