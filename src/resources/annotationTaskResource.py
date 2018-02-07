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
        self.parser.add_argument('creator_id', type=int, location='json')
        self.parser.add_argument('name', type=str, location='json')
        self.parser.add_argument('anno_type', type=int, location='json')

    @marshal_with(task_fields)
    def get(self, task_id):
        return AnnotationTask.get(task_id), 200

    def delete(self, task_id):
        id = AnnotationTask.delete(task_id)

        return {'ID': id}, 200

    @marshal_with(task_fields)
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
    def get(self):
        return AnnotationTask.get_all(), 200

    @marshal_with(task_fields)
    def post(self):
        args = self.parser.parse_args()

        at = AnnotationTask.create(crawler_job_id=args['crawler_job_id'], creator_id=args['creator_id'], name=args['name'], anno_type=args['anno_type'], number_of_annotators=args['number_of_annotators'])

        return at, 201


class UserAnnotationTaskListResource(Resource):
    def __init__(self):
        super(UserAnnotationTaskListResource, self).__init__()

    @marshal_with(task_fields)
    def get(self, user_id):
        return AnnotationTask.get_all_for_user(user_id), 200
