from videomaker import create_video
import json
if __name__ == "__main__":
    # Generate transcript from the audio file
    audio_file_path = "output/audio.mp3"
    # generarate sentence transcript
    transcript_file_path = "output/transcript.json"
    # keyword collector
    sentence_file_path = "output/sentence_transcript_with_ids.json" 
    
        # keyword to transcript maker mapping
    keywords_file = "output/keywords.json"
    mapping_output_file = "output/mapped.json"
    
    # search content by type
    # video maker
    output_path = 'output_video.mp4'
    try:
        with open(mapping_output_file, 'r') as file:
            data = json.load(file)
        create_video(data, audio_file_path, output_path)
        print(f"Video successfully created at: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

