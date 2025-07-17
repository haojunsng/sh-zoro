.PHONY: setup convert run clean

setup:
	pip install -r requirements.txt

convert:
	python utils/csv_to_jsonl.py --input data/activities.csv --output data/activities.jsonl

run:
	streamlit run chatbot/main.py

clean:
	rm -f data/activities.jsonl
