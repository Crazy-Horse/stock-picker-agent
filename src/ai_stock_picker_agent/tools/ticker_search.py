from crewai.tools import BaseTool
from crewai_tools import RagTool
from pydantic import BaseModel, Field
import os

# Define the input schema
class TickerSearchInput(BaseModel):
    query: str = Field(..., description="The research question or topic to search for.")
    ticker: str = Field(..., description="The stock ticker (e.g., AAPL) to filter by.")

class TickerSpecificSearch(BaseTool):
    name: str = "internal_research_search"
    description: str = "Search internal filings and transcripts for a SPECIFIC ticker."
    args_schema: type[BaseModel] = TickerSearchInput

    def _run(self, query: str, ticker: str) -> str:
        # Initialize the underlying Chroma tool inside the run method 
        # or pass it via __init__
        rag_tool = RagTool(
            config={
                "llm": {"provider": "openai", "config": {"model": "gpt-4o"}},
                "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
            }
        )
        
        try:
            enhanced_query = f"Stock Ticker: {ticker.upper()} - {query}"
        
            return rag_tool.run(query=enhanced_query)
        
        except Exception as e:
            return f"Error searching internal docs for {ticker}: {str(e)}"