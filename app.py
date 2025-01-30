import json


from scriptmaker import generate_script
from audiomakereleven import generate_audio, read_script
from transcript import generate_transcript
from sentencetranscript import transcript_to_sentences
from keywordcollector import process_json_file
from mapping import map_keywords_and_timestamps
from searchbytype import search_and_save_by_type
from videomaker import create_video


if __name__ == "__main__":
    # Read the prompt from the summary.txt file
    with open("output/summary.txt", "r") as file:
        prompt = file.read()
    
    # Generate the script using the prompt
    generate_script(prompt)

    # Generate audio from the script
    script_file_path = "output/script.txt"
    script_content = read_script(script_file_path)
    generate_audio(script_content)

    # Generate transcript from the audio file
    audio_file_path = "output/audio.mp3"
    generate_transcript(audio_file_path)

    # generarate sentence transcript
    transcript_file_path = "output/transcript.json"
    transcript_to_sentences(transcript_file_path)

    # keyword collector
    sentence_file_path = "output/sentence_transcript_with_ids.json"  # Replace with your JSON file path
    process_json_file(sentence_file_path)
    
    # keyword to transcript maker mapping
    keywords_file = "output/keywords.json"
    mapping_output_file = "mapped.json"
    
    result = map_keywords_and_timestamps(keywords_file, transcript_file_path, mapping_output_file)
    print(f"Processing complete. Output saved to {mapping_output_file}")

    # search content by type
    search_and_save_by_type(mapping_output_file)

    # video maker
    output_path = 'output_video.mp4'
    try:
        with open(mapping_output_file, 'r') as file:
            data = json.load(file)
        create_video(data, audio_file_path, output_path)
        print(f"Video successfully created at: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")