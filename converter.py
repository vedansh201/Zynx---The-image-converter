from PIL import Image
import os

def convert_image(input_path, output_format):
    image = Image.open(input_path)

    if output_format.upper() == "JPEG":
        image = image.convert("RGB")

    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}.{output_format.lower()}"

    image.save(output_path, output_format.upper())

    return output_path
