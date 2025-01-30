import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
google_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=google_api_key)

def extract_json_from_response(response_text):
    """
    Extracts valid JSON from the Gemini API response text.
    """
    try:
        # Use regex to find JSON-like content in the response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Parse the JSON string
            return json.loads(json_str)
        else:
            print("No valid JSON found in the response.")
            return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return []

def get_keywords_from_gemini(text):
    """
    Generates keywords for a given sentence using the Google Gemini API.
    Prioritizes types in the order: image > gif > text.
    Ensures each keyword appears only once with a single type.
    Returns a list of keywords with order_id, type, and keyword.
    """
    try:
        # System instruction for Gemini AI
        instruction = """
        You are tasked with processing a sentence and extracting relevant keywords for video content. Each keyword should be assigned an order ID based on its position in the sentence, and you must determine whether it should be represented as text, image, or gif in the video.

        Rules:
        1. Extract meaningful and relevant keywords from the sentence **in the order they appear**.
        2. Assign 'image' for specific objects, products, or visual concepts.
        3. Assign 'gif' for humorous, dynamic, or action-oriented terms.
        4. Assign 'text' for generic phrases, numbers, or descriptive terms.
        5. Assign an 'order_id' to each keyword, starting from 1, based on its position in the sentence.
        6. Ensure each keyword appears only once with a single type.

        Output Format:
        [
            {"order_id": 1, "type": "image", "keyword": "example keyword"},
            {"order_id": 2, "type": "gif", "keyword": "example keyword"},
            {"order_id": 3, "type": "text", "keyword": "example keyword"}
        ]
        """

        # Combine instruction and input text
        prompt = instruction + "\n\nInput Sentence:\n" + text

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Configure safety settings to allow all content
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]

        # Generate content with safety settings
        response = model.generate_content(prompt, safety_settings=safety_settings)

        # Extract the text from the response
        response_text = response.text

        # Extract valid JSON from the response
        keywords_output = extract_json_from_response(response_text)

        # Deduplicate keywords and prioritize types
        deduplicated_keywords = []
        seen_keywords = set()

        for keyword in keywords_output:
            keyword_text = keyword["keyword"]
            if keyword_text not in seen_keywords:
                # Prioritize types: image > gif > text
                if keyword["type"] == "image":
                    deduplicated_keywords.append(keyword)
                elif keyword["type"] == "gif" and not any(k["keyword"] == keyword_text and k["type"] == "image" for k in deduplicated_keywords):
                    deduplicated_keywords.append(keyword)
                elif keyword["type"] == "text" and not any(k["keyword"] == keyword_text and k["type"] in ["image", "gif"] for k in deduplicated_keywords):
                    deduplicated_keywords.append(keyword)

                seen_keywords.add(keyword_text)

        return deduplicated_keywords

    except Exception as e:
        print(f"Error processing Gemini AI response: {e}")
        return []


# Function 1: Process JSON file and generate keywords
def process_json_file(json_file_path):
    """
    Reads the JSON file, processes each sentence, and generates keywords using the Gemini API.
    If no keywords are generated for a sentence, the entire sentence text is used as a keyword with type 'text'.
    Saves the results to a keywords.json file.
    """
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize an empty list to store the results
    results = []
    global_order_id = 1  # Track order_id globally across all sentences

    # Loop through each sentence in the JSON
    for sentence in data:
        text = sentence["sentence"]

        # Get keywords from the Gemini API
        try:
            keywords = get_keywords_from_gemini(text)

            # If no keywords are generated, use the entire sentence text as a keyword with type 'text'
            if not keywords:
                print(f"No keywords generated for sentence: {text}. Using full text as keyword.")
                keywords = [
                    {"order_id": global_order_id, "type": "text", "keyword": text}
                ]
                global_order_id += 1

            # Update order_id for each keyword and add to results
            for keyword in keywords:
                keyword["order_id"] = global_order_id
                results.append(keyword)
                global_order_id += 1

            print("done!")

            # Add a delay to avoid hitting API rate limits
            time.sleep(1)  # Adjust the delay as needed

        except Exception as e:
            print(f"Error processing sentence: {text}: {e}")
            # If an error occurs, use the entire sentence text as a keyword with type 'text'
            results.append({
                "order_id": global_order_id,
                "type": "text",
                "keyword": text
            })
            global_order_id += 1
            continue

    # Save the results to a keywords.json file
    with open("output/keywords.json", "w") as output_file:
        json.dump(results, output_file, indent=4)

    print("Keywords saved to keywords.json")

if __name__ == "__main__":
    # Example usage
    json_file_path = "output/sentence_transcript_with_ids.json"  # Replace with your JSON file path
    process_json_file(json_file_path)