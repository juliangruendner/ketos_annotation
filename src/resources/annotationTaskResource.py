from flask_restful import reqparse, fields, marshal_with
from flask_restful_swagger_2 import swagger, Resource
import rdb.models.annotationTask as AnnotationTask

task_fields = {
    'id': fields.Integer,
    'crawler_job_id': fields.String,
    'creator_id': fields.Integer,
    'name': fields.String,
    'anno_type': fields.Integer
}


class AnnotationTaskResource(Resource):
    def __init__(self):
        super(AnnotationTaskResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('crawler_job_id', type=str, location='json')
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('anno_type', type=int, location='json')

    @marshal_with(task_fields)
    @swagger.doc({
        "summary": "Returns a specific annotation task",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns the annotation task for the given ID',
        "responses": {
            "200": {
                "description": "Returns the annotation task with the given ID"
            },
            "404": {
                "description": "Not found error when annotation task doesn't exist"
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
        return AnnotationTask.get(task_id), 200

    @swagger.doc({
        "summary": "Deletes a specific annotation task",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Delete the annotation task for the given ID',
        "responses": {
            "200": {
                "description": "Success: Returns the given ID"
            },
            "404": {
                "description": "Not found error when annotation task doesn't exist"
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
    def delete(self, task_id):
        id = AnnotationTask.delete(task_id)

        return {'ID': id}, 200

    @marshal_with(task_fields)
    @swagger.doc({
        "summary": "Update annotation task",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Update annotation task',
        "responses": {
            "200": {
                "description": "Success: Newly updated annotation task is returned"
            },
            "404": {
                "description": "Not found error when annotation task doesn't exist"
            }
        },
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the annotation task",
                "required": True
            },
            {
                "name": "annotation_task",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "crawler_job_id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "anno_type": {
                            "type": "integer"
                        }
                    }
                }
            }
        ],
    })
    def put(self, task_id):
        args = self.parser.parse_args()

        at = AnnotationTask.update(id=task_id, name=args['name'], anno_type=args['anno_type'])

        return at, 200


class AnnotationTaskListResource(Resource):
    def __init__(self):
        super(AnnotationTaskListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('crawler_job_id', type=str, location='json')
        self.parser.add_argument('creator_id', type=int, location='json')
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('anno_type', type=int, location='json')
        self.parser.add_argument('number_of_annotators', type=int, location='args')

    @marshal_with(task_fields)
    @swagger.doc({
        "summary": "Returns all existing annotation tasks",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all existing annotation tasks',
        "responses": {
            "200": {
                "description": "Returns the list of annotation tasks"
            }
        }
    })
    def get(self):
        return AnnotationTask.get_all(), 200

    @marshal_with(task_fields)
    @swagger.doc({
        "summary": "Create annotation task",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Create annotation task',
        "responses": {
            "200": {
                "description": "Success: Returns newly created annotation task"
            },
            "404": {
                "description": "Not found error when crawler job doesn't exist"
            }
        },
        "parameters": [
            {
                "name": "number_of_annotators",
                "in": "query",
                "type": "integer",
                "description": "Number of annotators for the current task",
                "required": True
            },
            {
                "name": "annotation_task",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "crawler_job_id": {
                            "type": "string"
                        },
                        "creator_id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        },
                        "anno_type": {
                            "type": "integer"
                        }
                    }
                }
            }
        ],
    })
    def post(self):
        args = self.parser.parse_args()

        at = AnnotationTask.create(crawler_job_id=args['crawler_job_id'], creator_id=args['creator_id'], name=args['name'], anno_type=args['anno_type'], number_of_annotators=args['number_of_annotators'])

        return at, 201


class UserAnnotationTaskListResource(Resource):
    def __init__(self):
        super(UserAnnotationTaskListResource, self).__init__()

    @marshal_with(task_fields)
    @swagger.doc({
        "summary": "Returns all annotation tasks for a user",
        "tags": ["annotation tasks"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all the annotation tasks for a user',
        "responses": {
            "200": {
                "description": "Returns the list of annotation tasks for a user"
            }
        },
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the user",
                "required": True
            }
        ],
    })
    def get(self, user_id):
        return AnnotationTask.get_all_for_user(user_id), 200
