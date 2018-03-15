from flask_restful import fields, marshal_with, reqparse
from flask_restful_swagger_2 import swagger, Resource
import rdb.models.scaleEntry as ScaleEntry

scale_entry_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'code': fields.String,
    'task_id': fields.Integer
}


class AnnotationTaskScaleEntryListResource(Resource):
    def __init__(self):
        super(AnnotationTaskScaleEntryListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('code', type=str, location='json')

    @marshal_with(scale_entry_fields)
    @swagger.doc({
        "summary": "Returns all scale entries for annotation task",
        "tags": ["annotation task scale entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all scale entries for annotation task',
        "responses": {
            "200": {
                "description": "Returns all scale entries for annotation task"
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
        return ScaleEntry.get_all_for_task(task_id), 200

    @marshal_with(scale_entry_fields)
    @swagger.doc({
        "summary": "Create scale entry for annotation task",
        "tags": ["annotation task scale entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Create scale entry for annotation task',
        "responses": {
            "200": {
                "description": "Success: Returns newly created scale entry"
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
                "name": "scale_entry",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "code": {
                            "type": "string"
                        }
                    }
                }
            }
        ],
    })
    def post(self, task_id):
        args = self.parser.parse_args()

        se = ScaleEntry.create(name=args['name'], code=args['code'], task_id=task_id)

        return se, 201


class AnnotationTaskScaleEntry(Resource):
    def __init__(self):
        super(AnnotationTaskScaleEntry, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('code', type=str, location='json')

    @marshal_with(scale_entry_fields)
    @swagger.doc({
        "summary": "Returns specific scale entry for annotation task",
        "tags": ["annotation task scale entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns specific scale entry for annotation task',
        "responses": {
            "200": {
                "description": "Returns specific scale entry for annotation task"
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
                "name": "scale_entry_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the scale entry",
                "required": True
            }
        ],
    })
    def get(self, task_id, scale_entry_id):
        return ScaleEntry.get(scale_entry_id), 200

    @marshal_with(scale_entry_fields)
    @swagger.doc({
        "summary": "Update scale entry for annotation task",
        "tags": ["annotation task scale entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Update scale entry for annotation task',
        "responses": {
            "200": {
                "description": "Success: Returns newly updated scale entry"
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
                "name": "scale_entry_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the scale entry",
                "required": True
            },
            {
                "name": "scale_entry",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "code": {
                            "type": "string"
                        }
                    }
                }
            }
        ],
    })
    def put(self, task_id, scale_entry_id):
        args = self.parser.parse_args()

        se = ScaleEntry.update(id=scale_entry_id, name=args['name'], code=args['code'])

        return se, 201

    @swagger.doc({
        "summary": "Delete specific scale entry for annotation task",
        "tags": ["annotation task scale entries"],
        "produces": [
            "application/json"
        ],
        "description": 'Delete specific scale entry for annotation task',
        "responses": {
            "200": {
                "description": "Returns the given scale entry ID"
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
                "name": "scale_entry_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the scale entry",
                "required": True
            }
        ],
    })
    def delete(self, task_id, scale_entry_id):
        id = ScaleEntry.delete(scale_entry_id)

        return {'id': id}, 200
