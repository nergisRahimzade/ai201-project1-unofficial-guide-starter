# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Student reviews of dining halls at Stanford University. This knowledge is valuable because Stanford has a large variety of dining halls with their own distinctive features, and official sources don't capture the student experience — things like food quality, atmosphere, wait times, and hidden gems. My system helps students find the dining hall that best suits their preferences and needs based on real reviews, without having to read through every source manually.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Niche — Stanford Campus Life | Poll results / ratings | https://www.niche.com/colleges/stanford-university/campus-life/ |
| 2 | Reddit r/stanford — Taking food out the dining hall | Reddit thread | https://www.reddit.com/r/stanford/comments/1sgzl6a/taking_food_out_the_dining_hall/ |
| 3 | Reddit r/stanford — Dining Halls | Reddit thread | https://www.reddit.com/r/stanford/comments/1mvw2p8/dining_halls/ |
| 4 | Reddit r/stanford — Flo Mo dining discussion | Reddit thread | https://www.reddit.com/r/stanford/comments/zwa937/a_couple_of_hours_ago_i_asked_if_flo_mo_was_the/ |
| 5 | Spoon University — Stanford Dining Halls Definitive Ranking | Student article / ranking | https://spoonuniversity.com/lifestyle/dining-halls-at-stanford-definitive-ranking/ |
| 6 | The Stanford Daily — Students on Their Favorite Dining Halls | Student newspaper article | https://stanforddaily.com/2022/01/09/stanford-students-on-their-favorite-dining-halls/ |
| 7 | Stanford Official Dining & Hospitality | Official university page | https://rde.stanford.edu/dining-hospitality/welcome-stanford-dining-hospitality-auxiliaries |
| 8 | Yelp — Arrillaga Family Dining Commons | Yelp reviews | https://www.yelp.com/biz/arrillaga-family-dining-commons-stanford-3 |
| 9 | Yelp — Arrillaga Nights | Yelp reviews | https://www.yelp.com/biz/arrillaga-nights-stanford-3 |
| 10 | Yelp — Stern Dining Hall | Yelp reviews | https://www.yelp.com/biz/stern-dining-hall-stanford |
| 11 | Yelp — Top 10 Stanford Dining Halls | Yelp search / reviews | https://www.yelp.com/search?find_desc=Dining+Hall&find_loc=Stanford%2C+CA+94305 |
| 12 | Yelp — Wilbur Dining | Yelp reviews | https://m.yelp.com/biz/wilbur-dining-stanford |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
