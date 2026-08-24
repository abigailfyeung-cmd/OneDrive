# Python Projects Workspace

This workspace contains a collection of Python scripts and small practice programs covering different tasks such as data processing, file handling, utilities, and media creation.

## Project overview

The files in this folder include:

- `lesson2.py` through `lesson14.py` — lesson-based Python exercises and mini projects
- `currency_translator.py` — converts money between currencies using an online exchange rate API
- `lesson12.py` — dictionary lookup tool with text-to-speech support
- `lesson14.py` — creates a video from a folder of images and can preview/export the result

## Main scripts

### 1. Image-to-video creator
File: `lesson14.py`

This script:
- reads images from a folder
- resizes them to a common size
- creates an MP4 video
- optionally shows a preview during export
- can open the final video automatically
- can generate a description for the image set

Example usage:

```bash
python lesson14.py
python lesson14.py --path "C:\Users\abiga\Desktop\Python" --fps 15
python lesson14.py --save myvideo.mp4
python lesson14.py --preview --open
python lesson14.py --describe
python lesson14.py --description "A trip through my photos"
```

Requirements:

```bash
pip install opencv-python pillow torch transformers
```

### 2. Currency translator
File: `currency_translator.py`

This script fetches current exchange rates from an online API and converts a given amount from one currency to another.

Example:

```bash
python currency_translator.py --amount 100 --from USD --to EUR
```

### 3. Dictionary lookup + speech
File: `lesson12.py`

This script looks up a word definition from the Dictionary API and optionally speaks it aloud using a system voice.

Example:

```bash
python lesson12.py --word happiness
python lesson12.py --word "machine learning" --voice "Microsoft Zira Desktop"
```

## General setup

Make sure Python is installed, then install any needed packages for the script you want to run.

```bash
python --version
pip install requests opencv-python pillow torch transformers pyttsx3
```

## Running scripts

Most scripts are run directly with Python:

```bash
python filename.py
```

Replace `filename.py` with the script you want to use.

## Notes

- Some scripts may rely on internet access for APIs or model downloads.
- The image-to-video tool may download a Hugging Face model on first use.
- This workspace appears to be a learning/experiments folder, so several files are individual exercises rather than a single app.

## Suggested next steps

- Try the lesson scripts individually to understand each concept.
- Use `lesson14.py` to turn a folder of photos into a simple slideshow video.
- Expand any script by adding better error handling, more features, or a GUI.

## License

No formal license has been added for this project yet.
