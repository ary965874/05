#!/usr/bin/env python3
"""
Subtitle Channel Manager - Store and retrieve subtitles from Telegram channels
"""
import asyncio
import logging
import os
import json
import hashlib
from typing import Dict, List, Optional, Tuple
import aiohttp
from hydrogram import Client
from hydrogram.types import Message
from database.users_chats_db import db

logger = logging.getLogger(__name__)

class SubtitleChannelManager:
    """Manage subtitles in Telegram channels"""
    
    def __init__(self, subtitle_channel_id: str = None):
        # Import config
        try:
            from subtitle_config import SUBTITLE_STORAGE_CHANNEL, MAX_CHANNEL_HISTORY_CHECK
            self.subtitle_channel_id = subtitle_channel_id or SUBTITLE_STORAGE_CHANNEL
            self.max_history_check = MAX_CHANNEL_HISTORY_CHECK
        except ImportError:
            self.subtitle_channel_id = subtitle_channel_id or "-1002614174192"
            self.max_history_check = 1000
            
        self.session = None
        self.subtitle_index = {}
        
    async def _get_subtitle_from_db(self, subtitle_key: str) -> Optional[Dict]:
        """Get subtitle info from database"""
        try:
            from database.users_chats_db import db
            # Use MongoDB to store subtitle metadata
            result = db.db.subtitles.find_one({'key': subtitle_key})
            return result
        except Exception as e:
            logger.error(f"Error getting subtitle from DB: {e}")
            return None
    
    async def _save_subtitle_to_db(self, subtitle_key: str, subtitle_info: Dict) -> bool:
        """Save subtitle info to database"""
        try:
            from database.users_chats_db import db
            subtitle_info['key'] = subtitle_key
            # Update or insert
            db.db.subtitles.update_one(
                {'key': subtitle_key},
                {'$set': subtitle_info},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error saving subtitle to DB: {e}")
            return False
        
    async def get_session(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    def clean_movie_name(self, filename: str) -> str:
        """Clean movie name for consistent searching"""
        # Remove file extension and common tags
        name = os.path.splitext(filename)[0]
        name = name.replace('@', '').replace('_', ' ').replace('.', ' ')
        
        # Remove quality tags
        quality_tags = ['HD', '720p', '1080p', '4K', 'BluRay', 'WEB-DL', 'HDTV', 'DVDRip', 'CAMRip']
        for tag in quality_tags:
            name = name.replace(tag, '')
        
        # Clean multiple spaces
        name = ' '.join(name.split())
        return name.strip()
    
    def generate_subtitle_key(self, movie_name: str, language: str) -> str:
        """Generate unique key for subtitle"""
        clean_name = self.clean_movie_name(movie_name).lower()
        return f"{clean_name}_{language.lower()}"
    
    async def get_subtitle(self, client: Client, movie_name: str, language: str) -> Optional[bytes]:
        """Get subtitle - optimized with intelligent API usage"""
        try:
            # Track this request for popularity analysis
            from advanced_subtitle_optimizer import subtitle_optimizer
            await subtitle_optimizer.track_movie_request(movie_name, language)
            
            subtitle_key = self.generate_subtitle_key(movie_name, language)
            
            # STEP 1: Check channel cache first (free)
            cached_subtitle = await self._get_from_channel(client, subtitle_key)
            if cached_subtitle:
                logger.info(f"✅ Cache HIT: Found cached subtitle for {movie_name} ({language})")
                return cached_subtitle
            
            logger.info(f"❌ Cache MISS: No cached subtitle for {movie_name} ({language})")
            
            # STEP 2: Intelligent API decision
            should_use_api = await subtitle_optimizer.should_use_api(movie_name, language)
            
            if should_use_api:
                # STEP 3: Download from APIs (uses quota)
                logger.info(f"🔄 API DOWNLOAD: Downloading new subtitle for {movie_name} ({language})")
                subtitle_content = await self._download_from_apis(movie_name, language)
                
                if subtitle_content:
                    # Save to channel for future use
                    await self._save_to_channel(client, subtitle_key, movie_name, language, subtitle_content)
                    logger.info(f"💾 CACHED: Saved {movie_name} ({language}) for future requests")
                    return subtitle_content
            else:
                logger.info(f"🚫 API SKIP: Conserving API quota for {movie_name} ({language})")
            
            # STEP 4: Create helpful fallback (free)
            logger.warning(f"📝 FALLBACK: Creating helpful subtitle for {movie_name} ({language})")
            fallback_subtitle = self._create_fallback_subtitle(movie_name, language)
            if fallback_subtitle:
                # Save fallback to channel too (for consistency)
                await self._save_to_channel(client, subtitle_key, movie_name, language, fallback_subtitle)
                return fallback_subtitle
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting subtitle: {e}")
            return None
    
    async def _get_from_channel(self, client: Client, subtitle_key: str) -> Optional[bytes]:
        """Check if subtitle exists in channel using bot-compatible method"""
        try:
            # Since bots can't use get_chat_history, we'll use a different approach
            # We'll maintain a simple database of uploaded subtitles
            from database.users_chats_db import db
            
            # Try to get from our subtitle tracking database
            subtitle_info = await self._get_subtitle_from_db(subtitle_key)
            if subtitle_info and subtitle_info.get('message_id'):
                try:
                    # Try to get the message by ID
                    message = await client.get_messages(self.subtitle_channel_id, subtitle_info['message_id'])
                    if message and message.document:
                        # Download the subtitle file
                        file_path = await message.download(in_memory=True)
                        if isinstance(file_path, bytes):
                            return file_path
                        else:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                            os.remove(file_path)  # Clean up temp file
                            return content
                except Exception as e:
                    logger.error(f"Error downloading subtitle from message ID: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking channel for subtitle: {e}")
            return None
    
    async def _save_to_channel(self, client: Client, subtitle_key: str, movie_name: str, 
                              language: str, subtitle_content: bytes) -> bool:
        """Save subtitle to channel"""
        try:
            # Create filename
            filename = f"{subtitle_key}.srt"
            
            # Create temporary file
            temp_path = f"temp_{filename}"
            with open(temp_path, 'wb') as f:
                f.write(subtitle_content)
            
            # Upload to channel with descriptive caption
            caption = (f"🎬 **{movie_name}**\n"
                      f"🗣️ **Language**: {language.title()}\n"
                      f"📝 **Subtitle File**\n"
                      f"🔍 **Key**: `{subtitle_key}`")
            
            message = await client.send_document(
                chat_id=self.subtitle_channel_id,
                document=temp_path,
                file_name=filename,
                caption=caption
            )
            
            # Save message info to database for future retrieval
            if message:
                await self._save_subtitle_to_db(subtitle_key, {
                    'message_id': message.id,
                    'filename': filename,
                    'movie_name': movie_name,
                    'language': language,
                    'file_size': len(subtitle_content)
                })
            
            # Clean up temp file
            os.remove(temp_path)
            
            logger.info(f"Saved subtitle to channel: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving subtitle to channel: {e}")
            return False
    
    async def _download_from_apis(self, movie_name: str, language: str) -> Optional[bytes]:
        """Download subtitle from various APIs"""
        try:
            # Try different subtitle sources
            sources = [
                self._download_from_opensubtitles,
                self._download_from_alternative_api,
                self._download_from_yts_api
            ]
            
            for source in sources:
                try:
                    result = await source(movie_name, language)
                    if result:
                        return result
                except Exception as e:
                    logger.error(f"Error with {source.__name__}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error downloading from APIs: {e}")
            return None
    
    async def _download_from_opensubtitles(self, movie_name: str, language: str) -> Optional[bytes]:
        """Download from OpenSubtitles API"""
        try:
            session = await self.get_session()
            
            # Language mapping
            lang_codes = {
                'english': 'en', 'korean': 'ko', 'spanish': 'es', 'french': 'fr',
                'german': 'de', 'italian': 'it', 'portuguese': 'pt', 'chinese': 'zh',
                'japanese': 'ja', 'arabic': 'ar', 'hindi': 'hi', 'tamil': 'ta',
                'malayalam': 'ml', 'telugu': 'te'
            }
            
            lang_code = lang_codes.get(language.lower(), 'en')
            clean_name = self.clean_movie_name(movie_name)
            
            # Use the new OpenSubtitles API v1 (requires API key)
            search_url = "https://api.opensubtitles.com/api/v1/subtitles"
            
            # Get API key from config
            try:
                from subtitle_config import OPENSUBTITLES_API_KEY, OPENSUBTITLES_USER_AGENT
                api_key = OPENSUBTITLES_API_KEY
                user_agent = OPENSUBTITLES_USER_AGENT
            except ImportError:
                api_key = ""
                user_agent = "SubtitleBot v1.0"
            
            headers = {
                'User-Agent': user_agent,
                'Content-Type': 'application/json'
            }
            
            # API key is required for the new API
            if not api_key:
                logger.warning("OpenSubtitles API key is required for the new API v1")
                return None
                
            headers['Api-Key'] = api_key
            logger.info("Using OpenSubtitles API v1 with authentication")
            
            # Search parameters for the new API
            params = {
                'query': clean_name,
                'languages': lang_code,
                'type': 'movie'
            }
            
            try:
                async with session.get(search_url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data and data.get('data') and len(data['data']) > 0:
                            # Get first result
                            subtitle_info = data['data'][0]
                            attributes = subtitle_info.get('attributes', {})
                            files = attributes.get('files', [])
                            
                            if files and len(files) > 0:
                                file_id = files[0].get('file_id')
                                if file_id:
                                    # Download the subtitle using the download endpoint
                                    download_url = f"https://api.opensubtitles.com/api/v1/download"
                                    download_data = {
                                        'file_id': file_id,
                                        'sub_format': 'srt'
                                    }
                                    
                                    async with session.post(download_url, headers=headers, json=download_data) as dl_response:
                                        if dl_response.status == 200:
                                            dl_result = await dl_response.json()
                                            file_url = dl_result.get('link')
                                            if file_url:
                                                # Download the actual subtitle file
                                                async with session.get(file_url) as file_response:
                                                    if file_response.status == 200:
                                                        content = await file_response.read()
                                                        logger.info(f"Successfully downloaded subtitle from OpenSubtitles API v1")
                                                        return content
                    elif response.status == 401:
                        logger.error(f"OpenSubtitles API: Invalid API key")
                    elif response.status == 403:
                        logger.warning(f"OpenSubtitles API: Access forbidden - check API key permissions")
                    elif response.status == 429:
                        logger.warning(f"OpenSubtitles API: Rate limited")
                    else:
                        logger.warning(f"OpenSubtitles API returned status {response.status}")
                        
            except Exception as e:
                logger.error(f"Error with OpenSubtitles API v1: {e}")
                                    
        except Exception as e:
            logger.error(f"OpenSubtitles API error: {e}")
        
        return None
    
    async def _download_from_alternative_api(self, movie_name: str, language: str) -> Optional[bytes]:
        """Download from alternative subtitle APIs"""
        try:
            session = await self.get_session()
            
            # Try SubDB API (example)
            clean_name = self.clean_movie_name(movie_name)
            api_url = f"http://api.thesubdb.com/?action=search&query={clean_name}"
            
            headers = {'User-Agent': 'SubDB/1.0 (SubtitleBot/1.0; http://github.com/subtitlebot)'}
            
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    # Process response based on API format
                    # This is a placeholder - implement based on actual API
                    pass
                    
        except Exception as e:
            logger.error(f"Alternative API error: {e}")
        
        return None
    
    async def _download_from_yts_api(self, movie_name: str, language: str) -> Optional[bytes]:
        """Download from YTS subtitles API"""
        try:
            session = await self.get_session()
            
            # YTS subtitles API (if available)
            clean_name = self.clean_movie_name(movie_name)
            # Implement YTS API calls here
            
        except Exception as e:
            logger.error(f"YTS API error: {e}")
        
        return None
    
    async def search_channel_subtitles(self, client: Client, movie_name: str) -> List[Dict]:
        """Search available subtitles in database for a movie"""
        try:
            from database.users_chats_db import db
            clean_name = self.clean_movie_name(movie_name).lower()
            
            # Search in database instead of channel history
            cursor = db.db.subtitles.find({
                'movie_name': {'$regex': clean_name, '$options': 'i'}
            })
            
            found_subtitles = []
            for subtitle in cursor:
                found_subtitles.append({
                    'language': subtitle.get('language', 'unknown'),
                    'filename': subtitle.get('filename', ''),
                    'message_id': subtitle.get('message_id', 0),
                    'file_size': subtitle.get('file_size', 0)
                })
            
            return found_subtitles
            
        except Exception as e:
            logger.error(f"Error searching channel subtitles: {e}")
            return []
    
    async def get_subtitle_stats(self, client: Client) -> Dict:
        """Get statistics about stored subtitles from database"""
        try:
            from database.users_chats_db import db
            
            # Get stats from database instead of channel
            stats = {
                'total_subtitles': 0,
                'languages': {},
                'unique_movies': 0
            }
            
            # Count total subtitles
            total_count = db.db.subtitles.count_documents({})
            stats['total_subtitles'] = total_count
            
            # Count by language
            pipeline = [
                {'$group': {'_id': '$language', 'count': {'$sum': 1}}}
            ]
            
            language_counts = db.db.subtitles.aggregate(pipeline)
            for item in language_counts:
                if item['_id']:
                    stats['languages'][item['_id']] = item['count']
            
            # Count unique movies
            unique_movies = len(db.db.subtitles.distinct('movie_name'))
            stats['unique_movies'] = unique_movies
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting subtitle stats: {e}")
            return {}
    
    def _create_fallback_subtitle(self, movie_name: str, language: str) -> bytes:
        """Create a helpful fallback subtitle when APIs fail"""
        clean_movie = self.clean_movie_name(movie_name)
        
        # Create informative subtitle content
        subtitle_content = f"""1
00:00:01,000 --> 00:00:05,000
🎬 {clean_movie}

2
00:00:06,000 --> 00:00:10,000
{language.title()} Subtitles

3
00:00:12,000 --> 00:00:16,000
⚠️ Real subtitles not available from online sources

4
00:00:18,000 --> 00:00:22,000
This is a placeholder subtitle file

5
00:00:24,000 --> 00:00:28,000
📋 Movie: {clean_movie}

6
00:00:30,000 --> 00:00:34,000
🗣️ Language: {language.title()}

7
00:00:36,000 --> 00:00:40,000
💡 To get real subtitles:

8
00:00:42,000 --> 00:00:46,000
1. Check if movie name is correct

9
00:00:48,000 --> 00:00:52,000
2. Try a different language

10
00:00:54,000 --> 00:00:58,000
3. Contact admin for manual subtitle upload

11
00:01:00,000 --> 00:01:04,000
✅ Bot is working correctly

12
00:01:06,000 --> 00:01:10,000
🤖 Subtitle system operational

13
00:01:12,000 --> 00:01:16,000
📱 Report issues to bot admin

14
00:01:18,000 --> 00:01:22,000
🔍 Subtitle APIs may be temporarily unavailable

15
00:01:24,000 --> 00:01:28,000
⏰ Try again later for real subtitles
"""
        
        return subtitle_content.encode('utf-8')

# Global instance
subtitle_channel_manager = SubtitleChannelManager()