from rdb.rdb import db
import rdb.models.entry as Entry
import rdb.models.annotator as Annotator
import rdb.models.result as Result
import requests
from flask_restful import abort


class AnnotationTask(db.Model):
    """Annotation Task Class"""

    __tablename__ = "annotation_task"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    crawler_job_id = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    anno_type = db.Column(db.Integer)
    scale_entries = db.relationship('ScaleEntry', lazy='select', cascade='all', backref='task')
    annotators = db.relationship('Annotator', lazy='select', cascade='all', backref='task')
    entries = db.relationship('Entry', lazy='select', cascade='all', backref='task')

    def __init__(self):
        super(AnnotationTask, self).__init__()

    def __repr__(self):
        """Display when printing a annotation task object"""

        return "<ID: {}, Name: {}, type: {}>".format(self.id, self.name, self.anno_type)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def abort_if_task_doesnt_exist(task_id):
        abort(404, message="annotation task {} doesn't exist".format(task_id))


def create(crawler_job_id, creator_id, name, anno_type, number_of_annotators=None):
    at = AnnotationTask()
    at.crawler_job_id = crawler_job_id
    at.creator_id = creator_id
    at.name = name
    at.anno_type = anno_type

    db.session.add(at)
    db.session.commit()

    data = requests.get('http://data_pre:5000/aggregation/' + crawler_job_id + '?output_type=json&aggregation_type=latest').json()
    entries = list()
    for d in data:
        e = Entry.create(patient_id=d['patient_id'], json=str(d['entries']), task_id=at.id)
        entries.append(e)

    if number_of_annotators:
        for i in range(0, number_of_annotators):
            a = Annotator.create(name=str(i), task_id=at.id)
            a.entries = entries

    db.session.commit()

    return at


def get(id, raise_abort=True):
    at = AnnotationTask.query.get(id)

    if not at:
        abort_if_task_doesnt_exist(id)

    return at


def get_all():
    return AnnotationTask.query.all()


def get_all_for_user(creator_id):
    return AnnotationTask.query.filter_by(creator_id=creator_id).all()


def update(id, name=None, anno_type=None, raise_abort=True):
    at = get(id)

    if not at:
        return abort_if_task_doesnt_exist(id)

    if name:
        at.name = name

    if anno_type:
        at.anno_type = anno_type

    db.session.commit()
    return at


def delete(id):
    at = get(id)

    if not at:
        return abort_if_task_doesnt_exist(id)

    for e in at.entries:
        e.annotators = []

    db.session.commit()

    db.session.delete(at)
    db.session.commit()

    return id
