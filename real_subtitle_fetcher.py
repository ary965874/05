#!/usr/bin/env python3
"""
Real Subtitle Fetcher - Multiple sources for actual movie subtitles
"""
import aiohttp
import asyncio
import logging
import re
import json
import os
from typing import Dict, List, Optional
import tempfile
import zipfile
import io

logger = logging.getLogger(__name__)

class RealSubtitleFetcher:
    """Fetch real subtitles from multiple sources"""
    
    def __init__(self):
        self.session = None
        
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    def extract_movie_info(self, filename: str) -> Dict[str, str]:
        """Extract movie info from filename"""
        name = os.path.splitext(filename)[0]
        
        # Clean filename patterns
        patterns = [
            r'(.+?)\.(\d{4})\..*',
            r'(.+?)\.(\d{4})$',
            r'(.+?)\s+(\d{4})',
            r'(.+?)\[(\d{4})\]',
            r'(.+?)\((\d{4})\)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                movie_name = match.group(1).replace('.', ' ').replace('_', ' ').strip()
                year = match.group(2)
                return {'name': movie_name, 'year': year}
        
        movie_name = name.replace('.', ' ').replace('_', ' ').strip()
        return {'name': movie_name, 'year': ''}
    
    async def search_subtitles(self, movie_name: str, language: str = 'en') -> Optional[bytes]:
        """Search and download real subtitles from multiple sources"""
        movie_info = self.extract_movie_info(movie_name)
        
        # Try different sources in order of preference
        sources = [
            self._fetch_from_opensubtitles,
            self._fetch_from_subscene,
            self._fetch_from_yifysubtitles,
            self._fetch_from_subdl
        ]
        
        for source in sources:
            try:
                subtitle_content = await source(movie_info, language)
                if subtitle_content:
                    logger.info(f"Found subtitles from {source.__name__}")
                    return subtitle_content
            except Exception as e:
                logger.error(f"Error with {source.__name__}: {e}")
                continue
        
        logger.warning(f"No real subtitles found for {movie_name} in {language}")
        return None
    
    async def _fetch_from_opensubtitles(self, movie_info: Dict, language: str) -> Optional[bytes]:
        """Fetch from OpenSubtitles (requires API key)"""
        try:
            session = await self.get_session()
            
            # Language mapping
            lang_map = {
                'english': 'en', 'korean': 'ko', 'spanish': 'es', 'french': 'fr',
                'german': 'de', 'italian': 'it', 'portuguese': 'pt', 'chinese': 'zh',
                'japanese': 'ja', 'arabic': 'ar', 'hindi': 'hi', 'tamil': 'ta',
                'malayalam': 'ml', 'telugu': 'te'
            }
            
            lang_code = lang_map.get(language.lower(), 'en')
            
            # OpenSubtitles search
            search_url = "https://api.opensubtitles.com/api/v1/subtitles"
            headers = {
                'User-Agent': 'SubtitleBot v1.0',
                'Api-Key': 'YOUR_API_KEY_HERE'  # Get free API key from opensubtitles.com
            }
            
            params = {
                'query': movie_info['name'],
                'languages': lang_code,
                'type': 'movie'
            }
            
            async with session.get(search_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        # Get first subtitle
                        subtitle = data['data'][0]
                        download_url = subtitle['attributes']['url']
                        
                        # Download subtitle
                        async with session.get(download_url, headers=headers) as dl_response:
                            if dl_response.status == 200:
                                return await dl_response.read()
                                
        except Exception as e:
            logger.error(f"OpenSubtitles error: {e}")
        
        return None
    
    async def _fetch_from_subscene(self, movie_info: Dict, language: str) -> Optional[bytes]:
        """Fetch from Subscene (web scraping)"""
        try:
            session = await self.get_session()
            
            # Search movie on Subscene
            search_query = movie_info['name'].replace(' ', '+')
            search_url = f"https://subscene.com/subtitles/searchbytitle?query={search_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with session.get(search_url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Parse HTML to find subtitle links (simplified)
                    if movie_info['name'].lower() in html.lower():
                        # This would need proper HTML parsing
                        # For now, return None to move to next source
                        pass
                        
        except Exception as e:
            logger.error(f"Subscene error: {e}")
        
        return None
    
    async def _fetch_from_yifysubtitles(self, movie_info: Dict, language: str) -> Optional[bytes]:
        """Fetch from YifySubtitles"""
        try:
            session = await self.get_session()
            
            # Search on YifySubtitles
            search_query = movie_info['name'].replace(' ', '%20')
            search_url = f"https://yifysubtitles.org/search?q={search_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # This would require web scraping implementation
            # For now, return None
            
        except Exception as e:
            logger.error(f"YifySubtitles error: {e}")
        
        return None
    
    async def _fetch_from_subdl(self, movie_info: Dict, language: str) -> Optional[bytes]:
        """Fetch from SubDL"""
        try:
            session = await self.get_session()
            
            # SubDL API (if available)
            # This would need implementation based on their API
            
        except Exception as e:
            logger.error(f"SubDL error: {e}")
        
        return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return [
            'english', 'korean', 'spanish', 'french', 'german', 'italian',
            'portuguese', 'chinese', 'japanese', 'arabic', 'hindi', 'tamil',
            'malayalam', 'telugu'
        ]

# Create global instance
real_subtitle_fetcher = RealSubtitleFetcher()