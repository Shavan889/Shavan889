import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def remove_background(image_path):
    """Remove background using rembg."""
    with open(image_path, "rb") as f:
        input_bytes = f.read()

    output_bytes = remove(input_bytes)

    image = Image.open(
        __import__("io").BytesIO(output_bytes)
    ).convert("RGBA")

    return image


def composite_white(image):
    """Composite transparent image onto white background."""
    white = Image.new("RGBA", image.size, (255, 255, 255, 255))
    white.paste(image, mask=image)
    return white.convert("RGB")


def enhance_contrast(image):
    """Convert to grayscale and apply CLAHE."""
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    return Image.fromarray(enhanced)


def process(input_path, output_path):
    print("Removing background...")
    img = remove_background(input_path)

    print("Applying white background...")
    img = composite_white(img)

    print("Enhancing contrast...")
    img = enhance_contrast(img)

    img.save(output_path)

    print(f"\nDone!\nSaved: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python scripts/prep_photo.py photo.jpg")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print("Input image not found.")
        sys.exit(1)

    output_file = "source-prepped.png"

    process(str(input_file), output_file)


if __name__ == "__main__":
    main()