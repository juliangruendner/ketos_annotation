from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.types as types
import config


db = SQLAlchemy()


class LowerCaseText(types.TypeDecorator):
    '''Converts strings to lower case on the way in.'''

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return value.lower()


def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + config.POSTGRES_USER + ':' + config.POSTGRES_PASSWORD + '@anno_db:5432/' + config.POSTGRES_DB
    db.app = app
    db.init_app(app)


def create_all():
    """Create all db tables"""

    from rdb.models.annotationTask import AnnotationTask
    from rdb.models.scaleEntry import ScaleEntry
    from rdb.models.annotator import Annotator
    from rdb.models.result import Result

    db.create_all()
    db.session.commit()
