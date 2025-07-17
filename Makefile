.PHONY: convert

convert:
	python utils/csv_to_jsonl.py --input data/activities.csv --output data/activities.jsonl
