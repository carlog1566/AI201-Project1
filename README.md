# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
Best dining options at Cal Poly Pomona - This is useful because there may be incoming freshman or transfer students who don't know what to eat with there being many options. It also helps with students who live on campus who are trying to decide which meal plan is the best.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #  | Source           | Type                         | URL or file path |
|----|------------------|------------------------------|------------------|
| 1  | Yelp             | Review Page                  | https://www.yelp.com/biz/centerpointe-dining-commons-pomona |
| 2  | OpenTable        | Restaurant Directory         | https://www.opentable.com/landmark/restaurants-near-california-state-polytechnic-university-pomona |
| 3  | CPP Dining       | Official Dining Website      | https://cppdining.com/eat-well-cpp/ |
| 4  | CPP Dining       | Official University Page     | https://www.cpp.edu/aboutcpp/visitor-information/dining.shtml |
| 5  | The Poly Post    | School News Article          | https://thepolypost.com/arts-and-culture/2020/02/04/review-centerpointe-dining-commons-is-the-new-go-to-spot/ |
| 6  | Reddit           | Discussion Thread            | https://www.reddit.com/r/CalPolyPomona/comments/1fg56da/cpp_dining_tier_list/ |
| 7  | Reddit           | Search Thread (Dining Posts) | https://www.reddit.com/r/CalPolyPomona/search/?q=dining |
| 8  | Tripadvisor      | Review Directory             | https://www.tripadvisor.com/RestaurantsNear-g32911-d5789363-California_State_Polytechnic_University_Pomona-Pomona_California.html |
| 9  | Niche            | Student Reviews              | https://www.niche.com/colleges/california-state-polytechnic-university-pomona/reviews/ |
| 10 | CPP Housing Page | Dining Information Page      | https://www.cpp.edu/housing/dining.shtml |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 350 Tokens

**Overlap:** 50 Tokens

**Why these choices fit your documents:** I chose a chunk size of 350 tokens becuase it felt like a balance to preserve context while also having precision. Since most of the websites had short content due to it mainly being composed of review pages, social media posts, and some official university websites, this token size felt like a good balance to retain complete opinions and dining experiences while also being able to preserve information for the more text heavy websites. An overlap of 50 tokens would also help retain that important information.

**Final chunk count:** 13

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** The tradeoffs in choosing a different embedding model depends on either prioritizing efficiency or accuracy. If we chose a more lightweight model, it would be more efficient and fast making it good for a small-scale RAG system, but it may not be as good with semantic understanding which is a very important aspect due to our domain and sources being heavily based on semantics. A more advanced embedding model would improve semantic undertsanding which would work great for this, but it would introduce higher latency and cost.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system enforces grounding by instructing the LLM to use only the retrieved context and to explicitly say it lacks information if the answer is not present in the provided chunks.

**How source attribution is surfaced in the response:** Source attribution is handled outside the model by attaching source metadata to each retrieved chunk and displaying the deduplicated list of source URLs in the UI alongside the generated answer.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the wait times at Centerpointe Dining Commons during lunch hours? | Students usually report that there usually isn't any rush lines and even at its peak hours the lines are very minor to none. | States it does not have enough information but mentions an approximate 10 minute wait time for sushi | Partially Relevant | Inaccurate |
| 2 | Is the meal plan at Cal Poly Pomona considered worth it by students? | Mixed opinions; As it is a required purchase in order to live on campus, some feel as though they are wasting money they could use on food they actually want while others like it for the convenience. | Says it is well worth the money for at least some students | Relevant | Accurate |
| 3 | What are common complaints about campus dining at CPP? | Common complaints include the lack of dining options, inconsistent food quality, and long wait times at the fast food places during peak hours. | Not enought information/doesn't mention complaints | Off-target | Inaccurate |
| 4 | Where do students recommend eating near Cal Poly Pomona off-campus? | Students usually recommend the nearby fast food or local restaurants in Pomona, West Covina, or Diamond Bar as better alternatives to campus dining. | Not enough information, says it provides dining options but not where students recommend | Partially relevant | Inaccurate |
| 5 | How do students compare the Centerpointe Dining Commons to other options on campus? | Students do like the price and buffet nature of Centerpointe; however, students often prefer the other on campus restaurants like Panda Express and Qdoba. | Not enough information/no direct comparison | Off-target | Inaccurate |

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

**Question that failed:** What are common complaints about campus dining at CPP?

**What the system returned:** The system failed to retrive complaint-specific chunks and responded with not enough information.

**Root cause (tied to a specific pipeline stage):** The failure originates from the Ingest and Chunking stage as it failed to properly scrape and chunk the right information from sties that provide complaints

**What you would change to fix it:** Fix the scraper and increase the chunk overlap to retain more important information

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The pipeline design in planning.md guided me on how each stage is split within the RAG pipeline and also helped me test each stage. Defining a chunk size and overlap within planning.md also helped since it helped me avoid inconsistent splitting and overall helped me be more structured within this process.

**One way your implementation diverged from the spec, and why:** During my implementation, I adjusted the learning rules and filtering logic to remove irrelevant text. I also reduced the reliance from some of the social media sources since they didn't contribute any meaningful and retrievable text.

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

- *What I gave the AI:* My chunking strategy from planning.md and sample scraped dining reviews
- *What it produced:* A basic chunking function with fixed-size splits (400 chars)
- *What I changed or overrode:* I adjusted the chunking to use word-based splitting rather than character-based and increased the overlap to 80 words

**Instance 2**

- *What I gave the AI:* My pipeline design for retrieval and embedding
- *What it produced:* A working RAG architecture suing sentence-transformers and ChromaDB but without source tracking
- *What I changed or overrode:* I made it so that the pipeline would have attatched metadata to every chunk so I can trace the answers back to their original source
