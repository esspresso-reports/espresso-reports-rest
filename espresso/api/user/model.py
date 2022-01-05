from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict

from espresso.extensions import db


class User(db.Model):
    __tablename__ = 'ESPRESSO_USER'
    id = db.Column(db.Text, primary_key=True)
    email = db.Column(db.String, nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_disabled = db.Column(db.Boolean, nullable=False, default=False)
    settings = db.Column(MutableDict.as_mutable(JSON), nullable=False, default={})
