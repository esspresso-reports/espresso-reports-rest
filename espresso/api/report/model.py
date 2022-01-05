from sqlalchemy import ForeignKey

from espresso.extensions import db


class Report(db.Model):
    __tablename__ = 'ESPRESSO_REPORT'
    __permissions__ = dict(
        owner=['read', 'update', 'delete'],
        group=['read'],
        other=[]
    )

    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    check_in = db.Column(db.DateTime)
    next_working_day = db.Column(db.Date)
    accomplished_tasks = db.Column(db.TEXT)
    planned_tasks = db.Column(db.TEXT)
    general_notes = db.Column(db.TEXT)
    user_id = db.Column(ForeignKey('ESPRESSO_USER.id'))
