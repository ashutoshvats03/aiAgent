import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from buildolaaiagent.utils import etl_tools
from buildolaaiagent.utils.llm_pick import pick_llm
from buildolaaiagent.utils.etl_tools import ETLTools
from buildolaaiagent.models.schema import ETLAgentSchema , RouteSchema , DataAgentSchema
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain_groq import ChatGroq
from buildolaaiagent.agents.etl_analyst import etl_analyst
from buildolaaiagent.agents.sql_analyst import sql_analyst

llm = pick_llm("medium")

llm_router = llm.with_structured_output(RouteSchema)

#------------------------Data graph agent------------------------
def router_node(state:DataAgentSchema):
    message = state.messages[-1].content
    router_response_dict = llm_router.invoke(message).model_dump()
    router_response = router_response_dict['answer']
    state.router_response = router_response
    return state

def etl_node(state:DataAgentSchema):
    message = state.messages[-1].content
    
    message = state.messages[-1].content

    response = etl_analyst.invoke(
             {"messages":[HumanMessage(content=f"""
            {message}
    """)]}
        ) 
    state.messages = state.messages + [response]

    return state


def sql_node(state:DataAgentSchema):

    message = state.messages[-1].content
    print(f"--------------------------------------{message}")
    input_schema = {
        "messages": [],
        "user_question": f"{message}",
        "curated_ques": "",
        "prompt_query_context": "",
        "generated_sql_query": "",
        "is_safe": "No",
        "comments": "",
        "sql_query_exec_result": "",
        "final_answer": ""
    }

    response = sql_analyst.invoke(input_schema)

    state.messages = state.messages + [response]

    return state

data_agent_graph = StateGraph(DataAgentSchema)

data_agent_graph.add_node("router_node", router_node)
data_agent_graph.add_node("etl_node", etl_node)
data_agent_graph.add_node("sql_node", sql_node)

data_agent_graph.add_edge(START, "router_node")

def route_edge(state: DataAgentSchema) -> str:
    print(f"----------------------------------Choosing SQL/ETL------------------")
    if state.router_response == "sql":
        return "sql_node"
    elif state.router_response == "etl":
        return "etl_node"
    else:
        raise ValueError(f"Invalid route response: {state.router_response}")


data_agent_graph.add_conditional_edges("router_node", route_edge,
                                      {
                                          "sql_node": "sql_node",
                                          "etl_node": "etl_node"
                                      })

data_agent = data_agent_graph.compile()

# Optional|
from IPython.display import display, Image
img = Image(data_agent.get_graph().draw_mermaid_png())
with open("data_agent_graph.png", "wb") as f:
    f.write(img.data)



if __name__ == "__main__":
    content = "I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' in the json format and save it to data/extract folder in the json folder and then give me 5 top data of rides table"
    response = data_agent.invoke(
        {"messages":[HumanMessage(content=content)],
         "router_response": ""}
    )

    print(response)