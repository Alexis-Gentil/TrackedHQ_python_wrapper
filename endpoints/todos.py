from .base import Resource


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

    def update(self, basecamp_project_id, basecamp_todo_id, new_position: int, list_name: str):
        return self._put("/projects/{0}/todos/{1}".format(basecamp_project_id, basecamp_todo_id),
                         data={"new_position": new_position, "list_name": list_name})
