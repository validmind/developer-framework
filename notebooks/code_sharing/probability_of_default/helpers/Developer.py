import datetime
import inspect
import os
import re
import pandas as pd
import logging
import pickle
import statsmodels.api as sm  # To recognize GLMResultsWrapper objects
from statsmodels.genmod.generalized_linear_model import GLMResultsWrapper


# Set up the logging configuration
logging.basicConfig(level=logging.INFO, format="INFO: %(message)s")


class Developer:
    def __init__(self):
        self.tasks_log = []
        self.tasks_details = []
        self.validation_log = []  # Log for validation tests
        self.tasks = {}  # Dictionary to store tasks

    def add_task(self, task_id, task):
        """Register a task."""
        if task_id in self.tasks:
            raise ValueError(f"Task ID '{task_id}' already exists!")
        self.tasks[task_id] = {"task": task}
        return task_id

    def get_caller_info(self, frame):
        """Fetch the calling line of code and the variable names."""
        code_context = inspect.getframeinfo(frame).code_context
        line_of_code = code_context[0].strip() if code_context else ""
        input_vars = {id(var): name for name, var in frame.f_locals.items()}
        return line_of_code, input_vars

    def get_task(self, task_id):
        """Retrieve task entry based on the task ID."""
        task_entry = self.tasks.get(task_id)
        if not task_entry:
            raise ValueError(f"No task found for ID {task_id}")
        return task_entry

    def execute_task(self, task_id, inputs=None, area_id=None, validation_tests=None):
        if inputs is None:
            inputs = []

        logging.info(f"Executing task '{task_id}'...\n")

        frame = inspect.currentframe().f_back
        line_of_code, input_vars = self.get_caller_info(frame)
        input_var_names = [input_vars.get(id(inp), "N/A") for inp in inputs]
        task_entry = self.get_task(task_id)

        result = task_entry["task"](*inputs)

        # Extract the variable name to which the result is assigned
        output_match = re.search(r"^\s*([\w\s,]+?)\s*=", line_of_code)
        output_var_name = (
            output_match.group(1).replace(" ", "") if output_match else "N/A"
        )

        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).seconds

        # Log the task details internally
        self.tasks_log.append(task_id)
        self.tasks_details.append(
            {
                "Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Area ID": area_id,
                "Task ID": task_id,
                "Input": ", ".join(input_var_names),
                "Output": output_var_name,
                "Duration": f"{duration} seconds",
            }
        )

        # Log the validation tests
        self.validation_log.append(
            {
                "Area ID": area_id,
                "Task ID": task_id,
                "Input": ", ".join(input_var_names),
                "Output": output_var_name,
                "Validation Tests": ", ".join(validation_tests)
                if validation_tests
                else "N/A",
            }
        )

        return result

    def show_validation_plan(self):
        """Return the validation plan details in a tabular format."""
        df = pd.DataFrame(self.validation_log)

        # Use HTML line breaks for Jupyter Notebook rendering
        separator = "<br>"
        df["Validation Tests"] = df["Validation Tests"].apply(
            lambda x: separator.join(x.split(", ")) if x != "none" else "none"
        )

        # Replace "N/A" with "none"
        df.replace({"N/A": "none"}, inplace=True)

        return df

    def show_lifecycle(self):
        """Display the model lifecycle details in a tabular format."""
        df = pd.DataFrame(self.tasks_details)
        return df

    def save_objects_to_pickle(self, filename, objects_to_save):
        """
        Save provided objects to a pickle file.

        Parameters:
        - filename: Name of the pickle file.
        - objects_to_save: Dictionary where keys are names/identifiers and values are the objects to be saved.
        """
        # Ensure the directory exists
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(filename, "wb") as f:
            pickle.dump(objects_to_save, f)

        logging.info(f"Saved {len(objects_to_save)} objects to {filename}")
        return list(objects_to_save.keys())

    def load_objects_from_pickle(self, filename):
        """
        Load objects from a pickle file.

        Parameters:
        - filename: Name of the pickle file.

        Returns:
        - A dictionary of loaded objects.
        """
        with open(filename, "rb") as f:
            loaded_objects = pickle.load(f)

        logging.info(f"Loaded {len(loaded_objects)} objects from {filename}")
        return loaded_objects
