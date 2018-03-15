from flask_restful import fields, marshal_with, reqparse
from flask_restful_swagger_2 import swagger, Resource
import rdb.models.annotator as Annotator
import rdb.models.annotationTask as AnnotationTask

annotator_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'task_id': fields.Integer,
    'token': fields.String
}


class AnnotationTaskAnnotatorListResource(Resource):
    def __init__(self):
        super(AnnotationTaskAnnotatorListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')

    @marshal_with(annotator_fields)
    @swagger.doc({
        "summary": "Returns all annotators a annotation task",
        "tags": ["annotators"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all annotators a annotation task',
        "responses": {
            "200": {
                "description": "Returns the list of annotation tasks for a user"
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
        return Annotator.get_all_for_task(task_id), 200

    @marshal_with(annotator_fields)
    @swagger.doc({
        "summary": "Create annotator",
        "tags": ["annotators"],
        "produces": [
            "application/json"
        ],
        "description": 'Create annotator',
        "responses": {
            "200": {
                "description": "Success: Returns newly created annotator"
            },
            "404": {
                "description": "Not found error when annotation task doesn't exist"
            }
        },
        "parameters": [
            {
                "name": "annotator",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }
                }
            }
        ],
    })
    def post(self, task_id):
        task = AnnotationTask.get(task_id)

        args = self.parser.parse_args()

        a = Annotator.create(name=args['name'], task_id=task_id, entries=task.entries)

        return a, 201


class AnnotatorResource(Resource):
    def __init__(self):
        super(AnnotatorResource, self).__init__()

    @marshal_with(annotator_fields)
    @swagger.doc({
        "summary": "Returns the annotator for a token",
        "tags": ["annotators"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns the annotator for a token',
        "responses": {
            "200": {
                "description": "Returns the annotator for a token"
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
        return Annotator.get_by_token(token), 200
