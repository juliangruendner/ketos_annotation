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
    def get(self, task_id):
        return Entry.get_all_for_task(task_id), 200


class EntriesForAnnotatorResource(Resource):
    def __init__(self):
        super(EntriesForAnnotatorResource, self).__init__()

    @marshal_with(entry_fields)
    def get(self, token):
        return Entry.get_all_for_annotator_token(token), 200
