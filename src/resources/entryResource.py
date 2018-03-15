from flask_restful import fields, marshal_with
from flask_restful_swagger_2 import swagger, Resource
import rdb.models.entry as Entry

entry_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'task_id': fields.Integer,
    'json': fields.String
}


class AnnotationTaskEntryListResource(Resource):
    def __init__(self):
        super(AnnotationTaskEntryListResource, self).__init__()

    @marshal_with(entry_fields)
    @swagger.doc({
        "summary": "Returns all entries for specific annotation task",
        "tags": ["annotation entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all entries for specific annotation task',
        "responses": {
            "200": {
                "description": "Returns all entries for specific annotation task"
            }
        },
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the annotation task",
                "required": True
            }
        ],
    })
    def get(self, task_id):
        return Entry.get_all_for_task(task_id), 200


class EntriesForAnnotatorResource(Resource):
    def __init__(self):
        super(EntriesForAnnotatorResource, self).__init__()

    @marshal_with(entry_fields)
    @swagger.doc({
        "summary": "Returns all entries for annotator token",
        "tags": ["annotation entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all entries for annotator token',
        "responses": {
            "200": {
                "description": "Returns all entries for annotator token"
            }
        },
        "parameters": [
            {
                "name": "token",
                "in": "path",
                "type": "string",
                "description": "token of an annotator",
                "required": True
            }
        ],
    })
    def get(self, token):
        return Entry.get_all_for_annotator_token(token), 200
