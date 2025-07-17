.PHONY: setup convert_csv embed

setup:
	@echo "Installing necessary packages for this repository..."
	brew bundle

convert:
	poetry run python roronoa/utils/csv_to_jsonl.py --input roronoa/data/activities.csv --output roronoa/data/activities.jsonl

embed:
	poetry run python roronoa/embeddings/embed.py
