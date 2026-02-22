from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from crewai import Crew
from ai_stock_picker_agent.crew import StockPicker
import json

# 1. Define the shared State
class AgentState(TypedDict):
    sector: str
    tickers: List[str]
    research_results: List[dict]
    scores: dict
    decision_memo: str
    retry_count: int
    feedback: str

# 2. Define the Nodes (Mapping CrewAI Tasks to Graph Nodes)
def discovery_node(state: AgentState):
    print("--- Node: Discovery ---")
    crew_instance = StockPicker()
    task = crew_instance.find_trending_companies()
    # Run a mini-crew for just this task
    result = Crew(agents=[crew_instance.trending_company_finder()], tasks=[task]).kickoff(inputs={'sector': state['sector']})
    return {"tickers": [c.ticker for c in result.pydantic.companies], "retry_count": 0}

def research_node(state: AgentState):
    print(f"--- Node: Research (Attempt {state['retry_count'] + 1}) ---")
    crew_instance = StockPicker()
    task = crew_instance.research_trending_companies()
    # Pass tickers and feedback into the researcher
    result = Crew(agents=[crew_instance.financial_researcher()], tasks=[task]).kickoff(inputs={
        "tickers": state["tickers"],
        "feedback": state.get("feedback", "None")
    })
    return {"research_results": result.pydantic.research_list, "retry_count": state["retry_count"] + 1}

def scoring_node(state: AgentState):
    print("--- Node: Scoring ---")
    crew_instance = StockPicker()
    task = crew_instance.score_candidates()
    
    # Convert Pydantic objects to plain dictionaries
    # This resolves the "Unsupported type TrendingCompanyResearch" error
    serialized_research = [
        res.model_dump() if hasattr(res, 'model_dump') else res 
        for res in state["research_results"]
    ]
    
    result = Crew(
        agents=[crew_instance.stock_picker()], 
        tasks=[task]
    ).kickoff(inputs={
        "research_report": serialized_research
    })
    
    # Return the pydantic result from the crew kickoff
    return {"scores": result.pydantic}

def picking_node(state: AgentState):
    print("--- Node: Final Selection ---")
    crew_instance = StockPicker()
    task = crew_instance.pick_best_company() 
    
    # 1. Serialize Research Results into a list of dicts
    research_dict = [
        res.model_dump() if hasattr(res, 'model_dump') else res 
        for res in state["research_results"]
    ]
    
    # 2. Serialize Scores into a dict
    scores_dict = state["scores"]
    if hasattr(scores_dict, 'model_dump'):
        scores_dict = scores_dict.model_dump()

    # 3. Clean both (The Fixed Line)
    # Using 'research_dict' instead of the mistyped 'research_research'
    clean_research = json.loads(json.dumps(research_dict, default=str))
    clean_scores = json.loads(json.dumps(scores_dict, default=str))
    
    result = Crew(
        agents=[crew_instance.stock_picker()], 
        tasks=[task]
    ).kickoff(inputs={
        "research_report": clean_research,
        "scores": clean_scores
    })
    
    return {"decision_memo": result.raw}

# 3. Routing Logic (The Quality Gate)
def quality_gate(state: AgentState):
    # Logic: If any researcher flagged missing data, retry up to 3 times
    # This aligns with your instructions in tasks.yaml
    has_missing_data = any(res.investment_potential == "DATA_MISSING" for res in state["research_results"])
    
    if has_missing_data and state["retry_count"] < 3:
        print("Gating: Data missing. Routing to Retry...")
        return "retry"
    return "proceed"

# 4. Assemble the Graph
workflow = StateGraph(AgentState)
workflow.add_node("discover", discovery_node)
workflow.add_node("research", research_node)
workflow.add_node("score", scoring_node)
workflow.add_node("pick", picking_node)

workflow.add_edge(START, "discover")
workflow.add_edge("discover", "research")
workflow.add_conditional_edges("research", quality_gate, {"retry": "research", "proceed": "score"})
workflow.add_edge("score", "pick")
workflow.add_edge("pick", END)

app = workflow.compile()