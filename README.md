<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">AIAGENT</h1></p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

## 🔗 Table of Contents

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
  - [📂 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
- [🔰 Contributing](#-contributing)
- [🙌 Acknowledgments](#-acknowledgments)

---

## 📍 Problem Statement 
You are a non-tech guy and has to make a report from the SQL Database
Manually you have to go a GenAI model and start with <code>I want to all the payments more than 1 Lakh</code> ,then it'll
give code <code>SELECT * FROM payments WHERE amt > 100000</code> 
✔️ Correct code , until you work it with your Database , it crashed telling 
<code>You don't have any table payments</code>
<code>You don't have any field amt</code>

Things you should send to GenAI operators are:

	- Schema
	- Well written prompt
	- Constraints(if any)

Which is not possible everytime , so this can be automated.

<code>"Show me the average rating for each vehicle type"</code>
```python
class AgentSchema(BaseModel):
    messages: List                    # Conversation messages
    user_question: str                # Original user query
    curated_ques: str                 # Refined question
    prompt_query_context: str         # Database context + prompt
    generated_sql_query: str          # Generated SQL
    is_safe: Literal["Yes", "No"]     # Safety validation result
    comments: str                     # Safety check comments
    sql_query_execution_result: str   # Query result
    final_answer: str                 # Final formatted answer
```
```python
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            Show me the top 5 users with the highest ratings
        """)
    ],
    "route_response": ""
})
```

Issues:

- Prevents execution of dangerous commands (INSERT, UPDATE, DELETE, DROP, ALTER)
- Validates query before execution
- Automatic result limiting to 10 rows (unless specified)
- Schema validation against database

Responsibility:

- Converts natural language queries to SQL
- Handles all database query operations
- Validates query safety
- Executes queries and returns results

Workflow:

- Query Curation - Refines user question for clarity
- Context Gathering - Fetches database schema details
- Prompt Construction - Creates detailed context for LLM
- SQL Generation - Generates SQL query using LLM
- Safety Check - Validates query safety
- Query Execution - Executes validated query on database
- Answer Generation - Formats and returns results

------------------------------------------------------------------------------------

## 📍 Problem Statement 
You are a non-tech guy and has to make a report from data Extracted from an API.
For this you will to to give the link to the ai and get the data , and then ask to do the operations 
<code>Transform the rides.csv data by filtering only rides with rating > 4.5 and save to data/transform</code>

Things you should send to GenAI operators with the API are:

- Schema
- Well written prompt
- Constraints(if any)

Which is not possible everytime , so this can be automated.

<code>"Show me the average rating for each vehicle type"</code>
```python
class ETLAgentSchema(BaseModel):
    messages: List                    # Conversation messages
```
```python
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            Transform the rides.csv data by filtering only rides 
            with rating > 4.5 and save to data/transform
        """)
    ],
    "route_response": ""
})
```

Issues:

- This is repeated task , so if you have to it for 10 times then it will waste time
- If you are non tech guy you will not change the model , and  Vendor Lock-In will happen . Use the best model for extraction , choose the high reasoning model to transform the data and best coding model to generate the code that'll be executed

Responsibility:

- Handles data extraction from APIs
- Performs data transformation using Pandas
- Manages data loading to various formats
- Executes code safely in controlled environment

  
Workflow:

- Tool Binding - Attaches ETL tools to LLM
- User Intent Understanding - Analyzes transformation requirements
- Tool Selection - Chooses appropriate ETL operation
- Code Generation - Generates Pandas code for transformation
- Safe Execution - Executes generated code in sandboxed environment
- Result Reporting - Returns execution status and generated code
Supported Formats:

- CSV (default)
- JSON (Lines or Records)
- Parquet

------------------------------------------------------------------------------------
## 📍 Problem Statement 
When to you which model , the best thing will be right now to give decision to laya the tools used for decision making

```python
class RouterSchema(BaseModel):
    answer: Literal["sql", "etl"]     # Query classification
    comments: str                     # Reasoning for classification

class DataAgentSchema(BaseModel):
    messages: List                    # All conversation messages
    route_response: str               # Router decision (sql/etl)
```
```python
from agents.data_agent import data_agent
from langchain_core.messages import HumanMessage

# Example: Extract data from API
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            I want to extract the data from the API endpoint 
            'https://pokeapi.co/api/v2/pokemon' and save it to 
            data/extract folder in CSV format
        """)
    ],
    "route_response": ""
})

print(response)
```

Responsibility:

- Receives natural language user queries
- Classifies queries as either SQL or ETL operations
- Routes queries to appropriate sub-agents
- Aggregates results and returns to user


Components:

- Router Node: Uses structured output to classify query intent
- Conditional Routing: Routes to SQL or ETL based on classification
- Graph Orchestration: Manages workflow using LangGraph


---

## 👾 Features

### Core Capabilities

- **Intelligent Query Routing**: Automatically classifies user queries as SQL or ETL operations
- **SQL Analysis Agent**:
  - Natural language to SQL query conversion
  - Automatic schema context gathering
  - SQL safety validation (prevents harmful operations)
  - Query execution on PostgreSQL database
  - Intelligent query refinement

- **ETL Agent**:
  - API data extraction (JSON to structured formats)
  - Data transformation using Pandas
  - Multi-format support (CSV, JSON, Parquet)
  - Dynamic code generation based on user requirements
  - Safe code execution

- **Multi-LLM Support**:
  - Low-complexity queries: Faster, cost-effective LLM
  - Medium-complexity queries: Balanced LLM
  - High-complexity queries: Premium LLM (Claude)

- **Safety & Validation**:
  - SQL query safety checking
  - Protection against database modifications (INSERT, UPDATE, DELETE, DROP, etc.)
  - Input validation and sanitization
  - Structured output validation using Pydantic

---

## 📁 Project Structure

```sh
└── aiAgent/
    ├── README.md
    ├── data_agent_graph.png
    ├── etl_analyst_graph.png
    ├── pyproject.toml
    ├── requirements.txt
    ├── sql_analyst_graph.png
    ├── src
    │   └── buildolaaiagent
    │       ├── __init__.py
    │       ├── __pycache__
    │       │   └── __init__.cpython-312.pyc
    │       ├── agents
    │       │   ├── __pycache__
    │       │   │   ├── etl_analyst.cpython-312.pyc
    │       │   │   └── sql_analyst.cpython-312.pyc
    │       │   ├── data_agent.py
    │       │   ├── etl_analyst.py
    │       │   └── sql_analyst.py
    │       ├── data
    │       │   ├── extract
    │       │   │   ├── extracted_data.json
    │       │   │   └── json
    │       │   ├── ratings.csv
    │       │   ├── rides.csv
    │       │   ├── transform
    │       │   │   └── bulbasaur_moves.csv
    │       │   ├── users.csv
    │       │   └── vehicles.csv
    │       ├── feed_db.py
    │       ├── models
    │       │   ├── __pycache__
    │       │   │   └── schema.cpython-312.pyc
    │       │   └── schema.py
    │       └── utils
    │           ├── __pycache__
    │           │   ├── database.cpython-312.pyc
    │           │   ├── etl_tools.cpython-312.pyc
    │           │   └── llm_pick.cpython-312.pyc
    │           ├── database.py
    │           ├── etl_tools.py
    │           └── llm_pick.py
    ├── test_schema_details.txt
    └── uv.lock
```


### 📂 Project Index
<details open>
	<summary><b><code>AIAGENT/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/pyproject.toml'>pyproject.toml</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/test_schema_details.txt'>test_schema_details.txt</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- src Submodule -->
		<summary><b>src</b></summary>
		<blockquote>
			<details>
				<summary><b>buildolaaiagent</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/feed_db.py'>feed_db.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
					<details>
						<summary><b>models</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/models/schema.py'>schema.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>agents</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/agents/etl_analyst.py'>etl_analyst.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/agents/data_agent.py'>data_agent.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/agents/sql_analyst.py'>sql_analyst.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>utils</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/utils/llm_pick.py'>llm_pick.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/utils/etl_tools.py'>etl_tools.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/ashutoshvats03/aiAgent/blob/master/src/buildolaaiagent/utils/database.py'>database.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
## 🚀 Getting Started

### ☑️ Prerequisites

Before getting started with aiAgent, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


### ⚙️ Installation

Install aiAgent using one of the following methods:

**Build from source:**

1. Clone the aiAgent repository:
```sh
❯ git clone https://github.com/ashutoshvats03/aiAgent/
```

2. Navigate to the project directory:
```sh
❯ cd aiAgent
```

3. Install the project dependencies:


**Using `uv`**

```sh
❯ uv init
❯ uv venv
❯ uv add -r requirements.txt
❯ python main.py
```

---

## 🙌 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---



```text
GOOGLE_API_KEY = 
GROQ_API_KEY = 
OPENAI_API_KEY =
TAVILY_API_KEY =
LANGSMITH_API_KEY =

DATABASE = 
PORT = 
HOST =
USER = 
PASSWORD = 

--------------------------------- Models from each operators
gemini-3.1-flash-lite
qwen/qwen3.8-27b
gpt-4o-mini
---------------------------------- List of models from groq for free
groq/compound-mini
qwen/qwen3.8-27b
openai/gpt-oss-120b
groq/compound
whisper-large-v3-turbo
meta-llama/llama-prompt-guard-2-86m
allam-2-7b
whisper-large-v3
meta-llama/llama-prompt-guard-2-22m
canopylabs/orpheus-arabic-saudi
canopylabs/orpheus-v1-english
openai/gpt-oss-safeguard-20b
openai/gpt-oss-20b
```
