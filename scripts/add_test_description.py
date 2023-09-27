"""Script that generates a description for a test using GPT-4 and automatically inserts it into the class docstring

Usage:
    python scripts/add_test_description.py <path> // path can be either a file or a directory

Before running this, you need to either set an environment variable OPENAI_API_KEY
or create a .env file in the root of the project with the following contents:
OPENAI_API_KEY=<your api key>
"""
import os

import click
import dotenv
import openai

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """
You are an expert in validating Machine Learning models using MRM (Model Risk Management) best practices. You are also an expert in writing descriptions that are pleasant to read while being very useful.
You will be provided the source code for a metric or threshold test that is run against an ML model. You will analyze the code to determine the details and implementation of the test. Finally, you will write clear, descriptive and informative descriptions in the format described that will document the tests for developers and risk management teams.

For each test you will return a description with the following sections:
1. *Purpose*
2. *Test Mechanism*
3. *Signs of High Risk*
4. *Strengths*
5. *Limitations*

You will populate each section according to the following guidelines:
1. *Purpose*: Brief explanation of why this metric is being used and what it is intended to evaluate or measure in relation to the model.
2. *Test Mechanism*: Describe the methodology used to test or apply the metric, including any grading scales or thresholds
3. *Signs of High Risk**: List or describe any signs or indicators that might suggest a high risk or a failure in the model's performance as related to this metric
4. *Strengths**: List or describe the strengths or advantages of using this metric in evaluating the model
5. *Limitations*: List or describe the limitations or disadvantages of this metric, including any potential bias or areas it might not fully address

Ensure that each section is populated with succinct, clear, and relevant information pertaining to the test. Respond with a markdown description where each section name is in bold and is followed by a colon and then the content for that section. Respond only with the description and don't include any explanation or other text.
""".strip()


def indent_and_wrap(text, indentation=4, wrap_length=120):
    lines = text.split('\n')
    result = []

    for line in lines:
        if line == '':
            result.append('')
            continue

        line = ' ' * indentation + line

        while len(line) > wrap_length:
            space_index = line.rfind(' ', 0, wrap_length)

            if space_index == -1:
                space_index = wrap_length

            result.append(line[:space_index])
            line = ' ' * indentation + line[space_index:].lstrip()

        result.append(line)

    return '\n'.join(result)


def add_description_to_test(path):
    """Generate a test description using gpt4
    You can switch to gpt3.5 if you don't have access but gpt4 should do a better job
    """
    # get file contents from path
    click.echo(f"\n\n{path}:\n")
    with open(path, "r") as f:
        file_contents = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4", # or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"```python\n{file_contents}```"},
        ],
        stream=True,
    )
    description = ""
    for chunk in response:
        if chunk.choices[0].finish_reason == "stop":
            break

        click.echo(chunk.choices[0].delta.content, nl=False)
        description += chunk.choices[0].delta.content

    click.echo("\n")

    # format the description to go into the test code
    # the description should be trimmed and have 4 spaces prepended to each line
    # each line should be wrapped at 120 characters
    description = indent_and_wrap(description.strip())

    # insert the description into the test code
    # the description should be inserted after the class definition line
    class_definition_line = None
    existing_description_lines = []
    lines = file_contents.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("class"):
            class_definition_line = i
            # check if there is already a doc string for the class
            if '"""' in lines[i + 1]:
                existing_description_lines.append(i + 1)
                j = i + 2
                while j < len(lines):
                    existing_description_lines.append(j)
                    if '"""' in lines[j]:
                        break
                    j += 1
            break

    if class_definition_line is None:
        raise ValueError("Could not find class definition line")

    # remove any existing description lines
    for i in reversed(existing_description_lines):
        lines.pop(i)

    # insert the new description lines
    lines.insert(class_definition_line + 1, f'    """\n{description}\n    """')

    # write the updated file contents back to the file
    with open(path, "w") as f:
        f.write("\n".join(lines))


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=True))
def main(path):
    """Recursively processes the specified DIRECTORY and updates files needing metadata injection."""
    # check if path is a file or directory
    if os.path.isfile(path):
        if path.endswith(".py"):
            add_description_to_test(path)

    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py") and file[0].isupper():
                    add_description_to_test(os.path.join(root, file))


if __name__ == "__main__":
    main()
