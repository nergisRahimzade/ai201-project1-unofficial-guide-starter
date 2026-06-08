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

## Sample Chunks

<!-- At least 5 labeled sample chunks, each with its source document name.
     These are verbatim chunks produced by ingest_and_chunk.py. -->

These are five verbatim chunks emitted by `ingest_and_chunk.py` (256-char window, 50-char overlap). Each is labeled with its chunk ID, which encodes the source document name and chunk index.

**Chunk 1 — `niche_stanford_poll_results.txt::chunk0`**
> Title: Niche - Stanford University Campus Life Polls Overall Rating: 4.0 Total Reviews: 154 Reviewer: Student Poll (Dining Facility Rating) Date: Updated recently Review: 80% of students highly rate the dining facilities. (Based on 108 responses) Reviewe

**Chunk 2 — `reddit_stanford_dining_1_content.txt::chunk0`**
> Title: Reddit - r/stanford (Thread: Taking food out the dining hall) Reviewer: ineedfundingpls Date: 2 months ago Review: Yes, you're allowed to take plates outside (since there's outdoor seating too), though you are expected to return the plates/cutlery.

**Chunk 3 — `spoon_university_ranking.txt::chunk0`**
> The Definitive Ranking of Stanford Dining Halls April 1, 2015 Spoon University It's 6 pm, you just came home from a full day of classes, finished a physics review session, and are on your way to orchestra practice. On top of all that, you're hungry. Where

**Chunk 4 — `yelp_stern_reviews.txt::chunk0`**
> Dining Hall Name: Stern Dining Hall Address: 618 Escondido Road, Stanford, CA 94305 Overall Rating: 3.3 Total Reviews: 7 Reviewer: Tamara M. Date: 2 years ago Review: Chipotle-style burrito bowls save an otherwise ho-hum dining hall. This reporter also lo

**Chunk 5 — `yelp_wilbur_dining_reviews.txt::chunk0`**
> Dining Hall Name: Wilbur Dining Address: 658 Escondido Rd, Stanford, CA 94305 Overall Rating: 2.7 Total Reviews: 9 Reviewer: Andrew A. Date: 3 months ago Review: Some old reviews. Food is good. Not sure why a review is allowed from 10 years ago. Just note

> Note: chunks are truncated mid-sentence at the 256-character boundary by design — the 50-character overlap with the following chunk recovers the cut-off text so no content is lost across the boundary.

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

## Retrieval Test Results

<!-- At least 3 queries, each showing the query and the top returned chunks.
     For at least 2, explain why the returned chunks are relevant. -->

The following are real top-5 retrievals from the ChromaDB store (`retrieve()` in `embed_and_retrieve.py`, cosine distance — **lower = more similar**). Chunk text is condensed to one line for readability; source and distance are shown verbatim.

### Query 1 — "Which dining hall has the best Indian food?"

| Rank | Source chunk | Distance | Snippet |
|------|--------------|----------|---------|
| 1 | `yelp_top10_stanford_dining_reviews.txt #chunk2` | 0.3436 | "...they consistently have **good indian food and vegetarian dishes** that actually taste seasoned..." |
| 2 | `stanford_daily_dining_opinions.txt #chunk8` | 0.3713 | "...Stern is my favorite... Gerhard Casper... most amazing roasted vegetables..." |
| 3 | `spoon_university_ranking.txt #chunk7` | 0.3724 | "...burrito bowls save an otherwise ho-hum dining hall... 6. Lakeside Dining..." |
| 4 | `spoon_university_ranking.txt #chunk6` | 0.3732 | "...extensive vegan and vegetarian options, homemade soups... 5. Stern Dining..." |
| 5 | `stanford_daily_dining_opinions.txt #chunk10` | 0.3811 | "...quality of the food at each of the dining halls is comparable..." |

**Why these chunks are relevant:** Rank 1 is the single most on-target chunk for this query — it explicitly says a dining hall "consistently [has] good indian food and vegetarian dishes that actually taste seasoned," which directly matches the Indian-cuisine specifier. The embedding surfaced it at distance 0.3436 because "indian food" appears verbatim, the strongest possible signal. Ranks 2–5 are relevant but weaker: they are general "favorite dining hall" / "best options" passages that share the query's intent ("best ... food") without naming Indian cuisine, which is why they cluster just behind the literal match.

### Query 2 — "Can I take food out of the dining hall?"

| Rank | Source chunk | Distance | Snippet |
|------|--------------|----------|---------|
| 1 | `reddit_stanford_dining_1_content.txt #chunk0` | 0.3156 | "...you're allowed to take plates outside... expected to return the plates/cutlery..." |
| 2 | `reddit_stanford_dining_1_content.txt #chunk10` | 0.3719 | "...staff might side-eye you... grabbing a few reusable containers... pack real meals..." |
| 3 | `yelp_wilbur_dining_reviews.txt #chunk17` | 0.4233 | "...pay with cash or cardinal dollars... even for dining hall food it's not great..." |
| 4 | `stanford_daily_dining_opinions.txt #chunk5` | 0.4244 | "...if I'm busy... I need a quick meal, I'll go to Arrillaga..." |
| 5 | `spoon_university_ranking.txt #chunk4` | 0.4543 | "...grilled selections, and pizza every day... 3. Ricker Dining... Death by Chocolate Cake..." |

**Why these chunks are relevant:** This is the strongest retrieval in the test set. Rank 1 sits at distance 0.3156 — closer than anything in Query 1 — because the chunk is literally the answer: plates can be taken outside but must be returned. Rank 2, from the same Reddit takeout thread, reinforces it with the informal workaround (students using their own reusable containers). Ranks 3–5 are off-topic intrusions — generic dining-hall passages that share the words "food" / "dining hall" but say nothing about taking food out, which is why they fall off sharply past distance 0.42.

### Query 3 — "Which dining hall has the best vegetarian food?"

| Rank | Source chunk | Distance | Snippet |
|------|--------------|----------|---------|
| 1 | `spoon_university_ranking.txt #chunk6` | 0.2971 | "...extensive **vegan and vegetarian options**, homemade soups... 5. Stern Dining..." |
| 2 | `stanford_daily_dining_opinions.txt #chunk8` | 0.3355 | "...Gerhard Casper... most amazing **roasted vegetables**... best fish..." |
| 3 | `stanford_daily_dining_opinions.txt #chunk10` | 0.3931 | "...quality of the food at each of the dining halls is comparable..." |
| 4 | `yelp_arrillaga_reviews.txt #chunk30` | 0.3936 | "...so many options and I can always find some food I'll be happy with..." |
| 5 | `yelp_stern_reviews.txt #chunk3` | 0.3961 | "...meat options are solid, and the guacamole is actually pretty good..." |

**Why these chunks are relevant:** Rank 1 is the cleanest match in the entire test set (distance 0.2971) — it explicitly names a hall with "extensive vegan and vegetarian options," exactly the dietary specifier the query asks for. Rank 2 reinforces it with Gerhard Casper's "most amazing roasted vegetables." The drop from 0.3355 (rank 2) to 0.3931 (rank 3) marks the boundary where retrieval shifts from vegetable-specific endorsements to generic "good food" passages — the system found two strongly relevant chunks and then ran out of vegetarian-specific material in the corpus, which is the honest shape of this small review set.

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

## Example Responses

<!-- At least 2 responses with source attribution visible in the output text,
     plus one out-of-scope query showing the refusal response. -->

These are verbatim outputs from `generate()` in `generate_and_interface.py` (Groq `llama-3.3-70b-versatile` over the top-5 retrieved chunks). Source attribution is visible inline in every answer.

### Example 1 — in-scope, with source attribution

**Query:** "Which dining hall allows take outs?"

> According to the context, it appears that taking food out of the dining hall is not officially allowed, but students have been able to do so without being stopped by using their own reusable containers. There is no specific dining hall mentioned that explicitly allows take outs. However, the context suggests that students have been able to take food out of the dining hall without issue, as long as they use their own containers.
>
> * Source: reddit_stanford_dining_1_content.txt (https://www.reddit.com/r/stanford/comments/1sgzl6a/taking_food_out_the_dining_hall/)
> * Source: spoon_university_ranking.txt (https://spoonuniversity.com/lifestyle/dining-halls-at-stanford-definitive-ranking/)
> * Source: stanford_daily_dining_opinions.txt (https://stanforddaily.com/2022/01/09/stanford-students-on-their-favorite-dining-halls/)

### Example 2 — in-scope, with source attribution

**Query:** "Which dining hall has the best vegetarian food?"

> According to the retrieved context, Branner dining hall has extensive vegan and vegetarian options, homemade soups, and consistently good food five nights a week, making it a go-to dining hall. Additionally, Gerhard Casper Dining Commons is mentioned as having the "most amazing roasted vegetables". However, based on the available information, it seems that Branner might have a wider range of vegetarian options.
>
> * Source: spoon_university_ranking.txt (https://spoonuniversity.com/lifestyle/dining-halls-at-stanford-definitive-ranking/)
> * Source: stanford_daily_dining_opinions.txt (https://stanforddaily.com/2022/01/09/stanford-students-on-their-favorite-dining-halls/)

### Example 3 — out-of-scope query (refusal)

**Query:** "What time does the campus library close?"

> Sorry, I can only answer questions related to Stanford dining halls.
>
> * No citations

The off-topic guard in the system prompt fires correctly here: the query has nothing to do with dining, no retrieved chunk supports an answer, and the model returns the exact refusal string instead of speculating.

---

## Query Interface

<!-- Describe the input and output fields, plus a sample interaction transcript
     showing one complete query and response. -->

The interface is a Gradio `ChatInterface` (`build_interface()` in `generate_and_interface.py`), launched with `python scripts/generate_and_interface.py`.

**Input field:** a single free-text textbox (placeholder *"Ask about Stanford dining halls..."*) where the user types one natural-language question. Three example questions are shown as clickable chips. Each question is answered fresh from freshly-retrieved context — prior chat history is intentionally **not** fed back into the model (see `chat_fn`), so every answer is grounded only in the chunks retrieved for the current question.

**Output field:** a chat bubble containing the model's response. The response always has two parts, enforced by the system prompt: (1) the answer grounded in retrieved context, and (2) a bullet-list of citations naming the source document (and URL when available), or the literal string "No citations".

**Processing pipeline per query:** user question → `retrieve()` embeds the query with `all-MiniLM-L6-v2` and pulls the top-5 nearest chunks from ChromaDB → `format_context()` numbers and labels each chunk with its source → the labeled context plus the question are sent to Groq `llama-3.3-70b-versatile` under the grounding system prompt → the answer is rendered in the chat window.

**Sample interaction transcript:**

```
User:  Which dining hall allows take outs?

Guide: According to the context, it appears that taking food out of the
       dining hall is not officially allowed, but students have been able to
       do so without being stopped by using their own reusable containers.
       There is no specific dining hall mentioned that explicitly allows take
       outs. However, the context suggests that students have been able to
       take food out of the dining hall without issue, as long as they use
       their own containers.

       * Source: reddit_stanford_dining_1_content.txt
         (https://www.reddit.com/r/stanford/comments/1sgzl6a/taking_food_out_the_dining_hall/)
       * Source: spoon_university_ranking.txt
         (https://spoonuniversity.com/lifestyle/dining-halls-at-stanford-definitive-ranking/)
       * Source: stanford_daily_dining_opinions.txt
         (https://stanforddaily.com/2022/01/09/stanford-students-on-their-favorite-dining-halls/)
```

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
