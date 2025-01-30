import json

def clean_word(word):
    return word.lower().rstrip('.,?!:;\'\"').strip()

def words_match(word1, word2):
    word1 = clean_word(word1)
    word2 = clean_word(word2)
    
    if word1 == word2:
        return True
    if word1.startswith(word2) or word2.startswith(word1):
        return True
    return False

def find_phrase_timestamps(phrase, words_list, last_end_time=0, used_timestamps=None):
    if used_timestamps is None:
        used_timestamps = set()
        
    phrase_words = phrase.lower().split()
    
    cleaned_words = [
        {
            'word': clean_word(entry['word']),
            'start': entry['start'],
            'end': entry['end']
        }
        for entry in words_list
    ]
    
    matches = []
    i = 0
    while i < len(cleaned_words):
        current_word = cleaned_words[i]
        
        if current_word['start'] <= last_end_time:
            i += 1
            continue
            
        if words_match(current_word['word'], phrase_words[0]):
            match_found = True
            phrase_start = current_word['start']
            phrase_end = current_word['end']
            matched_positions = set([i])
            
            if len(phrase_words) > 1:
                remaining_words = phrase_words[1:]
                search_pos = i + 1
                
                for phrase_word in remaining_words:
                    word_found = False
                    while search_pos < len(cleaned_words):
                        if (cleaned_words[search_pos]['start'], cleaned_words[search_pos]['end']) not in used_timestamps:
                            if words_match(cleaned_words[search_pos]['word'], phrase_word):
                                phrase_end = cleaned_words[search_pos]['end']
                                matched_positions.add(search_pos)
                                word_found = True
                                search_pos += 1
                                break
                        search_pos += 1
                    if not word_found:
                        match_found = False
                        break
            
            if match_found:
                timestamp_used = any(
                    (cleaned_words[pos]['start'], cleaned_words[pos]['end']) in used_timestamps 
                    for pos in matched_positions
                )
                if not timestamp_used:
                    matches.append((phrase_start, phrase_end, matched_positions))
        i += 1
    
    if matches:
        matches.sort()
        return matches[0][0], matches[0][1], matches[0][2]
    return (0, 0, set())

def map_keywords_and_timestamps(keywords_file_path, timestamps_file_path, output_file_path):
    with open(keywords_file_path, 'r') as f:
        keywords_data = json.load(f)
    
    with open(timestamps_file_path, 'r') as f:
        timestamps_data = json.load(f)
    
    words_list = timestamps_data.get('words', [])
    
    used_timestamps = set()
    last_end_time = -1  # Initialize to -1 to find earliest matches
    
    combined_data = []
    
    for keyword_entry in keywords_data:
        order_id = keyword_entry['order_id']
        entry_type = keyword_entry['type']
        keyword = keyword_entry['keyword']
        
        start_time, end_time, matched_positions = find_phrase_timestamps(
            keyword, 
            words_list, 
            last_end_time,
            used_timestamps
        )
        
        # Only add entries with valid timestamps (start >= 0 and end > 0)
        if start_time >= 0 and end_time > 0:
            for pos in matched_positions:
                word_entry = words_list[pos]
                used_timestamps.add((word_entry['start'], word_entry['end']))
            
            last_end_time = end_time
            
            # Generate path
            media_types = {
                'text': 'text',
                'gif': 'mp4',
                'image': 'jpg'
            }
            media_type = media_types.get(entry_type, 'other')
            path = f"output/media/{entry_type}/{order_id}.{media_type if media_type != 'text' else 'mp4'}"
            
            combined_entry = {
                "order_id": order_id,
                "type": entry_type,
                "keyword": keyword,
                "start": start_time,
                "end": end_time,
                "path": path
            }
            
            combined_data.append(combined_entry)
    
    # Post-processing adjustments
    if combined_data:
        # Force first entry to start at 0
        combined_data[0]['start'] = 0
        
        # Adjust end times to be 1ms before next start
        for i in range(len(combined_data) - 1):
            combined_data[i]['end'] = combined_data[i+1]['start'] - 1
    
    with open(output_file_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    return combined_data

# Example usage
if __name__ == "__main__":
    keywords_file = "output/keywords.json"
    timestamps_file = "output/transcript.json"
    output_file = "mapped1.json"
    
    result = map_keywords_and_timestamps(keywords_file, timestamps_file, output_file)
    print(f"Processing complete. Output saved to {output_file}")