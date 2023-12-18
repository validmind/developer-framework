import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI()


def generate_summary(context, code):
    """
    Generate a summary of the given code using GPT-4.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful expert code summarizer. Your job is to create a detailed summary of the user-submitted code and explain what it does. You will be provided with the code and a summary of the files in the codebase along with their summaries (if they have been summarized already).",
            },
            {
                "role": "user",
                "content": "Here is the context of the surrounding files in the repo along with their summaries if they exist:\n{context}",
            },
            {
                "role": "user",
                "content": "Here is the code:```python\n{code}```",
            }
        ]
    )
    return response.choices[0].message.strip()


def generate_tree(path):
    """
    Generate a text tree representation of the Python files in the given directory.
    """
    tree = ""

    for root, _, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree += f'{indent}{os.path.basename(root)}/\n'
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                tree += f'{subindent}{file}\n'

    return tree


# Path to the codebase or folder you want to index
path = 'validmind'

# Generate the directory summary
tree = generate_tree(path)
print(tree)
