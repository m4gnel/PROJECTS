import arxiv
import httpx
import datetime
import asyncio
from supabase import Client
from .state import AgentState
from .planner import update_agent_run
from model_router import ModelRouter, RateLimitError, ProviderUnavailableError, AllProvidersExhaustedError

async def fetch_pubmed(query: str, max_results: int = 3):
    sources = []
    try:
        # Step 1: Search
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax={max_results}"
        async with httpx.AsyncClient() as client:
            search_res = await client.get(search_url, timeout=10.0)
            search_res.raise_for_status()
            id_list = search_res.json().get("esearchresult", {}).get("idlist", [])
            
        if not id_list:
            return sources
            
        # Step 2: Fetch details
        ids = ",".join(id_list)
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids}&retmode=json"
        async with httpx.AsyncClient() as client:
            summary_res = await client.get(summary_url, timeout=10.0)
            summary_res.raise_for_status()
            data = summary_res.json().get("result", {})
            for uid in id_list:
                item = data.get(uid)
                if item:
                    sources.append({
                        "title": item.get("title", ""),
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                        "source_type": "pubmed",
                        "published_date": item.get("pubdate", "")
                    })
    except Exception as e:
        print(f"PubMed fetch error: {e}")
    return sources

async def fetch_arxiv(query: str, max_results: int = 3):
    sources = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        # Wrapping synchronous arxiv call in a thread or running it synchronously
        # since arxiv package is sync, let's just do it directly for MVP
        results = list(client.results(search))
        for r in results:
            sources.append({
                "title": r.title,
                "url": r.entry_id,
                "source_type": "arxiv",
                "published_date": r.published.date().isoformat()
            })
    except Exception as e:
        print(f"arXiv fetch error: {e}")
    return sources


async def researcher_node(state: AgentState, config: dict):
    supabase: Client = config["configurable"]["supabase"]
    model_router: ModelRouter = config["configurable"]["research_router"]
    session_id = state["session_id"]
    
    update_agent_run(supabase, session_id, "researcher", "running")
    
    query = state["query"]
    prompt = f"Extract a 2-4 word search query based on the user's research topic: {query}\nOnly return the search string, nothing else."
    
    try:
        response = await model_router.call(prompt)
        search_query = response.text.strip().strip('"\'')
        
        # Parallel fetch from Arxiv and PubMed
        arxiv_task = asyncio.create_task(fetch_arxiv(search_query, max_results=3))
        pubmed_task = asyncio.create_task(fetch_pubmed(search_query, max_results=3))
        
        results = await asyncio.gather(arxiv_task, pubmed_task, return_exceptions=True)
        
        raw_sources = []
        for res in results:
            if isinstance(res, list):
                raw_sources.extend(res)
                
        # Save to Supabase
        sources_list = []
        for src in raw_sources:
            src_data = {
                "session_id": session_id,
                "title": src["title"],
                "url": src["url"],
                "source_type": src["source_type"],
            }
            if src.get("published_date"):
                # Simplistic date parsing/passing
                # Supabase expects YYYY-MM-DD or full timestamp
                # Let's pass it as is or null if empty
                date_str = src["published_date"]
                # Try to sanitize date_str or set to None
                # PubMed returns weird formats like "2024 Oct 1"
                # If it's not ISO, we might just omit it for safety
                if len(date_str) >= 4 and date_str[:4].isdigit():
                    src_data["published_date"] = f"{date_str[:4]}-01-01" # dummy fallback
                else:
                    src_data["published_date"] = None

            try:
                db_res = supabase.table("sources").insert(src_data).execute()
                src["id"] = db_res.data[0]["id"] if len(db_res.data) > 0 else None
                sources_list.append(src)
            except Exception as e:
                print(f"Failed to insert source: {e}")
                
        update_agent_run(supabase, session_id, "researcher", "done", raw_output={"sources_count": len(sources_list), "search_query": search_query})
        
        return {"sources": sources_list}
        
    except AllProvidersExhaustedError as e:
        update_agent_run(supabase, session_id, "researcher", "degraded", error_detail=str(e))
        return {"status": "degraded", "errors": [f"Research step degraded: {e}"]}
    except Exception as e:
        update_agent_run(supabase, session_id, "researcher", "failed", error_detail=str(e))
        return {"status": "failed", "errors": [f"Research step failed: {e}"]}
