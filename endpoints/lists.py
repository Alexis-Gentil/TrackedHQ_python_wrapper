from .base import Resource


class Lists(Resource):
    def list(self, basecamp_project_id):
        return self._get("/projects/{0}/lists".format(basecamp_project_id))
