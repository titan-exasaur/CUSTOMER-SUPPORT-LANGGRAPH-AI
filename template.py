from pathlib import Path


PROJECT_TEMPLATE = [
    # Source package
    "src/__init__.py",

    # Agents
    "src/agents/__init__.py",
    "src/agents/classifier.py",
    "src/agents/responder.py",
    "src/agents/escalation.py",

    # Tools
    "src/tools/__init__.py",
    "src/tools/classify_ticket.py",
    "src/tools/draft_response.py",
    "src/tools/check_escalation.py",

    # Graph
    "src/graph/__init__.py",
    "src/graph/state.py",
    "src/graph/builder.py",
    "src/graph/state_mapper.py"

    # Config
    "src/config/__init__.py",
    "src/config/settings.py",

    # API
    "src/api/__init__.py",
    "src/api/routes.py",
    "src/api/schemas.py",
    "src/api/dependencies.py",

    # Database
    "src/database/__init__.py",
    "src/database/mongo.py",
    "src/database/models.py",
    "src/database/repository.py",

    # Services
    "src/services/__init__.py",
    "src/services/ticket_service.py",
    "src/services/queue_service.py",
    "src/services/agent_service.py",

    # Workers
    "src/workers/__init__.py",
    "src/workers/sqs_worker.py",

    # Prompts
    "src/prompts/__init__.py",
    "src/prompts/classifier_prompt.py",
    "src/prompts/responder_prompt.py",
    "src/prompts/escalation_prompt.py",

    # Utils
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helpers.py",
    "src/utils/ticket.py",
    "src/utils/retry.py",

    # Deployment
    "src/deployment/__init__.py",
    "src/deployment/api_lambda.py",
    "src/deployment/worker_lambda.py",
    "src/deployment/Dockerfile",
    "src/deployment/serverless.yml",

    # App entry
    "src/main.py",

    # Tests
    "tests/__init__.py",
    "tests/test_tools.py",
    "tests/test_agents.py",
    "tests/test_graph.py",
    "tests/test_api.py",
]


def create_project_structure(project_template: list[str]) -> None:
    """
    Creates project files and folders safely.

    Args:
        project_template: List of file paths to create.

    Returns:
        None
    """
    for item in project_template:
        path = Path(item)

        if item.endswith("/"):
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

    print("Project structure created successfully.")


if __name__ == "__main__":
    create_project_structure(PROJECT_TEMPLATE)