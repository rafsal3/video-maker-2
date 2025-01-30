import json
import os
import re

def transcript_to_sentences(file_path):
    """
    Converts a word-by-word transcript into a sentence-by-sentence transcript and adds primary IDs.

    Args:
        file_path (str): The path to the input transcript JSON file.

    Returns:
        str: The path to the output JSON file with sentence-level transcripts including primary IDs.
    """
    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the transcript JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    text = data.get("text", "")
    words = data.get("words", [])
    
    # Split the text into sentences using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    sentence_transcripts = []
    sentence_start_index = 0
    
    # Match sentences with timestamps
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_start_time = words[sentence_start_index]["start"]
        sentence_end_time = None
        
        word_count = len(sentence.split())
        sentence_words = words[sentence_start_index:sentence_start_index + word_count]
        
        # Adjust the end timestamp based on the last word in the sentence
        if sentence_words:
            sentence_end_time = sentence_words[-1]["end"]
        
        sentence_transcripts.append({
            "sentence": sentence,
            "start": sentence_start_time,
            "end": sentence_end_time
        })
        
        sentence_start_index += word_count
    
    # Add primary IDs to each sentence
    for index, sentence in enumerate(sentence_transcripts, start=1):
        sentence['id'] = index
    
    # Define the output file path
    output_path = os.path.join(output_dir, "sentence_transcript_with_ids.json")
    
    # Save the sentence-level transcripts with IDs to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(sentence_transcripts, json_file, ensure_ascii=False, indent=4)
    
    return output_path

if __name__ == "__main__":
    # Path to the input JSON file
    file_path = "output/transcript.json"
    
    # Generate sentence-level transcripts with primary IDs
    transcript_to_sentences(file_path)