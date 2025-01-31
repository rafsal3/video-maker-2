import json
from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import freeze

# Define the resolution for the final video
VIDEO_RESOLUTION = (1080, 1920)

def create_clip(keyword_data):
    try:
        print(f"Loading file from: {keyword_data['path']}")
        start_sec = keyword_data['start'] / 1000
        end_sec = keyword_data['end'] / 1000
        duration = end_sec - start_sec
        
        if duration <= 0:
            print(f"Invalid duration for {keyword_data['path']}: {duration}")
            return None

        if keyword_data['type'] == 'image':
            clip = ImageClip(keyword_data['path']).set_duration(duration)
            
        elif keyword_data['type'] == 'gif':
            clip = VideoFileClip(keyword_data['path'])
            if clip.duration < duration:
                clip = clip.loop(duration=duration)
            else:
                clip = clip.subclip(0, duration)
                
        elif keyword_data['type'] == 'text':
            clip = VideoFileClip(keyword_data['path'])
            if clip.duration < duration:
                # Instead of looping, create a freeze frame for the remaining duration
                main_clip = clip
                remaining_duration = duration - clip.duration
                # Create a frozen frame from the last frame
                last_frame = clip.get_frame(clip.duration - 0.001)  # Get last frame
                frozen_clip = ImageClip(last_frame).set_duration(remaining_duration)
                # Concatenate the original clip with the frozen frame
                clip = concatenate_videoclips([main_clip, frozen_clip])
            else:
                clip = clip.subclip(0, duration)
                
        else:
            raise ValueError(f"Unknown type: {keyword_data['type']}")

        # Resize and position the clip
        clip = clip.resize(height=VIDEO_RESOLUTION[1] - 40).set_position('center')
        return clip

    except Exception as e:
        print(f"Error processing {keyword_data['path']}: {e}")
        return None

def create_video(data, audio_path, output_path):
    try:
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        sorted_keywords = sorted(data, key=lambda x: x['order_id'])
        
        # Adjust end times to eliminate gaps between clips
        adjusted_data = []
        for i in range(len(sorted_keywords)):
            current = sorted_keywords[i]
            if i < len(sorted_keywords) - 1:
                next_kw = sorted_keywords[i + 1]
                new_end = next_kw['start']
            else:
                new_end = current['end']
            
            # Ensure valid duration
            new_end = max(new_end, current['start'])
            if new_end > total_duration * 1000:
                new_end = total_duration * 1000
            
            adjusted_kw = current.copy()
            adjusted_kw['end'] = new_end
            adjusted_data.append(adjusted_kw)

        clips = []
        for keyword in adjusted_data:
            clip = create_clip(keyword)
            if clip is not None:
                start_time = keyword['start'] / 1000
                clip = clip.set_start(start_time)
                clips.append(clip)
                print(f"Added {keyword['type']} clip {keyword['order_id']} at {start_time}s")

        # Add black background covering full duration
        background = ColorClip(
            size=VIDEO_RESOLUTION,
            color=(0, 0, 0),
            duration=total_duration
        )
        clips.insert(0, background)

        # Create final composition
        final_clip = CompositeVideoClip(clips, size=VIDEO_RESOLUTION)
        final_clip = final_clip.set_audio(audio_clip)
        
        # Write output video
        print("Rendering final video...")
        final_clip.write_videofile(
            output_path,
            fps=24,
            threads=4,
            preset='fast',
            ffmpeg_params=['-crf', '28']
        )

        # Cleanup resources
        final_clip.close()
        audio_clip.close()
        for clip in clips:
            clip.close()

    except Exception as e:
        print(f"Error in create_video: {e}")
        raise

# (main function remains the same as previous version)

def main():
    json_path = 'mapped1.json'
    audio_path = 'output/audio.mp3'
    output_path = 'output_video_2.mp4'
    
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        create_video(data, audio_path, output_path)
        print(f"Video successfully created at: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()