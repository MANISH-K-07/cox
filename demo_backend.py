
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Terminal formatting
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def line(char="=", width=76):
    print(char * width)


def heading(title):
    print()
    line()
    print(f"{BOLD}{CYAN}{title.center(76)}{RESET}")
    line()


def status(label, success, detail=""):
    symbol = f"{GREEN}PASS{RESET}" if success else f"{RED}FAIL{RESET}"
    print(f"  [{symbol}] {label}")
    if detail:
        print(f"         {detail}")


def request_api(endpoint, method="GET", payload=None):
    url = BASE_URL + endpoint

    data = None
    headers = {}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )

    with urllib.request.urlopen(req, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def print_section(title, items):
    print(f"\n{BOLD}{title}{RESET}")
    line("-", 76)

    if not items:
        print("  None reported.")
        return

    for index, item in enumerate(items, start=1):
        print(f"  {index}. {item}")


def main():

    start_time = datetime.now()
    checks_passed = 0
    checks_failed = 0

    print("\033[2J\033[H", end="")

    print(f"{CYAN}{BOLD}")
    print("   ____ ___       __  __")
    print("  / ___/ _ \\      \\ \\/ /")
    print(" | |  | | | |______\\  /")
    print(" | |__| |_| |______/  \\")
    print("  \\____\\___/      /_/\\_\\")
    print(f"{RESET}")

    print(f"{BOLD}  CO-X | BACKEND SYSTEM DEMONSTRATION{RESET}")
    print("  Knowledge Synthesis & Hybrid RAG Prototype")
    print(f"  Demo started: {start_time.strftime('%B %d, %Y | %I:%M:%S %p')}")

    # --------------------------------------------------
    # 1. API CONNECTION
    # --------------------------------------------------

    heading("1. BACKEND CONNECTIVITY")

    try:
        home = request_api("/")
        health = request_api("/health")

        api_ok = (
            home.get("status") == "running"
            and health.get("status") == "healthy"
        )

        status("FastAPI application", api_ok, "API is responding")
        checks_passed += int(api_ok)
        checks_failed += int(not api_ok)

    except Exception as error:
        status("FastAPI application", False, str(error))
        print(f"\n{RED}Backend is unavailable. Start it using:{RESET}")
        print("uvicorn app.main:app --reload")
        return

    # --------------------------------------------------
    # 2. LLM CONNECTION
    # --------------------------------------------------

    heading("2. LANGUAGE MODEL CONNECTIVITY")

    try:
        llm_result = request_api(
            "/ai/test",
            method="POST",
            payload={
                "prompt": "Reply with one short sentence confirming that the Co-X language model is responding."
            }
        )

        model = llm_result.get("model", "Configured model")
        answer = llm_result.get("answer", "")

        status("LLM connection", bool(answer), f"Model: {model}")

        if answer:
            print(f"\n  Response: {answer}")

        checks_passed += int(bool(answer))
        checks_failed += int(not bool(answer))

    except Exception as error:
        status("LLM connection", False, str(error))
        checks_failed += 1

    # --------------------------------------------------
    # 3. DATA INGESTION
    # --------------------------------------------------

    heading("3. KNOWLEDGE BASE INITIALIZATION")

    try:
        ingestion = request_api(
            "/ingest/sample-data",
            method="POST"
        )

        ingestion_ok = ingestion.get("status") == "success"

        status(
            "Sample data ingestion",
            ingestion_ok,
            f"{ingestion.get('documents_loaded', 0)} documents loaded"
        )

        for key, label in [
            ("chunks_created", "Chunks created"),
            ("unique_chunks", "Unique chunks"),
            ("vector_records", "Vector database records"),
            ("keyword_records", "Keyword index records"),
            ("graph_nodes", "Knowledge graph nodes"),
            ("graph_relationships", "Knowledge graph relationships"),
        ]:
            print(f"  {label:<34}: {ingestion.get(key, 'N/A')}")

        checks_passed += int(ingestion_ok)
        checks_failed += int(not ingestion_ok)

    except Exception as error:
        status("Data ingestion", False, str(error))
        checks_failed += 1
        print(f"\n{RED}Cannot continue without successful ingestion.{RESET}")
        return

    # --------------------------------------------------
    # 4. AI SYNTHESIS
    # --------------------------------------------------

    heading("4. AI-POWERED KNOWLEDGE SYNTHESIS")

    question = (
        "Why is the Orion pilot schedule at risk, "
        "and what actions need to happen to keep it on track?"
    )

    print(f"\n  Query: {question}")

    try:
        result = request_api(
            "/briefs/generate",
            method="POST",
            payload={"question": question}
        )

        synthesis_ok = bool(result.get("answer"))

        status(
            "Brief generation",
            synthesis_ok,
            "Retrieved information and generated synthesis"
        )

        checks_passed += int(synthesis_ok)
        checks_failed += int(not synthesis_ok)

        if synthesis_ok:

            print_section("EXECUTIVE SUMMARY", [result["answer"]])

            print_section(
                "KEY FINDINGS",
                result.get("key_points", [])
            )

            print_section(
                "IDENTIFIED RISKS",
                result.get("risks", [])
            )

            print_section(
                "ACTION ITEMS",
                result.get("action_items", [])
            )

            print_section(
                "SOURCE DOCUMENTS",
                result.get("sources", [])
            )

    except Exception as error:
        status("AI synthesis", False, str(error))
        checks_failed += 1

    # --------------------------------------------------
    # 5. FINAL SYSTEM REPORT
    # --------------------------------------------------

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    heading("5. FINAL SYSTEM HEALTH REPORT")

    print(f"\n  Project                 : Co-X")
    print(f"  Backend                 : FastAPI")
    print(f"  Retrieval architecture  : Hybrid RAG + Knowledge Graph")
    print(f"  Vector storage          : ChromaDB")
    print(f"  Keyword storage         : SQLite FTS5")
    print(f"  Graph storage           : NetworkX")
    print(f"  LLM integration         : {model if 'model' in locals() else 'Configured'}")

    line("-", 76)

    print(f"  Successful checks       : {GREEN}{checks_passed}{RESET}")
    print(f"  Failed checks           : {RED}{checks_failed}{RESET}")
    print(f"  Execution time          : {duration:.2f} seconds")

    line()

    if checks_failed == 0:
        print(f"\n{GREEN}{BOLD}")
        print("       ALL SYSTEM CHECKS PASSED")
        print("       CO-X BACKEND DEMONSTRATION SUCCESSFUL")
        print(f"{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}")
        print("       DEMONSTRATION COMPLETED WITH ISSUES")
        print("       PLEASE REVIEW THE FAILED CHECKS")
        print(f"{RESET}")

    print(f"\n  API documentation: {BASE_URL}/docs")
    print(f"  Demo completed: {end_time.strftime('%I:%M:%S %p')}")
    line()


if __name__ == "__main__":
    main()
