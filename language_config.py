"""
Language-specific channel configuration for subtitle bot
Update these channel IDs with your actual language-specific channels
"""

# Common channel that all users must join
COMMON_CHANNEL = '-1002614174192'

# Language-specific channels with actual channel IDs
LANGUAGE_CHANNELS = {
    'english': {
        'channel': '-1002766947260',
        'display_name': 'English',
        'flag': '🇺🇸'
    },
    
    'korean': {
        'channel': '-1002886647880',
        'display_name': 'Korean',
        'flag': '🇰🇷'
    },
    
    'spanish': {
        'channel': '-1002783974864',
        'display_name': 'Spanish',
        'flag': '🇪🇸'
    },
    
    'french': {
        'channel': '-1002758900991',
        'display_name': 'French',
        'flag': '🇫🇷'
    },
    
    'german': {
        'channel': '-1002861718794',
        'display_name': 'German',
        'flag': '🇩🇪'
    },
    
    'italian': {
        'channel': '-1002207907276',
        'display_name': 'Italian',
        'flag': '🇮🇹'
    },
    
    'portuguese': {
        'channel': '-1002561296642',
        'display_name': 'Portuguese',
        'flag': '🇵🇹'
    },
    
    'chinese': {
        'channel': '-1002622821443',
        'display_name': 'Chinese',
        'flag': '🇨🇳'
    },
    
    'japanese': {
        'channel': '-1002781237685',
        'display_name': 'Japanese',
        'flag': '🇯🇵'
    },
    
    'arabic': {
        'channel': '-1002831127039',
        'display_name': 'Arabic',
        'flag': '🇸🇦'
    },
    
    'hindi': {
        'channel': '-1002767591536',
        'display_name': 'Hindi',
        'flag': '🇮🇳'
    },
    
    'tamil': {
        'channel': '-1002750405093',
        'display_name': 'Tamil',
        'flag': '🇮🇳'
    },
    
    'malayalam': {
        'channel': '-1002596417585',
        'display_name': 'Malayalam',
        'flag': '🇮🇳'
    },
    
    'telugu': {
        'channel': '-1002822738923',
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
    """Get channels for a specific language (common + language-specific)"""
    lang_info = get_language_info(language)
    return [COMMON_CHANNEL, lang_info['channel']]

def get_language_channel(language: str) -> str:
    """Get the specific channel for a language"""
    lang_info = get_language_info(language)
    return lang_info['channel']

def get_language_display_name(language: str) -> str:
    """Get display name for a language"""
    lang_info = get_language_info(language)
    return f"{lang_info['flag']} {lang_info['display_name']}"