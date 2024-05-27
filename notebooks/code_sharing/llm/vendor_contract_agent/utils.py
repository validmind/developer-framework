import json
import os
import re
import requests
import sqlite3
import time
from typing_extensions import override

import mistune
from bs4 import BeautifulSoup
from IPython.display import display
from ipywidgets import HTML
from openai import AssistantEventHandler, OpenAI
from serpapi.google_search import GoogleSearch

TOOL_FOLDER = os.getenv("OPENAI_TOOL_FOLDER", "tool_definitions")

CONTRACTS_DATA = "data/contracts.json"
VENDORS_DATA = "data/vendors.json"

AGENT_MESSAGE_WRAPPER_HTML = """
<div id="message_container">
{message_html}
</div>
<style>
#message_container {{
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 10px 0;
}}
</style>
"""


client = OpenAI()

GoogleSearch.SERP_API_KEY = os.getenv("SERP_API_KEY", "")

db_connection = None
print_lock = False


def blocking_print(*parts, **kwargs):
    global print_lock

    # print to console but wait until the lock is released
    while print_lock:
        time.sleep(0.1)
        pass

    print_lock = True
    print(*parts, **kwargs)
    print_lock = False


class AgentEventHandler(AssistantEventHandler):
    def __init__(self, input):
        self.input = input
        super().__init__()

    @override
    def on_event(self, event):
        if os.environ["DEBUG"] == "1":
            print("got event...")
            blocking_print(f"Event: {event}")
            blocking_print(f"Data: {event}")

        if event.event == "thread.run.requires_action":
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            kwargs = json.loads(tool.function.arguments)
            self.input.setdefault("tool_calls", []).append(
                {
                    "function": tool.function.name,
                    "arguments": kwargs,
                }
            )

            if tool.function.name == "query_database":
                blocking_print("> Querying database with: ", kwargs)
                result = call_tool(query_db, **kwargs)
                blocking_print("> Result: ", result)
                blocking_print("\n")

                tool_outputs.append(
                    {
                        "tool_call_id": tool.id,
                        "output": result,
                    }
                )
                self.input.setdefault("contexts", []).append(result)

            elif tool.function.name == "search_online":
                blocking_print("> Searching online with: ", kwargs)
                result = call_tool(search_online, **kwargs)
                blocking_print("> Result: ", result)
                blocking_print("\n")
                tool_outputs.append(
                    {
                        "tool_call_id": tool.id,
                        "output": result,
                    }
                )
                self.input.setdefault("contexts", []).append(result)

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=AgentEventHandler(self.input),
        ) as stream:

            started = False
            widget = HTML(AGENT_MESSAGE_WRAPPER_HTML.format(message_html=""))
            agent_message = ""

            for text in stream.text_deltas:
                if not started:
                    started = True
                    blocking_print("> Receiving message from agent:")
                    display(widget)

                agent_message += text
                widget.value = AGENT_MESSAGE_WRAPPER_HTML.format(
                    message_html=mistune.markdown(agent_message)
                )

            if started:
                self.input.setdefault("messages", []).append(agent_message)


# Helper Functions
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


def show_json(obj):
    display(json.loads(obj.model_dump_json()))


# Function Call Functions
def search_online(search_type, query=None, url=None):
    if search_type == "browse":
        # use duckduckgo to search for the query
        # results = DDGS().text(query, max_results=5)
        # return json.dumps(results)

        # use serpapi to search for the query
        search = GoogleSearch({"q": query, "location": "Austin, Texas"})
        results = search.get_dict()

        # remove the ads, search metadata, params and info
        results.pop("ads", None)
        results.pop("search_metadata", None)
        results.pop("search_parameters", None)
        results.pop("search_information", None)
        results.pop("top_stories_links", None)
        results.pop("top_stories_serpapi_link", None)
        results.pop("pagination", None)
        results.pop("serpapi_pagination", None)

        return json.dumps(results)

    if search_type == "scrape":
        # scrape the text of the url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        return re.sub(r"\s+", " ", text).strip()

    raise ValueError(f"Unknown search type: {search_type}")


def query_db(query):
    global db_connection

    cursor = db_connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    # return as string
    return json.dumps(results)


def call_tool(func, **kwargs):
    try:
        return func(**kwargs)
    except Exception as e:
        # return a string explaining to the llm what went wrong
        message = f"Error calling tool: {func.__name__}"

        return f"{message}: {str(e)}"


# Function Call Spec
def get_tools_spec():
    tools_spec = []

    for tool_file in os.listdir(TOOL_FOLDER):
        if tool_file.endswith(".json"):
            with open(os.path.join(TOOL_FOLDER, tool_file)) as f:
                tool_spec = json.load(f)
                tools_spec.append(tool_spec)

    print(f"Loaded {len(tools_spec)} tool definitions")
    print(json.dumps(tools_spec, indent=6))

    return tools_spec


# Agent Functions


def _load_data():
    with open(CONTRACTS_DATA) as f:
        contracts_data = json.load(f)

    with open(VENDORS_DATA) as f:
        vendors_data = json.load(f)

    return contracts_data, vendors_data


def init_db():
    global db_connection

    # Create a new database connection
    db_connection = sqlite3.connect("vendors_contracts.db")

    # Create tables
    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id TEXT PRIMARY KEY,
            vendor_name TEXT,
            category TEXT,
            total_spend INTEGER,
            contracts TEXT  -- This will store contract IDs as a comma-separated string
        )
    """
    )

    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS contracts (
            contract_id TEXT PRIMARY KEY,
            vendor_id TEXT,
            start_date TEXT,
            end_date TEXT,
            contract_value INTEGER,
            terms_conditions TEXT,
            products_description TEXT,
            FOREIGN KEY (vendor_id) REFERENCES vendors (vendor_id)
        )
    """
    )

    # Load JSON data from files
    with open(VENDORS_DATA, "r") as file:
        vendors_data = json.load(file)
        for vendor in vendors_data:
            vendor["contracts"] = ",".join(vendor["contracts"])

        vendors_insert = [
            (
                v["vendor_id"],
                v["vendor_name"],
                v["category"],
                v["total_spend"],
                v["contracts"],
            )
            for v in vendors_data
        ]
        db_connection.executemany(
            "INSERT INTO vendors VALUES (?, ?, ?, ?, ?)", vendors_insert
        )

    with open(CONTRACTS_DATA, "r") as file:
        contracts_data = json.load(file)
        contracts_insert = [
            (
                c["contract_id"],
                c["vendor_id"],
                c["start_date"],
                c["end_date"],
                c["contract_value"],
                c["terms_conditions"],
                c["products_description"],
            )
            for c in contracts_data
        ]
        db_connection.executemany(
            "INSERT INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?)", contracts_insert
        )


def _get_schema():
    global db_connection

    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}
    for table_name in tables:
        cursor.execute(f"PRAGMA table_info({table_name[0]})")
        columns = cursor.fetchall()
        schema[table_name[0]] = [
            {"column_name": col[1], "data_type": col[2]} for col in columns
        ]

    return schema


def get_schema_description():
    """Get description of the database schema to feed into an LLM"""
    description = ""
    schema = _get_schema()

    for table_name, columns in schema.items():
        description += f"Table: {table_name}\n"
        for column in columns:
            description += f"  {column['column_name']}: {column['data_type']}\n"

    return description
