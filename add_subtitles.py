#!/usr/bin/env python3
"""
Add Subtitles Script - Helper to add real subtitle files
"""
import os
import sys
from subtitle_manager import subtitle_manager

def add_single_subtitle():
    """Add a single subtitle file"""
    print("=== Add Single Subtitle ===")
    movie_name = input("Enter movie name: ").strip()
    language = input("Enter language (english/korean/spanish/etc): ").strip()
    year = input("Enter year (optional): ").strip()
    subtitle_file = input("Enter path to subtitle file (.srt): ").strip()
    
    if not os.path.exists(subtitle_file):
        print(f"File not found: {subtitle_file}")
        return
    
    try:
        with open(subtitle_file, 'rb') as f:
            content = f.read()
        
        if subtitle_manager.add_subtitle(movie_name, language, content, year):
            print(f"✅ Added subtitle for {movie_name} ({language})")
        else:
            print("❌ Failed to add subtitle")
    except Exception as e:
        print(f"Error: {e}")

def add_bulk_subtitles():
    """Add subtitles from a directory"""
    print("=== Add Bulk Subtitles ===")
    directory = input("Enter directory path containing .srt files: ").strip()
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return
    
    count = subtitle_manager.bulk_add_from_directory(directory)
    print(f"✅ Added {count} subtitle files")

def list_subtitles():
    """List available subtitles"""
    print("=== Available Subtitles ===")
    movies = subtitle_manager.list_movies()
    
    if not movies:
        print("No subtitles found")
        return
    
    for movie in movies:
        print(f"📁 {movie['movie']}")
        print(f"   Languages: {', '.join(movie['languages'])}")
        print(f"   Total: {movie['count']} subtitles")
        print()

def search_subtitle():
    """Search for subtitles"""
    print("=== Search Subtitles ===")
    query = input("Enter movie name to search: ").strip()
    
    results = subtitle_manager.search_subtitles(query)
    
    if not results:
        print(f"No subtitles found for '{query}'")
        return
    
    print(f"Found subtitles for '{query}':")
    for movie, languages in results.items():
        print(f"📁 {movie}: {', '.join(languages)}")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("📝 Subtitle Manager")
        print("="*50)
        print("1. Add single subtitle")
        print("2. Add bulk subtitles from directory")
        print("3. List all subtitles")
        print("4. Search subtitles")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            add_single_subtitle()
        elif choice == '2':
            add_bulk_subtitles()
        elif choice == '3':
            list_subtitles()
        elif choice == '4':
            search_subtitle()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()