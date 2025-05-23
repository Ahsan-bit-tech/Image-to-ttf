import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from connvert_to_svg import convert_png_to_svg

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
image_dir = "extracted_characters"
def analyze_and_rename_images():
    for image_filename in os.listdir(image_dir):
        if image_filename.endswith(".png"):
            image_path = os.path.join(image_dir, image_filename)

            # Encode the image to base64
            base64_image = encode_image(image_path)

            # Request GPT-4 to identify the alphabet
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What alphabet is in the image? if the alphabets is not reconginse name as NULL Otherwise just give the alphabet like its capital (A) or small (a) and so on. just give response in alphabets only",
                                # "text": "Detect the text in the image. If the text is a single recognized alphabet, return the alphabet in lowercase (e.g., 'a'). If the text is not recognized as an alphabet, return 'null'.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
            )

            # Get the identified alphabet from the response
            alphabet = response.choices[0].message.content

            # Rename the image based on the identified alphabet
            new_image_filename = f"{alphabet}.png"
            new_image_path = os.path.join(image_dir, new_image_filename)

            # Rename the image file
            os.rename(image_path, new_image_path)
            print(f"Renamed {image_filename} to {new_image_filename}")
    convert_png_to_svg()
