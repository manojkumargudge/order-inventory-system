"""
Takes the JSON output of `aws ecs describe-task-definition`, replaces the
container image with the newly built one, strips fields that
`register-task-definition` doesn't accept on input, and writes the result
back out so it can be passed to `--cli-input-json`.

Usage:
    python render_task_def.py <current-task-def.json> <new-image-uri> <output.json>
"""

import json
import sys

READ_ONLY_FIELDS = [
    "taskDefinitionArn",
    "revision",
    "status",
    "requiresAttributes",
    "compatibilities",
    "registeredAt",
    "registeredBy",
]


def main() -> None:
    input_path, new_image, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(input_path) as f:
        task_def = json.load(f)

    for field in READ_ONLY_FIELDS:
        task_def.pop(field, None)

    # Assumes a single-container task definition, which matches this app.
    if not task_def.get("containerDefinitions"):
        raise ValueError("Task definition has no containerDefinitions")

    task_def["containerDefinitions"][0]["image"] = new_image

    with open(output_path, "w") as f:
        json.dump(task_def, f, indent=2)


if __name__ == "__main__":
    main()
