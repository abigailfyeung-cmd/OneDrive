#!/usr/bin/env python3
import argparse
import json
import platform
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


def fetch_definition(word: str) -> str:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "No definition found for this word."
        raise
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    if not isinstance(data, list) or not data:
        return "No definition found for this word."

    definitions = []
    for entry in data:
        word_text = entry.get("word", word)
        for meaning in entry.get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "")
            for definition in meaning.get("definitions", []):
                text = definition.get("definition")
                if not text:
                    continue
                example = definition.get("example")
                formatted = f"- ({part_of_speech}) {text}"
                if example:
                    formatted += f"\n    Example: {example}"
                definitions.append(formatted)
                if len(definitions) >= 3:
                    break
            if len(definitions) >= 3:
                break
        if len(definitions) >= 3:
            break

    if not definitions:
        return "No definition found for this word."

    header = f"Definition for '{word_text}':"
    return f"{header}\n" + "\n".join(definitions)


def speak_text(text: str, voice: str = "", rate: int = 0) -> None:
    if platform.system() == "Windows":
        voice_escaped = voice.replace("'", "''")
        script = (
            "Add-Type -AssemblyName System.Speech; "
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "if ('" + voice_escaped + "' -ne '') { try { $synth.SelectVoice('" + voice_escaped + "') } catch { Write-Error \"Voice '$voice' not found\"; exit 1 } }; "
            "$synth.Rate = " + str(rate) + "; "
            "$synth.Speak([Console]::In.ReadToEnd())"
        )
        process = subprocess.Popen(
            ["powershell", "-NoProfile", "-Command", script],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        process.communicate(text)
        return

    try:
        import pyttsx3

        engine = pyttsx3.init()
        if voice:
            voices = engine.getProperty("voices")
            selected = None
            key = voice.lower()
            for v in voices:
                if key in v.name.lower() or key in getattr(v, "id", "").lower():
                    selected = v.id
                    break
            if selected:
                engine.setProperty("voice", selected)
            else:
                print(f"Warning: voice '{voice}' not found, using default voice.")
        engine.setProperty("rate", rate)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("Text-to-speech is not available on this system.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Look up a word definition and speak it aloud."
    )
    parser.add_argument("--word", required=True, help="The word to define")
    parser.add_argument(
        "--voice",
        default="Microsoft Zira Desktop",
        help="Name of the voice to use for speech",
    )
    parser.add_argument("--rate", type=int, default=0, help="Speech rate adjustment (-10 to 10)")
    args = parser.parse_args()

    try:
        definition_text = fetch_definition(args.word.strip())
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    print(definition_text)
    if definition_text.startswith("No definition found"):
        return 0

    try:
        speak_text(definition_text, voice=args.voice, rate=args.rate)
    except Exception as exc:
        print(f"Speech error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


