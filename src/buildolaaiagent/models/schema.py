from pydantic import BaseModel, Field
from typing import Annotated , Literal
from operator import add

class AgentSchema(BaseModel):
    messages : Annotated[list, add ] = Field(... , description = "List of messages to processed by the agent")
    is_safe : Literal["Yes" ,"No"] =  Field(... , description = "Boolean to keep the flags")
    user_question : str =  Field(... , description = "The original question asked by the user")
    curated_ques : str = Field(... , description = "Curated user question")
    comments :  str = Field(... , description = "Comments regarding the safety of the generated SQL query")
    prompt_query_context : str = Field(... , description = "A detailed prompt with SQL DB context that will help agent to generate SQL query")
    generated_sql_query : str = Field(... , description = "The SQL query gemerated by the Agent")
    sql_query_exec_result : str = Field(... , description = "The result of executing the query of the Database")
    final_answer : str = Field(... , description = "Answer that is summarised and will be shown to the user , as per the")

class JudgeSchema(BaseModel):
    answer : Literal["Yes","No"] = Field(..., description="Indicates whether the generated SQL query is safe to execute or not")
    comments : str = Field(..., description="Additional comments or feedback from the judge regarding the SQL query")
    

class ETLAgentSchema(BaseModel):
    messages : Annotated[list , add] = Field(... , description="List of messages to be processes by the ETL agent")
    
class RouteSchema(BaseModel):
    answer : Literal["sql","etl"] = Field(..., description="Indicates whether the user's questio has to deal with SQL agent or ETL agent")
    comments : str = Field(..., description="Additional comments or feedback from the judge regarding the SQL query")
    

class DataAgentSchema(BaseModel):
    messages : Annotated[list,add] = Field(..., description="List of messages to be processed by the Data agent")
    router_response : str = Field(..., description="The response from the router indicating whether to route to SQL or ETL operations")