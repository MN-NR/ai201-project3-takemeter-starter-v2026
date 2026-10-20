import json
from pathlib import Path

import pandas as pd

from takemeter import NaiveBayesTextClassifier, compute_metrics, stratified_split

DATA_PATH = Path(__file__).resolve().parent / "data" / "posts.csv"
RESULTS_PATH = Path(__file__).resolve().parent / "results" / "metrics.json"


def main():
    df = pd.read_csv(DATA_PATH)
    train_df, test_df = stratified_split(df, label_column="label", test_size=0.2)

    model = NaiveBayesTextClassifier(labels=["critique", "hot_take", "recap"])
    model.fit(train_df["text"].tolist(), train_df["label"].tolist())

    y_true = test_df["label"].tolist()
    y_pred = model.predict(test_df["text"].tolist())
    metrics = compute_metrics(y_true, y_pred)
    metrics["label_distribution"] = dict(df["label"].value_counts().sort_index().to_dict())
    metrics["train_size"] = len(train_df)
    metrics["test_size"] = len(test_df)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)

    print(f"train_size={len(train_df)}")
    print(f"test_size={len(test_df)}")
    print(f"accuracy={metrics['accuracy']:.4f}")
    print(f"macro_f1={metrics['macro_f1']:.4f}")
    print(json.dumps(metrics["per_class"], indent=2, sort_keys=True))
    print(json.dumps(metrics["confusion_matrix"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
