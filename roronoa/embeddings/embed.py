import json
import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

model = SentenceTransformer('all-MiniLM-L6-v2')

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "strava-activities"

pc = Pinecone(api_key=PINECONE_API_KEY)

def parse_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
    
def parse_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def make_embedding_text(activity):
    distance_km = parse_float(activity.get('Distance')) / 1000
    elapsed_minutes = parse_float(activity.get('Elapsed Time')) / 60
    calories = parse_int(activity.get('Calories'))
    avg_hr = parse_int(activity.get('Average Heart Rate'))

    return (
        f"{activity.get('Activity Name', '')} on {activity.get('Activity Date', '')}, "
        f"distance {distance_km:.2f} km, "
        f"duration {elapsed_minutes:.0f} min, "
        f"avg heart rate {avg_hr} bpm, "
        f"calories {calories}."
    )

def batch_embed_activities(activities, batch_size=32):
    texts = [make_embedding_text(a) for a in activities]
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    return [(a.get('Activity ID') or str(hash(texts[i])), embeddings[i].tolist(), a) for i, a in enumerate(activities)]

def main():
    index = pc.Index(INDEX_NAME)

    with open("roronoa/data/activities.jsonl") as f:
        activities = [json.loads(line) for line in f]

        batch_size = 32
        
        for i in range(0, len(activities), batch_size):
            batch = activities[i:i+batch_size]
            vectors = batch_embed_activities(batch)
            index.upsert(vectors)

    print("All activities embedded and indexed!")

if __name__ == "__main__":
    main()
