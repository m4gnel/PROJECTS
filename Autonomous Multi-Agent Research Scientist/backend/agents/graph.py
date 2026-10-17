from langgraph.graph import StateGraph, START, END
from .state import AgentState

from .memory import memory_node
from .planner import planner_node
from .researcher import researcher_node
from .fact_checker import fact_checker_node
from .critic import critic_node
from .business_analyst import business_analyst_node
from .startup_generator import startup_generator_node
from .technical_architect import technical_architect_node
from .data_analyst import data_analyst_node
from .knowledge_graph import knowledge_graph_node
from .evaluator import evaluator_node
from .report_writer import report_writer_node

def create_research_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("memory", memory_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("business_analyst", business_analyst_node)
    workflow.add_node("startup_generator", startup_generator_node)
    workflow.add_node("technical_architect", technical_architect_node)
    workflow.add_node("data_analyst", data_analyst_node)
    workflow.add_node("knowledge_graph", knowledge_graph_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("report_writer", report_writer_node)
    
    # Edges
    workflow.add_edge(START, "memory")
    workflow.add_edge("memory", "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "fact_checker")
    workflow.add_edge("fact_checker", "critic")
    
    def route_after_critic(state: AgentState):
        plan = state.get("plan", [])
        if "business_analyst" in plan: return "business_analyst"
        if "startup_generator" in plan: return "startup_generator"
        if "technical_architect" in plan: return "technical_architect"
        return "data_analyst"

    workflow.add_conditional_edges("critic", route_after_critic)
    
    def route_after_ba(state: AgentState):
        plan = state.get("plan", [])
        if "startup_generator" in plan: return "startup_generator"
        if "technical_architect" in plan: return "technical_architect"
        return "data_analyst"
        
    workflow.add_conditional_edges("business_analyst", route_after_ba)
    
    def route_after_sg(state: AgentState):
        plan = state.get("plan", [])
        if "technical_architect" in plan: return "technical_architect"
        return "data_analyst"
        
    workflow.add_conditional_edges("startup_generator", route_after_sg)
    
    workflow.add_edge("technical_architect", "data_analyst")
    workflow.add_edge("data_analyst", "knowledge_graph")
    workflow.add_edge("knowledge_graph", "evaluator")
    workflow.add_edge("evaluator", "report_writer")
    workflow.add_edge("report_writer", END)
    
    return workflow.compile()
