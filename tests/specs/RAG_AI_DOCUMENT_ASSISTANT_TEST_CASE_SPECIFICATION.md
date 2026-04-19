# RAG AI Document Assistant — Test Case Specification

## Purpose

This document defines structured, quantifiable test cases to evaluate the correctness, reliability, and performance of the RAG AI Document Assistant system.

Each test includes:

- Input document(s)
- User query
- Expected behavior
- Measurable success criteria

The goal is to verify:

- Document processing accuracy
- Retrieval quality
- Answer correctness
- System consistency

---

## Section 1 — Small Document Test (Sanity Check)

Document Name: doc_small_1.txt
Content:
"The capital of France is Paris. It is known for the Eiffel Tower."

Query:
"What is the capital of France?"

Expected Output:
"Paris"

Success Criteria:

- Retrieved chunk must contain "Paris"
- Answer must include "Paris"
- No hallucinated information (e.g., no unrelated facts)
- Response length <= 20 words

Failure Conditions:

- Incorrect city
- Inclusion of unrelated information
- "I don't know" response

---

## Section 1b — Small Document Summary

Document Name: doc_small_1.txt
Content:
"The capital of France is Paris. It is known for the Eiffel Tower."

Query:
"Summarize the document."

Expected Output:
One or two sentences that mention the key facts (Paris and/or Eiffel Tower).

Success Criteria:

- Answer includes "Paris" OR "Eiffel"
- Response length <= 35 words
- Summary is grounded in the document

Failure Conditions:

- "I don't know" response
- Unrelated or fabricated details

---

## Section 2 — Small Document (Multi-Fact)

Document Name: doc_small_2.txt
Content:
"Python is a programming language. It is used for data science, web development, and automation."

Query:
"What are Python used for?"

Expected Output:
Mentions at least:

- data science
- web development
- automation

Success Criteria:

- At least 2/3 correct uses retrieved
- Answer grounded in document
- No external additions (e.g., AI/ML unless stated)

---

## Section 3 — Medium Document (Paragraph Understanding)

Document Name: doc_medium_1.txt
Content:
"Air traffic control systems manage aircraft movement to ensure safety and efficiency. Controllers monitor aircraft positions and provide instructions. These systems reduce collision risk and improve traffic flow."

Query:
"What is the purpose of air traffic control systems?"

Expected Output:

- Ensure safety
- Manage aircraft movement
- Reduce collision risk

Success Criteria:

- Answer includes at least 2 key purposes
- Retrieval includes correct paragraph
- No hallucinated systems or technologies

---

## Section 4 — Medium Document (Irrelevant Query Test)

Document Name: doc_medium_2.txt
Content:
"Basketball is a sport played between two teams of five players. The objective is to score points by shooting a ball through a hoop."

Query:
"What is the capital of Germany?"

Expected Output:
"I don't know" OR equivalent uncertainty

Success Criteria:

- System must NOT fabricate an answer
- Must explicitly indicate lack of information

Failure Condition:

- Any attempt to answer the question incorrectly

---

## Section 5 — Large Document (Multi-Chunk Retrieval)

Document Name: doc_large_1.txt
Content:
A 1500-3000 word document about climate change including:

- causes (greenhouse gases)
- effects (rising sea levels, temperature)
- mitigation strategies (renewable energy)

Query:
"What are the effects of climate change?"

Expected Output:
Includes:

- rising sea levels
- increasing temperatures

Success Criteria:

- At least 2 correct effects retrieved
- Retrieval must include relevant chunk(s)
- Answer must not include unrelated sections (e.g., causes unless relevant)

---

## Section 6 — Large Document (Precision Test)

Document Name: doc_large_2.txt
Content:
A long technical document where only ONE section mentions:
"The system latency is 120 milliseconds under normal load."

Query:
"What is the system latency?"

Expected Output:
"120 milliseconds"

Success Criteria:

- Exact numeric value retrieved
- No approximation unless stated
- Response includes correct unit

Failure Conditions:

- Wrong number
- Missing unit
- Fabricated estimate

---

## Section 7 — Multi-Document Test

Documents:

doc_multi_1.txt:
"New York is a city in the United States."

doc_multi_2.txt:
"Tokyo is the capital of Japan."

Query:
"What is the capital of Japan?"

Expected Output:
"Tokyo"

Success Criteria:

- Retrieval must select correct document
- No mixing of unrelated documents
- Correct answer from correct source

---

## Section 8 — Context Limit Test

Document Name: doc_large_3.txt
Content:
Very large document (3000+ words) with relevant answer buried deep.

Query:
Specific detail from later section

Expected Output:
Correct answer from deep section

Success Criteria:

- System retrieves relevant chunk despite size
- No early-chunk bias
- Answer accuracy >= 90% (manual verification)

---

## Section 9 — Ambiguous Query Test

Document Name: doc_medium_3.txt
Content:
"Apple is a fruit. Apple Inc. is a technology company."

Query:
"What is Apple?"

Expected Output:
Acknowledges ambiguity OR provides both meanings

Success Criteria:

- Mentions both interpretations OR clarifies ambiguity
- No assumption without evidence

---

## Section 10 — Performance Test

Input:

- 5 documents (~2000 words each)

Query:
Any relevant question

Expected Behavior:

- Response time <= 3 seconds (local) OR <= 5 seconds (API-based)
- Retrieval returns <= 5 chunks

Success Criteria:

- System remains responsive
- No crashes or timeouts

---

## Section 11 — Consistency Test

Repeat the same query 5 times:

Query:
"What is the capital of France?"

Expected Output:
Consistent answer each time

Success Criteria:

- Same answer across runs
- No variation in correctness

---

## Final Evaluation Metrics

The system should achieve:

- Retrieval Accuracy: >= 80% relevant chunks
- Answer Accuracy: >= 85% correct responses
- Hallucination Rate: <= 5%
- Response Time: <= 5 seconds
- Failure Rate: <= 10% across all tests

---

End of Test Specification
