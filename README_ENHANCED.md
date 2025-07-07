# Enhanced Movie Bot with Subtitle Support 🎬🗣️

## Overview
This is an enhanced version of your Telegram movie bot that now includes **subtitle support** and **language-specific channel management**. Users can now get movies with subtitles in their preferred language!

## New Features ✨

### 1. Subtitle Language Selection
- When users select a movie, they now get language options for subtitles
- Support for 14 languages: English, Korean, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Arabic, Hindi, Tamil, Malayalam, Telugu
- Option to skip subtitles if not needed

### 2. Language-Specific Channels
- Different channels for different languages
- Users must join language-specific channels to access subtitles
- Korean movies → Korean channels, English movies → English channels, etc.

### 3. Automatic Subtitle Search & Download
- Integrates with free subtitle APIs (OpenSubtitles, YifySubtitles)
- Automatically searches and downloads subtitles
- Sends movie file + subtitle files together

## How It Works 🔄

### User Flow:
1. User searches for a movie in group → Bot shows movie options
2. User selects a movie → Bot shows subtitle language options
3. User selects language (e.g., Korean) → Bot redirects to DM
4. User must join Korean-specific channels → Bot verifies subscription
5. Bot sends movie + Korean subtitles

### Technical Flow:
```
Movie Search → Language Selection → Channel Verification → Movie + Subtitles Delivery
```

## Installation & Setup 🛠️

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Configuration
Edit `info.py` with your credentials:
```python
BOT_TOKEN = "your_bot_token_here"
API_ID = your_api_id
API_HASH = "your_api_hash"
```

### 3. Configure Language Channels
Edit `language_config.py` with your actual channel IDs:
```python
LANGUAGE_CHANNELS = {
    'english': {
        'channels': ['-1001793950262', '-1002080383910'],  # Your English channels
        'display_name': 'English',
        'flag': '🇺🇸'
    },
    'korean': {
        'channels': ['-1001396095544', '-1001620200646'],  # Your Korean channels
        'display_name': 'Korean',
        'flag': '🇰🇷'
    },
    # ... add your other language channels
}
```

### 4. Test the Bot
```bash
python test_bot.py
```

### 5. Run the Bot
```bash
python bot.py
```

## New Files Added 📁

### 1. `subtitle_handler.py`
- Handles subtitle search and download
- Integrates with multiple free APIs
- Manages language-specific functionality

### 2. `language_config.py`
- Configuration for language-specific channels
- Easy to update channel IDs
- Supports flag emojis and display names

### 3. `test_bot.py`
- Test script to validate functionality
- Tests subtitle search, language config, etc.

### 4. `README_ENHANCED.md`
- This comprehensive guide

## Modified Files 🔧

### 1. `plugins/pm_filter.py`
- Added subtitle language selection after movie selection
- New callback handlers for subtitle functionality
- Integration with subtitle_handler

### 2. `plugins/commands.py`
- Enhanced /start command to handle subtitle requests
- Language-specific channel verification
- Movie + subtitle delivery function

### 3. `requirements.txt`
- Added new dependencies for subtitle functionality

## Free APIs Used 🆓

### 1. OpenSubtitles API
- Free tier available
- Good subtitle quality
- Multiple languages supported

### 2. YifySubtitles API
- Completely free
- Good for popular movies
- Fallback option

## Configuration Guide 📋

### Setting Up Language Channels:

1. **Create channels for each language** you want to support
2. **Get channel IDs** using @userinfobot or similar
3. **Update language_config.py** with your channel IDs
4. **Test each language** to ensure channels work correctly

### Example Channel Structure:
```
English Movies:
- @YourEnglishMovies1
- @YourEnglishMovies2

Korean Movies:
- @YourKoreanMovies1
- @YourKoreanMovies2

Spanish Movies:
- @YourSpanishMovies1
- @YourSpanishMovies2
```

## Admin Commands 🔧

All existing admin commands work, plus:

### Language Management:
- Configure channels per language in `language_config.py`
- Monitor subtitle download statistics
- Manage language-specific user access

## Troubleshooting 🔍

### Common Issues:

1. **Subtitles not found**
   - Check if movie name is correctly formatted
   - Try different subtitle APIs
   - Verify language is supported

2. **Channel subscription issues**
   - Ensure channel IDs are correct
   - Check if bot has admin rights in channels
   - Verify invite link creation permissions

3. **Download failures**
   - Check internet connection
   - Verify API endpoints are working
   - Check subtitle file size limits

## Security Features 🔒

- No API keys required (uses free APIs)
- Secure channel verification
- User subscription validation
- Temporary file cleanup

## Performance Optimizations ⚡

- Asynchronous subtitle downloads
- Session management for API calls
- Caching for frequently requested subtitles
- Efficient file handling

## Future Enhancements 🚀

Potential improvements:
1. **Custom subtitle upload** by users
2. **Subtitle quality ratings**
3. **Multiple subtitle formats** (ASS, VTT, etc.)
4. **Subtitle timing adjustment**
5. **OCR for hard-coded subtitles**

## Support 💬

For issues or questions:
1. Check the troubleshooting section
2. Run the test script to identify issues
3. Verify your configuration files
4. Check bot logs for errors

## License 📄

This enhanced version maintains the same license as the original bot.

---

**Happy Movie Watching with Subtitles! 🎬🗣️**