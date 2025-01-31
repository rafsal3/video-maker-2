# from textvideo import create_video_for_single_keyword
# from searchandsave import search_and_save_image_google,search_and_save_image_unsplash,search_and_save_GIF
# from searchbytype import search_and_save_by_type
# from audiomakereleven import generate_audio
# from sentencetranscript import transcript_to_sentences
# from keywordcollector import process_json_file
# from mapping import map_keywords_and_timestamps
from videomakercopy import create_video
from searchbytype import search_and_save_by_type
import json
if __name__ == "__main__":
    # output_path = "output/image3.mp4"
    # create_video_for_single_keyword("Hello world",output_path ,font_color=(0,0,0),bg_color=(255, 255, 255))
    # search_and_save_image_google("elon musk",output_path)
    # search_and_save_image_unsplash("elon musk",output_path)
    # search_and_save_GIF("elon musk smile",output_path)
    # search_and_save_by_type("keyword.json")
    # generate_transcript("output/audio.mp3")
    # transcript_to_sentences("output/transcript.json")
    # process_json_file("output/sentence_transcript_with_ids.json")
    # keyword to transcript maker mapping
    # keywords_file = "output/keywords.json"
    mapping_output_file = "output/mapped.json"
    # transcript_file_path = "output/transcript.json"
    
    # result = map_keywords_and_timestamps(keywords_file, transcript_file_path, mapping_output_file)
    # print(f"Processing complete. Output saved to {mapping_output_file}")
    # search content by type
    # search_and_save_by_type(mapping_output_file)
    output_path = 'output_video.mp4'
    audio_file_path = "output/audio.mp3"
    try:
        with open(mapping_output_file, 'r') as file:
            data = json.load(file)
        create_video(data, audio_file_path, output_path)
        print(f"Video successfully created at: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")