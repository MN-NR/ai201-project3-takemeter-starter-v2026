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

## How I Used AI

1. **Repository audit:** I asked Codex to compare the existing local project with the official starter. It found generated example sentences and a custom Naive Bayes model. I replaced those with the starter notebook and genuine public comments, while keeping the existing Git history.
2. **Labeling support:** I used simple text rules to propose labels for 180 comments, then had Codex inspect their full text against the written definitions. Codex changed 41 preliminary tags, including comments where a question introduced an argument rather than seeking an answer. Codex independently labeled and then reread the first 20, changing two more labels. This did not involve human cold labeling.

No hosted model was used for fine-tuning; the official notebook trained locally. To reproduce the run, follow [RUNNING.md](RUNNING.md), create a Python 3.11–3.13 virtual environment, install `requirements.txt`, and run notebook sections 1–5 in order.
