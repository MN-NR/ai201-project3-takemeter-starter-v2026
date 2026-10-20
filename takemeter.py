import json
import math
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

LABELS = ["critique", "hot_take", "recap"]


def normalize_text(text: str) -> list[str]:
    text = text.lower()
    text = text.replace("'", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [token for token in text.split() if token.strip()]
    return tokens


class NaiveBayesTextClassifier:
    def __init__(self, labels=None):
        self.labels = labels or LABELS
        self.vocab = []
        self.class_priors = {}
        self.word_log_probs = {label: {} for label in self.labels}
        self.word_counts = {label: Counter() for label in self.labels}
        self.class_totals = {label: 0 for label in self.labels}

    def fit(self, texts, labels):
        self.vocab = sorted({token for text in texts for token in normalize_text(text)})
        for label in self.labels:
            self.class_totals[label] = 0
            self.word_counts[label] = Counter()

        for text, label in zip(texts, labels):
            tokens = normalize_text(text)
            if not tokens:
                continue
            self.class_totals[label] += len(tokens)
            self.word_counts[label].update(tokens)

        total_documents = len(labels)
        for label in self.labels:
            self.class_priors[label] = math.log((sum(1 for y in labels if y == label) + 1) / (total_documents + len(self.labels)))

        vocab_size = max(len(self.vocab), 1)
        for label in self.labels:
            label_token_total = sum(self.word_counts[label].values()) + vocab_size
            label_log_probs = {}
            for token in self.vocab:
                token_count = self.word_counts[label].get(token, 0) + 1
                prob = token_count / label_token_total
                label_log_probs[token] = math.log(prob)
            self.word_log_probs[label] = label_log_probs

    def predict_one(self, text):
        tokens = normalize_text(text)
        if not tokens:
            return {label: 0.0 for label in self.labels}, "hot_take"

        scores = {}
        for label in self.labels:
            score = self.class_priors[label]
            for token in set(tokens):
                score += self.word_log_probs[label].get(token, math.log(1 / max(len(self.vocab), 1)))
            scores[label] = score

        best_label = max(self.labels, key=lambda label: scores[label])
        top_score = scores[best_label]
        total = sum(math.exp(score - top_score) for score in scores.values())
        probabilities = {label: math.exp(scores[label] - top_score) / total for label in self.labels}
        return probabilities, best_label

    def predict(self, texts):
        return [self.predict_one(text)[1] for text in texts]


def stratified_split(df, label_column="label", test_size=0.2):
    labels = df[label_column].unique().tolist()
    train_frames = []
    test_frames = []
    for label in labels:
        subset = df[df[label_column] == label].copy()
        subset = subset.sample(frac=1, random_state=42)
        split_index = max(1, int(round(len(subset) * (1 - test_size))))
        train_frames.append(subset.iloc[:split_index])
        test_frames.append(subset.iloc[split_index:])
    return pd.concat(train_frames, ignore_index=True), pd.concat(test_frames, ignore_index=True)


def compute_metrics(y_true, y_pred):
    labels = LABELS
    confusion = {true: {pred: 0 for pred in labels} for true in labels}
    for true, pred in zip(y_true, y_pred):
        confusion[true][pred] += 1

    precision = {}
    recall = {}
    f1 = {}

    for label in labels:
        tp = confusion[label][label]
        fp = sum(confusion[other][label] for other in labels if other != label)
        fn = sum(confusion[label][other] for other in labels if other != label)
        precision[label] = tp / (tp + fp) if (tp + fp) else 0.0
        recall[label] = tp / (tp + fn) if (tp + fn) else 0.0
        f1[label] = 2 * precision[label] * recall[label] / (precision[label] + recall[label]) if (precision[label] + recall[label]) else 0.0

    accuracy = sum(1 for true, pred in zip(y_true, y_pred) if true == pred) / len(y_true)
    macro_f1 = sum(f1.values()) / len(labels)
    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "per_class": {label: {"precision": precision[label], "recall": recall[label], "f1": f1[label]} for label in labels},
        "confusion_matrix": confusion,
    }


def save_metrics(path, metrics):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)
