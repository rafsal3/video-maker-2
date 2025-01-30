import os
import pygame
import shutil
import random
from moviepy.editor import ImageSequenceClip

# Initialize Pygame
pygame.init()

# Vibrant solid color palette
# Vibrant solid color palette (used if no custom color is provided)
COLORS = [
    (255, 255, 255),    # White
    (82, 183, 255),     # Bright blue
    (255, 94, 94),      # Bright Red
    (94, 255, 114),     # Bright Green
    (255, 187, 85),     # Bright Orange
    (190, 94, 255),     # Bright Purple
    (255, 94, 219),     # Bright Pink
    (94, 255, 247),     # Bright Cyan
]

class TextEffect:
    def __init__(self, word, resolution, font_color, bg_color):
        self.word = word
        self.resolution = resolution
        self.color = font_color if font_color else random.choice(COLORS)
        self.bg_color = bg_color
        
        # Dynamic base font size based on word length
        self.base_font_size = self.calculate_base_font_size(len(word))
        
        # Apply zoom effect only for short words (less than 5 characters)
        self.apply_zoom = len(word) < 5

        print(f"Creating video for word: {word} (length: {len(word)}) with base font size: {self.base_font_size}")
        print(f"Font color: RGB{self.color}, Background: RGB{self.bg_color}")
        print(f"Zoom effect: {'enabled' if self.apply_zoom else 'disabled'}")

    def calculate_base_font_size(self, word_length):
        """Calculate dynamic base font size based on word length"""
        # Base sizes for different word lengths
        if word_length <= 3:
            return 300  # Very large for short words
        elif word_length <= 5:
            return 250
        elif word_length <= 7:
            return 200
        elif word_length <= 10:
            return 150
        elif word_length <= 15:
            return 120
        else:
            return 100  # Minimum size for very long words

    def apply_zoom_effect(self, t):
        """Apply zoom-in effect for short words"""
        if not self.apply_zoom:
            return self.base_font_size
        
        # Smooth zoom-in effect: start small and grow to full size
        if t < 1:
            # Zoom in from 10% to 100% size during the first second
            scale = 0.1 + t * 0.9
        else:
            # Stay at full size after zooming in
            scale = 1.0

        return int(self.base_font_size * scale)
    
    def wrap_text(self, text, font, max_width):
        """Wrap text into multiple lines to fit within max_width"""
        lines = []
        words = text.split(" ")  # Split text into words

        current_line = []
        current_line_width = 0

        for word in words:
            # Calculate width of the word
            word_width = font.size(word)[0]

            # If adding the word exceeds the max width, start a new line
            if current_line_width + word_width > max_width:
                lines.append(" ".join(current_line))  # Add current line to lines
                current_line = [word]  # Start new line with the current word
                current_line_width = word_width
            else:
                # Add the word to the current line
                current_line.append(word)
                current_line_width += word_width + font.size(" ")[0]  # Add space width

        # Add the last line
        if current_line:
            lines.append(" ".join(current_line))

        return lines
    
    def render_frame(self, revealed_text, t):
        """Render a single frame with text wrapping for paragraphs"""
        surface = pygame.Surface(self.resolution)
        surface.fill(self.bg_color)

        # Calculate dynamic font size with zoom effect (if applicable)
        font_size = self.apply_zoom_effect(t)
        font = pygame.font.Font(None, font_size)

        if self.apply_zoom:
            # For short words: render the full word with zoom effect
            text_surface = font.render(self.word, True, self.color)
            
            # Calculate centered position
            text_x = (self.resolution[0] - text_surface.get_width()) // 2
            text_y = (self.resolution[1] - text_surface.get_height()) // 2
            
            surface.blit(text_surface, (text_x, text_y))
        else:
            # For longer text: split into lines and render
            lines = self.wrap_text(revealed_text, font, self.resolution[0] * 0.9)  # 90% of screen width
            total_height = len(lines) * font_size
            y_offset = (self.resolution[1] - total_height) // 2  # Center vertically

            for line in lines:
                # Calculate total width of the line (including spaces)
                total_width = 0
                char_surfaces = []
                space_width = font.size(" ")[0]  # Get the width of a space character

                for char in line:
                    if char.strip():  # If it's not a space
                        char_surface = font.render(char, True, self.color)
                        char_surfaces.append((char_surface, False))  # False = not a space
                        total_width += char_surface.get_width()
                    else:  # If it's a space
                        char_surfaces.append((None, True))  # True = space
                        total_width += space_width
                
                # Calculate starting x position for centering
                x_offset = (self.resolution[0] - total_width) // 2

                # Render each character or space
                for char_surface, is_space in char_surfaces:
                    if is_space:
                        # Add space width
                        x_offset += space_width
                    else:
                        # Render character
                        surface.blit(char_surface, (x_offset, y_offset))
                        x_offset += char_surface.get_width()
                
                # Move to the next line
                y_offset += font_size
            
        return surface

def create_text_video(word, temp_folder="temp_frames",output_path="output/video/text.mp4",
                     resolution=(1280, 720), font_color=None, bg_color=(0, 0, 0),
                     duration=5,reveal_time=1):
    
    # Create all necessary directories in the path
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    # Make sure the output file doesn't exist or isn't in use
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except PermissionError:
            raise PermissionError(f"Cannot write to {output_path}. File may be in use by another process.")
            

    fps = 24
    effect = TextEffect(word, resolution, font_color, bg_color)

    frames = []
    total_frames = int(fps * duration)
    
    # Calculate reveal duration (only for longer words)
    reveal_frames = int(fps * reveal_time) if len(word) >= 5 else 0
    letters_per_frame = len(word) / reveal_frames if reveal_frames > 0 else 0

    for i in range(total_frames):
        t = i / fps
        
        # Calculate revealed text (only for longer words)
        if len(word) >= 5:
            if i < reveal_frames:
                revealed_count = min(len(word), int(i * letters_per_frame))
            else:
                revealed_count = len(word)
            revealed_text = word[:revealed_count]
        else:
            # For short words, always show the full word
            revealed_text = word
        
        # Render frame
        surface = effect.render_frame(revealed_text, t)
        frame_path = os.path.join(temp_folder, f"frame_{i:04d}.png")
        pygame.image.save(surface, frame_path)
        frames.append(frame_path)

    # Create video
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_path, codec="libx264", fps=fps)

    # Cleanup
    for frame in frames:
        os.remove(frame)
    shutil.rmtree(temp_folder)

    return output_path

def create_video_for_single_keyword(word, output_path,
                                   resolution=(1280, 720), font_color=None,
                                   bg_color=(0, 0, 0), duration=5, reveal_time=1):
    try:
        video_path = create_text_video(
            word,
            temp_folder="temp_frames",
            output_path=output_path,
            resolution=resolution,
            font_color=font_color,
            bg_color=bg_color,
            duration=duration,
            reveal_time=reveal_time
        )
        print(f"Created video: {video_path}")
        return video_path
    except OSError as e:
        print(f"Error creating video: {str(e)}")
        print("Please check if:")
        print("- The output directory exists and is writable")
        print("- The output file is not in use")
        print("- You have sufficient permissions")
        raise