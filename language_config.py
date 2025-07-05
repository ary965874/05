"""
Language-specific channel configuration for subtitle bot
Update these channel IDs with your actual language-specific channels
"""

# Testing configuration - Using 2 channels for all languages
TEST_CHANNELS = ['-1002614174192', '-1001641168678']

LANGUAGE_CHANNELS = {
    # All languages use the same 2 test channels for now
    'english': {
        'channels': TEST_CHANNELS,
        'display_name': 'English',
        'flag': '🇺🇸'
    },
    
    'korean': {
        'channels': TEST_CHANNELS,
        'display_name': 'Korean',
        'flag': '🇰🇷'
    },
    
    'spanish': {
        'channels': TEST_CHANNELS,
        'display_name': 'Spanish',
        'flag': '🇪🇸'
    },
    
    'french': {
        'channels': TEST_CHANNELS,
        'display_name': 'French',
        'flag': '🇫🇷'
    },
    
    'german': {
        'channels': TEST_CHANNELS,
        'display_name': 'German',
        'flag': '🇩🇪'
    },
    
    'italian': {
        'channels': TEST_CHANNELS,
        'display_name': 'Italian',
        'flag': '🇮🇹'
    },
    
    'portuguese': {
        'channels': TEST_CHANNELS,
        'display_name': 'Portuguese',
        'flag': '🇵🇹'
    },
    
    'chinese': {
        'channels': TEST_CHANNELS,
        'display_name': 'Chinese',
        'flag': '🇨🇳'
    },
    
    'japanese': {
        'channels': TEST_CHANNELS,
        'display_name': 'Japanese',
        'flag': '🇯🇵'
    },
    
    'arabic': {
        'channels': TEST_CHANNELS,
        'display_name': 'Arabic',
        'flag': '🇸🇦'
    },
    
    'hindi': {
        'channels': TEST_CHANNELS,
        'display_name': 'Hindi',
        'flag': '🇮🇳'
    },
    
    'tamil': {
        'channels': TEST_CHANNELS,
        'display_name': 'Tamil',
        'flag': '🇮🇳'
    },
    
    'malayalam': {
        'channels': TEST_CHANNELS,
        'display_name': 'Malayalam',
        'flag': '🇮🇳'
    },
    
    'telugu': {
        'channels': TEST_CHANNELS,
        'display_name': 'Telugu',
        'flag': '🇮🇳'
    }
}

def get_language_info(language: str) -> dict:
    """Get language information"""
    return LANGUAGE_CHANNELS.get(language.lower(), LANGUAGE_CHANNELS['english'])

def get_all_languages() -> list:
    """Get all supported languages"""
    return list(LANGUAGE_CHANNELS.keys())

def get_language_channels(language: str) -> list:
    """Get channels for a specific language"""
    lang_info = get_language_info(language)
    return lang_info['channels']

def get_language_display_name(language: str) -> str:
    """Get display name for a language"""
    lang_info = get_language_info(language)
    return f"{lang_info['flag']} {lang_info['display_name']}"