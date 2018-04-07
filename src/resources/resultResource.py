from flask_restful import fields, marshal_with, reqparse
from flask_restful_swagger_2 import swagger, Resource
# from resources.scaleEntryResource import scale_entry_fields
import rdb.models.result as Result
import rdb.models.entry as Entry
import rdb.models.scaleEntry as ScaleEntry
import fhir_helper

result_fields = {
    'id': fields.Integer,
    'scale_entry_id': fields.Integer,
    'annotator_id': fields.Integer,
    'entry_id': fields.Integer,
    # 'scale_entry': fields.Nested(scale_entry_fields)
}


class AnnotationResultListResource(Resource):
    def __init__(self):
        super(AnnotationResultListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('scale_entry_id', type=int, location='json')
        self.parser.add_argument('annotator_id', type=int, location='json')
        self.parser.add_argument('entry_id', type=int, location='json')

    @marshal_with(result_fields)
    @swagger.doc({
        "summary": "Returns all existing annotation results",
        "tags": ["annotation results"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all existing annotation results',
        "responses": {
            "200": {
                "description": "Returns the list of annotation results"
            }
        }
    })
    def get(self):
        return Result.get_all(), 200

    @marshal_with(result_fields)
    @swagger.doc({
        "summary": "Create annotation result",
        "tags": ["annotation results"],
        "produces": [
            "application/json"
        ],
        "description": 'Create annotation result',
        "responses": {
            "200": {
                "description": "Success: Returns newly created annotation result"
            }
        },
        "parameters": [
            {
                "name": "annotation_result",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "scale_entry_id": {
                            "type": "integer"
                        },
                        "annotator_id": {
                            "type": "integer"
                        },
                        "entry_id": {
                            "type": "integer"
                        }
                    }
                }
            }
        ],
    })
    def post(self):
        args = self.parser.parse_args()

        r = Result.create(scale_entry_id=args['scale_entry_id'], annotator_id=args['annotator_id'], entry_id=args['entry_id'])

        return r, 201


class AnnotatorResultListResource(Resource):
    def __init__(self):
        super(AnnotatorResultListResource, self).__init__()

    @marshal_with(result_fields)
    @swagger.doc({
        "summary": "Returns all annotation results for a specific annotator",
        "tags": ["annotation results"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all annotation results for a specific annotator',
        "responses": {
            "200": {
                "description": "Returns the list of annotation results for a annotator"
            }
        },
        "parameters": [
            {
                "name": "annotator_id",
                "in": "path",
                "type": "integer",
                "description": "The ID of the annotator",
                "required": True
            }
        ],
    })
    def get(self, annotator_id):
        return Result.get_all_for_annotator(annotator_id), 200


class AnnotationTaskResultListResource(Resource):
    def __init__(self):
        super(AnnotationTaskResultListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('server_url', type=str, location='json')
        self.parser.add_argument('code', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')

    @marshal_with(result_fields)
    @swagger.doc({
        "summary": "Returns all annotation results for a specific annotation task",
        "tags": ["annotation results"],
        "produces": [
            "application/json"
        ],
        "description": 'Returns all annotation results for a specific annotation task',
        "responses": {
            "200": {
                "description": "Returns the list of annotation results for a annotation task"
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
        return Result.get_all_for_task(task_id), 200

    def post(self, task_id):
        args = self.parser.parse_args()
        system = args["system"]
        code = args["code"]
        server_url = args["server_url"] 
        #http://ketos.ai:8080/gtfhir/base/

        results = Result.get_all_for_task(task_id) 
        
        for result in results:
            patient_id = Entry.get(result.entry_id).patient_id
            result_code = ScaleEntry.get(result.scale_entry_id).code
            fhir_helper.write(server_url, system, code, patient_id, result_code)
            
        return {"success": True}, 201
