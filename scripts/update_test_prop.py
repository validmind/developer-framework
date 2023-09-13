import ast
import os

import click


class MetadataChecker(ast.NodeVisitor):
    def __init__(self, class_name):
        self.class_name = class_name
        self.needs_update = False
        self.last_property_lineno = 0

    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            # Find the last class property's line number
            for item in node.body:
                if isinstance(item, ast.Assign):
                    # Checking for end_lineno if it's a multiline statement
                    self.last_property_lineno = getattr(item, "end_lineno", item.lineno)
                    if any(
                        isinstance(target, ast.Name) and target.id == "metadata"
                        for target in item.targets
                    ):
                        self.needs_update = False
                        return
            self.needs_update = True
        self.generic_visit(node)


def check_and_get_insertion_line(file_path, class_name):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    checker = MetadataChecker(class_name)
    checker.visit(tree)

    return checker.needs_update, checker.last_property_lineno


def insert_metadata_to_file(file_path):
    metadata_snippet = """\n    metadata = {
        "task_types": [],
        "tags": [],
    }\n\n"""

    with open(file_path, "r") as f:
        lines = f.readlines()

    insertion_line = None

    # Try to find 'default_params' first
    for idx, line in enumerate(lines):
        if "default_params" in line:
            # Find the next closing brace '}'
            for sub_idx, sub_line in enumerate(lines[idx:]):
                if "}" in sub_line:
                    insertion_line = idx + sub_idx + 1
                    break
            break

    # If 'default_params' is not found, then look for 'required_inputs'
    if insertion_line is None:
        for idx, line in enumerate(lines):
            if "required_inputs" in line:
                # Find the next closing square bracket ']'
                for sub_idx, sub_line in enumerate(lines[idx:]):
                    if "]" in sub_line:
                        insertion_line = idx + sub_idx + 1
                        break
                break

    if insertion_line is None:
        for idx, line in enumerate(lines):
            if "name" in line:
                insertion_line = idx + 1
                break

    # If both are not found, just print the file name
    if insertion_line is None:
        print(f"Cannot find an insertion point for: {file_path}")
        return

    # insert the metadata snippet after the identified location
    lines.insert(insertion_line, metadata_snippet)

    with open(file_path, "w") as f:
        f.writelines(lines)


def process_directory(directory):
    files_needing_update = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".py") and file_name[0].isupper():
                class_name = file_name.rstrip(".py")
                file_path = os.path.join(root, file_name)
                needs_update, insertion_line = check_and_get_insertion_line(
                    file_path, class_name
                )
                if needs_update:
                    files_needing_update.append((file_path, insertion_line))
    return files_needing_update


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def main(directory):
    """Recursively processes the specified DIRECTORY and updates files needing metadata injection."""
    files_to_update = process_directory(directory)
    if files_to_update:
        click.echo("Updating the following files:")
        for file_path, insertion_line in files_to_update:
            click.echo(f"- {file_path}")
            insert_metadata_to_file(file_path)
    else:
        click.echo("No files need metadata injection.")


if __name__ == "__main__":
    main()
