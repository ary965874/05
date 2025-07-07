#!/usr/bin/env python3
"""
Subtitle Configuration - Settings for subtitle channel storage
"""

# Channel where subtitles will be stored
# This should be a channel where the bot has admin permissions
SUBTITLE_STORAGE_CHANNEL = "-1002614174192"  # Use your common channel or create a dedicated one

# Alternative: You can create a dedicated subtitle storage channel
# SUBTITLE_STORAGE_CHANNEL = "-1002XXXXXXXXX"  # Dedicated subtitle channel

# Subtitle API settings
# Get your free API key from: https://www.opensubtitles.com/api
OPENSUBTITLES_API_KEY = "Z7wZXFOP8Nty4UrefAdCoidFVPvTBnTy"  # Add your OpenSubtitles API key here
OPENSUBTITLES_USER_AGENT = "SubtitleBot v1.0"

# API Keys for different subtitle sources (all free):
# 1. OpenSubtitles.com - Main subtitle database
# 2. TheMovieDB.org - For movie information (optional)
# 3. OMDb API - Alternative movie info (optional)

# Cache settings
MAX_SUBTITLE_CACHE_DAYS = 30  # How long to keep subtitles in channel
MAX_CHANNEL_HISTORY_CHECK = 1000  # How many messages to check when searching

# Subtitle quality preferences
PREFERRED_SUBTITLE_SOURCES = [
    "opensubtitles",
    "subscene", 
    "yifysubtitles",
    "subdl"
]

# Language priority (when multiple subtitles available)
LANGUAGE_PRIORITY = {
    'english': 1,
    'korean': 2,
    'spanish': 3,
    'french': 4,
    'german': 5,
    'italian': 6,
    'portuguese': 7,
    'chinese': 8,
    'japanese': 9,
    'arabic': 10,
    'hindi': 11,
    'tamil': 12,
    'malayalam': 13,
    'telugu': 14
}

# Subtitle file naming convention
SUBTITLE_FILENAME_FORMAT = "{movie_key}_{language}.srt"

# Enable/disable features
ENABLE_AUTO_DOWNLOAD = True  # Automatically download subtitles when not found
ENABLE_CHANNEL_STORAGE = True  # Store subtitles in Telegram channel
ENABLE_API_FALLBACK = True  # Try APIs when channel doesn't have subtitle
ENABLE_SUBTITLE_CACHING = True  # Cache subtitles for faster access