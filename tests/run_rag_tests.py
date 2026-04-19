import os
import json
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "documents"
OUT_DIR = BASE_DIR / "tests" / "outcomes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def reset_store() -> None:
    requests.post(f"{BACKEND_URL}/reset", timeout=30)


def upload_doc(doc_name: str) -> None:
    path = DOCS_DIR / doc_name
    with path.open("rb") as file:
        files = {"file": (doc_name, file.read())}
    resp = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
    resp.raise_for_status()


def query(question: str, top_k: int = 4) -> dict:
    payload = {"question": question, "top_k": top_k}
    resp = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def evaluate_tests() -> dict:
    results = []

    # Section 1
    reset_store()
    upload_doc("doc_small_1.txt")
    start = time.time()
    data = query("What is the capital of France?")
    elapsed = time.time() - start
    answer = normalize(data.get("answer", ""))
    sources_text = " ".join(item["text"].lower() for item in data.get("sources", []))
    word_count = len(answer.split())
    passed = "paris" in answer and "paris" in sources_text and word_count <= 20
    results.append({
        "test": "Small document sanity",
        "passed": passed,
        "elapsed_sec": round(elapsed, 3),
        "answer": data.get("answer", ""),
    })

    # Section 1b - summary
    reset_store()
    upload_doc("doc_small_1.txt")
    data = query("Summarize the document.")
    answer = normalize(data.get("answer", ""))
    word_count = len(answer.split())
    passed = ("paris" in answer or "eiffel" in answer) and word_count <= 35
    results.append({
        "test": "Small document summary",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 2
    reset_store()
    upload_doc("doc_small_2.txt")
    data = query("What are Python used for?")
    answer = normalize(data.get("answer", ""))
    expected_terms = ["data science", "web development", "automation"]
    passed = count_hits(answer, expected_terms) >= 2
    results.append({
        "test": "Small document multi-fact",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 3
    reset_store()
    upload_doc("doc_medium_1.txt")
    data = query("What is the purpose of air traffic control systems?")
    answer = normalize(data.get("answer", ""))
    key_terms = ["safety", "aircraft", "collision", "traffic flow"]
    passed = count_hits(answer, key_terms) >= 2
    results.append({
        "test": "Medium document paragraph understanding",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 4
    reset_store()
    upload_doc("doc_medium_2.txt")
    data = query("What is the capital of Germany?")
    answer = normalize(data.get("answer", ""))
    passed = (
        contains_any(answer, ["i don't know", "do not know", "not enough context"])
        or "unknown" in answer
    )
    results.append({
        "test": "Medium document irrelevant query",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 5
    reset_store()
    upload_doc("doc_large_1.txt")
    data = query("What are the effects of climate change?")
    answer = normalize(data.get("answer", ""))
    passed = "sea level" in answer and "temperature" in answer
    results.append({
        "test": "Large document multi-chunk",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 6
    reset_store()
    upload_doc("doc_large_2.txt")
    data = query("What is the system latency?")
    answer = normalize(data.get("answer", ""))
    passed = "120" in answer and "millisecond" in answer
    results.append({
        "test": "Large document precision",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 7
    reset_store()
    upload_doc("doc_multi_1.txt")
    upload_doc("doc_multi_2.txt")
    data = query("What is the capital of Japan?")
    answer = normalize(data.get("answer", ""))
    passed = "tokyo" in answer
    results.append({
        "test": "Multi-document retrieval",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 8
    reset_store()
    upload_doc("doc_large_3.txt")
    data = query("What year did the Orion program begin?")
    answer = normalize(data.get("answer", ""))
    passed = "2017" in answer
    results.append({
        "test": "Context limit retrieval",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 9
    reset_store()
    upload_doc("doc_medium_3.txt")
    data = query("What is Apple?")
    answer = normalize(data.get("answer", ""))
    passed = "fruit" in answer and ("company" in answer or "technology" in answer)
    results.append({
        "test": "Ambiguous query",
        "passed": passed,
        "answer": data.get("answer", ""),
    })

    # Section 10 - performance
    reset_store()
    for doc in [
        "doc_large_1.txt",
        "doc_large_2.txt",
        "doc_large_3.txt",
        "doc_medium_1.txt",
        "doc_medium_2.txt",
    ]:
        upload_doc(doc)
    start = time.time()
    data = query("What are the effects of climate change?", top_k=5)
    elapsed = time.time() - start
    sources_count = len(data.get("sources", []))
    passed = elapsed <= 5 and sources_count <= 5
    results.append({
        "test": "Performance",
        "passed": passed,
        "elapsed_sec": round(elapsed, 3),
        "sources_count": sources_count,
    })

    # Section 11 - consistency
    reset_store()
    upload_doc("doc_small_1.txt")
    answers = []
    for _ in range(5):
        data = query("What is the capital of France?")
        answers.append(normalize(data.get("answer", "")))
    passed = len(set(answers)) == 1 and "paris" in answers[0]
    results.append({
        "test": "Consistency",
        "passed": passed,
        "answer": answers[0] if answers else "",
    })

    passed_count = sum(1 for item in results if item["passed"])
    return {
        "passed": passed_count,
        "total": len(results),
        "results": results,
    }


def write_report(summary: dict) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUT_DIR / f"test_results_{timestamp}.md"

    lines = [
        "# RAG AI Document Assistant - Test Results",
        "",
        f"Total Passed: {summary['passed']} / {summary['total']}",
        "",
        "| Test | Result | Details |",
        "| --- | --- | --- |",
    ]
    for item in summary["results"]:
        result = "PASS" if item["passed"] else "FAIL"
        details = item.get("answer") or ""
        if "elapsed_sec" in item:
            details = f"elapsed_sec={item['elapsed_sec']}"
        lines.append(f"| {item['test']} | {result} | {details} |")

    out_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = OUT_DIR / f"test_results_{timestamp}.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return out_path


def main() -> None:
    summary = evaluate_tests()
    report_path = write_report(summary)
    print(f"Wrote test report to {report_path}")


if __name__ == "__main__":
    main()
