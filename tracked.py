import requests
import json

_TRACKED_API_URL = 'https://www.trackedhq.com/api/v2/'


class Resource:
    def __init__(self, api):
        self._api = api
        self._session = api.session

    def _get_returned(self, response):
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text

    def _get(self, url):
        response = self._session.get(self._getURL(url))
        return self._get_returned(response)

    def _post(self, url, data):
        response = self._session.post(self._getURL(url), json.dumps(data))
        return self._get_returned(response)

    def _put(self, url, data):
        response = self._session.put(self._getURL(url), json.dumps(data))
        return self._get_returned(response)

    def _delete(self, url):
        response = self._session.delete(self._getURL(url))
        return self._get_returned(response)

    # ==============================================================
    # Helper functions
    # ==============================================================
    def _getURL(self, url):
        credentials = ("&" if "?" in url else "?") + \
                      "email_address=" + self._api.email_address + \
                      "&api_token=" + self._api.api_token
        new_url = _TRACKED_API_URL + str(self._api.basecamp_account_id) + url + credentials
        return new_url


class Projects(Resource):
    def list(self):
        return self._get("/projects")


class Lists(Resource):
    def list(self, basecamp_project_id):
        return self._get("/projects/{0}/lists".format(basecamp_project_id))


class Todos(Resource):
    class TodoType:
        ACTIVE = "active"
        COMPLETED = "completed"
        ALL = "all"

    def list(self, basecamp_project_id, todo_type=TodoType.ALL, page_id=1):
        todos = self._get('/projects/{0}/todos?todo_type={1}&page={2}'.format(basecamp_project_id, todo_type, page_id))
        if len(todos) >= 100:
            todos += self.list(basecamp_project_id, todo_type, page_id+1)
        return todos

    def update(self, basecamp_project_id, basecamp_todo_id, new_position: int, lists: list):
        return self._put("/projects/{0}/todos/{1}".format(basecamp_project_id, basecamp_todo_id),
                         data={"new_position": new_position, "lists": lists})


class Labels(Resource):
    def create(self, basecamp_project_id, label_name, tag_color):
        tag_color = tag_color.replace("#", "%23")
        return self._post('/projects/{0}/labels?label_name={1}&tag_color={2}'.format(basecamp_project_id,
                                                                                     label_name,
                                                                                     tag_color),
                          data={})

    def add(self, basecamp_project_id, label_id, basecamp_todo_id):
        return self._post('/projects/{0}/labels/{1}/add_to_todo?basecamp_todo_id={2}'.format(basecamp_project_id,
                                                                                             label_id,
                                                                                             basecamp_todo_id),
                          data={})

    def list(self, basecamp_project_id):
        return self._get('/projects/{0}/labels/'.format(basecamp_project_id))

    def get(self, basecamp_project_id, basecamp_todo_id):
        return self._get('/projects/{0}/labels/todos/{1}'.format(basecamp_project_id, basecamp_todo_id))


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
