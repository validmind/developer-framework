# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from .load import list_tests


def list_tags():
    """
    List unique tags from all test classes.
    """

    unique_tags = set()

    for test_class in list_tests(__as_class=True):
        if hasattr(test_class, "metadata") and "tags" in test_class.metadata:
            for tag in test_class.metadata["tags"]:
                unique_tags.add(tag)

    return list(unique_tags)


def list_tasks_and_tags():
    """
    List all task types and their associated tags, with one row per task type and
    all tags for a task type in one row.

    Returns:
        pandas.DataFrame: A DataFrame with 'Task Type' and concatenated 'Tags'.
    """
    task_tags_dict = {}

    for test_class in list_tests(__as_class=True):
        if hasattr(test_class, "metadata"):
            task_types = test_class.metadata.get("task_types", [])
            tags = test_class.metadata.get("tags", [])

            for task_type in task_types:
                if task_type not in task_tags_dict:
                    task_tags_dict[task_type] = set()
                task_tags_dict[task_type].update(tags)

    # Convert the dictionary into a DataFrame
    task_tags_data = [
        {"Task Type": task_type, "Tags": ", ".join(tags)}
        for task_type, tags in task_tags_dict.items()
    ]
    return format_dataframe(pd.DataFrame(task_tags_data))


def list_task_types():
    """
    List unique task types from all test classes.
    """

    unique_task_types = set()

    for test_class in list_tests(__as_class=True):
        if hasattr(test_class, "metadata") and "task_types" in test_class.metadata:
            for task_type in test_class.metadata["task_types"]:
                unique_task_types.add(task_type)

    return list(unique_task_types)
