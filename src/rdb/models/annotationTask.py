from rdb.rdb import db
import rdb.models.entry as Entry
import rdb.models.annotator as Annotator
import requests


class AnnotationTask(db.Model):
    """Annotation Task Class"""

    __tablename__ = "annotation_task"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    crawler_job_id = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    anno_type = db.Column(db.Integer)
    scale_entries = db.relationship('ScaleEntry', lazy='select', cascade='delete, delete-orphan', backref='task')
    annotators = db.relationship('Annotator', lazy='select', cascade='delete, delete-orphan', backref='task')
    entries = db.relationship('Entry', lazy='select', cascade='delete, delete-orphan', backref='task')

    def __init__(self):
        super(AnnotationTask, self).__init__()

    def __repr__(self):
        """Display when printing a annotation task object"""

        return "<ID: {}, Name: {}, type: {}>".format(self.id, self.name, self.anno_type)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create(crawler_job_id, creator_id, name, anno_type, number_of_annotators=None):
    at = AnnotationTask()
    at.crawler_job_id = crawler_job_id
    at.creator_id = creator_id
    at.name = name
    at.anno_type = anno_type

    db.session.add(at)
    db.session.commit()

    annotators = list()
    if number_of_annotators:
        for i in range(0, number_of_annotators):
            a = Annotator.create(name=str(i), task_id=at.id)
            annotators.append(a)

    data = requests.get('http://data_pre:5000/aggregation/' + crawler_job_id + '?output_type=json&aggregation_type=latest').json()
    for d in data:
        e = Entry.create(patient_id=d['patient_id'], json=str(d['entries']), task_id=at.id)
        e.annotators = annotators

    db.session.commit()

    return at


def get(id):
    return AnnotationTask.query.get(id)


def get_all():
    return AnnotationTask.query.all()


def get_all_for_user(creator_id):
    return AnnotationTask.query.filter_by(creator_id=creator_id).all()


def update(id, name=None, anno_type=None):
    at = get(id)

    if not at:
        return None

    if name:
        at.name = name

    if anno_type:
        at.anno_type = anno_type

    db.session.commit()
    return at


def delete(id):
    at = get(id)

    if not at:
        return None

    db.session.delete(at)
    db.session.commit()

    return id
