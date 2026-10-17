import pytest
from backend.agents.router_agent import router_node
from backend.agents.translator_agent import is_malayalam, translator_pre_node
from backend.agents.graph import graph


@pytest.mark.asyncio
async def test_router_classifies_weather_query():
    state = {"farmer_query": "Will it rain tomorrow in Ernakulam?"}
    res = await router_node(state)
    assert "WEATHER" in res["query_intent"]


@pytest.mark.asyncio
async def test_router_classifies_pest_query():
    state = {"farmer_query": "There are white spots on my coconut leaves"}
    res = await router_node(state)
    assert "PEST" in res["query_intent"]
    assert res["crop"] == "coconut"


@pytest.mark.asyncio
async def test_translator_detects_malayalam():
    ml_text = "നാളെ മഴ ഉണ്ടാകുമോ?"
    assert is_malayalam(ml_text) is True

    state = {"farmer_query": ml_text}
    res = await translator_pre_node(state)
    assert res["language"] == "ml"
    assert res["farmer_query"] != ""


def test_graph_compiles_without_error():
    assert graph is not None


@pytest.mark.asyncio
async def test_state_merges_parallel_outputs():
    initial_state = {
        "farmer_id": "farmer_123",
        "farmer_query": "What is the weather and pest risk for coconut?",
        "location": {"district": "Ernakulam", "lat": 9.98, "lon": 76.29},
        "crop": "coconut"
    }
    config = {"configurable": {"thread_id": "test_thread_1"}}
    res = await graph.ainvoke(initial_state, config=config)

    assert "final_answer_ml" in res or "final_answer_en" in res
    assert "query_intent" in res
