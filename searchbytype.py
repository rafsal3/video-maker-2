import json

from searchandsave import search_and_save_image_google, search_and_save_image_unsplash, search_and_save_GIF
from textvideo import create_video_for_single_keyword


def search_and_save_by_type(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Iterate through each entry in the JSON
    for keyword in data:
        keyword_type = keyword['type']
        keyword_text = keyword['keyword']
        output_path = keyword['path']

        # Calculate duration from start and end timestamps (assuming timestamps are in seconds)
        if keyword['start'] is not None and keyword['end'] is not None:
            duration = (keyword['end'] - keyword['start']) / 1000 # Duration in seconds
            reveal_time = duration / 5
        else:
            print(f"Warning: Missing start or end time for keyword: {keyword_text}")
            duration = 0  # Default duration if timestamps are missing

        # Call the appropriate function based on the type
        if keyword_type == 'image':
            # Try Unsplash first, fallback to Google if Unsplash fails
            if not search_and_save_image_unsplash(keyword_text, output_path):
                search_and_save_image_google(keyword_text, output_path)
        elif keyword_type == 'gif':
            search_and_save_GIF(keyword_text, output_path)
        elif keyword_type == 'text':
            create_video_for_single_keyword(keyword_text, output_path, duration=duration,reveal_time=reveal_time)
        else:
            print(f"Unknown type '{keyword_type}' for keyword: {keyword_text}")

if __name__ == "__main__":
    json_path = 'mapped.json'
    search_and_save_by_type(json_path)