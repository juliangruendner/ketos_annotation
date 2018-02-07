from rdb.rdb import db


class Annotator(db.Model):
    """Annotator Class"""

    __tablename__ = "annotator"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('annotation_task.id'), nullable=False)
    results = db.relationship('Result', lazy='select', cascade='delete, delete-orphan', backref='annotator')
    entries = db.relationship('Entry', lazy=True, secondary='annotator_entries')

    def __init__(self):
        super(Annotator, self).__init__()

    def __repr__(self):
        """Display when printing a annotator task object"""

        return "<ID: {}, Name: {}}>".format(self.id, self.name)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create(name, task_id, entries=None):
    a = Annotator()
    a.name = name
    a.task_id = task_id

    if entries:
        a.entries = entries

    db.session.add(a)
    db.session.commit()
    return a


def get(id):
    return Annotator.query.get(id)


def get_all():
    return Annotator.query.all()


def get_all_for_task(task_id):
    return Annotator.query.filter_by(task_id=task_id).all()


def update(id, name=None):
    a = get(id)

    if not a:
        return None

    if name:
        a.name = name

    db.session.commit()
    return a


def delete(id):
    a = get(id)

    if not a:
        return None

    db.session.delete(a)
    db.session.commit()

    return id
