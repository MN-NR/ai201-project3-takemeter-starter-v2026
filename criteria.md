# Acceptance criteria — filed before training

These targets apply to the held-out test set for each seed (42, 7, and 2024) in the next unit. A criterion is met only if all three seeds meet it. They were written before the first training run.

## 1. Overall accuracy ≥ 0.70

**Why this target:** The three labels are observable writing moves in Hacker News comments, and the sample has roughly 200 comments. A classifier that is wrong on more than 3 of 10 comments would be too unreliable for triage.

## 2. Macro F1 ≥ 0.65

**Why this target:** Accuracy can hide failure on the smaller `assertion` group. Macro F1 gives each of the three writing moves equal weight.

## 3. `question` F1 ≥ 0.75

**Why this target:** Questions usually have an explicit interrogative. The rhetorical questions are harder, but this label should still be the easiest one to recognize.

## 4. `assertion` F1 ≥ 0.55

**Why this target:** The boundary between a bare assertion and a reasoned claim depends on whether the text *states* its support. Some short comments imply a reason without spelling it out, and this will be the smallest group after review.

## 5. Accuracy in the most confident third ≥ 0.80

**Why this target:** If confidence is useful, the ten most confident predictions in a 30-comment test split should be correct at least eight times. This is stricter than the overall accuracy target.
