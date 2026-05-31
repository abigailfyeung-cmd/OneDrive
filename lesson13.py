"""Describe an image using a local vision captioning model.

Usage:
    python lesson13.py --image path/to/image.jpg

Install dependencies with:
    pip install transformers pillow torch
"""

import argparse
import sys


def describe_image(image_path: str) -> str:
    try:
        from PIL import Image
    except ImportError as exc:
        raise ImportError(
            "Pillow is required to load images. Install it with `pip install pillow`."
        ) from exc

    try:
        from transformers import (
            VisionEncoderDecoderModel,
            ViTImageProcessor,
            AutoTokenizer,
        )
    except ImportError as exc:
        raise ImportError(
            "Transformers is required for image captioning. "
            "Install it with `pip install transformers torch pillow`."
        ) from exc

    image = Image.open(image_path).convert("RGB")
    model_name = "nlpconnect/vit-gpt2-image-captioning"

    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    feature_extractor = ViTImageProcessor.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    output_ids = model.generate(pixel_values, max_length=64, num_beams=4)
    print(output_ids)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

    return caption


def main() -> int:
    parser = argparse.ArgumentParser(description="Describe an image using a local transformer captioning model.")
    parser.add_argument("--image", required=True, help="Path to the image file to describe.")
    args = parser.parse_args()

    try:
        description = describe_image(args.image)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Image description:")
    print(description)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
