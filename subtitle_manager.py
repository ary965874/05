#!/usr/bin/env python3
"""
Subtitle Manager - Manage real subtitle files
"""
import os
import json
import logging
import re
from typing import Dict, List, Optional
import hashlib

logger = logging.getLogger(__name__)

class SubtitleManager:
    """Manage locally stored subtitle files"""
    
    def __init__(self, subtitle_dir: str = "subtitles"):
        self.subtitle_dir = subtitle_dir
        self.index_file = os.path.join(subtitle_dir, "subtitle_index.json")
        self.ensure_directory()
        self.load_index()
    
    def ensure_directory(self):
        """Create subtitle directory if not exists"""
        if not os.path.exists(self.subtitle_dir):
            os.makedirs(self.subtitle_dir)
    
    def load_index(self):
        """Load subtitle index"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
            else:
                self.index = {}
        except Exception as e:
            logger.error(f"Error loading subtitle index: {e}")
            self.index = {}
    
    def save_index(self):
        """Save subtitle index"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving subtitle index: {e}")
    
    def add_subtitle(self, movie_name: str, language: str, subtitle_content: bytes, 
                    year: str = "", quality: str = "") -> bool:
        """Add a subtitle file to the database"""
        try:
            # Create unique filename
            clean_name = self.clean_filename(movie_name)
            filename = f"{clean_name}_{year}_{language}.srt"
            filepath = os.path.join(self.subtitle_dir, filename)
            
            # Save subtitle file
            with open(filepath, 'wb') as f:
                f.write(subtitle_content)
            
            # Add to index
            movie_key = f"{clean_name}_{year}".lower()
            if movie_key not in self.index:
                self.index[movie_key] = {}
            
            self.index[movie_key][language.lower()] = {
                'filename': filename,
                'filepath': filepath,
                'size': len(subtitle_content),
                'quality': quality,
                'year': year
            }
            
            self.save_index()
            logger.info(f"Added subtitle for {movie_name} ({language})")
            return True
            
        except Exception as e:
            logger.error(f"Error adding subtitle: {e}")
            return False
    
    def get_subtitle(self, movie_name: str, language: str, year: str = "") -> Optional[bytes]:
        """Get subtitle file content"""
        try:
            clean_name = self.clean_filename(movie_name)
            movie_key = f"{clean_name}_{year}".lower()
            
            # Try exact match first
            if movie_key in self.index and language.lower() in self.index[movie_key]:
                filepath = self.index[movie_key][language.lower()]['filepath']
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        return f.read()
            
            # Try without year
            movie_key_no_year = clean_name.lower()
            for key in self.index:
                if key.startswith(movie_key_no_year):
                    if language.lower() in self.index[key]:
                        filepath = self.index[key][language.lower()]['filepath']
                        if os.path.exists(filepath):
                            with open(filepath, 'rb') as f:
                                return f.read()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting subtitle: {e}")
            return None
    
    def search_subtitles(self, movie_name: str) -> Dict[str, List[str]]:
        """Search available subtitles for a movie"""
        clean_name = self.clean_filename(movie_name).lower()
        results = {}
        
        for movie_key, languages in self.index.items():
            if clean_name in movie_key:
                for lang in languages.keys():
                    if movie_key not in results:
                        results[movie_key] = []
                    results[movie_key].append(lang)
        
        return results
    
    def list_movies(self) -> List[Dict]:
        """List all movies with subtitles"""
        movies = []
        for movie_key, languages in self.index.items():
            movies.append({
                'movie': movie_key,
                'languages': list(languages.keys()),
                'count': len(languages)
            })
        return movies
    
    def clean_filename(self, filename: str) -> str:
        """Clean filename for consistent storage"""
        # Remove file extension
        name = os.path.splitext(filename)[0]
        # Remove special characters
        name = ''.join(c for c in name if c.isalnum() or c in ' -_')
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        return name
    
    def bulk_add_from_directory(self, source_dir: str) -> int:
        """Add subtitles from a directory"""
        added_count = 0
        
        if not os.path.exists(source_dir):
            logger.error(f"Source directory does not exist: {source_dir}")
            return 0
        
        for filename in os.listdir(source_dir):
            if filename.endswith('.srt'):
                filepath = os.path.join(source_dir, filename)
                try:
                    # Parse filename to extract movie info
                    movie_info = self.parse_subtitle_filename(filename)
                    
                    with open(filepath, 'rb') as f:
                        content = f.read()
                    
                    if self.add_subtitle(
                        movie_info['name'], 
                        movie_info['language'], 
                        content,
                        movie_info.get('year', ''),
                        movie_info.get('quality', '')
                    ):
                        added_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
        
        logger.info(f"Added {added_count} subtitle files")
        return added_count
    
    def parse_subtitle_filename(self, filename: str) -> Dict[str, str]:
        """Parse subtitle filename to extract info"""
        # Remove extension
        name = os.path.splitext(filename)[0]
        
        # Default values
        result = {
            'name': name,
            'language': 'english',
            'year': '',
            'quality': ''
        }
        
        # Try to extract language
        language_patterns = [
            r'\.english\.',
            r'\.korean\.',
            r'\.spanish\.',
            r'\.french\.',
            r'\.german\.',
            r'\.italian\.',
            r'\.portuguese\.',
            r'\.chinese\.',
            r'\.japanese\.',
            r'\.arabic\.',
            r'\.hindi\.',
            r'\.tamil\.',
            r'\.malayalam\.',
            r'\.telugu\.'
        ]
        
        for pattern in language_patterns:
            if pattern.replace('.', '').replace('\\', '') in name.lower():
                result['language'] = pattern.replace('.', '').replace('\\', '')
                break
        
        # Try to extract year
        year_match = re.search(r'(\d{4})', name)
        if year_match:
            result['year'] = year_match.group(1)
        
        # Clean movie name
        clean_name = re.sub(r'\.\w+\.', ' ', name)
        clean_name = re.sub(r'\d{4}', '', clean_name)
        result['name'] = clean_name.strip()
        
        return result

# Global instance
subtitle_manager = SubtitleManager()