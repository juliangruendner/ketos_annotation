from rdb.rdb import db


class Entry(db.Model):
    """Entry Class"""

    __tablename__ = "entry"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patient_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer, db.ForeignKey('annotation_task.id'), nullable=False)
    json = db.Column(db.Text)
    results = db.relationship('Result', lazy='select', cascade='all', backref='entry')
    annotators = db.relationship('Annotator', lazy='subquery', secondary='annotator_entries')

    def __init__(self):
        super(Entry, self).__init__()

    def __repr__(self):
        """Display when printing a result object"""

        return "<ID: {}, patient ID: {}, json: {}>".format(self.id, self.patient_id, self.json)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create(patient_id, task_id, json):
    e = Entry()
    e.patient_id = patient_id
    e.task_id = task_id
    e.json = json

    db.session.add(e)
    db.session.commit()
    return e


def get(id):
    return Entry.query.get(id)


def get_all():
    return Entry.query.all()


def get_all_for_task(task_id):
    return Entry.query.filter_by(task_id=task_id).all()


def delete(id):
    e = get(id)

    if not e:
        return None

    db.session.delete(e)
    db.session.commit()

    return id
