# 🔑 API Keys Setup Guide

To get **real subtitles** from online sources, you should set up these free API keys:

## 📋 Required APIs (All Free!)

### 1. **OpenSubtitles.com API** (Recommended)
- **What it does**: Provides access to millions of real movie subtitles
- **Cost**: FREE (with rate limits)
- **Signup**: https://www.opensubtitles.com/api

**Steps to get API key:**
1. Go to https://www.opensubtitles.com/api
2. Click "Sign Up" and create account
3. Verify your email
4. Go to "My Profile" → "API Keys"
5. Generate a new API key
6. Copy the API key

**Add to your bot:**
1. Open `subtitle_config.py`
2. Replace: `OPENSUBTITLES_API_KEY = ""`
3. With: `OPENSUBTITLES_API_KEY = "your_api_key_here"`

### 2. **TheMovieDB API** (Optional)
- **What it does**: Better movie information and metadata
- **Cost**: FREE
- **Signup**: https://www.themoviedb.org/settings/api

### 3. **OMDb API** (Optional)
- **What it does**: Alternative movie database
- **Cost**: FREE (1000 requests/day)
- **Signup**: http://www.omdbapi.com/apikey.aspx

## ⚙️ Current Setup Status

Without API keys, your bot will:
- ✅ Work perfectly for channel management
- ✅ Cache and serve previously downloaded subtitles
- ⚠️ Show "403 Forbidden" when trying to download new subtitles
- ✅ Create helpful fallback subtitles with instructions

With OpenSubtitles API key, your bot will:
- ✅ Download real subtitles from OpenSubtitles database
- ✅ Access to millions of subtitle files
- ✅ Higher rate limits (200 downloads/day vs 20/day)
- ✅ Priority access during peak times

## 🚀 Quick Setup (2 minutes)

1. **Get OpenSubtitles API key** (most important):
   ```
   https://www.opensubtitles.com/api
   ```

2. **Edit subtitle_config.py**:
   ```python
   OPENSUBTITLES_API_KEY = "your_actual_api_key_here"
   ```

3. **Restart your bot**:
   ```cmd
   c:\Users\yasir\Downloads\movie\.venv\Scripts\python.exe bot.py
   ```

4. **Test with admin command**:
   ```
   /test_subtitle KGF english
   ```

## 📊 Rate Limits

| Service | Without API Key | With API Key |
|---------|----------------|--------------|
| OpenSubtitles | 20 downloads/day | 200 downloads/day |
| Search requests | 40/day | 400/day |
| Priority access | No | Yes |

## 🔧 Troubleshooting

**Getting 403 errors?**
- Add OpenSubtitles API key
- Check if key is valid
- Ensure account is verified

**Still no real subtitles?**
- Check movie name spelling
- Try different language
- Some movies may not have subtitles available

**Bot working but subtitles are placeholders?**
- This is normal when APIs are unavailable
- Users get helpful instructions
- Try again later or add API keys

## ✅ Test Your Setup

Send this command as admin:
```
/test_subtitle KGF english
```

Expected results:
- **With API key**: Real subtitle file from OpenSubtitles
- **Without API key**: Helpful placeholder subtitle with instructions

Your bot works great either way! 🎉