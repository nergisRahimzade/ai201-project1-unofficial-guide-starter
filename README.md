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

**Chunk size:** 256 characters. The initial spec planned for 400, but this was revised to match the maximum input length of the `all-MiniLM-L6-v2` embedding model. Chunks longer than 256 tokens would be silently truncated by the model, causing the tail of each chunk to be lost entirely — not carried into the next chunk — which could introduce hallucinations or missing context in retrieval.

**Overlap:** 50 characters (~20% of chunk size). Carried over proportionally from the original 80-character overlap planned for 400-character chunks. This is enough to prevent important sentences from being split clean across a boundary, without producing excessive redundancy across adjacent chunks.

**Why these choices fit your documents:** The context is mostly short, self-contained reviews (Yelp, Reddit, Niche). A 256-character chunk captures one to two review sentences cleanly. Preprocessing strips extra whitespace and collapses repeated blank lines (`clean_text()` in `ingest_and_chunk.py`) but no HTML stripping was needed since all sources were pre-saved as plain text. URL files (`*_url.txt`) are excluded during ingestion and stored as chunk metadata instead.

**Final chunk count:** 158 chunks across all 12 source documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, stored in a local ChromaDB persistent vector store with cosine similarity.

**Production tradeoff reflection:** The main tradeoff worth weighing for a real deployment would be multilingual support. Stanford's student body has substantial international diversity, and students may search in their first language or use transliterated food terms (e.g., "dal", "pho", "banh mi"). `all-MiniLM-L6-v2` is English-only and would fail to match cross-lingual queries. A model like `paraphrase-multilingual-MiniLM-L12-v2` or OpenAI's `text-embedding-3-small` (API-hosted) would handle this better, at the cost of slightly higher latency or per-query API costs. 

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt explicitly instructs the model: `"ONLY use the retrieved context when answering questions."` It also includes: `"If the user asks you a question which is not related to Stanford dining halls or information about them, say 'Sorry, I can only answer questions related to Stanford dining halls.'"` This creates a two-layer guard — the model is told to stay within the retrieved context, and to reject queries that fall outside the domain entirely.

**How source attribution is surfaced in the response:** The prompt instructs the model to end every answer with a bullet list of citations, each including the source filename and URL if available. The context itself is pre-formatted by `format_context()` in `generate_and_interface.py`, which prepends each chunk with a numbered header: `[N] Source: <filename> (<url>)`. This gives the model explicit, structured attribution labels to reference in its citations.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which dining hall provides halal food around 8–10 pm? | Lakeside Dining is the most reliable option for halal-compatible food close to the 8–10 PM window | Could not identify a specific dining hall; stated no explicit halal information was in the retrieved chunks. Retrieved Stern, Spoon University, and Stanford Daily chunks instead of the official dining page that contains the halal guidance | Off-target | Inaccurate |
| 2 | Which dining hall has the least wait time during lunch that also serves Indian food? | FloMo is the best for Indian food; sources lack direct lunch wait-time comparisons | Correctly noted Stern has faster lines but serves Mexican food; confused Late Night at Lakeside with FloMo for Indian food; could not answer the compound question | Partially relevant | Partially accurate |
| 3 | Which dining hall provides food for Suhoor in Ramadan? | Wilbur Dining and Lakeside Dining both provide Suhoor meal options during Ramadan | Returned "Sorry, I can only answer questions related to Stanford dining halls" — the off-topic guard fired because no retrieved chunk was relevant enough, so the model concluded the question was out of scope | Off-target | Inaccurate |
| 4 | Which dining hall has the best vegetarian food? | FloMo for diverse vegetarian/Indian options; Stern praised by vegetarians specifically | Identified Gerhard Casper based on a roasted vegetables mention; noted Wilbur's poor vegetarian options. A valid partial answer but missed FloMo and Stern as the stronger candidates | Partially relevant | Partially accurate |
| 5 | Which dining hall allows take outs? | No official takeout policy for cooked food; fruit is allowed; students informally use own containers | Correctly explained that takeout containers were phased out, plates can be taken outside but must be returned, and students use personal containers informally. Accurate and well-cited | Relevant | Accurate |

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

**Question that failed:** "Which dining hall provides food for Suhoor in Ramadan?"

**What the system returned:** `"Sorry, I can only answer questions related to Stanford dining halls."` — the system's off-topic guard fired and refused to answer entirely, despite the question being directly relevant to dining.

**Root cause (tied to a specific pipeline stage):** The failure originates in the **embedding and retrieval stage**. The word "Suhoor" (the pre-dawn Ramadan meal) is a transliterated Arabic term that does not appear in any of the source documents. `all-MiniLM-L6-v2` is an English-only model, so it has no semantic representation for this term and instead retrieves chunks based on superficial similarity — returning unrelated dining hall review fragments. With no relevant context in the top-5 chunks, the LLM correctly detected that none of the retrieved chunks were useful, but then incorrectly concluded the question was off-topic and triggered the refusal instruction rather than acknowledging a retrieval gap.

**What you would change to fix it:** Two fixes would help. First, add query expansion or synonym mapping at the retrieval stage — translating "Suhoor" to "pre-dawn meal", "early morning food", or "Ramadan breakfast" before embedding, so the model can retrieve the relevant official dining content. Second, revise the system prompt to distinguish between "the retrieved context doesn't cover this" (which should produce a "I couldn't find information on that" response) versus "this question is not about Stanford dining" (which should produce the refusal). Currently both cases collapse into the same refusal response.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Chunking Strategy section forced an early decision about chunk size relative to the embedding model's context window. Writing it down before implementation revealed the mismatch between the originally planned 400-character chunks and `all-MiniLM-L6-v2`'s 256-token limit. Without the spec, this would likely have been discovered only after seeing degraded retrieval quality, wasting time debugging a silent truncation issue.

**One way your implementation diverged from the spec, and why:** The architecture diagram in planning.md listed `RecursiveCharacterTextSplitter` (a LangChain utility) as the chunking tool, but the final implementation uses a plain Python sliding-window loop in `ingest_and_chunk.py`. This divergence was intentional — after the first AI-generated code used LangChain and produced unnecessarily complex scaffolding, the chunking logic was rewritten from scratch to keep the codebase minimal and dependency-light, since the fixed-size character split is simple enough to implement directly without a framework.

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

- *What I gave the AI: @sources/  @planning.md  
Use these sections of planning.md and sources folder as a reference when executing the task below: Documents, Chunking Strategy, Architecture.

Task:  Implement a script that loads my documents, cleans them and produces chunks matching to my specified chunk size and overlap.*
- *What it produced: A very complicated and detailed code including loading, cleaning and chunking functions. But every function was unnecessarily complicated. And since I already had my sources files formatted and cleaned before starting Milestone 3, I used Claude again to simplify the code and focus on writing the simplest code possible for my application to work faster and cleaner.*
- *What I changed or overrode: Simplified the code by removing unnecessary complexity and focusing on the essential functionality.*

**Instance 2**

- *What I gave the AI: @documents/chunks.jsonl  @sources/ @planning.md  @scripts/ingest_and_chunk.py 

Use Retrieval Approach, Architecture section of planning.md to execute the task below.

Task:  Implement the embedding step (load chunks from my ingestion pipeline, embedding with all-MiniLM-L6-v2, store in ChromaDB with source metadata), and write a retrieval function.

Explain everything you did in detail and why you did it to me at the end of your response, please.
*
- *What it produced: A simple embedding and retrieval pipeline using all-MiniLM-L6-v2 and ChromaDB*
- *What I changed or overrode: Honestly, I didn't change or override anything after testing with a question. The results were good enough to give the user an accurate results.*
