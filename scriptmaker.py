import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

google_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=google_api_key)

def generate_script(prompt, output_format="text"):
    try:
        print("Generating Script ...")
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = f"""Act like Fireship, a tech-focused YouTube channel known for its fast-paced, witty, and snarky narration style. Write a 3–5 minute video script about {prompt}. Make the tone sarcastic, humorous, and self-aware, while breaking down complex ideas into digestible explanations. Use relatable analogies, pop culture references, and sharp commentary to keep it engaging. Include plenty of humor, but also deliver valuable insights and a key takeaway at the end.

The output should be in text format, structured like this:



  "Your Fireship-style narration script goes here as a single string. Make sure it is concise, natural, and humorous, suitable for a 3–5 minute video. Do not add emojis or visual cues; focus purely on the narration text."
"""

        response = model.generate_content(system_prompt)

        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

        if output_format == "json":
            # Save as JSON file
            result = {"prompt": prompt, "response": response.text}
            file_path = os.path.join(output_dir, "script.json")
            print(f"Saving to: {file_path}")
            with open(file_path, "w",encoding='utf-8') as f:
                json.dump(result, f, indent=4)
            print(f"JSON saved to {file_path}")
            return file_path
        elif output_format == "text":
            # Save only the response text to a plain text file
            file_path = os.path.join(output_dir, "script.txt")
            print(f"Saving to: {file_path}")
            with open(file_path, "w",encoding='utf-8') as f:
                f.write(response.text)
            print(f"Text saved to {file_path}")
            return file_path

        # If an unsupported format is passed
        raise ValueError(f"Unsupported output format: {output_format}")
    except Exception as e:
        return f"Error: {e}"

