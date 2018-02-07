from flask import Flask
from flask_restful_swagger_2 import Api
from rdb.rdb import connect_to_db, create_all
from flask_cors import CORS
from resources.annotationTaskResource import AnnotationTaskResource, AnnotationTaskListResource, UserAnnotationTaskListResource
import json
import logging
import logging.config
logging.config.dictConfig(json.load(open("logging_config.json", "r")))


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app, add_api_spec_resource=True, api_version='0.0', api_spec_url='/api/swagger')  # Wrap the Api and add /api/swagger endpoint

connect_to_db(app)
create_all()

CORS(app)

api.add_resource(AnnotationTaskResource, '/annotation_tasks/<int:task_id>', endpoint='annotation_task')
api.add_resource(AnnotationTaskListResource, '/annotation_tasks', endpoint='annotation_tasks')
api.add_resource(UserAnnotationTaskListResource, '/users/<int:user_id>/annotation_tasks', endpoint='annotation_tasks_for_user')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
