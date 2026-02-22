#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from ai_stock_picker_agent.graph import app

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the Research Workflow via LangGraph.
    """
    # 1. Initialize the State
    initial_state = {
        'sector': 'Technology',
        'retry_count': 0,
        'feedback': '',
        'tickers': [],
        'research_results': []
    }

    print("--- Starting Stock Picker AI (LangGraph + CrewAI) ---")

    # 2. Execute the Graph
    # This will handle discovery, research (with retries), and picking.
    final_state = app.invoke(initial_state)

    # 3. Handle Outputs
    print("\n\n=== FINAL INVESTMENT SUMMARY ===\n")
    if "decision_memo" in final_state:
        print(final_state["decision_memo"])
    else:
        print("Workflow completed, but no final decision memo was generated.")

if __name__ == "__main__":
    run()
