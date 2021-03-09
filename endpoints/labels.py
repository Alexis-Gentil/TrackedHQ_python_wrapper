from .base import Resource


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
