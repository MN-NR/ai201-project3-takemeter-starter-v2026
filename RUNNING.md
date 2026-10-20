# Running TakeMeter

## Setup

```bash
cd /Users/admin/Desktop/codepath/ai201-project5-takemeter-starter-v2026
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 train.py
python3 app.py "the bass is muddy and the album loses momentum after the second track"
```

The project uses only the standard library plus `numpy` and `pandas`, which are already available in the course environment.

## What to expect

- `train.py` loads `data/posts.csv`, trains the classifier, and writes metrics to `results/metrics.json`.
- `app.py` accepts a single text string and prints a predicted label and confidence.
- The dataset is fixed at 200 labeled posts, intentionally split across the three classes to make the boundary easy to reason about.

## Training output

The script prints a short summary containing:

- validation accuracy
- macro F1
- per-class precision, recall, and F1
- confusion matrix

A run log is saved under `results/metrics.json` for the next unit's evaluation.
