import json
import re
import os


INPUT_FILE = "kanji_structural_category.ts"
OUTPUT_FILE = "kanji-structure.json"


def main():
    if not os.path.exists(INPUT_FILE):
        print(f" Error: Could not find '{INPUT_FILE}' in this folder.")
        return

    print(f"Reading from {INPUT_FILE}...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    print("Cleaning and Parsing data...")

    match = re.search(r"const data:.*?=\s*({[\s\S]*})", content)

    if not match:
        print("Could not find the 'const data' object in the file.")
        print(
            "   Make sure the file contains: const data: Record<...> = { ... }")
        return

    raw_json = match.group(1)

    cleaned_json = re.sub(r",\s*}", "}", raw_json)

    try:
        data = json.loads(cleaned_json)
        print(f"Successfully parsed {len(data)} Kanji entries.")
    except json.JSONDecodeError as e:
        print(f" JSON Parsing Failed: {e}")

        print(f"Error context: {cleaned_json[max(0, e.pos-20):e.pos+20]}")
        return

    print(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    print(" Done! Move 'kanji-structure.json' to your /public/json/ folder.")


if __name__ == "__main__":
    main()
