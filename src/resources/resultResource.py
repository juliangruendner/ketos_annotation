from flask_restful import fields, marshal_with, reqparse
from flask_restful_swagger_2 import swagger, Resource
from resources.scaleEntryResource import scale_entry_fields
import rdb.models.result as Result

result_fields = {
    'id': fields.Integer,
    'scale_entry_id': fields.Integer,
    'annotator_id': fields.Integer,
    'entry_id': fields.Integer,
    'scale_entry': fields.Nested(scale_entry_fields)
}


class AnnotationTaskResultListResource(Resource):
    def __init__(self):
        super(AnnotationTaskResultListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('scale_entry_id', type=int, location='json')
        self.parser.add_argument('annotator_id', type=int, location='json')
        self.parser.add_argument('entry_id', type=int, location='json')

    @marshal_with(result_fields)
    def get(self, task_id):
        return Result.get_all_for_task(task_id), 200

    @marshal_with(result_fields)
    def post(self):
        args = self.parser.parse_args()

        r = Result.create(scale_entry_id=args['scale_entry_id'], annotator_id=args['annotator_id'], entry_id=args['entry_id'])

        return r, 201


class AnnotatorResultListResource(Resource):
    def __init__(self):
        super(AnnotatorResultListResource, self).__init__()

    @marshal_with(result_fields)
    def get(self, annotator_id):
        return Result.get_all_for_annotator(annotator_id), 200
