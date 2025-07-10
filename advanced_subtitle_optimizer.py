#!/usr/bin/env python3
"""
Advanced Subtitle Optimizer - Maximize API efficiency and user capacity
"""
import logging
import asyncio
from typing import Dict, List, Optional, Set
from database.users_chats_db import db
import hashlib
import time

logger = logging.getLogger(__name__)

class SubtitleOptimizer:
    """Advanced subtitle optimization strategies"""
    
    def __init__(self):
        # Track popular requests to prioritize caching
        self.request_counter = {}
        self.daily_api_usage = 0
        self.api_limit = 200
        self.cache_hit_ratio = 0.0
        
    async def should_use_api(self, movie_name: str, language: str) -> bool:
        """Intelligent decision: should we use API or create fallback?"""
        
        # Check current API usage
        current_usage = await self.get_daily_api_usage()
        remaining = self.api_limit - current_usage
        
        # Priority rules for API usage
        if remaining <= 0:
            logger.warning("API limit reached, using fallback subtitles")
            return False
        
        # Save API calls for popular movies (more likely to be requested again)
        popularity_score = await self.get_movie_popularity(movie_name)
        
        # Use different thresholds based on remaining quota
        if remaining > 100:  # Plenty of quota left
            return True
        elif remaining > 50:  # Moderate quota - be selective
            return popularity_score > 2  # Only if movie requested 2+ times
        elif remaining > 20:  # Low quota - very selective
            return popularity_score > 5  # Only for very popular movies
        else:  # Very low quota - emergency mode
            return popularity_score > 10  # Only for extremely popular movies
    
    async def get_movie_popularity(self, movie_name: str) -> int:
        """Get popularity score for a movie (how many times requested)"""
        try:
            movie_key = self.normalize_movie_name(movie_name)
            
            # Check database for request count
            result = db.db.movie_requests.find_one({'movie_key': movie_key})
            if result:
                return result.get('request_count', 0)
            
            return 0
        except Exception as e:
            logger.error(f"Error getting movie popularity: {e}")
            return 0
    
    async def track_movie_request(self, movie_name: str, language: str):
        """Track movie requests to identify popular content"""
        try:
            movie_key = self.normalize_movie_name(movie_name)
            
            # Update request count
            db.db.movie_requests.update_one(
                {'movie_key': movie_key},
                {
                    '$inc': {'request_count': 1},
                    '$set': {
                        'last_requested': time.time(),
                        'movie_name': movie_name,
                        'languages_requested': language
                    },
                    '$addToSet': {'languages': language}
                },
                upsert=True
            )
            
            logger.info(f"Tracked request for {movie_name} ({language})")
            
        except Exception as e:
            logger.error(f"Error tracking movie request: {e}")
    
    async def get_popular_movies(self, limit: int = 20) -> List[Dict]:
        """Get most popular movies for proactive caching"""
        try:
            cursor = db.db.movie_requests.find().sort('request_count', -1).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error getting popular movies: {e}")
            return []
    
    async def get_daily_api_usage(self) -> int:
        """Get current daily API usage from OpenSubtitles"""
        try:
            import aiohttp
            from subtitle_config import OPENSUBTITLES_API_KEY
            
            if not OPENSUBTITLES_API_KEY:
                return 0
            
            async with aiohttp.ClientSession() as session:
                url = "https://api.opensubtitles.com/api/v1/infos/user"
                headers = {
                    'Api-Key': OPENSUBTITLES_API_KEY,
                    'Content-Type': 'application/json',
                    'User-Agent': 'SubtitleBot v1.0'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_info = data.get('data', {})
                        return user_info.get('downloads_count', 0)
            
            return 0
        except Exception as e:
            logger.error(f"Error getting API usage: {e}")
            return 0
    
    def normalize_movie_name(self, movie_name: str) -> str:
        """Normalize movie name for consistent tracking"""
        # Remove common prefixes/suffixes and normalize
        name = movie_name.lower()
        name = name.replace('@', '').replace('_', ' ').replace('.', ' ')
        name = ' '.join(name.split())  # Remove extra spaces
        
        # Remove quality indicators
        quality_terms = ['720p', '1080p', '4k', 'hd', 'bluray', 'webrip', 'dvdrip', 'cam']
        for term in quality_terms:
            name = name.replace(term, '')
        
        return name.strip()
    
    async def suggest_preload_subtitles(self) -> List[Dict]:
        """Suggest popular movies to preload during off-peak hours"""
        try:
            # Get movies with high request count but no cached subtitles
            popular_movies = await self.get_popular_movies(50)
            suggestions = []
            
            for movie in popular_movies:
                movie_key = movie['movie_key']
                
                # Check if we have cached subtitles for popular languages
                for lang in ['english', 'spanish', 'french', 'german', 'sinhala']:
                    cached = db.db.subtitles.find_one({
                        'movie_name': {'$regex': movie_key, '$options': 'i'},
                        'language': lang
                    })
                    
                    if not cached and movie['request_count'] > 3:
                        suggestions.append({
                            'movie_name': movie['movie_name'],
                            'language': lang,
                            'request_count': movie['request_count'],
                            'priority': movie['request_count']
                        })
            
            # Sort by priority (request count)
            suggestions.sort(key=lambda x: x['priority'], reverse=True)
            
            return suggestions[:20]  # Top 20 suggestions
            
        except Exception as e:
            logger.error(f"Error getting preload suggestions: {e}")
            return []
    
    async def get_optimization_stats(self) -> Dict:
        """Get optimization statistics"""
        try:
            # Cache hit ratio
            total_requests = db.db.movie_requests.aggregate([
                {'$group': {'_id': None, 'total': {'$sum': '$request_count'}}}
            ])
            total_count = next(total_requests, {}).get('total', 0)
            
            # Cached subtitles count
            cached_count = db.db.subtitles.count_documents({})
            
            # API usage
            api_usage = await self.get_daily_api_usage()
            
            # Estimate cache hit ratio
            unique_movies = db.db.movie_requests.count_documents({})
            if total_count > 0:
                estimated_cache_hits = total_count - unique_movies
                cache_hit_ratio = (estimated_cache_hits / total_count) * 100
            else:
                cache_hit_ratio = 0
            
            return {
                'total_requests': total_count,
                'cached_subtitles': cached_count,
                'unique_movies': unique_movies,
                'api_usage_today': api_usage,
                'api_remaining': max(0, self.api_limit - api_usage),
                'cache_hit_ratio': cache_hit_ratio,
                'efficiency_score': cache_hit_ratio
            }
            
        except Exception as e:
            logger.error(f"Error getting optimization stats: {e}")
            return {}

# Global instance
subtitle_optimizer = SubtitleOptimizer()