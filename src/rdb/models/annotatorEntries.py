from rdb.rdb import db
import rdb.models.entry as Entry


class AnnotatorEntries(db.Model):
    __tablename__ = 'annotator_entries'

    annotator_id = db.Column(db.Integer, db.ForeignKey('annotator.id'), primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), primary_key=True)
    annotator = db.relationship('Annotator', backref=db.backref("annotator_entry_link"))
    entry = db.relationship('Entry', backref=db.backref("entry_annotator_link"))
