from rdb.rdb import db


class ScaleEntry(db.Model):
    """Scale Entry Class"""

    __tablename__ = "scale_entry"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    code = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('annotation_task.id'), nullable=False)
    results = db.relationship('Result', lazy='select', cascade='delete, delete-orphan', backref='scale_entry')

    def __init__(self):
        super(ScaleEntry, self).__init__()

    def __repr__(self):
        """Display when printing a annotation task object"""

        return "<ID: {}, Name: {}, code: {}>".format(self.id, self.name, self.code)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create(name, code, task_id):
    se = ScaleEntry()
    se.name = name
    se.code = code
    se.task_id = task_id

    db.session.add(se)
    db.session.commit()
    return se


def get(id):
    return ScaleEntry.query.get(id)


def get_all():
    return ScaleEntry.query.all()


def get_all_for_task(task_id):
    return ScaleEntry.query.filter_by(task_id=task_id).all()


def update(id, name=None, code=None):
    se = get(id)

    if not se:
        return None

    if name:
        se.name = name

    if code:
        se.code = code

    db.session.commit()
    return se


def delete(id):
    se = get(id)

    if not se:
        return None

    db.session.delete(se)
    db.session.commit()

    return id
