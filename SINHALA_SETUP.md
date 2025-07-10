# Sinhala Subtitle System Setup Guide

## 🎯 **Overview**
Your bot now supports Sinhala subtitles with advanced features:
- ✅ **Sinhala language support** added to your bot
- ✅ **TheMovieDB API integration** for better movie matching
- ✅ **Multiple Sinhala subtitle sources** support
- ✅ **Fallback Sinhala subtitles** when no online sources found
- ✅ **Smart caching system** for Sinhala subtitles

## 🔧 **Required Setup**

### **1. Add Sinhala Channel**
Update your channel ID in `language_config.py`:
```python
'sinhala': {
    'channel': '-1002XXXXXXXXX',  # Replace with your Sinhala channel ID
    'display_name': 'Sinhala',
    'flag': '🇱🇰'
}
```

### **2. Get TheMovieDB API Key**
1. Go to [TheMovieDB](https://www.themoviedb.org/settings/api)
2. Create account and request API key
3. Add to `themoviedb_config.py`:
```python
THEMOVIEDB_API_KEY = "your_api_key_here"
```

### **3. Railway Environment Variables**
Add these to your Railway environment:
```
THEMOVIEDB_API_KEY=your_themoviedb_api_key
```

## 🎬 **How It Works**

### **Sinhala Subtitle Flow:**
1. **User selects Sinhala** → Bot searches cache first
2. **Cache Miss** → Bot searches multiple Sinhala sources:
   - Baiscope.com
   - Zoom.lk
   - Movie Sinhala sites
3. **TheMovieDB Integration** → Gets accurate movie info
4. **Download & Cache** → Stores in Telegram channel
5. **Fallback** → Creates helpful Sinhala subtitle if nothing found

### **Features:**
- **Smart Search**: Uses both English and Sinhala movie names
- **Multiple Sources**: Searches 3+ Sinhala subtitle websites
- **Quality Check**: Validates subtitle file format
- **Auto-Cache**: Saves to channel for future requests
- **Fallback**: Creates informative Sinhala subtitle with instructions

## 🧪 **Testing Commands**

### **For Admins:**
```bash
# Test Sinhala subtitle download
/test_sinhala KGF

# Test TheMovieDB API
/tmdb_test Avengers

# Test regular subtitle with Sinhala
/test_subtitle KGF sinhala
```

### **For Users:**
```bash
# Start bot and select Sinhala
/start

# Search for movie and select Sinhala subtitles
# Bot will automatically use new system
```

## 📊 **Monitoring**

### **Check Performance:**
```bash
# View optimization stats (includes Sinhala)
/optimization_stats

# Check popular movies (includes Sinhala requests)
/popular_movies

# View subtitle statistics
/subtitle_stats
```

## 🔧 **Advanced Configuration**

### **Add More Sinhala Sources:**
Edit `sinhala_subtitle_downloader.py` to add more websites:
```python
SINHALA_SUBTITLE_SOURCES = {
    "your_site": {
        "name": "Your Site",
        "base_url": "https://yoursite.com",
        "search_url": "https://yoursite.com/search",
        "enabled": True
    }
}
```

### **Customize Sinhala Fallback:**
Edit the `create_fallback_sinhala_subtitle()` function to customize the fallback subtitle content.

## 🚀 **Deployment**

### **Files Added:**
- ✅ `sinhala_subtitle_downloader.py` - Main Sinhala subtitle system
- ✅ `themoviedb_config.py` - TheMovieDB API configuration
- ✅ `language_config.py` - Updated with Sinhala support
- ✅ `requirements.txt` - Added BeautifulSoup4 and lxml
- ✅ Updated existing files with Sinhala integration

### **Deploy to Railway:**
```bash
git add .
git commit -m "Add Sinhala subtitle support with TheMovieDB integration"
git push origin main
```

## 🎯 **Expected Results**

### **For Users:**
- 🇱🇰 **Sinhala appears** in language selection
- 🔍 **Better subtitle matching** with TheMovieDB
- 📥 **Real Sinhala subtitles** when available
- 📝 **Helpful fallback** when not available
- ⚡ **Cached subtitles** for faster access

### **For Admins:**
- 📊 **Monitor Sinhala usage** in stats
- 🧪 **Test Sinhala system** with commands
- 🔍 **Debug movie search** with TheMovieDB
- 📈 **Track popular Sinhala movies**

## 🔑 **API Keys Needed**

1. **TheMovieDB API** (Free)
   - Get: https://www.themoviedb.org/settings/api
   - Usage: Movie information and better matching

2. **OpenSubtitles API** (Already configured)
   - Your existing: `Z7wZXFOP8Nty4UrefAdCoidFVPvTBnTy`
   - Usage: Subtitle downloads (200/day limit)

## 📞 **Support**

### **Common Issues:**
- **No API key**: Add TheMovieDB API key to config
- **No Sinhala channel**: Update channel ID in language_config.py
- **Scraping blocked**: Websites may block bots (expected)
- **Fallback subtitles**: Normal when no online sources found

### **Next Steps:**
1. **Create Sinhala channel** and get channel ID
2. **Get TheMovieDB API key** and add to config
3. **Deploy to Railway** with updated code
4. **Test** with `/test_sinhala MovieName`
5. **Monitor** with admin commands

Your bot now has comprehensive Sinhala subtitle support! 🎉