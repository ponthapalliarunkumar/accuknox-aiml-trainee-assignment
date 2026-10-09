# AccuKnox AI/ML Trainee Assignment

**Name:** Ponthapalli Arun Kumar
**Email:** ponthapalliarun@gmail.com | **Phone:** 9032858909
**GitHub:** https://github.com/ponthapalliarunkumar
**Resume:** [Ponthapalli_Arun_Kumar_Resume.pdf](Ponthapalli_Arun_Kumar_Resume.pdf)

---

## Contents

1. [Assignment 1: Coding](#assignment-1-coding)
2. [Most complex code links](#most-complex-code-links)
3. [Assignment 2: Research](#assignment-2-research)
4. [How to run](#how-to-run)

---

## Assignment 1: Coding

| # | Problem | File | Output |
|---|---------|------|--------|
| 1 | Fetch books from a REST API, store in SQLite, display | [`api_to_sqlite.py`](Assignment_1_Coding/api_to_sqlite.py) | `books.db` + printed table |
| 2 | Fetch student scores, find the average, draw a bar chart | [`test_scores_viz.py`](Assignment_1_Coding/test_scores_viz.py) | `scores_chart.png` |
| 3 | Read users from a CSV and insert into SQLite | [`csv_to_db.py`](Assignment_1_Coding/csv_to_db.py) | `users.db` |

### Assumptions

**Problem 1: Books API to SQLite**
- The API returns JSON with a title, an author and a publication year for each book. I used a public books API (Open Library). If a field is missing, I store `NULL` / "Unknown" instead of crashing.
- Table name is `books` with columns `id` (auto), `title`, `author`, `year`.
- Running the script twice should not create duplicates. I treat `title + author` as unique and skip repeats.
- If the API fails or times out, the script prints a clear error and exits. It does not write partial data.

**Problem 2: Test scores and bar chart**
- No fixed API was given, so I assumed a JSON endpoint that returns a list like `[{"name": "Asha", "score": 78}, ...]`. For testing I used a mock/public endpoint with the same shape.
- Scores are numbers from 0 to 100. Entries with a missing or non-numeric score are skipped and counted in the output.
- The average is the simple mean of all valid scores. The chart shows one bar per student, with a dashed line for the average. It is saved as a PNG.

**Problem 3: CSV to SQLite**
- The CSV has a header row with `name,email`.
- Email is unique. Rows with a blank name or email, or a duplicate email, are skipped and reported at the end.
- Insertion is done in a single transaction, so a crash in the middle does not leave half-loaded data.

### Sample output

> Add screenshots here after running each script:
> - `screenshots/books_output.png`
> - `screenshots/scores_chart.png`
> - `screenshots/csv_import_output.png`

---

## Most complex code links

- **Most complex Python code:** [PASTE LINK, for example the AI Research & Analysis Agent repo]
  Short description: what it does, which libraries it uses (Streamlit, Gemini, RAG), and what was hardest about it.

- **Most complex database code:** [PASTE LINK, for example your SQLite scripts or the Student Management System]
  Short description: tables, relations, queries, and what was hardest about it.

---

## Assignment 2: Research

### 1. Self-rating

(A = can code independently, B = can code under supervision, C = little or no understanding)

| Area | Rating | Note |
|------|--------|------|
| LLM | **[B]** | Built chatbot / RAG apps using hosted APIs. Not trained or fine-tuned large models on my own. |
| Deep Learning | **[B]** | Understand networks, backpropagation and training basics. Still learning advanced architectures. |
| AI | **[B]** | Built agents with tool calling and a RAG Q&A app. |
| ML | **[B]** | Comfortable with Python, pandas, NumPy and standard ML workflow. |

*Change these to what is true for you. Interviewers will ask about whatever you rate yourself.*

### 2. Key components of an LLM-based chatbot

A chatbot is more than a model. These are the parts, in the order a message flows through them:

```
 User
  |
  v
[1] Frontend (web / app / Slack)
  |
  v
[2] Backend API  --> auth, rate limits, logging
  |
  v
[3] Input guardrails (filter bad / unsafe input)
  |
  v
[4] Memory / history  <--> session store (Redis / DB)
  |
  v
[5] Retriever (RAG) <--> embedding model <--> vector database <--> documents
  |
  v
[6] Prompt builder = system prompt + history + retrieved context + question
  |
  v
[7] LLM (hosted API or self-hosted)
  |
  v
[8] Output guardrails (check answer, remove sensitive data)
  |
  v
 Answer to user
  |
  v
[9] Logging and evaluation (feedback, quality checks, cost tracking)
```

**What each part does**

1. **Frontend:** where the user types. Can be a simple web chat or Streamlit page.
2. **Backend API:** receives the message, handles login, and calls the other parts (FastAPI / Flask).
3. **Input guardrails:** blocks prompt-injection attempts and unsafe or off-topic input.
4. **Memory:** the LLM does not remember by itself. We save previous messages and send the recent ones with each request. Long chats get summarised to stay inside the context window.
5. **Retriever (RAG):** the LLM only knows its training data. For company documents, we split them into chunks, convert them to embeddings, store them in a vector database, and at question time fetch the most similar chunks.
6. **Prompt builder:** combines instructions, history, retrieved text and the question into one prompt. A good instruction like "answer only from the context, otherwise say you don't know" reduces made-up answers.
7. **LLM:** generates the answer. Choice depends on quality, cost, speed and privacy (a hosted API vs. a self-hosted open model).
8. **Output guardrails:** checks the response for policy problems, leaked secrets, or missing sources.
9. **Logging and evaluation:** store questions, answers and feedback, so we can measure answer quality, catch failures and control cost.

**Optional parts:** tools / function calling (so the bot can query a database or call an API), a re-ranker to improve retrieval, and caching to save cost.

### 3. Vector databases

**What problem they solve.** Normal databases search by exact values (`WHERE name = 'x'`). Text, images and audio have meaning that exact matching can't capture. "How do I reset my password?" and "I forgot my login" share no keywords but mean almost the same thing.

**How they work**
1. An *embedding model* turns each piece of data into a list of numbers (a vector, for example 384 or 1536 numbers). Similar meanings give vectors that are close together.
2. The vectors are stored along with the original text and metadata (source, date, etc.).
3. At query time, the question is converted to a vector too, and the database finds the nearest vectors using a distance measure (cosine similarity, dot product or Euclidean distance).
4. Checking every vector is slow at large scale, so vector databases use *approximate nearest neighbour* (ANN) indexes such as **HNSW** (graph-based), **IVF** (cluster-based) or **PQ** (compression). They trade a tiny bit of accuracy for a big speedup.

**Common options**

| Database | Type | Good for | Limitation |
|----------|------|----------|------------|
| FAISS | Library (not a full DB) | Fast local experiments | No built-in storage, filtering, or server |
| Chroma | Open source, embedded | Prototypes, small apps | Not meant for very large scale |
| Qdrant | Open source / cloud | Production, strong metadata filtering | Needs hosting / ops |
| Milvus | Open source, distributed | Very large scale (billions of vectors) | More complex to run |
| Pinecone | Managed cloud | No infrastructure to manage | Paid, data lives on their cloud |
| pgvector | PostgreSQL extension | Apps already on Postgres | Slower than dedicated systems at huge scale |

### Hypothetical problem and my choice

**Problem:** A cloud-security company wants an internal chatbot that answers engineers' questions from about 5,000 policy and runbook documents (around 100,000 chunks). The documents are internal, so they must not leave the company's environment. Answers must be filterable by team and document version, and the documents are updated weekly.

**Choice: Qdrant (self-hosted)**

Why:
- **Privacy:** it can run inside the company's own infrastructure, so internal documents are not sent to a third-party service.
- **Metadata filtering:** it filters well (team = "platform", version = "latest") while searching, which this problem needs.
- **Scale fits:** 100,000 chunks is easy for it, with room to grow to millions.
- **Updates:** inserting and deleting vectors is simple, which suits weekly document updates.
- **Cost:** open source, so no per-vector fee.

**Why not the others**
- *FAISS:* no storage, filtering or updates built in. I would have to build them myself.
- *Pinecone:* easiest to run, but data would be on an external cloud, which breaks the privacy requirement.
- *Chroma:* good for my prototype, but I would move to Qdrant for a shared production system.
- *pgvector:* a good option if the company already runs Postgres and the data stays small. I would pick it if simplicity mattered more than filtering and speed.
- *Milvus:* more than this scale needs, and harder to operate.

**When I would change my choice:** a small personal project would use Chroma. A team with no ops staff and non-sensitive data would use Pinecone. A project on Postgres with under about a million vectors would use pgvector.

---

## How to run

```bash
git clone https://github.com/ponthapalliarunkumar/accuknox-aiml-trainee-assignment.git
cd accuknox-aiml-trainee-assignment
pip install -r requirements.txt
python Assignment_1_Coding/api_to_sqlite.py
python Assignment_1_Coding/test_scores_viz.py
python Assignment_1_Coding/csv_to_db.py
```

Python version: 3.10 or newer.
