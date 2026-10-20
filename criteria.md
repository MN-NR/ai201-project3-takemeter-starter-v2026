# Acceptance criteria — TakeMeter

These are the five acceptance criteria for the model, written before the first training run.

## 1. The taxonomy is explicit and consistent

The project must define exactly three labels in a written taxonomy: `critique`, `hot_take`, and `recap`. The definition must state what counts as evidence, what counts as a claim without evidence, and how the model should classify the edge case where a post sounds like both a reaction and a review.

**Why this target:** The model can only generalize if the labels are stable. A label that depends on intuition is not a usable contract. This target is about making the distinction legible before the model ever sees the data.

## 2. The dataset has 200 labeled examples

The final CSV must contain at least 200 posts with a text field and a single label from the three-class taxonomy. The rows must include both easy and borderline examples, and the labels must be easy to audit by reading the post text.

**Why this target:** The first question is whether the training set really contains the distinction you claim to teach. A dataset with fewer than 200 examples is too small to learn the boundary reliably, while a larger one helps expose where the taxonomy still needs tightening.

## 3. The classifier reaches a minimum holdout score

On a held-out validation split, the model must reach at least 0.75 macro F1 and at least 0.80 accuracy. This score must be measured on unseen posts and recorded in the saved run output.

**Why this target:** Macro F1 matters here because the labels are not perfectly balanced. If one label dominates, a model can look good by guessing that class all the time. This threshold forces the classifier to actually separate the three categories.

## 4. The boundary cases are handled intentionally

For five manually chosen borderline posts that sit between `critique` and `hot_take`, the classifier must agree with the written decision rule in at least 4 of 5 cases. These posts must be logged as “hard cases” in the dataset or validation notes.

**Why this target:** The hardest part of a taxonomy is the cases in the middle. A model that can only classify obvious examples is not yet learning the task. This criterion checks whether the classifier is learning the boundary, not just the obvious majority pattern.

## 5. The training run is reproducible and the metrics are saved

Running `python3 train.py` from the repo root must produce a metrics file in `results/metrics.json` containing the validation metrics, confusion matrix, and class counts. The project must also expose a simple `app.py` inference path that predicts a label for a raw post.

**Why this target:** The unit is not just about making a model; it is about making the evidence durable. If the run cannot be reproduced and the metrics cannot be inspected later, the system is not production-reviewable.

---

> The model has not yet been trained. These criteria are intentionally written before the first score is known so that the dataset and decision rule are treated as the product, not as after-the-fact excuses.
