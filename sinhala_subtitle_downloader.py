#!/usr/bin/env python3
"""
Sinhala Subtitle Downloader
Integrates with TheMovieDB API and various Sinhala subtitle sources
"""
import logging
import aiohttp
import asyncio
import re
import json
import random
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import base64

logger = logging.getLogger(__name__)

class SinhalaSubtitleDownloader:
    """Download Sinhala subtitles from various sources"""
    
    def __init__(self):
        self.session = None
        self.tmdb_api_key = None
        self.load_config()
        
    def load_config(self):
        """Load configuration"""
        try:
            from themoviedb_config import (
                THEMOVIEDB_API_KEY, 
                THEMOVIEDB_ACCESS_TOKEN,
                THEMOVIEDB_BASE_URL, 
                SINHALA_SUBTITLE_SOURCES,
                USER_AGENTS
            )
            self.tmdb_api_key = THEMOVIEDB_API_KEY
            self.tmdb_access_token = THEMOVIEDB_ACCESS_TOKEN
            self.tmdb_base_url = THEMOVIEDB_BASE_URL
            self.subtitle_sources = SINHALA_SUBTITLE_SOURCES
            self.user_agents = USER_AGENTS
        except ImportError:
            logger.warning("TheMovieDB config not found, using defaults")
            self.tmdb_api_key = ""
            self.tmdb_access_token = ""
            self.tmdb_base_url = "https://api.themoviedb.org/3"
            self.subtitle_sources = {}
            self.user_agents = ['Mozilla/5.0 (compatible; SubtitleBot/1.0)']
    
    async def get_session(self):
        """Get HTTP session"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': random.choice(self.user_agents)
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def clean_movie_name(self, movie_name: str) -> str:
        """Clean movie name for searching"""
        # Remove common tags and clean
        name = re.sub(r'\([^)]*\)', '', movie_name)  # Remove parentheses
        name = re.sub(r'\[[^\]]*\]', '', name)      # Remove brackets
        name = re.sub(r'\d{4}', '', name)           # Remove years
        name = re.sub(r'[^\w\s]', ' ', name)        # Remove special chars
        name = re.sub(r'\s+', ' ', name)            # Clean spaces
        return name.strip()
    
    async def search_movie_tmdb(self, movie_name: str) -> Optional[Dict]:
        """Search movie using TheMovieDB API"""
        try:
            if not self.tmdb_api_key and not self.tmdb_access_token:
                logger.warning("TheMovieDB API key not configured")
                return None
            
            session = await self.get_session()
            clean_name = self.clean_movie_name(movie_name)
            
            url = f"{self.tmdb_base_url}/search/movie"
            
            # Use Bearer token (modern approach) if available, otherwise use API key
            if self.tmdb_access_token:
                headers = {
                    'Authorization': f'Bearer {self.tmdb_access_token}',
                    'Content-Type': 'application/json'
                }
                params = {
                    'query': clean_name,
                    'language': 'en-US'
                }
            else:
                headers = {}
                params = {
                    'api_key': self.tmdb_api_key,
                    'query': clean_name,
                    'language': 'en-US'
                }
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    if results:
                        movie = results[0]  # Get first result
                        return {
                            'id': movie.get('id'),
                            'title': movie.get('title'),
                            'original_title': movie.get('original_title'),
                            'release_date': movie.get('release_date'),
                            'year': movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                            'overview': movie.get('overview'),
                            'poster_path': movie.get('poster_path')
                        }
                        
        except Exception as e:
            logger.error(f"Error searching movie on TMDB: {e}")
        
        return None
    
    async def search_sinhala_subtitles(self, movie_name: str) -> List[Dict]:
        """Search for Sinhala subtitles from various sources"""
        subtitles = []
        
        # Method 1: Try OpenSubtitles for Sinhala (they do have some)
        subtitles.extend(await self._search_opensubtitles_sinhala(movie_name))
        
        # Method 2: Try direct download from known sources
        subtitles.extend(await self._search_baiscope(movie_name))
        subtitles.extend(await self._search_zoom_lk(movie_name))
        subtitles.extend(await self._search_movie_sinhala(movie_name))
        
        # Method 2: Search with TheMovieDB info
        movie_info = await self.search_movie_tmdb(movie_name)
        if movie_info:
            subtitles.extend(await self._search_with_tmdb_info(movie_info))
        
        # Remove duplicates
        unique_subtitles = []
        seen_urls = set()
        
        for subtitle in subtitles:
            if subtitle.get('download_url') not in seen_urls:
                unique_subtitles.append(subtitle)
                seen_urls.add(subtitle.get('download_url'))
        
        return unique_subtitles[:5]  # Return top 5 results
    
    async def _search_opensubtitles_sinhala(self, movie_name: str) -> List[Dict]:
        """Search OpenSubtitles for Sinhala subtitles"""
        try:
            # Use the existing OpenSubtitles integration from subtitle_channel_manager
            from subtitle_channel_manager import subtitle_channel_manager
            
            clean_name = self.clean_movie_name(movie_name)
            
            # Try to use the OpenSubtitles API for Sinhala
            subtitle_content = await subtitle_channel_manager._download_from_opensubtitles(clean_name, 'sinhala')
            
            if subtitle_content:
                return [{
                    'title': f"{clean_name} - Sinhala Subtitle",
                    'source': 'OpenSubtitles',
                    'download_url': 'opensubtitles_direct',  # Special marker
                    'language': 'sinhala',
                    'quality': 'good',
                    'content': subtitle_content  # Store the actual content
                }]
                
        except Exception as e:
            logger.error(f"Error searching OpenSubtitles for Sinhala: {e}")
        
        return []
    
    async def _search_baiscope(self, movie_name: str) -> List[Dict]:
        """Search Baiscope for Sinhala subtitles"""
        try:
            session = await self.get_session()
            clean_name = self.clean_movie_name(movie_name)
            
            # Try multiple search approaches
            search_queries = [
                clean_name,
                clean_name.replace(' ', '+'),
                clean_name.lower()
            ]
            
            for query in search_queries:
                try:
                    search_url = f"https://baiscope.com/search"
                    params = {'q': query}
                    
                    async with session.get(search_url, params=params) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # Basic subtitle link detection (this would need real website analysis)
                            if 'sinhala' in html.lower() or 'subtitle' in html.lower():
                                # Create a mock result for testing
                                return [{
                                    'title': f"{clean_name} - Sinhala Subtitle",
                                    'source': 'Baiscope',
                                    'download_url': f"https://baiscope.com/download/{quote(clean_name)}.srt",
                                    'language': 'sinhala',
                                    'quality': 'good'
                                }]
                                
                except Exception as e:
                    logger.error(f"Error with query '{query}': {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching Baiscope: {e}")
        
        return []
    
    async def _search_zoom_lk(self, movie_name: str) -> List[Dict]:
        """Search Zoom.lk for Sinhala subtitles"""
        try:
            session = await self.get_session()
            clean_name = self.clean_movie_name(movie_name)
            
            # Placeholder for Zoom.lk search
            # You'd implement actual website scraping here
            return []
            
        except Exception as e:
            logger.error(f"Error searching Zoom.lk: {e}")
        
        return []
    
    async def _search_movie_sinhala(self, movie_name: str) -> List[Dict]:
        """Search Movie Sinhala for subtitles"""
        try:
            session = await self.get_session()
            clean_name = self.clean_movie_name(movie_name)
            
            # Placeholder for Movie Sinhala search
            # You'd implement actual website scraping here
            return []
            
        except Exception as e:
            logger.error(f"Error searching Movie Sinhala: {e}")
        
        return []
    
    async def _search_with_tmdb_info(self, movie_info: Dict) -> List[Dict]:
        """Search using TheMovieDB movie information"""
        try:
            # Use both title and original title for better matching
            titles_to_search = [movie_info['title']]
            if movie_info.get('original_title') and movie_info['original_title'] != movie_info['title']:
                titles_to_search.append(movie_info['original_title'])
            
            subtitles = []
            for title in titles_to_search:
                # Add year for better matching
                search_term = f"{title} {movie_info['year']}" if movie_info['year'] else title
                subtitles.extend(await self._search_baiscope(search_term))
                subtitles.extend(await self._search_zoom_lk(search_term))
                subtitles.extend(await self._search_movie_sinhala(search_term))
            
            return subtitles
            
        except Exception as e:
            logger.error(f"Error searching with TMDB info: {e}")
        
        return []
    
    async def download_subtitle(self, subtitle_info: Dict) -> Optional[bytes]:
        """Download subtitle file"""
        try:
            # Check if this is a direct content subtitle (from OpenSubtitles)
            if subtitle_info.get('content'):
                return subtitle_info['content']
            
            session = await self.get_session()
            download_url = subtitle_info.get('download_url')
            
            if not download_url:
                return None
            
            # Handle special markers
            if download_url == 'opensubtitles_direct':
                # Already handled above with direct content
                return None
            
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # Validate that it's a subtitle file
                    if self._is_valid_subtitle(content):
                        return content
                    
        except Exception as e:
            logger.error(f"Error downloading subtitle: {e}")
        
        return None
    
    def _is_valid_subtitle(self, content: bytes) -> bool:
        """Check if content is a valid subtitle file"""
        try:
            text = content.decode('utf-8', errors='ignore')
            
            # Check for common subtitle patterns
            subtitle_patterns = [
                r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}',  # SRT format
                r'\d{2}:\d{2}:\d{2}\.\d{2} --> \d{2}:\d{2}:\d{2}\.\d{2}',  # WebVTT format
                r'{\d+}{\d+}',  # MicroDVD format
            ]
            
            for pattern in subtitle_patterns:
                if re.search(pattern, text):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def create_fallback_sinhala_subtitle(self, movie_name: str) -> bytes:
        """Create fallback Sinhala subtitle when no subtitles found"""
        clean_movie = self.clean_movie_name(movie_name)
        
        subtitle_content = f"""1
00:00:01,000 --> 00:00:05,000
🎬 {clean_movie}

2
00:00:06,000 --> 00:00:10,000
සිංහල උපසිරැස

3
00:00:12,000 --> 00:00:16,000
⚠️ අන්තර්ජාල මූලාශ්‍රවලින් සැබෑ උපසිරැසි නොමැත

4
00:00:18,000 --> 00:00:22,000
මෙය තැනකරුක් උපසිරැසි ගොනුවකි

5
00:00:24,000 --> 00:00:28,000
📋 චිත්‍රපටය: {clean_movie}

6
00:00:30,000 --> 00:00:34,000
🗣️ භාෂාව: සිංහල

7
00:00:36,000 --> 00:00:40,000
💡 සැබෑ උපසිරැසි ලබා ගැනීමට:

8
00:00:42,000 --> 00:00:46,000
1. චිත්‍රපට නම නිවැරදිද කීපා බලන්න

9
00:00:48,000 --> 00:00:52,000
2. වෙනත් භාෂාවකින් උත්සහා කරන්න

10
00:00:54,000 --> 00:00:58,000
3. හස්තීය උපසිරැසි උඩුගත කිරීම සඳහා පරිපාලකයා සම්බන්ධ කරන්න

11
00:01:00,000 --> 00:01:04,000
✅ බොට් නිවැරදිව ක්‍රියාත්මක වේ

12
00:01:06,000 --> 00:01:10,000
🤖 උපසිරැසි පද්ධතිය ක්‍රියාත්මකයි

13
00:01:12,000 --> 00:01:16,000
📱 ගැටලු සඳහා බොට් පරිපාලකයා වෙත වාර්තා කරන්න

14
00:01:18,000 --> 00:01:22,000
🔍 උපසිරැසි API තාවකාලිකව නොමැතිවිය හැක

15
00:01:24,000 --> 00:01:28,000
⏰ සැබෑ උපසිරැසි සඳහා පසුව නැවත උත්සහා කරන්න
"""
        
        return subtitle_content.encode('utf-8')

# Global instance
sinhala_subtitle_downloader = SinhalaSubtitleDownloader()