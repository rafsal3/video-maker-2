import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()
unsplash_api_key = os.getenv('UNSPLASH_ACCESS_KEY')
google_api_key = os.getenv('SEARCH_ENGINE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')
tenor_api_key = os.getenv('TENOR_API_KEY')
lmt = 1
ckey = os.getenv('C_KEY')




def search_and_save_image_google(keyword, output_path):
    """
    Searches for an image using Google Custom Search and saves it to the specified output path.
    
    :param keyword: The search keyword for the image.
    :param output_path: The full path, including the filename, where the image will be saved.
    :return: The path of the saved image if successful, otherwise None.
    """
    try:
        # Validate input parameters
        if not google_api_key or not search_engine_id:
            print("API Key and Search Engine ID are required.")
            return None
        
        print(f"Searching for image with keyword: '{keyword}'")
        
        # Ensure the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Google Custom Search API request
        params = {
            "q": keyword,
            "cx": search_engine_id,
            "key": google_api_key,
            "searchType": "image",
            "num": 1
        }
        url = f"https://www.googleapis.com/customsearch/v1?{urlencode(params)}"
        response = requests.get(url)
        
        # Check for API response success
        if response.status_code != 200:
            print(f"Failed to fetch image for keyword '{keyword}': {response.text}")
            return None
        
        response_json = response.json()
        if "items" not in response_json or not response_json["items"]:
            print(f"No images found for keyword '{keyword}'")
            return None
        
        # Get the first image URL
        image_url = response_json["items"][0]["link"]
        print(f"Found image URL: {image_url}")
        
        # Download the image content
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image locally
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved: {output_path}")
            return output_path
        else:
            print(f"Failed to download image from URL: {image_url}")
            return None
    
    except Exception as e:
        print(f"Error during image search and save: {e}")
        return None

    

def search_and_save_image_unsplash(keyword, output_path):

    try:
        print("Collecting images ...")

        # Ensure the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Unsplash API request
        url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={unsplash_api_key}&per_page=1"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch image for keyword '{keyword}': {response.text}")
            return None
        
        results = response.json().get("results", [])
        if not results:
            print(f"No images found for keyword '{keyword}'")
            return None
        
        # Get the first image URL
        image_url = results[0]["urls"]["regular"]
        print(f"Found image URL: {image_url}")

        # Download the image content
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image locally
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved: {output_path}")
            return output_path
        else:
            print(f"Failed to download image from URL: {image_url}")
            return None

    except Exception as e:
        print(f"Error during image search and save: {e}")
        return None


def search_and_save_GIF(search_term, output_path):
    """
    Searches for a GIF using the Tenor API and saves it as an MP4 file to the specified output path.

    :param search_term: The search term for the GIF.
    :param output_path: The full path, including the filename, where the MP4 file will be saved.
    :return: The path of the saved file if successful, otherwise None.
    """
    try:
        # Get the GIF data from the Tenor API
        print(f"Searching for GIF with search term: '{search_term}'")
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={tenor_api_key}&client_key={ckey}&limit={lmt}"
        r = requests.get(url)

        if r.status_code != 200:
            print(f"Failed to fetch GIF data: {r.text}")
            return None

        gif_data = r.json()
        if "results" not in gif_data or not gif_data["results"]:
            print(f"No GIFs found for search term '{search_term}'")
            return None

        # Extract the MP4 URL
        mp4_url = gif_data["results"][0]["media_formats"]["mp4"]["url"]
        print(f"Found MP4 URL: {mp4_url}")

        # Ensure the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Download the MP4 content
        mp4_response = requests.get(mp4_url)
        if mp4_response.status_code == 200:
            # Save the MP4 file locally
            with open(output_path, "wb") as f:
                f.write(mp4_response.content)
            print(f"MP4 file downloaded successfully: {output_path}")
            return output_path
        else:
            print("Failed to download the MP4 file.")
            return None

    except Exception as e:
        print(f"Error during GIF search and save: {e}")
        return None
    
def search_and_save_image_unsplash(keyword, output_path):

    try:
        print("Collecting images ...")

        # Ensure the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Unsplash API request
        url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={unsplash_api_key}&per_page=1"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch image for keyword '{keyword}': {response.text}")
            return None
        
        results = response.json().get("results", [])
        if not results:
            print(f"No images found for keyword '{keyword}'")
            return None
        
        # Get the first image URL
        image_url = results[0]["urls"]["regular"]
        print(f"Found image URL: {image_url}")

        # Download the image content
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image locally
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved: {output_path}")
            return output_path
        else:
            print(f"Failed to download image from URL: {image_url}")
            return None

    except Exception as e:
        print(f"Error during image search and save: {e}")
        return None
    
def search_and_save_GIF(search_term, output_path):
    """
    Searches for a GIF using the Tenor API and saves it as an MP4 file to the specified output path.

    :param search_term: The search term for the GIF.
    :param output_path: The full path, including the filename, where the MP4 file will be saved.
    :return: The path of the saved file if successful, otherwise None.
    """
    try:
        # Get the GIF data from the Tenor API
        print(f"Searching for GIF with search term: '{search_term}'")
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={tenor_api_key}&client_key={ckey}&limit={lmt}"
        r = requests.get(url)

        if r.status_code != 200:
            print(f"Failed to fetch GIF data: {r.text}")
            return None

        gif_data = r.json()
        if "results" not in gif_data or not gif_data["results"]:
            print(f"No GIFs found for search term '{search_term}'")
            return None

        # Extract the MP4 URL
        mp4_url = gif_data["results"][0]["media_formats"]["mp4"]["url"]
        print(f"Found MP4 URL: {mp4_url}")

        # Ensure the directory for output_path exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Download the MP4 content
        mp4_response = requests.get(mp4_url)
        if mp4_response.status_code == 200:
            # Save the MP4 file locally
            with open(output_path, "wb") as f:
                f.write(mp4_response.content)
            print(f"MP4 file downloaded successfully: {output_path}")
            return output_path
        else:
            print("Failed to download the MP4 file.")
            return None

    except Exception as e:
        print(f"Error during GIF search and save: {e}")
        return None