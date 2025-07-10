#!/usr/bin/env python3
"""
TheMovieDB API Configuration
Get free API key from: https://www.themoviedb.org/settings/api
"""

# TheMovieDB API Configuration
THEMOVIEDB_API_KEY = "a10369582ffb6e9ac4f8cf60f5dbd2b0"  # Your TheMovieDB API key
THEMOVIEDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMTAzNjk1ODJmZmI2ZTlhYzRmOGNmNjBmNWRiZDJiMCIsIm5iZiI6MTc1MjEzNzA2Mi44MjIsInN1YiI6IjY4NmY3ZDY2ZTU2YzQ3YTg0YzZlOTNhNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ksrQRh-duDz-u3xzYgnLqSO9a4HsXCGKYVp7-_z5goc"  # API Read Access Token
THEMOVIEDB_BASE_URL = "https://api.themoviedb.org/3"
THEMOVIEDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Sinhala Subtitle Sources
SINHALA_SUBTITLE_SOURCES = {
    "baiscope": {
        "name": "Baiscope",
        "base_url": "https://baiscope.com",
        "search_url": "https://baiscope.com/search",
        "enabled": True
    },
    "zoom_lk": {
        "name": "Zoom.lk",
        "base_url": "https://zoom.lk",
        "search_url": "https://zoom.lk/search",
        "enabled": True
    },
    "movie_sinhala": {
        "name": "Movie Sinhala",
        "base_url": "https://moviesinhala.com",
        "search_url": "https://moviesinhala.com/search",
        "enabled": True
    }
}

# Language codes for TheMovieDB
TMDB_LANGUAGE_CODES = {
    'english': 'en',
    'korean': 'ko',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'chinese': 'zh',
    'japanese': 'ja',
    'arabic': 'ar',
    'hindi': 'hi',
    'tamil': 'ta',
    'malayalam': 'ml',
    'telugu': 'te',
    'sinhala': 'si'
}

# Sinhala subtitle file extensions
SINHALA_SUBTITLE_EXTENSIONS = ['.srt', '.ass', '.vtt', '.sub']

# User agents for web scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]