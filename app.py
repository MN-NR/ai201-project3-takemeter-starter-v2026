import sys
from pathlib import Path

from takemeter import NaiveBayesTextClassifier

MODEL_PATH = Path(__file__).resolve().parent / "data" / "posts.csv"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 app.py \"your post here\"")

    text = sys.argv[1]
    import pandas as pd

    df = pd.read_csv(MODEL_PATH)
    model = NaiveBayesTextClassifier(labels=["critique", "hot_take", "recap"])
    model.fit(df["text"].tolist(), df["label"].tolist())
    probs, label = model.predict_one(text)
    print(f"label={label}")
    print(f"confidence={max(probs.values()):.4f}")
    print(json.dumps({k: round(v, 4) for k, v in probs.items()}, sort_keys=True))


if __name__ == "__main__":
    import json

    main()
