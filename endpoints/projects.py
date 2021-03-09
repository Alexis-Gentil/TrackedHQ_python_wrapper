from .base import Resource


class Projects(Resource):
    def list(self):
        return self._get("/projects")
