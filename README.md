# TakeMeter

## What This Does

TakeMeter classifies public [Hacker News](https://news.ycombinator.com/) comments by their main writing move: a `question`, a `reasoned` claim, or an `assertion` without stated support. This sample spans discussions in the community rather than one story. The aim is to help sort a discussion feed by how a comment engages with an idea, not to judge whether the author's claim is true.

## Label Taxonomy

### `question`

**Definition:** The comment's main move is asking for information, an explanation, or a response, including a direct rhetorical challenge.

- [Example 1](https://news.ycombinator.com/item?id=50172368): “Are there plans to make guides for other pieces of furniture as well?”
- [Example 2](https://news.ycombinator.com/item?id=50172132): “Do you have an example of something that a nation did solely for the good of mankind with no vested interest in the outcome?”

### `reasoned`

**Definition:** The comment's main move is a claim supported in the text by a stated cause, concrete example, comparison, observation, or checkable detail.

- [Example 1](https://news.ycombinator.com/item?id=50172329): The author says Subaru buyers value safety and reliability because their livelihood depends on the car, and explains why they may care less about the infotainment system.
- [Example 2](https://news.ycombinator.com/item?id=50172046): An operations worker explains why testing a cloud availability-zone failure in production is risky and gives their experience with staging environments.

### `assertion`

**Definition:** The comment's main move is a claim, preference, or reaction without a stated supporting reason or concrete example.

- [Example 1](https://news.ycombinator.com/item?id=50171891): “Let's hope that some of our elected officials actually do something about this.”
- [Example 2](https://news.ycombinator.com/item?id=50171965): The commenter predicts that claims about China's chip foundries will be out of date within a year or two, but gives no supporting evidence.

### The hardest boundary

The hardest boundary is `reasoned` versus `assertion`. I required support **stated in the comment**: a cause, example, comparison, observation, or checkable detail. An implied reason or confident tone stayed `assertion`. An explicit question or challenge is `question` when answering it is the comment's main purpose; a question that merely introduces a developed argument does not override `reasoned`. These rules were written in `label_definitions.txt` before training.

## The Dataset

**Source:** 200 unique, public Hacker News comments collected from the [HN Algolia comments feed](https://hn.algolia.com/api/v1/search_by_date?tags=comment) on October 20, 2026. Each `labels.csv` row has the complete comment text, one label, and a note with a direct source link. HTML tags were removed, entities decoded, and whitespace normalized; comment wording was not shortened. The sample was selected from the 1,000 most recent comments available in one API response. I read more than 40 comments before defining the taxonomy; `research_notes.md` records the candidate distinctions.

**Labeling:** The first 20 rows were classified independently by Codex without preliminary tags, then reread in a second full-text review; two labels changed. The [review log](data/review_first20.md) records all 20 decisions. The remaining 180 received simple rule-based preliminary tags; Codex read all of them and corrected 41. The note column records this for each row. **This was AI-assisted work, not an unaided human cold pass.**

| Label | Count | Share |
|---|---:|---:|
| `question` | 67 | 33.5% |
| `reasoned` | 85 | 42.5% |
| `assertion` | 48 | 24.0% |
| **Total** | **200** | **100%** |

**Three hard cases:**

1. [HN 50172375](https://news.ycombinator.com/item?id=50172375) quotes a reason to buy a Subaru and then asks why Toyota or Honda would not be a better choice. It could be `reasoned` or `question`; I chose `question` because the reply sought is the point of the comment.
2. [HN 50171903](https://news.ycombinator.com/item?id=50171903) starts by wondering whether hiring teams are trying to appear busy, then lists concrete delays candidates face. It could be `question` or `reasoned`; I chose `reasoned` because the examples develop the claim.
3. [HN 50171988](https://news.ycombinator.com/item?id=50171988) says an 11-foot cube is easier to imagine but gives no reason why that size changes the issue. It could be `reasoned` or `assertion`; I chose `assertion` because the comparison is named without support for the conclusion.

The `assertion` group has only 7 comments in the seed-42 test split. Its F1 will be sensitive to a few predictions.

## The Training Run

The official starter notebook fine-tuned `distilbert-base-uncased` on a stratified 139/31/30 train/validation/test split. It ran for 3 epochs at learning rate `2e-5`, batch size `16`, maximum length `128`, and seed `42`. I used the notebook defaults and changed only its `LABELS` list to match the CSV. After the second label review, I reran sections 1–5 locally on CPU with PyTorch 2.14.1, replacing `results.json` and `test_split.csv` so they match the corrected CSV. The held-out test set contains 10 questions, 13 reasoned claims, and 7 assertions.

The first held-out run scored **0.533 accuracy** and **0.371 macro F1**. It predicted every true `assertion` as `reasoned`, so `assertion` F1 is **0.000**. These results miss several targets in `criteria.md`; those targets were committed before training and have not been revised. Diagnosing and improving them belongs to the next unit.

## Unit 6 — Testing the Model

All unit 6 runs used Apple Silicon (`mps`), PyTorch 2.14.1. Seed 42 reproduced the unit 5 numbers exactly on this device.

### Baseline vs. Trained

The baseline is `facebook/bart-large-mnli` zero-shot, prompted with the definitions in `label_definitions.txt`, scored on the same 30 posts in `test_split.csv` (`baseline_results.json`). Trained is the unit 5 seed-42 model (3 epochs).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.333 | 0.533 | +0.200 |
| Macro F1 | 0.261 | 0.371 | +0.110 |
| F1 — `assertion` | 0.211 | 0.000 | -0.211 |
| F1 — `question` | 0.571 | 0.462 | -0.110 |
| F1 — `reasoned` | 0.000 | 0.650 | +0.650 |

No prediction was written before this table was produced, so I don't claim one. The gap is smaller than it looks. Calling every post `reasoned` scores 13/30 = **0.433**, so the trained model beats that by one post-in-ten, and its whole `reasoned` advantage is the majority class. The baseline is the only model here that finds any `assertion` posts at all, and it is better on `question`. The 3-epoch fine-tune bought almost nothing beyond learning the class prior.

### Three seeds (before)

`results_three_seeds_before.json`, defaults: 3 epochs, lr `2e-5`, batch 16.

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.533 | 0.467 | 0.433 | 0.100 |
| Macro F1 | 0.371 | 0.267 | 0.202 | 0.169 |
| F1 — `question` | 0.462 | 0.182 | 0.000 | 0.462 |
| F1 — `reasoned` | 0.650 | 0.619 | 0.605 | 0.045 |
| F1 — `assertion` | 0.000 | 0.000 | 0.000 | 0.000 |
| Accuracy, most confident third | 0.900 | 0.700 | 0.800 | 0.200 |

Seed 2024 predicted `reasoned` for all 30 posts; its 0.433 is exactly the majority-class rate.

### Confusion matrix (before, seed 42)

| true \ predicted | question | reasoned | assertion |
|---|---|---|---|
| **question** | 3 | 7 | 0 |
| **reasoned** | 0 | 13 | 0 |
| **assertion** | 0 | 7 | 0 |

Every error is a prediction of `reasoned`. The column, not a pair, is the story: the model has not learned any boundary, only the most common label. The training log shows why. Validation accuracy was 0.419 — the `reasoned` share of the validation split — at every epoch of every seed. With 139 training rows, batch 16 and 3 epochs, the model gets about 27 weight updates, which wasn't enough to move off the prior.

### Agreement with the staff set

`my_staff_labels.csv` labels the 30 staff posts under `data/staff_taxonomy.md`: 10 `analysis`, 10 `hot_take`, 10 `reaction`. The closest calls were sp_005 (`analysis`: the second 2% drop in the same shoes is the argument), sp_007 and sp_010 (`analysis` over `reaction` by rule 3), sp_014 (`hot_take`: it mirrors rule 1's decoration example), sp_017 and sp_018 (`hot_take`: the date and the pace threshold are not used as evidence), and sp_029 (`reaction`: it hints at a point about shoes but doesn't argue it).

**Result: 30 of 30, 100% agreement** (`agreement_results.json`). There are no disagreements to adjudicate.

I don't read that as proof the rules are tight, and I don't read it as proof my own 200 labels are consistent. The set was easier than the taxonomy's warning suggests. The posts fall into three blocks in id order (001–010, 011–020, 021–030), and within each block most posts are prototypes: the `analysis` posts lead with numbers, the `hot_take` posts are one-line aphorisms, and the `reaction` posts are first-person and in the present tense. What tested the rules were staff's 7 borderline posts, and those were matched too. My close-call list caught 4 of them ahead of time (sp_005, sp_010, sp_014, sp_029). The other 3 (sp_019, sp_020, sp_028) didn't look hard to me, and on sp_028 I gave the same reasoning staff did without having flagged it. The reverse also happened: I flagged sp_007, sp_017 and sp_018 as close, and staff didn't.

**What this says about the model's failure.** Staff rule 1 (`analysis` vs `hot_take`: does the fact carry the argument?) is the same kind of line as my `reasoned` vs `assertion`. Applying it the way staff did on 30 posts suggests the rule can be applied consistently when posts are clean. It doesn't clear my own labels. My HN comments are messier than these posts, and 180 of my 200 labels started as rule-based prelabels. So the agreement check can't separate a labeling problem from a model problem on that boundary. The evidence in **What's Still Broken** (the "and thus" assertion in the test split, and the 36 corrections that ended as `reasoned`) still points at the labels as part of the cause.

### Criteria verdicts (before)

A criterion passes only if all three seeds pass.

| # | Criterion | Target | Seeds 42 / 7 / 2024 | Verdict |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.70 | 0.533 / 0.467 / 0.433 | **Not met** |
| 2 | Macro F1 | ≥ 0.65 | 0.371 / 0.267 / 0.202 | **Not met** |
| 3 | `question` F1 | ≥ 0.75 | 0.462 / 0.182 / 0.000 | **Not met** |
| 4 | `assertion` F1 | ≥ 0.55 | 0.000 / 0.000 / 0.000 | **Not met** |
| 5 | Most-confident-third accuracy | ≥ 0.80 | 0.900 / 0.700 / 0.800 | **Not met** (seed 7) |

**Diagnosis.** Criteria 1–4 fail for one reason: the model is undertrained and predicts the majority class. That is a property of the training budget, not of the labels — `question` posts usually contain an explicit `?`, which a trained model should pick up easily, and this one missed 7–10 of 10. Criterion 5 passing on two seeds is not evidence that confidence is meaningful: when nearly every prediction is `reasoned`, the most confident third is simply the most typical `reasoned` posts, and 13 of 30 posts are `reasoned`.

### The improvement: 3 epochs → 10

One change: `EPOCHS = 10` in section 2. Everything else, including seeds and splits, is unchanged. Chosen because the diagnosis above is undertraining; more epochs is the direct test of that diagnosis. `results_three_seeds_after.json`.

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread | Before (mean) | After (mean) |
|---|---|---|---|---|---|---|
| Overall accuracy | 0.733 | 0.733 | 0.767 | 0.033 | 0.478 | 0.744 |
| Macro F1 | 0.561 | 0.627 | 0.707 | 0.146 | 0.280 | 0.632 |
| F1 — `question` | 0.909 | 0.857 | 0.947 | 0.090 | 0.215 | 0.904 |
| F1 — `reasoned` | 0.774 | 0.774 | 0.774 | 0.000 | 0.625 | 0.774 |
| F1 — `assertion` | 0.000 | 0.250 | 0.400 | 0.400 | 0.000 | 0.217 |
| Accuracy, most confident third | 0.900 | 1.000 | 1.000 | 0.100 | 0.800 | 0.967 |

Confusion matrix after, seed 42:

| true \ predicted | question | reasoned | assertion |
|---|---|---|---|
| **question** | 10 | 0 | 0 |
| **reasoned** | 1 | 12 | 0 |
| **assertion** | 1 | 6 | 0 |

| # | Criterion | After: 42 / 7 / 2024 | Verdict after |
|---|---|---|---|
| 1 | Accuracy ≥ 0.70 | 0.733 / 0.733 / 0.767 | **Met**, narrowly — seeds 42 and 7 are one post above 0.70 |
| 2 | Macro F1 ≥ 0.65 | 0.561 / 0.627 / 0.707 | **Not met** |
| 3 | `question` F1 ≥ 0.75 | 0.909 / 0.857 / 0.947 | **Met** |
| 4 | `assertion` F1 ≥ 0.55 | 0.000 / 0.250 / 0.400 | **Not met** |
| 5 | Most-confident third ≥ 0.80 | 0.900 / 1.000 / 1.000 | **Met**, and now meaningful: the least confident third scores 0.500 / 0.500 / 0.700 |

The undertraining diagnosis held: `question` went from the worst label to the best, and accuracy spread fell from 0.100 to 0.033.

## What's Still Broken

**`assertion` versus `reasoned`.** This is now the only confusion that matters, and it is one-directional: across the three seeds 16 of 21 true `assertion` posts were called `reasoned`, while only 1 of 39 `reasoned` posts was called `assertion`. Three properties of the data point at it:

1. **Length is a shortcut.** In `labels.csv` the median `assertion` is 20 words, `question` 35, `reasoned` 54. A model can learn "long and not a question means `reasoned`", and any assertion that runs longer than usual — the 54-word GitHub comment in the test split — gets pulled into `reasoned`.
2. **The boundary is defined by an absence.** `reasoned` requires support *stated* in the text; `assertion` is everything that lacks it. A small model learns the presence of features more easily than their absence, and 48 examples (about 34 in each training split) is very little to learn an absence from.
3. **Some test labels are arguable under my own rule.** "Plenty of major programs are not signed, *and thus* plenty of organizations don't enforce code signing" states a cause, which my definition makes `reasoned`. "This might be true but also ipadOS is a buggy mess…" gives a reason of a kind. Where the model calls posts like these `reasoned`, the error may be in the label, not the model. 41 of the 180 rule-based prelabels needed correcting, and 36 of those corrections ended as `reasoned`; this is the boundary the labeling process itself found hardest.

The staff agreement check is the test that would separate (3) from (1) and (2): staff rule 1 (`analysis` vs `hot_take` — does the fact carry the argument?) is the same kind of boundary as `reasoned` vs `assertion`. It came back at 100% on cleaner posts, so it doesn't settle the question. The next step is a second pass over the 48 `assertion` and 85 `reasoned` labels that asks only "is a reason stated?"

**What I would not trust yet.** Criterion 1 passes by one post on two of three seeds, and `assertion` F1 moves 0.400 between seeds on 7 test posts. On new Hacker News comments, I would trust this model to find questions, and not to tell an unsupported claim from a supported one.

## How I Used AI

1. **Repository audit:** I asked Codex to compare the existing local project with the official starter. It found generated example sentences and a custom Naive Bayes model. I replaced those with the starter notebook and genuine public comments, while keeping the existing Git history.
2. **Labeling support:** I used simple text rules to propose labels for 180 comments, then had Codex inspect their full text against the written definitions. Codex changed 41 preliminary tags, including comments where a question introduced an argument rather than seeking an answer. Codex independently labeled and then reread the first 20, changing two more labels. This did not involve human cold labeling.
3. **Unit 6:** Claude (Claude Code) ran the baseline and both three-seed runs, chose and applied the 10-epoch change, labeled the 30 staff posts in `my_staff_labels.csv`, and drafted the Unit 6 analysis in this README.

No hosted model was used for fine-tuning; the official notebook trained locally. To reproduce the run, follow [RUNNING.md](RUNNING.md), create a Python 3.11–3.13 virtual environment, install `requirements.txt`, and run notebook sections 1–5 in order.