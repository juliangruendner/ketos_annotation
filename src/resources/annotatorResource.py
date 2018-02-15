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
    def get(self, task_id):
        return Annotator.get_all_for_task(task_id), 200

    @marshal_with(annotator_fields)
    def post(self, task_id):
        task = AnnotationTask.get(task_id)

        args = self.parser.parse_args()

        a = Annotator.create(name=args['name'], task_id=task_id, entries=task.entries)

        return a, 201
