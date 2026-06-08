# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I chose the domain of student reviews of dining halls at Stanford University. I chose this domain because Stanford has a large variety of dining halls with their own distinctive features. My system will help students find the dining hall that best suits their preferences and needs based on the reviews and general information provided in the sources that I gathered. Students will be able to ask questions and get answers in a short amount of time, without having to read through every review or piece of information, based on the sources provided to the LLM.  

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source                                                       | Description                                                                                    | URL or location                                                                                    |
| --- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 1   | Niche — Stanford Campus Life                                 | Student poll results and ratings for Stanford campus life, including dining                    | https://www.niche.com/colleges/stanford-university/campus-life/                                    |
| 2   | Reddit r/stanford — Taking food out the dining hall          | Reddit thread discussing rules and experiences around taking food out of Stanford dining halls | https://www.reddit.com/r/stanford/comments/1sgzl6a/taking_food_out_the_dining_hall/                |
| 3   | Reddit r/stanford — Dining Halls                             | Reddit thread with student opinions and comparisons of Stanford dining halls                   | https://www.reddit.com/r/stanford/comments/1mvw2p8/dining_halls/                                   |
| 4   | Reddit r/stanford — Flo Mo dining discussion                 | Reddit thread debating whether FloMo is the best or worst dining hall at Stanford              | https://www.reddit.com/r/stanford/comments/zwa937/a_couple_of_hours_ago_i_asked_if_flo_mo_was_the/ |
| 5   | Spoon University — Stanford Dining Halls Definitive Ranking  | Student-written ranking of all Stanford dining halls with descriptions and opinions            | https://spoonuniversity.com/lifestyle/dining-halls-at-stanford-definitive-ranking/                 |
| 6   | The Stanford Daily — Students on Their Favorite Dining Halls | Stanford Daily article featuring student opinions on their favorite dining halls               | https://stanforddaily.com/2022/01/09/stanford-students-on-their-favorite-dining-halls/             |
| 7   | Stanford Official Dining & Hospitality                       | Official Stanford RDE page describing dining programs, hours, and offerings                    | https://rde.stanford.edu/dining-hospitality/welcome-stanford-dining-hospitality-auxiliaries        |
| 8   | Yelp — Arrillaga Family Dining Commons                       | Yelp reviews for Arrillaga Family Dining Commons at Stanford                                   | https://www.yelp.com/biz/arrillaga-family-dining-commons-stanford-3                                |
| 9   | Yelp — Arrillaga Nights                                      | Yelp reviews for Arrillaga Nights (late-night dining) at Stanford                              | https://www.yelp.com/biz/arrillaga-nights-stanford-3                                               |
| 10  | Yelp — Stern Dining Hall                                     | Yelp reviews for Stern Dining Hall at Stanford                                                 | https://www.yelp.com/biz/stern-dining-hall-stanford                                                |
| 11  | Yelp — Top 10 Stanford Dining Halls                          | Yelp search results listing and reviewing top dining halls at Stanford                         | https://www.yelp.com/search?find_desc=Dining+Hall&find_loc=Stanford%2C+CA+94305                    |
| 12  | Yelp — Wilbur Dining                                         | Yelp reviews for Wilbur Dining at Stanford                                                     | https://m.yelp.com/biz/wilbur-dining-stanford                                                      |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:*400 tokens*

**Overlap:*80 tokens*

**Reasoning:*Since the sources in this project are mostly reviews, chunk size of 400 tokens and overlap size of 80 (20% of chunk size) will be big enough to capture the context of each review and small enough to catch the details without a lot of repetition.*

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:*all-MiniLM-L6-v2 via sentence-transformers*

**Top-k:*5*

**Production tradeoff reflection:*Probably multilingual support since Stanford University has a large diversity in nationalities with their students.*

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                                                             | Expected answer                                                                                                                                                                                                                            |
| --- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Which dining hall provide halal food around 8-10 pm?                                 | Lakeside Dining is the most reliable option if you're specifically looking for halal-compatible food availability close to the 8–10 PM window.                                                                                             |
| 2   | Which dining hall has the least wait time during lunch that also serves Indian food? | FloMo is the best option for Indian food, though the sources don't directly compare lunch wait times across halls. The sources don't have enough data to definitively answer the "least wait time" part — this is worth flagging as a gap. |
| 3   | Which dining hall provide food for Sahoor in Ramadan?                                | Stanford explicitly lists:
Wilbur Dining
Lakeside Dining

Both provide build-your-own Suhoor meals/boxes during Ramadan. Lakeside additionally offers late-night pickup opportunities through its Late Night Kitchen. |
| 4 | Which dining hall has the best quality vegan food?| Most likely: Gerhard Dining (because of Lemongrass Kitchen).

Stanford also notes that all dining halls provide extensive vegan options and that the dining program has received strong recognition for vegan dining overall.|
| 5 | Which dining hall allows take outs?| No dining hall currently has an official takeout policy for cooked food. Fruit can be taken out. Students work around this by bringing their own containers, but this is informal, not an official service any specific dining hall offers.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Missing source attribution: If the user asks a too general question like "What do students say about the dining halls?" the system might not have enough information to provide an answer as accurate as the student was looking for.

2. Noisy or inconsistent documents: Since the reviews are not grouped or organized in any way, the system might have trouble retrieving the relevant topic from the reviews. For example, if the user asks about food hygiene, the system might answer topics related to food quality instead of sickness experience of the students, which is more relevant to hygiene.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     ```mermaid
     graph LR
          A[Document Ingestion\nos / pdfplumber] --> B[Chunking\nRecursiveCharacterTextSplitter]
          B --> C[Embedding\nall-MiniLM-L6-v2]
          C --> D[Vector Store\nChromaDB]
          D --> E[Retrieval\nChromaDB .query]
          E --> F[Generation\nGroq llama-3.3-70b]
          F --> G[UI\nGradio]
     ```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:*
     I will use Copilot to help me code Ingestion using the content in my sources folder. For Chunking, I will use Copilot to implement chunking using the RecursiveCharacterTextSplitter from Langchain, by giving the details of my chunking strategy from the Chunking Strategy section of planning.md. I expect it to produce a function or use a pre-built function that chunks the context using information in sources folder. I will verify the output by testing the function on a sample document and see if the output chunks are of the expected size and overlap as well as checking if I need to change the details of Chunking Strategy based on the output Copilot provides.
*

**Milestone 4 — Embedding and retrieval:*
     For Embedding and Retrieval, I will use Copilot to implement embedding using all-MiniLM-L6-v2 model via sentence-transformers, also giving it Retrieval Approach section of planning.md for Copilot to understand the details of embedding and retrieval and have an output closer to what I expect. I expect Copilot to produce a function that takes the chunks from the previous stage and use the model, I specified it to use for embedding and retrieval, to embed the vectors in ChromaDb effectively. I will verify the output by testing the function on a sample chunk and see if the output embedding is relevant to the input chunk and if the retrieval function works without any bugs or errors and retrieves the relevant chunks based on the sample chunk.
*

**Milestone 5 — Generation and interface:*
     For Generation, I will use Copilot to implement prompting the model, I provide by giving the Architecture section of planning.md, and generating an answer based on the retrieved chunks from previous stage. For Interface, I will use Copilot to implement a simple Gradio interface. I expect Copilot to create a clean, easy-to-use interface as well as a bugless function for generation. I will verify the output of generation by testing the function with the questions in Evaluation Plan section of planning.md and compare the results I get from the function with the expected answers. After comparing, I will decide if I need to change any detail of implementation in Ingestion, Chunking, Embedding, Retrieval or Generation stage to get a more accurate answer. 
*
