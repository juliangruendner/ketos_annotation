from rdb.rdb import db
import rdb.models.scaleEntry as ScaleEntry


class Result(db.Model):
    """Result Class"""

    __tablename__ = "result"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scale_entry_id = db.Column(db.Integer, db.ForeignKey('scale_entry.id'), nullable=False)
    annotator_id = db.Column(db.Integer, db.ForeignKey('annotator.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)

    def __init__(self):
        super(Result, self).__init__()

    def __repr__(self):
        """Display when printing a result object"""

        return "<ID: {}>".format(self.id)

    def as_dict(self):
        """Convert object to dictionary"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create(scale_entry_id, annotator_id, entry_id):
    r = Result()
    r.scale_entry_id = scale_entry_id
    r.annotator_id = annotator_id
    r.entry_id = entry_id

    db.session.add(r)
    db.session.commit()
    return r


def get(id):
    return Result.query.get(id)


def get_all():
    return Result.query.all()


def get_all_for_task(task_id):
    return Result.query.join(ScaleEntry.ScaleEntry).filter(ScaleEntry.ScaleEntry.task_id == task_id).all()


def get_all_for_annotator(annotator_id):
    return Result.query.filter_by(annotator_id=annotator_id).all()


def delete(id):
    r = get(id)

    if not r:
        return None

    db.session.delete(r)
    db.session.commit()

    return id
