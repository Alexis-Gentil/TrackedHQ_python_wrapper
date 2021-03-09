import requests

from endpoints.projects import Projects
from endpoints.lists import Lists
from endpoints.todos import Todos
from endpoints.labels import Labels


class Tracked:
    def __init__(self, email_address: str, api_token: str, basecamp_account_id: int):
        self.email_address = email_address
        self.api_token = api_token
        self.basecamp_account_id = basecamp_account_id
        self.session = requests.Session()

    @property
    def projects(self):
        return Projects(self)

    @property
    def lists(self):
        return Lists(self)

    @property
    def todos(self):
        return Todos(self)

    @property
    def labels(self):
        return Labels(self)


"""
========================================================
Examples
========================================================
tracked = Tracked(...)

# === PROJECTS ===
# Get all projects
tracked.projects.list()

# === LISTS ===
# Get all lists for a project
tracked.lists.list(project_id)

# === TODOS ===
# List todos from project
tracked.todos.list(project_id)

# Update Kanban list and/or position for a to-do 
tracked.todos.update(project_id, todo_id, position, list_name)

# === LABELS ===
# Create a label
tracked.labels.create(project_id, "TestLabel", "#00ffff")

# List labels
tracked.labels.list(project_id)

# Add a label to a todo
tracked.labels.add(project_id, label_id, todo_id)

# Get labels of a todo
tracked.labels.get(basecamp_project_id, basecamp_todo_id)
========================================================
"""
