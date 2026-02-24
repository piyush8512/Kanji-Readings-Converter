import pandas as pd
import json

input_filename = 'JOYOKANJIREADINGSver.1.1.xlsx'
output_filename = 'joyo_kanji_readings.json'

def clean_split(text, separator):
    if pd.isna(text) or str(text).strip() == "":
        return []
    return [t.strip() for t in str(text).split(separator) if t.strip()]

def get_arrow_at_index(row, index):
    if index >= len(row):
        return "?"
    val = str(row.iloc[index]).strip()
    if val in ['nan', '', 'None']:
        return "?"
    return val

print(f"Loading '{input_filename}'... (This might take a moment)")

try:
    df = pd.read_excel(input_filename, sheet_name='MAIN', header=0)
except FileNotFoundError:
    print(f"❌ Error: Could not find '{input_filename}'.")
    exit()
except ImportError:
    print("❌ Error: Missing 'openpyxl'. Please run: pip install openpyxl")
    exit()
except Exception as e:
    print(f"Could not find 'MAIN' sheet ({e}). Trying the first sheet...")
    df = pd.read_excel(input_filename, header=0)

output_data = {}

for index, row in df.iterrows():
    kanji = row.iloc[0] 

    if pd.isna(kanji): continue

    on_readings = clean_split(row.iloc[1], '、')
    kun_readings = clean_split(row.iloc[2], '、')
    vocab_list = clean_split(row.iloc[3], '・')
    
    total_readings_count = len(on_readings) + len(kun_readings)

    while len(vocab_list) < total_readings_count:
        vocab_list.append(None)

    kanji_entry = []
    vocab_cursor = 0 

    current_arrow_col = 4
    for reading in on_readings:
        arrow = get_arrow_at_index(row, current_arrow_col)
        example = vocab_list[vocab_cursor]
        
        kanji_entry.append({
            "reading": reading,
            "type": "ON",
            "frequency": arrow,
            "example_word": example
        })
        
        current_arrow_col += 1
        vocab_cursor += 1

    current_arrow_col = 7 
    for reading in kun_readings:
        arrow = get_arrow_at_index(row, current_arrow_col)
        example = vocab_list[vocab_cursor]
        
        kanji_entry.append({
            "reading": reading,
            "type": "KUN",
            "frequency": arrow,
            "example_word": example
        })
        
        current_arrow_col += 1
        vocab_cursor += 1

    output_data[kanji] = kanji_entry

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Success! Processed {len(output_data)} Kanji.")
print(f"Output saved to: {output_filename}")