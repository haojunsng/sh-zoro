import csv
import json
import argparse

def csv_to_jsonl(input_csv, output_jsonl):
    with open(input_csv, newline='', encoding='utf-8') as csvfile, open(output_jsonl, 'w', encoding='utf-8') as jsonlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            jsonlfile.write(json.dumps(row) + '\n')
    print(f"Converted {input_csv} to {output_jsonl}")

if __name__ == "__main__":
    csv_to_jsonl('data/activities.csv', 'data/activities.jsonl')
