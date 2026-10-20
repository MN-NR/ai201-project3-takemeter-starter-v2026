# Community reading notes

Community: public Hacker News comments. Source: the [HN Algolia comments API](https://hn.algolia.com/api/v1/search_by_date?tags=comment), sampled October 20, 2026. Each row in `labels.csv` links to its original HN comment. The API returns HTML; the CSV stores the full comment text with tags removed, HTML entities decoded, and whitespace normalized.

I read more than 40 candidate comments before setting the labels, including HN item IDs 50172723, 50172717, 50172716, 50172709, 50172708, 50172702, 50172699, 50172698, 50172697, 50172695, 50172694, 50172692, 50172686, 50172684, 50172682, 50172680, 50172676, 50172665, 50172663, 50172657, 50172375, 50172371, 50171890, 50172405, 50172314, 50172006, 50171912, 50172192, 50171829, 50172673, 50172089, 50171961, 50171657, 50172144, and 50172411.

Three candidate distinctions visible in the comments:

1. Some comments ask an answerable question or challenge another commenter with an explicit question; many make only a statement.
2. Some claims give a cause, firsthand observation, example, comparison, or concrete detail in the same comment; others expect the reader to supply the support.
3. A few comments merely react or express taste. This overlaps heavily with unsupported claims, so I folded reactions into `assertion` instead of making a fourth label.

Hardest boundary: `reasoned` versus `assertion`. See `label_definitions.txt` for the fixed decision rule. These notes and the five targets in `criteria.md` were committed before training.
