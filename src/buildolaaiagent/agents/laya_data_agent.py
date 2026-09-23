import json
import requests
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from buildolaaiagent.models.schema import DataAgentSchema
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from buildolaaiagent.agents.etl_analyst import etl_analyst
from buildolaaiagent.agents.sql_analyst import sql_analyst

url = "http://127.0.0.1:8000/predict"

def etl_node(message : str):

    response = etl_analyst.invoke(
             {"messages":[HumanMessage(content=f"""
            {message}
    """)]}
        ) 
    

    return response


def sql_node(message : str):

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

    return response


def laya_agent(task: str):
    payload = {
        "state": {"task" : task},
        "questions": {
            "department": {
                "type": "choice",
                "instructions": "Which department should handle this request?",
                "criteria": {
                    "SQL": (
                        "Use when the task involves querying, reading, aggregating, "
                        "filtering, or updating existing structured tables within a database. "
                        "Examples: fetching user metrics, running analytical queries, writing joins, "
                        "or creating specific database views/reports."
                    ),
                    "ETL": (
                        "Use when the task involves extracting data from external sources/APIs, "
                        "cleansing/transforming formats, building automated batch or streaming pipelines, "
                        "syncing disparate systems, or loading data into a data warehouse/lake."
                    )
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    return response

def main():
    content = "I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' in the json format and save it to data/extract folder in the json folder and then give me 5 top data of rides table"
    # content = "What are the different types of Payment Methods we have in our database"
    response = laya_agent(task = content)
    data = response.json()
    print("Status Code:", response.status_code)
    print("SQL agent probablity:", data["answers"]["department"]['probabilities']['SQL'])
    print("ETL agent probablity:", data["answers"]["department"]['probabilities']['ETL'])
    print("-----------------------------------------------------------------------------")
    print(data)

    choice = data["answers"]["department"]['choice']

    if choice == 'SQL':
        sql_node(content)
    elif choice == 'ETL':
        etl_node(content)

main()
