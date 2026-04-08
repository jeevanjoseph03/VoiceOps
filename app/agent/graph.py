from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.agent.state import GraphState
from app.agent.nodes import supervisor_node, tools

# 1. Initialize the Graph with our State schema
workflow = StateGraph(GraphState)

# 2. Add the Nodes
workflow.add_node("supervisor", supervisor_node)
# ToolNode automatically executes the tools defined in nodes.py
workflow.add_node("tools", ToolNode(tools))

# 3. Define the Routing Edges
# Start at the supervisor
workflow.set_entry_point("supervisor")

# If the supervisor calls a tool, go to "tools". If it just replies text, go to END.
workflow.add_conditional_edges(
    "supervisor",
    tools_condition, 
)

# After a tool executes, ALWAYS loop back to the supervisor so it can read the result
workflow.add_edge("tools", "supervisor")

# 4. Compile the Graph
# This is the object we will import into our FastAPI routes
voiceops_app = workflow.compile()