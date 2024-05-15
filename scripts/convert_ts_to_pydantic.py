import os
from ts_morph import Project
from typing import Dict

# Path to your TypeScript types file
TYPES_FILE = "gui_src/types.ts"
OUTPUT_FILE = "gui_src/py_types.py"


def convert_ts_to_pydantic():
    project = Project()
    source_file = project.add_source_file_at_path(TYPES_FILE)
    interfaces = source_file.get_interfaces()

    py_classes = []

    for interface in interfaces:
        class_name = interface.get_name()
        properties = interface.get_properties()

        py_class = f"class {class_name}Base(BaseModel):\n"
        for prop in properties:
            prop_name = prop.get_name()
            prop_type = prop.get_type().get_text()

            py_type = convert_ts_type_to_py_type(prop_type)
            py_class += f"    {prop_name}: {py_type}\n"

        py_classes.append(py_class)

    with open(OUTPUT_FILE, "w") as f:
        f.write("from pydantic import BaseModel\n")
        f.write("\n\n".join(py_classes))


def convert_ts_type_to_py_type(ts_type: str) -> str:
    type_mapping: Dict[str, str] = {
        "string": "str",
        "number": "float",
        "boolean": "bool",
        "any": "Any",
        "{}": "dict",
    }

    py_type = type_mapping.get(ts_type, ts_type)

    # Handle arrays
    if ts_type.endswith("[]"):
        inner_type = ts_type[:-2]
        py_type = f"List[{convert_ts_type_to_py_type(inner_type)}]"

    return py_type


if __name__ == "__main__":
    convert_ts_to_pydantic()
