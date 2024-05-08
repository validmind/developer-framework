import json
import os
import sqlite3

from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = os.environ.get("OPENAI_GPT_MODEL", "gpt-3.5-turbo-0613")
TOOL_FOLDER = os.environ.get("OPENAI_TOOL_FOLDER", "tool_definitions")
CONTRACTS_DATA = "contracts.json"
VENDORS_DATA = "vendors.json"

client = OpenAI()
db_connection = None


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


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(
                    f"system: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]])
            )
        elif message["role"] == "assistant" and message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['function_call']}\n",
                    role_to_color[message["role"]],
                )
            )
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "function":
            print(
                colored(
                    f"function ({message['name']}): {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )


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
    with open(CONTRACTS_DATA, "r") as file:
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

    with open(VENDORS_DATA, "r") as file:
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


def query_db(query):
    global db_connection

    cursor = db_connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# with open("contracts.json") as f:
#     contract_data = json.load(f)
# with open("vendors.json") as f:
#     vendors = json.load(f)
# response = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": "Please expand the user-provided data with synthetic data.\nDo not make up vendors though, use real, popular software vendors.",
#         },
#         {
#             "role": "user",
#             "content": f"Contracts data:\n{json.dumps(contract_data)}",
#         },
#         {
#             "role": "user",
#             "content": f"Vendors data:\n{json.dumps(vendors)}",
#         },
#         {
#             "role": "user",
#             "content": "Return a json object with the keys `vendors` and `contracts` that greatly expands the existing example data. Use the same schema and structure and create the contracts first so you can link the vendor and contracts correctly.",
#         }
#     ],
#     model="gpt-4-turbo",
#     temperature=1,
#     max_tokens=4096,
#     response_format={"type": "json_object"},
# )
