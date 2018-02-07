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
    def get(self, task_id):
        return ScaleEntry.get_all_for_task(task_id), 200

    @marshal_with(scale_entry_fields)
    def post(self, task_id):
        args = self.parser.parse_args()

        se = ScaleEntry.create(name=args['name'], code=args['code'], task_id=task_id)

        return se, 201
