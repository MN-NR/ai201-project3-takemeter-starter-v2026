# TakeMeter

TakeMeter is a lightweight text classifier for community posts. I chose the music discussion community pattern: it gives a clean three-way taxonomy that is easy to define and easy to judge by hand.

The label set is:

- `critique` — a post that evaluates the music with specific evidence, like production choices, songwriting, vocals, sequencing, or pacing.
- `hot_take` — a post that gives a strongly stated opinion but offers little or no supporting material.
- `recap` — a post that mainly summarizes what happened in a release cycle, show, or listening session without doing a real review.

This project builds the label taxonomy first, collects and labels 200 posts, trains a compact classifier on that data, and saves the training metrics in a repeatable run. The model is intentionally small and cheap enough to run on every post in a feed without needing a large GPU or a long inference loop.

## Dataset and decision rule

The core boundary is between critique and hot_take:

- If the post names at least two concrete musical details and makes a reasoned judgment, it is `critique`.
- If the post states a strong opinion with almost no evidence, it is `hot_take`.
- If the post mostly describes events, reactions, or a timeline, it is `recap`.

The hard case is any post that looks like a reaction and a verdict at the same time. My decision rule is: if the post contains specific material evidence (e.g. "the chorus is repetitive," "the bassline is muddy," "the mix is too bright") and grounds the opinion in those details, label `critique`. If it says "this is overrated / awful / genius" without describing why, label `hot_take`. If it reads like a release thread, show recap, or what happened last night, label `recap`.

## Taxonomy notes

The strongest signal in this dataset is not genre-specific vocabulary; it is structure. A critique post normally has a claim plus evidence. A hot take often has a claim without evidence. A recap is about sequence and event, not quality. That distinction is stable enough for two people to apply consistently once written down.

## Project files

- `criteria.md` — the five acceptance criteria written before the model was trained.
- `data/posts.csv` — 200 hand-labeled community posts with the taxonomy applied.
- `takemeter.py` — model and preprocessing logic.
- `train.py` — training loop, validation split, metrics export.
- `app.py` — simple inference CLI.
- `results/metrics.json` — saved metrics from the training run.

## Run it

```bash
python3 train.py
python3 app.py "this album is a masterpiece because the hooks are huge and the production balance keeps the vocals front and center"
```

The saved model is a simple bag-of-words classifier trained with a small custom Naive Bayes implementation. It is small, explainable, and fast enough to score a live feed in near-real time.
